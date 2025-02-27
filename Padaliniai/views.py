from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Padalinys
from .forms import PadalinysForm

class PadaliniaiListView(ListView):
    model = Padalinys
    template_name = "padaliniai.html"
    context_object_name = "padaliniai"

class PadalinysCreateView(CreateView):
    model = Padalinys
    form_class = PadalinysForm
    template_name = "padaliniai_add.html"

    def form_valid(self, form):
        messages.success(self.request, "Padalinys sėkmingai pridėtas!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("padaliniai_list")

class PadalinysUpdateView(UpdateView):
    model = Padalinys
    form_class = PadalinysForm
    template_name = "padaliniai_edit.html"

    def form_valid(self, form):
        messages.success(self.request, "Padalinys atnaujintas!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("padaliniai_list")

class PadalinysDeleteView(DeleteView):
    model = Padalinys
    template_name = "padalinys_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Padalinys ištrintas!")
        return reverse("padaliniai_list")
