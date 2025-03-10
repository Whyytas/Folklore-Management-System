from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import json

from Kuriniai.models import Kurinys
from Repeticijos.forms import RepeticijaForm
from Repeticijos.models import Repeticija


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

            repeticija = Repeticija.objects.create(
                pavadinimas=pavadinimas,
                data=data_value
            )

            selected_kuriniai = Kurinys.objects.filter(id__in=kuriniai_ids)
            repeticija.kuriniai.set(selected_kuriniai)

            return JsonResponse({"redirect": "/repeticijos"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    kuriniai = Kurinys.objects.all()
    return render(request, "repeticija_add.html", {"kuriniai": kuriniai})


@login_required
def repeticija_edit(request, pk):
    repeticija = get_object_or_404(Repeticija, pk=pk)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti repeticijų.")

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            repeticija.pavadinimas = data.get("pavadinimas", repeticija.pavadinimas)

            date_value = data.get("data", repeticija.data.strftime('%Y-%m-%d %H:%M'))
            date_value = date_value.strip()[:16]
            repeticija.data = datetime.strptime(date_value, '%Y-%m-%d %H:%M')

            kuriniai_ids = data.get("kuriniai", [])
            selected_kuriniai = Kurinys.objects.filter(id__in=kuriniai_ids)
            repeticija.kuriniai.set(selected_kuriniai)

            repeticija.save()
            return JsonResponse({"redirect": "/repeticijos"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    all_kuriniai = Kurinys.objects.all()
    return render(request, "repeticija_edit.html", {
        "repeticija": repeticija,
        "all_kuriniai": all_kuriniai
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