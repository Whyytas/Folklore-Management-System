import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from Kuriniai.models import Kurinys
from Repeticijos.forms import RepeticijaForm
from Repeticijos.models import Repeticija


def repeticijos_list(request):
    repeticijos = Repeticija.objects.all()
    return render(request, 'repeticijos.html', {'repeticijos': repeticijos})

def repeticija_create(request):
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

            # ✅ Add selected kūriniai to many-to-many field
            selected_kuriniai = Kurinys.objects.filter(id__in=kuriniai_ids)
            repeticija.kuriniai.set(selected_kuriniai)

            return JsonResponse({"redirect": "/repeticijos"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    kuriniai = Kurinys.objects.all()  # ✅ Fetch all kūriniai
    return render(request, "repeticija_add.html", {"kuriniai": kuriniai})

def repeticija_edit(request, pk):
    repeticija = get_object_or_404(Repeticija, pk=pk)

    if request.method == "POST":
        try:
            if not request.body:
                return JsonResponse({"error": "Empty request body"}, status=400)

            data = json.loads(request.body)

            repeticija.pavadinimas = data.get("pavadinimas", repeticija.pavadinimas)

            # 🔥 Convert string to datetime format
            date_value = data.get("data", repeticija.data.strftime('%Y-%m-%d %H:%M'))

            # 🔥 Ensure the string is in the correct format (remove extra "00:00")
            date_value = date_value.strip()  # Remove extra spaces
            date_value = date_value[:16]  # Keep only 'YYYY-MM-DD HH:MM'

            # 🔥 Convert to datetime
            repeticija.data = datetime.strptime(date_value, '%Y-%m-%d %H:%M')

            kuriniai_ids = data.get("kuriniai", [])
            if isinstance(kuriniai_ids, list):
                selected_kuriniai = Kurinys.objects.filter(id__in=kuriniai_ids)
                repeticija.kuriniai.set(selected_kuriniai)
            else:
                return JsonResponse({"error": "Invalid format for kūriniai"}, status=400)

            repeticija.save()
            return JsonResponse({"redirect": "/repeticijos"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    if request.method == "GET":
        all_kuriniai = Kurinys.objects.all()
        return render(request, "repeticija_edit.html", {
            "repeticija": repeticija,
            "all_kuriniai": all_kuriniai
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)


def repeticija_delete(request, pk):
    repeticija = get_object_or_404(Repeticija, pk=pk)

    if request.method == "POST":
        repeticija.delete()
        return JsonResponse({"success": True})  # ✅ Return JSON response

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
def repeticija_detail(request, pk):
    repeticija = get_object_or_404(Repeticija, pk=pk)
    return render(request, 'repeticija_detail.html', {'repeticija': repeticija})