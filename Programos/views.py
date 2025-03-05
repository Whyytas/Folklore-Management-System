import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProgramaForm
from Kuriniai.models import Kurinys
from .models import Programa, ProgramosKurinys
from django.views.decorators.csrf import csrf_exempt


def programos_page(request):
    programos = Programa.objects.all()  # ✅ Fetch programs from the database
    return render(request, 'programos.html', {'programos': programos})

def program_create(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            pavadinimas = data.get("pavadinimas")
            tipas = data.get("tipas")
            kuriniai_data = data.get("kuriniai", [])

            programa = Programa.objects.create(
                pavadinimas=pavadinimas,
                tipas=tipas
            )

            programos_kuriniai = []
            kurinys_ids = [item["id"] for item in kuriniai_data]
            kuriniai = {k.id: k for k in Kurinys.objects.filter(id__in=kurinys_ids)}

            for item in kuriniai_data:
                kurinys = kuriniai.get(int(item["id"]))
                if kurinys:
                    programos_kuriniai.append(
                        ProgramosKurinys(
                            programa=programa,
                            kurinys=kurinys,
                            eile=item["eile"]
                        )
                    )

            ProgramosKurinys.objects.bulk_create(programos_kuriniai)

            return JsonResponse({"redirect": "/programos"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    kuriniai = Kurinys.objects.all()
    tipai = Programa.PROGRAM_TIPAS  # ✅ Fetch from model dynamically
    return render(request, "programaAdd.html", {
        "kuriniai": kuriniai,
        "TIPAS_CHOICES": tipai  # ✅ Ensure choices are passed to template
    })
from django.http import JsonResponse

from django.http import JsonResponse
import json

def program_edit(request, pk):
    programa = get_object_or_404(Programa, pk=pk)
    kuriniai = Kurinys.objects.all()
    selected_kuriniai = ProgramosKurinys.objects.filter(programa=programa).order_by("eile")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            programa.pavadinimas = data.get("pavadinimas")
            programa.tipas = data.get("tipas")
            programa.save()

            # ✅ Update kūriniai ordering
            ProgramosKurinys.objects.filter(programa=programa).delete()  # Remove old entries
            for index, kurinys_data in enumerate(data.get("kuriniai", []), start=1):
                kurinys = Kurinys.objects.get(id=kurinys_data["id"])
                ProgramosKurinys.objects.create(programa=programa, kurinys=kurinys, eile=index)

            return JsonResponse({"redirect": "/programos"}, status=200)  # ✅ JSON response for frontend redirect
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    context = {
        "programa": programa,
        "kuriniai": kuriniai,
        "selected_kuriniai": selected_kuriniai,
        "selected_kuriniai_ids": [pk.kurinys.id for pk in selected_kuriniai],
        "TIPAS_CHOICES": Programa.PROGRAM_TIPAS,
    }
    return render(request, "programEdit.html", context)


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

    return render(request, 'programosKuriniai.html', {
        "programa": programa,
        "programos_kuriniai": programos_kuriniai
    })
