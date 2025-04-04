import re
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from Ansambliai.models import Ansamblis
from Kuriniai.models import Kurinys, Pozymis
from Renginiai.models import Renginys
from .models import Programa, ProgramosKurinys
import json
from django.http import JsonResponse, HttpResponseForbidden
import random


from django.core.paginator import Paginator

def programos_page(request):
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")
    sort_field = request.GET.get("sort", "pavadinimas")
    sort_dir = request.GET.get("dir", "asc")
    tipas_filter = request.GET.get("tipas")

    sort_order = sort_field if sort_dir == "asc" else f"-{sort_field}"
    programos = Programa.objects.all().order_by(sort_order, "-id")

    if selected_ansamblis_id:
        programos = programos.filter(ansamblis__id=selected_ansamblis_id)

    if tipas_filter:
        programos = programos.filter(tipas=tipas_filter)

    paginator = Paginator(programos, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'programos.html', {
        'programos': page_obj.object_list,
        'page_obj': page_obj,
        'sort_field': sort_field,
        'sort_dir': sort_dir,
        'tipas_filter': tipas_filter,
        'tipai': Programa.PROGRAM_TIPAS,
    })

def program_generate(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės generuoti programų.")

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
                tipas=tipas,
                aprasymas=data.get("aprasymas", ""),
                trukme=data.get("trukme", ""),
                ansamblis_id=data.get("ansamblis")
            )

            kurinys_ids = [item["id"] for item in kuriniai_data]
            kuriniai_qs = Kurinys.objects.filter(id__in=kurinys_ids)
            kuriniai_map = {k.id: k for k in kuriniai_qs}

            total_seconds = 0
            programos_kuriniai = []

            for item in kuriniai_data:
                kid = int(item["id"])
                eile = int(item.get("eile", 0))
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

    return render(request, "programGenerate.html", {
        "tipai": tipai,
        "ansambliai": ansambliai
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


@csrf_exempt
@require_POST
def generate_kuriniai(request):
    try:
        data = json.loads(request.body)
        tipas = data.get("tipas")
        trukme = data.get("trukme")
        ansamblis_id = int(data.get("ansamblis", 0))
        santykis = data.get("santykis", "")

        if not tipas or not trukme or not ansamblis_id:
            return JsonResponse({"error": "Trūksta duomenų."}, status=400)

        m, s = map(int, trukme.split(":"))
        target_seconds = m * 60 + s

        all_kuriniai = Kurinys.objects.filter(ansambliai__id=ansamblis_id)

        if tipas == "Susidainavimams":
            pozymis = Pozymis.objects.filter(pavadinimas__iexact="Susidainavimams").first()
            if not pozymis:
                return JsonResponse([], safe=False)

            filtered = all_kuriniai.filter(pozymiai=pozymis).exclude(paruosimas__in=["Archyvas", "Naujas"])
            return JsonResponse(_select_up_to_duration(filtered, target_seconds), safe=False)

        elif tipas == "Vakaronei":
            pozymis = Pozymis.objects.filter(pavadinimas__iexact="Vakaronei").first()
            if not pozymis:
                return JsonResponse([], safe=False)

            filtered = all_kuriniai.filter(pozymiai=pozymis).exclude(paruosimas__in=["Archyvas", "Naujas"])
            groups = {"Lėtas": [], "Vidutinis": [], "Greitas": []}
            for k in filtered:
                if k.trukme and k.greitumas and ":" in k.trukme:
                    groups[k.greitumas].append(k)

            for g in groups:
                random.shuffle(groups[g])

            result = []
            total = 0
            cycle = ["Lėtas", "Vidutinis", "Greitas"]
            i = 0
            while total < target_seconds and any(groups.values()):
                group = cycle[i % 3]
                if groups[group]:
                    k = groups[group].pop()
                    m, s = map(int, k.trukme.split(":"))
                    dur = m * 60 + s
                    if total + dur <= target_seconds:
                        result.append(k)
                        total += dur
                i += 1

            return JsonResponse(_kuriniai_to_json(result), safe=False)



        else:
            response = []
            used_pradzia_id = _recent_programa_pradzia_kurinys()
            pradzia_pozymis = Pozymis.objects.filter(pavadinimas__iexact="Pradžia").first()
            pradzia_candidates = all_kuriniai.exclude(paruosimas__in=["Archyvas", "Naujas"])

            if pradzia_pozymis:
                pradzia_candidates = pradzia_candidates.filter(pozymiai=pradzia_pozymis)

            if used_pradzia_id:
                pradzia_candidates = pradzia_candidates.exclude(id=used_pradzia_id)

            pradzia_kurinys = None

            for k in pradzia_candidates:
                if k.trukme and ":" in k.trukme:
                    pradzia_kurinys = k
                    break

            if pradzia_kurinys:
                response.append(pradzia_kurinys)

            if santykis and ":" in santykis:
                try:
                    d, s_, k = map(int, santykis.split(":"))

                except Exception:
                    return JsonResponse({
                        "error": "Neteisingas santykio formatas. Pvz: 3:2:1"
                    }, status=400)

                available = all_kuriniai.filter(
                    pozymiai__pavadinimas__iexact=tipas,
                    trukme__contains=":"
                ).exclude(paruosimas__in=["Archyvas", "Naujas"]).distinct()

                if pradzia_kurinys:
                    available = available.exclude(id=pradzia_kurinys.id)

                groups = {"Daina": [], "Šokis": [], "Kapela": []}

                for kur in available:
                    if kur.tipas in groups and ":" in kur.trukme:
                        groups[kur.tipas].append(kur)

                for g in groups:
                    random.shuffle(groups[g])

                # Convert ratio into cycle
                cycle = ["Daina"] * d + ["Šokis"] * s_ + ["Kapela"] * k
                total_result = []
                total_time = 0

                while True:
                    group = []
                    group_time = 0
                    for group_name in cycle:
                        if not groups[group_name]:
                            group = []
                            break

                        kur = groups[group_name].pop(0)
                        m, s = map(int, kur.trukme.split(":"))
                        dur = m * 60 + s
                        group.append((kur, dur))
                        group_time += dur

                    if not group:
                        break  # couldn't form full group

                    total_result.extend([k for k, _ in group])
                    total_time += group_time

                # Sort the group result (Pradzia already added)
                sort_order = {"Daina": 1, "Kapela": 2, "Šokis": 3}
                sorted_result = sorted(total_result, key=lambda x: sort_order.get(x.tipas, 99))
                if pradzia_kurinys:
                    final_result = [pradzia_kurinys] + sorted_result
                else:
                    final_result = sorted_result

                return JsonResponse(_kuriniai_to_json(final_result), safe=False)

            return JsonResponse(_kuriniai_to_json(response), safe=False)



    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def _kuriniai_to_json(kuriniai):
    return [
        {
            "id": k.id,
            "pavadinimas": k.pavadinimas,
            "trukme": k.trukme,
            "tipas": k.tipas,
            "regionas": k.regionas or "",
        }
        for k in kuriniai
    ]


def _select_up_to_duration(queryset, max_seconds):
    valid = [k for k in queryset if k.trukme and ":" in k.trukme]
    for k in valid:
        m, s = map(int, k.trukme.split(":"))
        k.seconds = m * 60 + s
    random.shuffle(valid)

    selected = []
    total = 0
    for k in valid:
        if total + k.seconds > max_seconds:
            continue
        selected.append(k)
        total += k.seconds
    return _kuriniai_to_json(selected)


def _recent_programa_pradzia_kurinys():
    recent_renginys = Renginys.objects.filter(
        data_laikas__lt=datetime.now(),
        programa__isnull=False
    ).order_by("-data_laikas").first()

    if not recent_renginys or not recent_renginys.programa:
        return None

    programa = recent_renginys.programa
    last = ProgramosKurinys.objects.filter(programa=programa, kurinys__tipas="Pradžia").first()

    return last.kurinys.id if last else None


def _duration_in_seconds(trukme_str):
    m, s = map(int, trukme_str.split(":"))
    return m * 60 + s
