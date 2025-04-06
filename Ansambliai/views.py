from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET

from Kuriniai.models import Kurinys
from .models import Ansamblis
from .forms import AnsamblisForm

from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def ansambliai_list(request):
    if request.user.role != "administratorius":
        return HttpResponseForbidden("Jūs neturite teisės peržiūrėti ansamblių.")

    query = request.GET.get("search", "").strip()
    miestas_filter = request.GET.get("miestas", "").strip()
    sort_param = request.GET.get("sort", "pavadinimas")

    ansambliai = Ansamblis.objects.all()

    if query:
        ansambliai = ansambliai.filter(pavadinimas__icontains=query)

    if miestas_filter:
        ansambliai = ansambliai.filter(miestas__icontains=miestas_filter)

    if sort_param not in ["pavadinimas", "-pavadinimas"]:
        sort_param = "pavadinimas"

    ansambliai = ansambliai.order_by(sort_param)

    paginator = Paginator(ansambliai, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'ansambliai.html', {
        'page_obj': page_obj,
        'ansambliai': page_obj.object_list,
        'sort_param': sort_param,
        'search_query': query,
        'miestas_filter': miestas_filter,
        'all_miestai': Ansamblis.objects.values_list('miestas', flat=True).distinct()
    })

def ansamblis_add(request):
    if request.method == "POST":
        form = AnsamblisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ansambliai_list')
    else:
        form = AnsamblisForm()
    return render(request, 'ansamblis_add.html', {'form': form})


@login_required
def ansamblis_edit(request, pk):
    if request.user.role != "administratorius":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti ansamblių.")

    ansamblis = get_object_or_404(Ansamblis, pk=pk)
    if request.method == "POST":
        form = AnsamblisForm(request.POST, instance=ansamblis)
        if form.is_valid():
            form.save()
            return redirect('ansambliai_list')
    else:
        form = AnsamblisForm(instance=ansamblis)

    return render(request, 'ansamblis_edit.html', {'form': form})


@login_required
def ansamblis_delete(request, pk):
    if request.user.role != "administratorius":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti ansamblių.")

    ansamblis = get_object_or_404(Ansamblis, pk=pk)
    if request.method == "POST":
        ansamblis.delete()
        return redirect('ansambliai_list')

    return render(request, 'ansamblis_confirm_delete.html', {'ansamblis': ansamblis})

@login_required
def get_kuriniai_by_ansamblis(request, pk):
    ansamblis = get_object_or_404(Ansamblis, pk=pk)

    kuriniai = Kurinys.objects.filter(ansambliai=ansamblis).prefetch_related("pozymiai")

    kuriniai_data = []
    for kurinys in kuriniai:
        pozymiai_list = list(kurinys.pozymiai.values_list("pavadinimas", flat=True))  # ✅ fix here

        kuriniai_data.append({
            "id": kurinys.id,
            "pavadinimas": kurinys.pavadinimas,
            "trukme": kurinys.trukme or "00:00",
            "tipas": kurinys.tipas or "N/A",
            "regionas": kurinys.regionas or "N/A",
            "lyrics": kurinys.lyrics,
            "aprašymas": kurinys.aprasymas,
            "youtube_url": kurinys.youtube_url,
            "natos": kurinys.natos.url if kurinys.natos else "",
            "natos_image": kurinys.natos_image.url if kurinys.natos_image else "",
            "pozymiai": pozymiai_list,  # ✅ critical
        })

    return JsonResponse(kuriniai_data, safe=False)

@require_GET
def filtered_kuriniai(request, ansamblis_id):
    pozymis = request.GET.get("pozymis")
    if not pozymis:
        return JsonResponse({"error": "Požymis parametras yra privalomas."}, status=400)

    kuriniai = Kurinys.objects.filter(
        ansambliai__id=ansamblis_id,
        pozymiai__pavadinimas=pozymis
    ).distinct().values(
        "id", "pavadinimas", "trukme", "tipas", "regionas",
        "lyrics", "aprasymas", "youtube_url", "natos", "natos_image"
    )

    return JsonResponse(list(kuriniai), safe=False)
