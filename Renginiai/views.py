from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import make_aware

from Ansambliai.models import Ansamblis
from Programos.models import Programa
from .models import Renginys
from .forms import RenginysForm
from django.http import HttpResponseForbidden
import datetime  # ✅ Correct way to import datetime module


def renginiai_list(request):
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")
    sort_field = request.GET.get("sort", "pavadinimas")
    sort_dir = request.GET.get("dir", "asc")
    programa_id = request.GET.get("programa_id")
    search = request.GET.get("search", "").strip()

    sort_order = sort_field if sort_dir == "asc" else f"-{sort_field}"
    renginiai = Renginys.objects.all().order_by(sort_order, "-id")

    if selected_ansamblis_id:
        renginiai = renginiai.filter(ansamblis__id=selected_ansamblis_id)
    if programa_id:
        renginiai = renginiai.filter(programa__id=programa_id)
    if search:
        renginiai = renginiai.filter(pavadinimas__icontains=search)

    paginator = Paginator(renginiai, 15)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return render(request, 'renginiai.html', {
        'renginiai': page_obj.object_list,
        'page_obj': page_obj,
        'sort_field': sort_field,
        'sort_dir': sort_dir,
        'programa_id': programa_id,
        'search': search,
        'programos': Programa.objects.all(),
    })
def renginiai_add(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti renginių.")

    if request.method == "POST":
        form = RenginysForm(request.POST)
        if form.is_valid():
            renginys = form.save(commit=False)
            renginys.data_laikas = make_aware(renginys.data_laikas)
            renginys.save()
            return redirect("renginiai")

    form = RenginysForm()
    return render(request, "renginiai_add.html", {"form": form})

def renginiai_edit(request, renginys_id):
    renginys = get_object_or_404(Renginys, id=renginys_id)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti renginių.")

    if request.method == "POST":
        form = RenginysForm(request.POST, instance=renginys)
        if form.is_valid():
            renginys = form.save(commit=False)
            if isinstance(form.cleaned_data["data_laikas"], str):
                naive_datetime = datetime.datetime.strptime(form.cleaned_data["data_laikas"], "%Y-%m-%d %H:%M")
                renginys.data_laikas = make_aware(naive_datetime)
            else:
                renginys.data_laikas = make_aware(form.cleaned_data["data_laikas"])
            renginys.save()
            return redirect('renginiai')

    renginys.data_laikas = renginys.data_laikas.strftime("%Y-%m-%d %H:%M") if renginys.data_laikas else ""
    form = RenginysForm(instance=renginys)

    return render(request, "renginiai_edit.html", {
        "renginys": renginys,
        "form": form,
        "ansambliai": Ansamblis.objects.all(),
        "programos": Programa.objects.all()
    })

def delete_renginys(request, renginys_id):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti renginių.")

    if request.method == "POST":
        renginys = get_object_or_404(Renginys, id=renginys_id)
        renginys.delete()
        return redirect("renginiai")  # ✅ Redirect to the renginiai list

    return JsonResponse({"error": "Invalid request method"}, status=400)

def publicEvents(request):
    return render(request, 'renginiaiPublic.html', )

