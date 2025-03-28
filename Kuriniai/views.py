import fitz
import requests
import logging

from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404

from Ansambliai.models import Ansamblis
from .forms import KurinysForm
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Kurinys
import re
from django.http import HttpResponseForbidden

# Set up logging
logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY  # ⚠️ Replace with your actual API key


def kuriniai_list(request):
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")
    kuriniai = Kurinys.objects.all().order_by("-created_at", "-id")
    if selected_ansamblis_id:
        kuriniai = kuriniai.filter(ansambliai__id=selected_ansamblis_id).distinct()
    all_ansambliai = Ansamblis.objects.all()

    return render(request, "kuriniai.html", {
        "kuriniai": kuriniai,
        "all_ansambliai": all_ansambliai
    })

def kuriniai_add(request):
    # Restrict access for 'narys' role
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti kūrinių.")

    # Determine which ansambliai the user can choose
    if request.user.role == "administratorius":
        ansambliai_queryset = Ansamblis.objects.all()
    else:
        ansambliai_queryset = request.user.ansambliai.all()

    if request.method == "POST":
        form = KurinysForm(request.POST, request.FILES)
        if form.is_valid():
            kurinys = form.save(commit=False)

            if kurinys.youtube_url:
                video_id = extract_video_id(kurinys.youtube_url)
                if video_id:
                    kurinys.trukme = get_video_duration(video_id)

            kurinys.save()
            kurinys.ansambliai.set(request.POST.getlist("ansambliai"))

            handle_pdf_conversion(kurinys)
            kurinys.save()

            return redirect('/kuriniai/?success=true')

    else:
        form = KurinysForm()

    return render(request, 'kuriniaiAdd.html', {
        "form": form,
        "ansambliai": ansambliai_queryset
    })


def kuriniai_edit(request, kurinys_id):
    kurinys = get_object_or_404(Kurinys, id=kurinys_id)

    # ✅ Show correct ansambliai
    user_ansambliai = Ansamblis.objects.all() if request.user.role == "administratorius" else request.user.ansambliai.all()

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti kūrinių.")
    if request.method == "POST":
        form = KurinysForm(request.POST, request.FILES, instance=kurinys)
        if form.is_valid():
            kurinys = form.save(commit=False)

            if kurinys.youtube_url:
                video_id = extract_video_id(kurinys.youtube_url)
                if video_id:
                    new_trukme = get_video_duration(video_id)
                    if new_trukme:
                        kurinys.trukme = new_trukme

            kurinys.save()
            kurinys.ansambliai.set(request.POST.getlist("ansambliai"))

            if 'natos' in request.FILES:
                handle_pdf_conversion(kurinys)
                kurinys.save()

            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "error": "Invalid form data"}, status=400)

    form = KurinysForm(instance=kurinys)
    return render(request, "kuriniaiEdit.html", {
        "kurinys": kurinys,
        "form": form,
        "ansambliai": user_ansambliai
    })

def delete_kurinys(request, kurinys_id):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti kūrinių.")

    if request.method == "POST":
        kurinys = get_object_or_404(Kurinys, id=kurinys_id)
        kurinys.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Neteisingas užklausos metodas"}, status=400)


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
        return f"{hours:02}:{minutes:02}:{seconds:02}"  # ✅ Show HH:MM:SS if hours exist
    return f"{minutes:02}:{seconds:02}"  # ✅ Show MM:SS if no hours


@csrf_exempt
def refresh_trukme(request):
    """ Refreshes `trukmė` for all Kūriniai with YouTube URLs """
    updated_count = 0

    for kurinys in Kurinys.objects.exclude(youtube_url="").exclude(youtube_url__isnull=True):
        video_id = extract_video_id(kurinys.youtube_url)
        if video_id:
            new_trukme = get_video_duration(video_id)
            if new_trukme and kurinys.trukme != new_trukme:
                kurinys.trukme = new_trukme
                kurinys.save(update_fields=["trukme"])
                updated_count += 1

    return JsonResponse({"success": True, "updated": updated_count})


def fetch_trukme(request):
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

def handle_pdf_conversion(kurinys):
    if kurinys.natos:
        kurinys.natos.seek(0)  # Reset file pointer
        pdf_data = kurinys.natos.read()

        doc = fitz.open(stream=pdf_data, filetype="pdf")
        if len(doc) == 1:
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=150)  # Adjust DPI if needed
            image_data = pix.tobytes("jpeg")

            filename = f"{kurinys.pavadinimas}_natos.jpg"
            kurinys.natos_image.save(filename, ContentFile(image_data), save=False)
        else:
            if kurinys.natos_image:
                kurinys.natos_image.delete(save=False)
        doc.close()
