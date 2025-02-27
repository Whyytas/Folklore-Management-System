from django.shortcuts import render, get_object_or_404, redirect
from .models import Ansamblis
from .forms import AnsamblisForm

def ansambliai_list(request):
    ansambliai = Ansamblis.objects.all()
    return render(request, 'Ansambliai/ansambliai.html', {'ansambliai': ansambliai})

def ansamblis_add(request):
    if request.method == "POST":
        form = AnsamblisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ansambliai_list')
    else:
        form = AnsamblisForm()
    return render(request, 'Ansambliai/ansamblis_add.html', {'form': form})

def ansamblis_edit(request, pk):
    ansamblis = get_object_or_404(Ansamblis, pk=pk)
    if request.method == "POST":
        form = AnsamblisForm(request.POST, instance=ansamblis)
        if form.is_valid():
            form.save()
            return redirect('ansambliai_list')
    else:
        form = AnsamblisForm(instance=ansamblis)
    return render(request, 'Ansambliai/ansamblis_edit.html', {'form': form})

def ansamblis_delete(request, pk):
    ansamblis = get_object_or_404(Ansamblis, pk=pk)
    if request.method == "POST":
        ansamblis.delete()
        return redirect('ansambliai_list')
    return render(request, 'ansamblis_confirm_delete.html', {'ansamblis': ansamblis})
