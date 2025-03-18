from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import json

from Kuriniai.models import Kurinys
from Repeticijos.models import Repeticija
from Ansambliai.models import Ansamblis  # ✅ Import Ansamblis


def repeticijos_list(request):
    repeticijos = Repeticija.objects.all()
    return render(request, 'repeticijos.html', {'repeticijos': repeticijos})


@login_required
def repeticija_create(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės kurti repeticijų.")

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pavadinimas = data.get("pavadinimas")
            data_value = data.get("data")
            kuriniai_ids = data.get("kuriniai", [])
            ansamblis_id = data.get("ansamblis")

            if not ansamblis_id:
                return JsonResponse({"error": "Nepasirinktas ansamblis!"}, status=400)

            selected_ansamblis = get_object_or_404(Ansamblis, id=ansamblis_id)

            data_datetime = datetime.strptime(data_value.strip()[:16], '%Y-%m-%d %H:%M')

            repeticija = Repeticija.objects.create(
                pavadinimas=pavadinimas,
                data=data_datetime,
                ansamblis=selected_ansamblis
            )

            selected_kuriniai = Kurinys.objects.filter(id__in=kuriniai_ids)
            repeticija.kuriniai.set(selected_kuriniai)

            return JsonResponse({"redirect": "/repeticijos"}, status=201)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)

    kuriniai = Kurinys.objects.all()
    ansambliai = Ansamblis.objects.all()
    return render(request, "repeticija_add.html", {
        "kuriniai": kuriniai,
        "ansambliai": ansambliai
    })


@login_required
def repeticija_edit(request, pk):
    repeticija = get_object_or_404(Repeticija, pk=pk)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti repeticijų.")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            repeticija.pavadinimas = data.get("pavadinimas", repeticija.pavadinimas)

            date_value = data.get("data", repeticija.data.strftime('%Y-%m-%d %H:%M')).strip()[:16]
            repeticija.data = datetime.strptime(date_value, '%Y-%m-%d %H:%M')

            kuriniai_ids = data.get("kuriniai", [])
            repeticija.kuriniai.set(Kurinys.objects.filter(id__in=kuriniai_ids))

            # 👇 Clearly handle the ansamblis field here:
            ansamblis_id = data.get("ansamblis")
            if ansamblis_id:
                repeticija.ansamblis = get_object_or_404(Ansamblis, id=ansamblis_id)
            else:
                repeticija.ansamblis = None  # Allow null if empty

            repeticija.save()
            return JsonResponse({"redirect": "/repeticijos"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    all_kuriniai = Kurinys.objects.all()
    ansambliai = Ansamblis.objects.all()
    return render(request, "repeticija_edit.html", {
        "repeticija": repeticija,
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
