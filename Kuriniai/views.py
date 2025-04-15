import fitz
import requests
import logging

from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET

from Ansambliai.models import Ansamblis
from .forms import KurinysForm
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Kurinys, Pozymis
import re
from django.http import HttpResponseForbidden

# Set up logging
logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY  # ⚠️ Replace with your actual API key



def kuriniai_list(request):
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")
    sort_param = request.GET.get("sort", "pavadinimas")

    valid_sorts = ["pavadinimas", "-pavadinimas", "trukme", "-trukme"]
    if sort_param not in valid_sorts:
        sort_param = "pavadinimas"

    filters = {
        'tipas': request.GET.get('tipas'),
        'regionas': request.GET.get('regionas'),
        'greitumas': request.GET.get('greitumas'),
        'paruosimas': request.GET.get('paruosimas'),
        'pozymiai': request.GET.get('pozymiai'),
    }

    # ⚡ Optimized QuerySet with prefetch
    kuriniai = Kurinys.objects.prefetch_related("ansambliai", "pozymiai")

    if selected_ansamblis_id:
        kuriniai = kuriniai.filter(ansambliai__id=selected_ansamblis_id)

    if filters['tipas']:
        kuriniai = kuriniai.filter(tipas=filters['tipas'])
    if filters['regionas']:
        kuriniai = kuriniai.filter(regionas=filters['regionas'])
    if filters['greitumas']:
        kuriniai = kuriniai.filter(greitumas=filters['greitumas'])
    if filters['paruosimas']:
        kuriniai = kuriniai.filter(paruosimas=filters['paruosimas'])
    if filters['pozymiai']:
        kuriniai = kuriniai.filter(pozymiai__id=filters['pozymiai'])

    kuriniai = kuriniai.order_by(sort_param)

    return render(request, "kuriniai.html", {
        "page_obj": None,
        "kuriniai": kuriniai,
        "all_ansambliai": Ansamblis.objects.all(),
        "all_pozymiai": Pozymis.objects.all(),
        "filters": filters,
        "tipas_choices": Kurinys.TIPAS_CHOICES,
        "greitumas_choices": Kurinys.GREITUMAS_CHOICES,
        "paruosimas_choices": Kurinys.PARUOSIMAS_CHOICES,
        "regionas_choices": Kurinys._meta.get_field("regionas").choices,
        "sort_param": sort_param,
    })

def kuriniai_add(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti kūrinių.")

    user_is_admin = request.user.role == "administratorius"
    ansambliai_queryset = Ansamblis.objects.all() if user_is_admin else request.user.ansambliai.all()

    if request.method == "POST":
        form = KurinysForm(request.POST, request.FILES)
        if form.is_valid():
            kurinys = form.save(commit=False)

            manual_trukme = request.POST.get("trukme", "").strip()
            if manual_trukme:
                kurinys.trukme = manual_trukme
            elif kurinys.youtube_url:
                video_id = extract_video_id(kurinys.youtube_url)
                if video_id:
                    kurinys.trukme = get_video_duration(video_id)

            kurinys.save()
            kurinys.ansambliai.set(request.POST.getlist("ansambliai"))
            kurinys.pozymiai.set(request.POST.getlist("pozymiai"))

            if 'natos' in request.FILES:
                handle_pdf_conversion(kurinys)
                kurinys.save()

            return redirect('/kuriniai/?success=true')
    else:
        form = KurinysForm()

    return render(request, 'kuriniaiAdd.html', {
        "form": form,
        "ansambliai": ansambliai_queryset,
        "pozymiai": Pozymis.objects.all(),  # ✅ provide Požymiai to template
    })


from .models import Kurinys, Pozymis

def kuriniai_edit(request, kurinys_id):
    kurinys = get_object_or_404(Kurinys, id=kurinys_id)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti kūrinių.")

    user_ansambliai = Ansamblis.objects.all() if request.user.role == "administratorius" else request.user.ansambliai.all()

    if request.method == "POST":
        form = KurinysForm(request.POST, request.FILES, instance=kurinys)
        if form.is_valid():
            kurinys = form.save(commit=False)

            manual_trukme = request.POST.get("trukme", "").strip()
            if manual_trukme:
                kurinys.trukme = manual_trukme
            elif kurinys.youtube_url:
                video_id = extract_video_id(kurinys.youtube_url)
                if video_id:
                    new_trukme = get_video_duration(video_id)
                    if new_trukme:
                        kurinys.trukme = new_trukme

            # Handle new PDF upload
            if 'natos' in request.FILES:
                if kurinys.natos:
                    kurinys.natos.delete(save=False)
                if kurinys.natos_image:
                    kurinys.natos_image.delete(save=False)

                kurinys.natos = request.FILES['natos']
                handle_pdf_conversion(kurinys)

            kurinys.save()
            kurinys.ansambliai.set(request.POST.getlist("ansambliai"))
            kurinys.pozymiai.set(request.POST.getlist("pozymiai"))

            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "error": "Invalid form data"}, status=400)

    form = KurinysForm(instance=kurinys)
    pozymiai = Pozymis.objects.all()

    return render(request, "kuriniaiEdit.html", {
        "kurinys": kurinys,
        "form": form,
        "ansambliai": user_ansambliai,
        "pozymiai": pozymiai,
    })

def delete_kurinys(request, kurinys_id):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti kūrinių.")

    if request.method == "POST":
        kurinys = get_object_or_404(Kurinys, id=kurinys_id)

        # Delete files from storage if they exist
        if kurinys.natos:
            kurinys.natos.delete(save=False)

        if kurinys.natos_image:
            kurinys.natos_image.delete(save=False)

        kurinys.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Neteisingas užklausos metodas"}, status=400)

def kurinys_details(request, kurinys_id):
    kurinys = get_object_or_404(Kurinys.objects.prefetch_related("pozymiai"), id=kurinys_id)

    return JsonResponse({
        "lyrics": kurinys.lyrics or "",
        "description": kurinys.aprasymas or "",
        "youtube_url": kurinys.youtube_url,
        "pdf_url": kurinys.natos.url if kurinys.natos else "",
        "image_url": kurinys.natos_image.url if kurinys.natos_image else "",
        "tipas": kurinys.tipas,
        "pavadinimas": kurinys.pavadinimas,
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

def kuriniai_by_ansamblis_pozymis(request):
    ansamblis_id = request.GET.get("ansamblis")
    pozymis_name = request.GET.get("pozymis")

    if not ansamblis_id or not pozymis_name:
        return JsonResponse([], safe=False)

    kuriniai = Kurinys.objects.filter(
        ansambliai__id=ansamblis_id,
        trukme__contains=":"
    ).filter(
        Q(pozymiai__pavadinimas__iexact=pozymis_name) |
        Q(pozymiai__pavadinimas__iexact="Pradžia")
    ).distinct()

    return JsonResponse([
        {
            "id": k.id,
            "pavadinimas": k.pavadinimas,
            "trukme": k.trukme,
            "tipas": k.tipas,
            "regionas": k.regionas or ""
        } for k in kuriniai
    ], safe=False)