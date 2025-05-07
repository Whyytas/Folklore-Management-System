import fitz
import requests
import logging

from django.core.files.base import ContentFile
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from Ensembles.models import Ensemble
from .forms import PieceForm
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Piece, Feature
import re
from django.http import HttpResponseForbidden

# Set up logging
logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY  # ⚠️ Replace with your actual API key



def pieces_list(request):
    user = request.user

    selected_ensemble_id = request.GET.get("ensemble_id") or request.session.get("selected_ensemble_id")
    sort_param = request.GET.get("sort", "title")

    valid_sorts = ["title", "-title", "duration", "-duration"]
    if sort_param not in valid_sorts:
        sort_param = "title"

    filters = {
        "type": request.GET.get("type"),
        "region": request.GET.get("region"),
        "speed": request.GET.get("speed"),
        "preparation": request.GET.get("preparation"),
        "features": request.GET.get("features"),
    }

    # Check role — exact match, case-insensitive
    is_admin = getattr(user, "role", "").lower() == "administratorius"

    if is_admin:
        # Admin sees all ensembles and all pieces
        allowed_ensembles = Ensemble.objects.all()
        pieces = Piece.objects.prefetch_related("ensembles", "features")
    else:
        allowed_ensembles = Ensemble.objects.filter(members=user)
        pieces = Piece.objects.prefetch_related("ensembles", "features").filter(
            ensembles__in=allowed_ensembles
        )

    # If selected ensemble exists in allowed ensembles, filter
    if selected_ensemble_id and allowed_ensembles.filter(id=selected_ensemble_id).exists():
        pieces = pieces.filter(ensembles__id=selected_ensemble_id)

    # Filters
    if filters["type"]:
        pieces = pieces.filter(type=filters["type"])
    if filters["region"]:
        pieces = pieces.filter(region=filters["region"])
    if filters["speed"]:
        pieces = pieces.filter(speed=filters["speed"])
    if filters["preparation"]:
        pieces = pieces.filter(preparation=filters["preparation"])
    if filters["features"]:
        pieces = pieces.filter(features__id=filters["features"])

    pieces = pieces.order_by(sort_param)

    return render(request, "pieces_list.html", {
        "page_obj": None,
        "pieces": pieces,
        "ensembles": allowed_ensembles,
        "features": Feature.objects.all(),
        "filters": filters,
        "types": Piece.TYPE_CHOICES,
        "speed": Piece.SPEED_CHOICES,
        "preparation": Piece.PREPARATION_CHOICES,
        "regions": Piece._meta.get_field("region").choices,
        "sort_param": sort_param,
        "all_ensembles": allowed_ensembles,
        "selected_ensemble_id": selected_ensemble_id,
    })

