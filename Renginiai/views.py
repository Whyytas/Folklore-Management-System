from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from Ansambliai.models import Ansamblis
from Programos.models import Programa
from .models import Renginys
from .forms import RenginysForm
import datetime  # ✅ Correct way to import datetime module


def renginiai_list(request):
    """ Retrieve and display all Renginiai """
    renginiai = Renginys.objects.all()
    return render(request, 'renginiai.html', {'renginiai': renginiai})

from django.utils.timezone import make_aware, localtime
import datetime

def renginiai_add(request):
    if request.method == "POST":
        form = RenginysForm(request.POST)
        if form.is_valid():
            renginys = form.save(commit=False)

            # ✅ Convert naive datetime to timezone-aware
            renginys.data_laikas = make_aware(renginys.data_laikas)

            renginys.save()
            return redirect("renginiai")

    else:
        form = RenginysForm()

    return render(request, "renginiai_add.html", {"form": form})


from django.utils.timezone import make_aware
import datetime  # ✅ Import the full module, not just `datetime`

def renginiai_edit(request, renginys_id):
    renginys = get_object_or_404(Renginys, id=renginys_id)

    if request.method == "POST":
        form = RenginysForm(request.POST, instance=renginys)
        if form.is_valid():
            renginys = form.save(commit=False)

            # ✅ Convert string "YYYY-MM-DD HH:MM" to a timezone-aware datetime
            if isinstance(form.cleaned_data["data_laikas"], str):
                naive_datetime = datetime.datetime.strptime(form.cleaned_data["data_laikas"], "%Y-%m-%d %H:%M")
                renginys.data_laikas = make_aware(naive_datetime)  # ✅ Convert to timezone-aware
            else:
                renginys.data_laikas = make_aware(form.cleaned_data["data_laikas"])

            renginys.save()
            return redirect('renginiai')

    else:
        # ✅ Format existing datetime to Lithuanian format (YYYY-MM-DD HH:MM)
        renginys.data_laikas = renginys.data_laikas.strftime("%Y-%m-%d %H:%M") if renginys.data_laikas else ""

        form = RenginysForm(instance=renginys)

    return render(request, "renginiai_edit.html", {
        "renginys": renginys,
        "form": form,
        "ansambliai": Ansamblis.objects.all(),
        "programos": Programa.objects.all()
    })

def delete_renginys(request, renginys_id):
    """ Deletes the selected Renginys """
    if request.method == "POST":
        renginys = get_object_or_404(Renginys, id=renginys_id)
        renginys.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request method"}, status=400)


def publicEvents(request):
    return render(request, 'renginiaiPublic.html', )

