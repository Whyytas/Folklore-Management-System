from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from Ensembles.models import Ensemble
from .models import Instrument
from .forms import InstrumentForm
from django.http import HttpResponseForbidden

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseForbidden

def instruments_list(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės peržiūrėti instrumentų.")

    selected_ensemble_id = request.session.get("selected_ensemble_id")
    search = request.GET.get("search", "").strip()
    sort_param = request.GET.get("sort", "title")

    instruments = Instrument.objects.select_related("ensemble").all()

    if selected_ensemble_id:
        instruments = instruments.filter(ensemble__id=selected_ensemble_id)

    if search:
        instruments = instruments.filter(title__icontains=search)

    instruments = instruments.order_by(sort_param)

    return render(request, "instruments_list.html", {
        "instruments": instruments,  # ⚠️ No pagination
        "all_ensembles": Ensemble.objects.all(),
        "selected_ensemble_id": selected_ensemble_id,
        "search": search,
        "sort_param": sort_param,
    })

def instrument_add(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės sukurti instrumentų.")

    ensembles = Ensemble.objects.all()

    if request.method == "POST":
        form = InstrumentForm(request.POST, request.FILES)  #  Include request.FILES to handle file uploads
        if form.is_valid():
            instrument = form.save(commit=False)

            #  Ensure the file is assigned properly
            if "photo" in request.FILES:
                instrument.photo = request.FILES["photo"]

            #  Save ansamblis selection
            ensemble_id = request.POST.get("ensemble")
            if ensemble_id:
                instrument.ensemble = get_object_or_404(Ensemble, pk=ensemble_id)

            instrument.save()
            messages.success(request, "Instrumentas sėkmingai pridėtas!")
            return redirect("instrumentai_list")

    else:
        form = InstrumentForm()

    return render(request, "instrument_add.html", {"form": form, "ensembles": ensembles})


def instrument_edit(request, pk):

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti instrumentų.")

    instrument = get_object_or_404(Instrument, pk=pk)
    ensembles = Ensemble.objects.all()

    if request.method == "POST":
        form = InstrumentForm(request.POST, request.FILES, instance=instrument)
        if form.is_valid():
            instrument = form.save(commit=False)

            #  Ensure nuotrauka is updated if a new file is uploaded
            if "photo" in request.FILES:
                instrument.photo = request.FILES["photo"]

            instrument.save()
            messages.success(request, "Instrumentas sėkmingai atnaujintas!")
            return redirect("instrumentai_list")

    else:
        form = InstrumentForm(instance=instrument)

    return render(request, "instrument_edit.html",
                  {"form": form, "instrument": instrument, "ensembles": ensembles})
def instrument_delete(request, pk):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti instrumentų.")

    instrument = get_object_or_404(Instrument, pk=pk)
    instrument.delete()
    messages.success(request, "Instrumentas ištrintas!")
    return redirect("instrumentai_list")
