from django.urls import reverse, NoReverseMatch
from django.shortcuts import render
from django.http import JsonResponse
from Renginiai.models import Renginys
from Repeticijos.models import Repeticija

# ✅ Define specific colors for different event types (models)
MODEL_COLORS = {
    "Renginiai": "#ff0000",  # Red
    "Repeticijos": "#28a745",  # Green
    "Kita": "#ffc107",  # Yellow (Default)
}


def kalendorius_view(request):
    """ Renders the calendar template """
    return render(request, "kalendorius.html")


def kalendorius_events(request):
    """Returns events with colors and links to details for FullCalendar"""
    events = []

    # ✅ Fetch events from Renginiai
    for event in Renginys.objects.all():
        event_type = "Renginiai"
        event_color = MODEL_COLORS.get(event_type, "#ffc107")  # Default Yellow if not found

        try:
            event_url = reverse('renginiai_detail', kwargs={'pk': event.pk})  # ✅ URL for event details
        except NoReverseMatch:
            event_url = "#"  # ✅ Prevents crash if URL is incorrect

        event_data = {
            "title": event.pavadinimas,
            "start": event.data_laikas.isoformat(),
            "url": event_url,  # ✅ Redirect URL
            "extendedProps": {
                "type": event_type,
                "color": event_color
            },
            "backgroundColor": event_color,
            "borderColor": event_color,
            "textColor": "#ffffff"
        }

        events.append(event_data)

    # ✅ Fetch events from Repeticijos
    for rehearsal in Repeticija.objects.all():
        event_type = "Repeticijos"
        event_color = MODEL_COLORS.get(event_type, "#ffc107")  # Default Yellow if not found

        try:
            event_url = reverse('repeticija_detail', kwargs={'pk': rehearsal.pk})  # ✅ URL for event details
        except NoReverseMatch:
            event_url = "#"  # ✅ Prevents crash if URL is incorrect

        event_data = {
            "title": rehearsal.pavadinimas,
            "start": rehearsal.data.isoformat(),
            "url": event_url,  # ✅ Redirect URL
            "extendedProps": {
                "type": event_type,
                "color": event_color
            },
            "backgroundColor": event_color,
            "borderColor": event_color,
            "textColor": "#ffffff"
        }

        events.append(event_data)

    return JsonResponse(events, safe=False)