def piece_add(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti kūrinių.")

    user_is_admin = request.user.role == "administratorius"
    ensembles_queryset = Ensemble.objects.all() if user_is_admin else request.user.ensembles.all()

    if request.method == "POST":
        form = PieceForm(request.POST, request.FILES)
        if form.is_valid():
            piece = form.save(commit=False)

            manual_duration = request.POST.get("duration", "").strip()
            if manual_duration:
                piece.duration = manual_duration
            elif piece.youtube_url:
                video_id = extract_video_id(piece.youtube_url)
                if video_id:
                    piece.duration = get_video_duration(video_id)

            piece.save()
            piece.ensembles.set(request.POST.getlist("ensembles"))
            piece.features.set(request.POST.getlist("features"))

            if 'notes' in request.FILES:
                handle_pdf_conversion(piece.notes.read(), piece)
                piece.save()

            return redirect('/kuriniai/?success=true')
    else:
        form = PieceForm()

    return render(request, 'piece_add.html', {
        "form": form,
        "ensembles": ensembles_queryset,
        "features": Feature.objects.all(),
    })

from .models import Piece, Feature

def piece_edit(request, piece_id):
    piece = get_object_or_404(
        Piece.objects.prefetch_related("ensembles", "features"),
        id=piece_id
    )

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti kūrinių.")

    user_ensembles = (
        Ensemble.objects.all()
        if request.user.role == "administratorius"
        else request.user.ensembles.all()
    )

    if request.method == "POST":
        form = PieceForm(request.POST, request.FILES, instance=piece)
        if form.is_valid():
            # Save file contents before it gets closed
            uploaded_file = request.FILES.get("notes")
            file_buffer = uploaded_file.read() if uploaded_file else None  # 🔐 read early
            uploaded_filename = uploaded_file.name if uploaded_file else None

            if piece.notes:
                piece.notes.delete(save=False)
            if piece.notes_image:
                piece.notes_image.delete(save=False)

            # Create temporary InMemoryFile if needed
            if uploaded_file:
                from django.core.files.uploadedfile import InMemoryUploadedFile
                import io
                uploaded_file = InMemoryUploadedFile(
                    file=io.BytesIO(file_buffer),
                    field_name="notes",
                    name=uploaded_filename,
                    content_type="application/pdf",
                    size=len(file_buffer),
                    charset=None,
                )

            # Assign file to model BEFORE saving
            if uploaded_file:
                piece.notes = uploaded_file

            # Save model first so `piece.notes.path` is valid if needed
            piece = form.save(commit=False)

            manual_trukme = request.POST.get("trukme", "").strip()
            if manual_trukme:
                piece.duration = manual_trukme
            elif piece.youtube_url:
                video_id = extract_video_id(piece.youtube_url)
                if video_id:
                    new_duration = get_video_duration(video_id)
                    if new_duration:
                        piece.duration = new_duration

            piece.save()
            piece.ensembles.set(request.POST.getlist("ensembles"))
            piece.features.set(request.POST.getlist("features"))

            # Now safely convert the PDF
            if file_buffer:
                handle_pdf_conversion(file_buffer, piece)

            return JsonResponse({"success": True})

    form = PieceForm(instance=piece)
    features = Feature.objects.all()

    return render(request, "piece_edit.html", {
        "piece": piece,
        "form": form,
        "ensembles": user_ensembles,
        "features": features,
    })

def piece_delete(request, piece_id):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti kūrinių.")

    if request.method == "POST":
        piece = get_object_or_404(Piece, id=piece_id)

        # Delete files from storage if they exist
        if piece.notes:
            piece.notes.delete(save=False)

        if piece.notes_image:
            piece.notes_image.delete(save=False)

        piece.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Neteisingas užklausos metodas"}, status=400)

def piece_details(request, piece_id):
    piece = get_object_or_404(Piece.objects.prefetch_related("features"), id=piece_id)

    return JsonResponse({
        "lyrics": piece.lyrics or "",
        "description": piece.description or "",
        "youtube_url": piece.youtube_url,
        "pdf_url": piece.notes.url if piece.notes else "",
        "image_url": piece.notes_image.url if piece.notes_image else "",
        "tipas": piece.type,
        "pavadinimas": piece.title,
    })

def extract_video_id(url):
    """ Extract video ID from YouTube URL """
    match = re.search(r'(?:youtu\.be/|youtube\.com/(?:.*v=|.*\/|.*embed\/))([\w-]{11})', url)
    return match.group(1) if match else None

def get_video_duration(video_id):
    """ Fetch and format video duration from YouTube API """
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=contentDetails&key={YOUTUBE_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return format_duration(data["items"][0]["contentDetails"]["duration"])

    logger.warning(f"Failed to fetch duration for video ID: {video_id}")
    return None  # Return None if API fails

def format_duration(duration):
    """ Convert YouTube ISO 8601 duration to HH:MM:SS or MM:SS format with zero padding """
    match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)

    hours = int(match[1][:-1]) if match[1] else 0
    minutes = int(match[2][:-1]) if match[2] else 0
    seconds = int(match[3][:-1]) if match[3] else 0

    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"  #  Show HH:MM:SS if hours exist
    return f"{minutes:02}:{seconds:02}"  #  Show MM:SS if no hours

@csrf_exempt
def refresh_duration(request):
    """ Refreshes `duration` for all Kūriniai with YouTube URLs """
    updated_count = 0

    for piece in Piece.objects.exclude(youtube_url="").exclude(youtube_url__isnull=True):
        video_id = extract_video_id(piece.youtube_url)
        if video_id:
            new_duration = get_video_duration(video_id)
            if new_duration and piece.duration != new_duration:
                piece.duration = new_duration
                piece.save(update_fields=["duration"])
                updated_count += 1

    return JsonResponse({"success": True, "updated": updated_count})

def fetch_duration(request):
    """API: Fetch YouTube duration based on URL"""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

    youtube_url = request.POST.get("youtube_url", "").strip()
    if not youtube_url:
        return JsonResponse({"success": False, "error": "No URL provided"}, status=400)

    video_id = extract_video_id(youtube_url)
    if not video_id:
        return JsonResponse({"success": False, "error": "Invalid YouTube URL"}, status=400)

    trukme = get_video_duration(video_id)
    return JsonResponse({"success": True, "trukme": trukme})

def handle_pdf_conversion(file_buffer, piece):
    if not file_buffer:
        return

    doc = fitz.open(stream=file_buffer, filetype="pdf")
    if len(doc) == 1:
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=150)
        image_data = pix.tobytes("jpeg")
        filename = f"{piece.title}_natos.jpg"
        piece.notes_image.save(filename, ContentFile(image_data), save=False)
    else:
        if piece.notes_image:
            piece.notes_image.delete(save=False)
    doc.close()

def pieces_by_ensemble_feature(request):
    ensemble_id = request.GET.get("ensemble")
    feature_name = request.GET.get("feature")

    if not ensemble_id or not feature_name:
        return JsonResponse([], safe=False)

    pieces = Piece.objects.filter(
        ensembles__id=ensemble_id,
        duration__contains=":"
    ).filter(
        Q(features__title__iexact=feature_name) |
        Q(features__title__iexact="Start")
    ).distinct()

    return JsonResponse([
        {
            "id": k.id,
            "title": k.title,
            "duration": k.duration,
            "type": k.type,
            "region": k.region or ""
        } for k in pieces
    ], safe=False)