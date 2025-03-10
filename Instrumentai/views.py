from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from Ansambliai.models import Ansamblis
from .models import Instrumentas
from .forms import InstrumentasForm
from django.http import HttpResponseForbidden

def instrumentai_list(request):
    instrumentai = Instrumentas.objects.all()
    return render(request, "instrumentai.html", {"instrumentai": instrumentai})

def instrumentai_add(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti instrumentų.")

    ansambliai = Ansamblis.objects.all()
    if request.method == "POST":
        form = InstrumentasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Instrumentas sėkmingai pridėtas!")
            return redirect("instrumentai_list")
    else:
        form = InstrumentasForm()

    return render(request, "instrumentai_add.html", {"form": form, "ansambliai": ansambliai})
def instrumentai_edit(request, pk):
    instrumentas = get_object_or_404(Instrumentas, pk=pk)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti instrumentų.")

    if request.method == "POST":
        form = InstrumentasForm(request.POST, instance=instrumentas)
        if form.is_valid():
            form.save()
            messages.success(request, "Instrumentas sėkmingai atnaujintas!")
            return redirect("instrumentai_list")
    else:
        form = InstrumentasForm(instance=instrumentas)

    return render(request, "instrumentai_edit.html", {"form": form})

def instrumentai_delete(request, pk):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti instrumentų.")

    instrumentas = get_object_or_404(Instrumentas, pk=pk)
    instrumentas.delete()
    messages.success(request, "Instrumentas ištrintas!")
    return redirect("instrumentai_list")
