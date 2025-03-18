from django.urls import reverse, NoReverseMatch
from django.shortcuts import render
from django.http import JsonResponse

from Ansambliai.models import Ansamblis
from Renginiai.models import Renginys
from Repeticijos.models import Repeticija

# ✅ Define specific colors for different event types (models)
MODEL_COLORS = {
    "Renginiai": "#ff0000",  # Red
    "Repeticijos": "#28a745",  # Green
    "Kita": "#ffc107",  # Yellow (Default)
}


def kalendorius_view(request):
    """ Renders the calendar template with ansamblis selection """
    all_ansambliai = Ansamblis.objects.all()
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")

    return render(request, "kalendorius.html", {
        "all_ansambliai": all_ansambliai,
        "selected_ansamblis_id": selected_ansamblis_id
    })

def kalendorius_events(request):
    events = []
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")

    # 🔴 Filter Renginiai
    renginiai_qs = Renginys.objects.all()
    if selected_ansamblis_id:
        renginiai_qs = renginiai_qs.filter(ansamblis__id=selected_ansamblis_id)

    for event in renginiai_qs:
        event_type = "Renginiai"
        event_color = MODEL_COLORS.get(event_type, "#ffc107")

        try:
            event_url = reverse('renginiai_detail', kwargs={'pk': event.pk})
        except NoReverseMatch:
            event_url = "#"

        events.append({
            "title": event.pavadinimas,
            "start": event.data_laikas.isoformat(),
            "url": event_url,
            "extendedProps": {
                "type": event_type,
                "color": event_color
            },
            "backgroundColor": event_color,
            "borderColor": event_color,
            "textColor": "#ffffff"
        })

    # 🟢 Filter Repeticijos
    repeticijos_qs = Repeticija.objects.all()
    if selected_ansamblis_id:
        repeticijos_qs = repeticijos_qs.filter(ansamblis__id=selected_ansamblis_id)

    for rehearsal in repeticijos_qs:
        event_type = "Repeticijos"
        event_color = MODEL_COLORS.get(event_type, "#ffc107")

        try:
            event_url = reverse('repeticija_detail', kwargs={'pk': rehearsal.pk})
        except NoReverseMatch:
            event_url = "#"

        events.append({
            "title": rehearsal.pavadinimas,
            "start": rehearsal.data.isoformat(),
            "url": event_url,
            "extendedProps": {
                "type": event_type,
                "color": event_color
            },
            "backgroundColor": event_color,
            "borderColor": event_color,
            "textColor": "#ffffff"
        })

    return JsonResponse(events, safe=False)
