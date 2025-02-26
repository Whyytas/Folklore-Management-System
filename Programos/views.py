import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProgramaForm
from Kuriniai.models import Kurinys
from .models import Programa, ProgramosKurinys


def programos_page(request):
    programos = Programa.objects.all()  # ✅ Fetch programs from the database
    return render(request, 'Programos/programos.html', {'programos': programos})

def program_create(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pavadinimas = data.get("pavadinimas")
        tipas = data.get("tipas")
        kuriniai_data = data.get("kuriniai", [])

        programa = Programa.objects.create(
            pavadinimas=pavadinimas,
            tipas=tipas
        )

        for item in kuriniai_data:
            kurinys_id = item["id"]
            eile = item["eile"]
            kurinys = Kurinys.objects.get(id=kurinys_id)
            ProgramosKurinys.objects.create(
                programa=programa,
                kurinys=kurinys,
                eile=eile
            )

        return JsonResponse({"redirect": "/programos"})

    kuriniai = Kurinys.objects.all()
    return render(request, "Programos/programaAdd.html", {"kuriniai": kuriniai})

def program_edit(request, pk):
    programa = get_object_or_404(Programa, pk=pk)

    if request.method == "POST":
        form = ProgramaForm(request.POST, instance=programa)
        if form.is_valid():
            form.save()

            # ✅ Update kūriniai ordering
            ProgramosKurinys.objects.filter(programa=programa).delete()  # Remove old entries
            selected_kuriniai = request.POST.getlist('kuriniai')
            for index, kurinys_id in enumerate(selected_kuriniai, start=1):
                kurinys = Kurinys.objects.get(id=kurinys_id)
                ProgramosKurinys.objects.create(programa=programa, kurinys=kurinys, eile=index)

            return redirect('programos')
    else:
        form = ProgramaForm(instance=programa)

    return render(request, 'Programos/programEdit.html', {'form': form, 'programa': programa})



def istrinti_programa(request, pk):
    programa = get_object_or_404(Programa, pk=pk)

    if request.method == "POST":
        programa.delete()
        return JsonResponse({"success": True})  # ✅ Return JSON response

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def programos_kuriniai_view(request, pk):
    programa = get_object_or_404(Programa, pk=pk)

    # Retrieve all Kūriniai in the correct order (`eile`)
    programos_kuriniai = ProgramosKurinys.objects.filter(programa=programa).order_by("eile")

    return render(request, 'Programos/programosKuriniai.html', {
        "programa": programa,
        "programos_kuriniai": programos_kuriniai
    })
