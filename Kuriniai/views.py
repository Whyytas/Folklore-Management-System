import requests
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Kurinys
from .forms import KurinysForm

# Set up logging
logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = "AIzaSyAX8QZHAYYSdEozYqHwH2XytcmrOG055Bo"  # ⚠️ Replace with your actual API key

def kuriniai_list(request):
    """ Retrieve and display all Kūriniai """
    kuriniai = Kurinys.objects.all()
    return render(request, 'Kuriniai/kuriniai.html', {'kuriniai': kuriniai})

def kuriniai_add(request):
    """ Handles the creation of a new Kūrinys """
    if request.method == "POST":
        form = KurinysForm(request.POST)
        if form.is_valid():
            kurinys = form.save(commit=False)

            # ✅ Fetch video duration if YouTube URL is provided
            if kurinys.youtube_url:
                video_id = extract_video_id(kurinys.youtube_url)
                if video_id:
                    kurinys.trukme = get_video_duration(video_id)

            kurinys.save()
            return redirect('kuriniai')  # ✅ Redirect back to the list view

    else:
        form = KurinysForm()

    return render(request, 'Kuriniai/kuriniaiAdd.html', {'form': form})

def kuriniai_edit(request, kurinys_id):
    kurinys = get_object_or_404(Kurinys, id=kurinys_id)

    if request.method == "POST":
        kurinys.pavadinimas = request.POST.get("pavadinimas")
        kurinys.tipas = request.POST.get("tipas")
        kurinys.youtube_url = request.POST.get("youtube_url", "").strip()
        kurinys.trukme = request.POST.get("trukme")

        kurinys.save()
        return JsonResponse({"success": True})

    return render(request, "Kuriniai/kuriniaiEdit.html", {
        "kurinys": kurinys,
        "TIPAS_CHOICES": Kurinys.TIPAS_CHOICES  # Pass choices dynamically
    })

def delete_kurinys(request, kurinys_id):
    """ Deletes the selected Kūrinys """
    if request.method == "POST":
        kurinys = get_object_or_404(Kurinys, id=kurinys_id)
        kurinys.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Neteisingas užklausos metodas"}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Kurinys
import re

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

