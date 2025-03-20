from django.shortcuts import render, redirect, get_object_or_404

from Ansambliai.models import Ansamblis
from Kuriniai.models import Kurinys
from .models import Programa, ProgramosKurinys
import json
from django.http import JsonResponse, HttpResponseForbidden

def programos_page(request):
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")
    programos = Programa.objects.all().order_by("-sukurtas", "-id")

    if selected_ansamblis_id:
        programos = programos.filter(ansamblis__id=selected_ansamblis_id)

    all_ansambliai = Ansamblis.objects.all()

    return render(request, 'programos.html', {
        'programos': programos,
        'all_ansambliai': all_ansambliai
    })


def program_create(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti programų.")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            pavadinimas = data.get("pavadinimas")
            tipas = data.get("tipas")
            kuriniai_data = data.get("kuriniai", [])

            if not pavadinimas or not tipas or not kuriniai_data:
                return JsonResponse({"error": "Trūksta reikiamų laukų arba kūrinių!"}, status=400)

            programa = Programa.objects.create(
                pavadinimas=pavadinimas,
                tipas=tipas
            )

            kurinys_ids = [item["id"] for item in kuriniai_data]
            kuriniai_qs = Kurinys.objects.filter(id__in=kurinys_ids)
            kuriniai_map = {k.id: k for k in kuriniai_qs}

            total_seconds = 0
            programos_kuriniai = []

            for item in kuriniai_data:
                kid = int(item["id"])
                eile = item.get("eile")
                kurinys = kuriniai_map.get(kid)

                if kurinys and eile is not None:
                    programos_kuriniai.append(
                        ProgramosKurinys(
                            programa=programa,
                            kurinys=kurinys,
                            eile=eile
                        )
                    )
                    # Calculate total trukme
                    if kurinys.trukme and ":" in kurinys.trukme:
                        m, s = map(int, kurinys.trukme.split(":"))
                        total_seconds += m * 60 + s

            Programa.objects.filter(id=programa.id).update(
                trukme=f"{total_seconds // 60:02}:{total_seconds % 60:02}"
            )

            ProgramosKurinys.objects.bulk_create(programos_kuriniai)

            return JsonResponse({"redirect": "/programos"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    ansambliai = Ansamblis.objects.all()
    tipai = Programa.PROGRAM_TIPAS

    return render(request, "programaAdd.html", {
        "tipai": tipai,
        "ansambliai": ansambliai
    })

def program_edit(request, pk):
    programa = get_object_or_404(Programa, pk=pk)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti programų.")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            programa.pavadinimas = data.get("pavadinimas")
            programa.tipas = data.get("tipas")
            programa.aprasymas = data.get("aprasymas", "")
            programa.trukme = data.get("trukme")

            ansamblis_id = data.get("ansamblis")
            programa.ansamblis_id = ansamblis_id if ansamblis_id else None

            # Calculate total trukme from kūriniai
            kuriniai_data = data.get("kuriniai", [])

            programa.save()

            ProgramosKurinys.objects.filter(programa=programa).delete()
            for index, k_data in enumerate(kuriniai_data, start=1):
                kurinys = Kurinys.objects.get(id=k_data["id"])
                ProgramosKurinys.objects.create(programa=programa, kurinys=kurinys, eile=index)

            return JsonResponse({"redirect": "/programos"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    kuriniai = Kurinys.objects.all()
    selected_kuriniai = ProgramosKurinys.objects.filter(programa=programa).order_by("eile")

    context = {
        "programa": programa,
        "kuriniai": kuriniai,
        "selected_kuriniai": selected_kuriniai,
        "selected_kuriniai_ids": [pk.kurinys.id for pk in selected_kuriniai],
        "tipai": Programa.PROGRAM_TIPAS,
        "ansambliai": Ansamblis.objects.all(),
    }
    return render(request, "programEdit.html", context)
def istrinti_programa(request, pk):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti programų.")

    programa = get_object_or_404(Programa, pk=pk)

    if request.method == "POST":
        programa.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def programos_kuriniai_view(request, pk):
    programa = get_object_or_404(Programa, pk=pk)

    # Retrieve all Kūriniai in the correct order (`eile`)
    programos_kuriniai = ProgramosKurinys.objects.filter(programa=programa).order_by("eile")

    return render(request, 'programosKuriniai.html', {
        "programa": programa,
        "programos_kuriniai": programos_kuriniai
    })
