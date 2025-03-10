from django.shortcuts import render, get_object_or_404, redirect
from .models import Ansamblis
from .forms import AnsamblisForm

from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

@login_required
def ansambliai_list(request):
    if request.user.role != "administratorius":
        return HttpResponseForbidden("Jūs neturite teisės peržiūrėti ansamblių.")

    ansambliai = Ansamblis.objects.all()
    return render(request, 'ansambliai.html', {'ansambliai': ansambliai})

def ansamblis_add(request):
    if request.method == "POST":
        form = AnsamblisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ansambliai_list')
    else:
        form = AnsamblisForm()
    return render(request, 'ansamblis_add.html', {'form': form})


@login_required
def ansamblis_edit(request, pk):
    if request.user.role != "administratorius":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti ansamblių.")

    ansamblis = get_object_or_404(Ansamblis, pk=pk)
    if request.method == "POST":
        form = AnsamblisForm(request.POST, instance=ansamblis)
        if form.is_valid():
            form.save()
            return redirect('ansambliai_list')
    else:
        form = AnsamblisForm(instance=ansamblis)

    return render(request, 'ansamblis_edit.html', {'form': form})


@login_required
def ansamblis_delete(request, pk):
    if request.user.role != "administratorius":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti ansamblių.")

    ansamblis = get_object_or_404(Ansamblis, pk=pk)
    if request.method == "POST":
        ansamblis.delete()
        return redirect('ansambliai_list')

    return render(request, 'ansamblis_confirm_delete.html', {'ansamblis': ansamblis})
