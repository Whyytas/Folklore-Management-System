from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Padalinys
from .forms import PadalinysForm

class PadaliniaiListView(LoginRequiredMixin, ListView):
    model = Padalinys
    template_name = "padaliniai.html"
    context_object_name = "padaliniai"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role in ["narys", "vadovas"]:
            return HttpResponseForbidden("Jūs neturite teisės peržiūrėti padalinių.")
        return super().dispatch(request, *args, **kwargs)

class PadalinysCreateView(LoginRequiredMixin, CreateView):
    model = Padalinys
    form_class = PadalinysForm
    template_name = "padaliniai_add.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role in ["narys", "vadovas"]:
            return HttpResponseForbidden("Jūs neturite teisės pridėti padalinių.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Padalinys sėkmingai pridėtas!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("padaliniai_list")

class PadalinysUpdateView(LoginRequiredMixin, UpdateView):
    model = Padalinys
    form_class = PadalinysForm
    template_name = "padaliniai_edit.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role in ["narys", "vadovas"]:
            return HttpResponseForbidden("Jūs neturite teisės redaguoti padalinių.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Padalinys atnaujintas!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("padaliniai_list")

class PadalinysDeleteView(LoginRequiredMixin, DeleteView):
    model = Padalinys
    template_name = "padalinys_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role in ["narys", "vadovas"]:
            return HttpResponseForbidden("Jūs neturite teisės ištrinti padalinių.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Padalinys ištrintas!")
        return reverse_lazy("padaliniai_list")
