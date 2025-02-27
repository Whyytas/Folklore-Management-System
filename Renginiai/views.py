from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Renginys
from .forms import RenginysForm

def renginiai_list(request):
    """ Retrieve and display all Renginiai """
    renginiai = Renginys.objects.all()
    return render(request, 'renginiai.html', {'renginiai': renginiai})

def renginiai_add(request):
    if request.method == "POST":
        form = RenginysForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('renginiai')
    else:
        form = RenginysForm()

    return render(request, 'renginiai_add.html', {'form': form})


def renginiai_edit(request, renginys_id):
    """ Handles editing an existing Renginys """
    renginys = get_object_or_404(Renginys, id=renginys_id)

    if request.method == "POST":
        form = RenginysForm(request.POST, instance=renginys)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

    return render(request, "renginiai_edit.html", {"renginys": renginys})

def delete_renginys(request, renginys_id):
    """ Deletes the selected Renginys """
    if request.method == "POST":
        renginys = get_object_or_404(Renginys, id=renginys_id)
        renginys.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request method"}, status=400)


def publicEvents(request):
    return render(request, 'renginiaiPublic.html', )