from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from Ensembles.models import Ensemble
from .models import Department
from .forms import DepartmentForm

class DepartmentsListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = "departments_list.html"
    context_object_name = "departments"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role in ["narys", "vadovas"]:
            return HttpResponseForbidden("Jūs neturite teisės peržiūrėti padalinių.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Department.objects.prefetch_related("ensembles").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_ensembles"] = Ensemble.objects.all()
        context["selected_ensemble_id"] = self.request.session.get("selected_ensemble_id")
        context["search"] = self.request.GET.get("search", "").strip()
        context["sort_param"] = self.request.GET.get("sort", "title")
        return context

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "departments_add.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role in ["narys", "vadovas"]:
            return HttpResponseForbidden("Jūs neturite teisės pridėti padalinių.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Padalinys sėkmingai pridėtas!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("padaliniai_list")

def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == "POST":
        department.title = request.POST.get("title")
        department.address = request.POST.get("address")
        department.phone = request.POST.get("phone")
        department.save()
        return redirect("padaliniai_list")

    return render(request, "departments_edit.html", {
        "department": department
    })

class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = "padalinys_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role in ["narys", "vadovas"]:
            return HttpResponseForbidden("Jūs neturite teisės ištrinti padalinių.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Padalinys ištrintas!")
        return reverse_lazy("padaliniai_list")
