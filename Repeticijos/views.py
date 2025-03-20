from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import json

from django.urls import reverse

from Kuriniai.models import Kurinys
from Repeticijos.models import Repeticija, RepeticijaKurinys
from Ansambliai.models import Ansamblis  # ✅ Import Ansamblis


def repeticijos_list(request):
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")
    repeticijos = Repeticija.objects.all().order_by("-data", "-id")

    if selected_ansamblis_id:
        repeticijos = repeticijos.filter(ansamblis__id=selected_ansamblis_id)

    all_ansambliai = Ansamblis.objects.all()

    return render(request, 'repeticijos.html', {
        'repeticijos': repeticijos,
        'all_ansambliai': all_ansambliai
    })

@login_required
def repeticija_create(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės kurti repeticijų.")

    if request.method == 'POST':
        try:
            if request.content_type != "application/json":
                return JsonResponse({"error": "Netinkamas užklausos tipas."}, status=400)

            data = json.loads(request.body)
            pavadinimas = data.get("pavadinimas", "").strip()
            data_value = data.get("data", "").strip()
            kuriniai_ids = data.get("kuriniai", [])
            ansamblis_id = data.get("ansamblis")

            if not pavadinimas or not data_value or not kuriniai_ids or not ansamblis_id:
                return JsonResponse({"error": "Prašome užpildyti visus laukus ir pasirinkti kūrinius."}, status=400)

            try:
                data_datetime = datetime.strptime(data_value[:16], '%Y-%m-%d %H:%M')
            except ValueError:
                return JsonResponse({"error": "Netinkamas datos formatas."}, status=400)

            selected_ansamblis = get_object_or_404(Ansamblis, id=ansamblis_id)
            repeticija = Repeticija.objects.create(
                pavadinimas=pavadinimas,
                data=data_datetime,
                ansamblis=selected_ansamblis
            )

            # Save kūriniai with order
            relations = [
                RepeticijaKurinys(repeticija=repeticija, kurinys_id=kur_id, order=index)
                for index, kur_id in enumerate(kuriniai_ids)
            ]
            RepeticijaKurinys.objects.bulk_create(relations)

            return JsonResponse({"redirect": reverse("repeticijos")}, status=201)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": f"Serverio klaida: {str(e)}"}, status=500)

    # GET → show form
    ansambliai = Ansamblis.objects.all()
    return render(request, "repeticija_add.html", {
        "ansambliai": ansambliai
    })


@login_required
def repeticija_edit(request, pk):
    repeticija = get_object_or_404(Repeticija, pk=pk)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti repeticijų.")

    if request.method == "POST":
        if request.content_type != "application/json":
            return HttpResponseBadRequest("Netinkamas užklausos tipas.")

        try:
            data = json.loads(request.body)

            repeticija.pavadinimas = data.get("pavadinimas", repeticija.pavadinimas)
            date_value = data.get("data")
            if date_value:
                repeticija.data = datetime.strptime(date_value.strip()[:16], '%Y-%m-%d %H:%M')

            ansamblis_id = data.get("ansamblis")
            if ansamblis_id:
                repeticija.ansamblis = get_object_or_404(Ansamblis, id=ansamblis_id)

            repeticija.save()

            kuriniai_ids = data.get("kuriniai", [])

            with transaction.atomic():
                repeticija.repeticijakurinys_set.all().delete()
                for order, kid in enumerate(kuriniai_ids):
                    kurinys = Kurinys.objects.get(id=kid)
                    RepeticijaKurinys.objects.create(
                        repeticija=repeticija,
                        kurinys=kurinys,
                        order=order
                    )

            return JsonResponse({"redirect": reverse("repeticijos")})

        except Exception as e:
            return JsonResponse({"error": f"Klaida: {str(e)}"}, status=500)

    # GET method
    ordered_kuriniai = repeticija.kuriniai.through.objects.filter(
        repeticija=repeticija
    ).select_related('kurinys').order_by('order')

    all_kuriniai = Kurinys.objects.filter(ansambliai=repeticija.ansamblis)
    ansambliai = Ansamblis.objects.all()

    return render(request, "repeticija_edit.html", {
        "repeticija": repeticija,
        "ordered_kuriniai": [rk.kurinys for rk in ordered_kuriniai],
        "all_kuriniai": all_kuriniai,
        "ansambliai": ansambliai
    })
@login_required
def repeticija_delete(request, pk):
    repeticija = get_object_or_404(Repeticija, pk=pk)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti repeticijų.")

    if request.method == "POST":
        repeticija.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def repeticija_detail(request, pk):
    repeticija = get_object_or_404(Repeticija, pk=pk)
    return render(request, 'repeticija_detail.html', {'repeticija': repeticija})
