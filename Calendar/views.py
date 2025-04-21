from django.urls import reverse, NoReverseMatch
from django.shortcuts import render
from django.http import JsonResponse

from Ensembles.models import Ensemble
from Events.models import Event
from Rehearsals.models import Rehearsal

# Specific colors for different event types (models)
MODEL_COLORS = {
    "Renginiai": "#ff0000",  # Red
    "Repeticijos": "#28a745",  # Green
    "Kita": "#ffc107",  # Yellow (Default)
}


def calendar_view(request):
    """ Renders the calendar template with ansamblis selection """
    all_ensembles = Ensemble.objects.all()
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")

    return render(request, "calendar.html", {
        "all_ensembles": all_ensembles,
        "selected_ansamblis_id": selected_ansamblis_id
    })

def calendar_events(request):
    events = []
    selected_ensemble_id = request.session.get("selected_ensemble_id")

    # Filter Renginiai
    events_qs = Event.objects.all()
    if selected_ensemble_id:
        events_qs = events_qs.filter(ensemble__id=selected_ensemble_id)

    for event in events_qs:
        event_type = "Renginiai"
        event_color = MODEL_COLORS.get(event_type, "#ffc107")

        try:
            event_url = reverse('renginiai_detail', kwargs={'pk': event.pk})
        except NoReverseMatch:
            event_url = "#"

        events.append({
            "title": event.title,
            "start": event.date.isoformat(),
            "url": event_url,
            "extendedProps": {
                "type": "Renginys",
                "color": event_color
            },
            "backgroundColor": event_color,
            "borderColor": event_color,
            "textColor": "#ffffff"
        })

    # Filter Repeticijos
    rehearsals_qs = Rehearsal.objects.all()
    if selected_ensemble_id:
        rehearsals_qs = rehearsals_qs.filter(ensemble__id=selected_ensemble_id)

    for rehearsal in rehearsals_qs:
        event_type = "Repeticijos"
        event_color = MODEL_COLORS.get(event_type, "#ffc107")

        try:
            event_url = reverse('repeticija_detail', kwargs={'pk': rehearsal.pk})
        except NoReverseMatch:
            event_url = "#"

        events.append({
            "title": rehearsal.title,
            "start": rehearsal.date.isoformat(),
            "url": event_url,
            "extendedProps": {
                "type": "Repeticija",
                "color": event_color
            },
            "backgroundColor": event_color,
            "borderColor": event_color,
            "textColor": "#ffffff"
        })

    return JsonResponse(events, safe=False)
