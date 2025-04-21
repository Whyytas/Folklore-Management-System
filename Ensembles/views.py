from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET

from Pieces.models import Piece
from Departments.models import Department
from .models import Ensemble
from .forms import EnsembleForm

from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required

def ensembles_list(request):
    if request.user.role != "administratorius":
        return HttpResponseForbidden("Jūs neturite teisės peržiūrėti ansamblių.")

    query = request.GET.get("search", "").strip()
    city_filter = request.GET.get("city", "").strip()
    sort_param = request.GET.get("sort", "title")

    if sort_param not in ["title", "-title"]:
        sort_param = "title"

    # Only fetch required fields
    ensembles_qs = Ensemble.objects.only("id", "title", "city", "department_id").select_related("department")

    if query:
        ensembles_qs = ensembles_qs.filter(title__icontains=query)

    if city_filter:
        ensembles_qs = ensembles_qs.filter(city__icontains=city_filter)

    ensembles_qs = ensembles_qs.order_by(sort_param)

    all_cities = Ensemble.objects.order_by().values_list('city', flat=True).distinct()

    return render(request, 'ensembles_list.html', {
        'ensembles': ensembles_qs,
        'sort_param': sort_param,
        'search_query': query,
        'city_filter': city_filter,
        'all_cities': all_cities,
    })

def ensemble_add(request):
    if request.method == "POST":
        form = EnsembleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ansambliai_list')
    else:
        form = EnsembleForm()
    departments = Department.objects.all()
    return render(request, 'ensemble_add.html', {'form': form, 'departments': departments})


@login_required
def ensemble_edit(request, pk):
    if request.user.role != "administratorius":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti ansamblių.")

    ensemble = get_object_or_404(Ensemble, pk=pk)
    if request.method == "POST":
        form = EnsembleForm(request.POST, instance=ensemble)
        if form.is_valid():
            form.save()
            return redirect('ansambliai_list')
    else:
        form = EnsembleForm(instance=ensemble)
    departments = Department.objects.all()
    return render(request, 'ensemble_edit.html', {
        'form': form,
        'departments': departments
    })


@login_required
def ensemble_delete(request, pk):
    if request.user.role != "administratorius":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti ansamblių.")

    ensemble = get_object_or_404(Ensemble, pk=pk)
    if request.method == "POST":
        ensemble.delete()
        return redirect('ansambliai_list')

    return render(request, 'ansamblis_confirm_delete.html', {'ensemble': ensemble})

@login_required
def get_pieces_by_ensemble(request, pk):
    ensemble = get_object_or_404(Ensemble, pk=pk)

    pieces = Piece.objects.filter(ensembles=ensemble).prefetch_related("features")

    pieces_data = []
    for piece in pieces:
        features_list = list(piece.features.values_list("title", flat=True))  #  fix here

        pieces_data.append({
            "id": piece.id,
            "title": piece.title,
            "duration": piece.duration or "00:00",
            "type": piece.type or "N/A",
            "region": piece.region or "N/A",
            "lyrics": piece.lyrics,
            "description": piece.description,
            "youtube_url": piece.youtube_url,
            "notes": piece.notes.url if piece.notes else "",
            "notes_image": piece.notes_image.url if piece.notes_image else "",
            "features": features_list,  #  critical
        })

    return JsonResponse(pieces_data, safe=False)

@require_GET
def filtered_pieces(request, ensemble_id):
    feature = request.GET.get("feature")
    if not feature:
        return JsonResponse({"error": "Požymis parametras yra privalomas."}, status=400)

    pieces = Piece.objects.filter(
        ensembles__id=ensemble_id,
        features__title=feature
    ).distinct().values(
        "id", "title", "duration", "type", "region",
        "lyrics", "description", "youtube_url", "notes", "notes_image"
    )

    return JsonResponse(list(pieces), safe=False)
