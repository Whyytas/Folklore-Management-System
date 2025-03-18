from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from Ansambliai.models import Ansamblis
from .models import Instrumentas
from .forms import InstrumentasForm
from django.http import HttpResponseForbidden

def instrumentai_list(request):
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")
    instrumentai = Instrumentas.objects.all().order_by("-id")

    if selected_ansamblis_id:
        instrumentai = instrumentai.filter(ansamblis__id=selected_ansamblis_id)

    all_ansambliai = Ansamblis.objects.all()

    return render(request, "instrumentai.html", {
        "instrumentai": instrumentai,
        "all_ansambliai": all_ansambliai,
        "selected_ansamblis_id": selected_ansamblis_id
    })

def instrumentai_add(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės sukurti instrumentų.")

    ansambliai = Ansamblis.objects.all()

    if request.method == "POST":
        form = InstrumentasForm(request.POST, request.FILES)  # ✅ Include request.FILES to handle file uploads
        if form.is_valid():
            instrumentas = form.save(commit=False)

            # ✅ Ensure the file is assigned properly
            if "nuotrauka" in request.FILES:
                instrumentas.nuotrauka = request.FILES["nuotrauka"]

            # ✅ Save ansamblis selection
            ansamblis_id = request.POST.get("ansamblis")
            if ansamblis_id:
                instrumentas.ansamblis = get_object_or_404(Ansamblis, pk=ansamblis_id)

            instrumentas.save()
            messages.success(request, "Instrumentas sėkmingai pridėtas!")
            return redirect("instrumentai_list")

    else:
        form = InstrumentasForm()

    return render(request, "instrumentai_add.html", {"form": form, "ansambliai": ansambliai})


def instrumentai_edit(request, pk):

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti instrumentų.")

    instrumentas = get_object_or_404(Instrumentas, pk=pk)
    ansambliai = Ansamblis.objects.all()

    if request.method == "POST":
        form = InstrumentasForm(request.POST, request.FILES, instance=instrumentas)
        if form.is_valid():
            instrumentas = form.save(commit=False)

            # ✅ Ensure nuotrauka is updated if a new file is uploaded
            if "nuotrauka" in request.FILES:
                instrumentas.nuotrauka = request.FILES["nuotrauka"]

            instrumentas.save()
            messages.success(request, "Instrumentas sėkmingai atnaujintas!")
            return redirect("instrumentai_list")

    else:
        form = InstrumentasForm(instance=instrumentas)

    return render(request, "instrumentai_edit.html",
                  {"form": form, "instrumentas": instrumentas, "ansambliai": ansambliai})
def instrumentai_delete(request, pk):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti instrumentų.")

    instrumentas = get_object_or_404(Instrumentas, pk=pk)
    instrumentas.delete()
    messages.success(request, "Instrumentas ištrintas!")
    return redirect("instrumentai_list")
