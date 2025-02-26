from django.shortcuts import render

# Hardcoded ensembles and Renginiai
ENSEMBLES = [
    {"id": 1, "name": "Folk Ensemble A"},
    {"id": 2, "name": "Folk Ensemble B"},
    {"id": 3, "name": "Folk Ensemble C"},
]

EVENTS = [
    {"id": 1, "name": "Event 1A", "address": "Address 1A", "date": "2024-01-10", "ensemble_id": 1},
    {"id": 2, "name": "Event 2A", "address": "Address 2A", "date": "2024-02-15", "ensemble_id": 1},
    {"id": 3, "name": "Event 3A", "address": "Address 3A", "date": "2024-03-20", "ensemble_id": 1},
    {"id": 4, "name": "Event 1B", "address": "Address 1B", "date": "2024-01-25", "ensemble_id": 2},
    {"id": 5, "name": "Event 2B", "address": "Address 2B", "date": "2024-02-28", "ensemble_id": 2},
    {"id": 6, "name": "Event 1C", "address": "Address 1C", "date": "2024-03-15", "ensemble_id": 3},
    {"id": 7, "name": "Event 2C", "address": "Address 2C", "date": "2024-04-01", "ensemble_id": 3},
]

def events_list(request):
    """
    Render the Renginiai list with ensemble selection.
    """
    selected_ensemble_id = request.GET.get('ensemble_id')
    filtered_events = EVENTS

    if selected_ensemble_id:
        # Filter Renginiai by ensemble
        filtered_events = [event for event in EVENTS if event["ensemble_id"] == int(selected_ensemble_id)]

    # Add ensemble name to each event
    for event in filtered_events:
        ensemble = next((e for e in ENSEMBLES if e["id"] == event["ensemble_id"]), None)
        if ensemble:
            event["ensemble_name"] = ensemble["name"]

    context = {
        "ensembles": ENSEMBLES,
        "events": filtered_events,  # Update key to match template variable
        "selected_ensemble_id": selected_ensemble_id,
    }
    return render(request, "renginiai.html", context)

def publicEvents(request):
    return render(request, 'renginiaiPublic.html', )