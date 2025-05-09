from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from Ensembles.models import Ensemble
from django.contrib.auth import get_user_model

User = get_user_model()  #  Ensure you're using the correct model


ROLE_ORDER = {
    'administratorius': 1,
    'vadovas': 2,
    'narys': 3
}

from django.core.paginator import Paginator
from django.db.models import Q, Prefetch


@login_required
def users_list(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės peržiūrėti narių.")

    selected_ensemble_id = request.session.get("selected_ensemble_id")
    role_filter = request.GET.get("role", "")
    search = request.GET.get("search", "").strip()
    sort = request.GET.get("sort", "username")

    valid_sort_fields = ['username', '-username', 'name', '-name', 'surname', '-surname', 'role', '-role']
    if sort not in valid_sort_fields:
        sort = "username"

    # Only fetch used fields
    users_qs = User.objects.only(
        "id", "username", "name", "surname", "role"
    ).prefetch_related(
        Prefetch("ensembles", queryset=Ensemble.objects.only("id", "title"))
    )

    if selected_ensemble_id:
        users_qs = users_qs.filter(ensembles__id=selected_ensemble_id)

    if role_filter:
        users_qs = users_qs.filter(role=role_filter)

    if search:
        users_qs = users_qs.filter(
            Q(username__icontains=search) |
            Q(name__icontains=search) |
            Q(surname__icontains=search)
        )

    users_qs = users_qs.order_by(sort)

    return render(request, 'users_list.html', {
        'users': users_qs,
        'all_ensembles': Ensemble.objects.only("id", "title"),
        'selected_ensemble_id': selected_ensemble_id,
        'role_filter': role_filter,
        'search_query': search,
        'sort_param': sort,
    })#  Custom Form for Creating a User
class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    ensembles = forms.ModelMultipleChoiceField(
        queryset=Ensemble.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'name', 'surname', 'email', 'phone_number', 'role', 'password1', 'password2', 'ensembles']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})#  View to Add a New User

@login_required
def user_add(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti narių.")

    if request.user.role == "vadovas":
        all_ensembles = request.user.ensembles.all()
    else:
        all_ensembles = Ensemble.objects.all()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.name = form.cleaned_data['name']
            user.surname = form.cleaned_data['surname']
            user.save()

            selected_ensembles_ids = request.POST.getlist("ensembles")
            selected_ensembles = Ensemble.objects.filter(id__in=selected_ensembles_ids)

            if request.user.role == "vadovas":
                selected_ensembles = selected_ensembles.filter(id__in=request.user.ensembles.values_list('id', flat=True))

            user.ensembles.set(selected_ensembles)
            messages.success(request, "Naujas naudotojas sėkmingai pridėtas!")
            return redirect('nariai')

    else:
        form = CustomUserCreationForm()

    return render(request, 'user_add.html', {'form': form, 'all_ensembles': all_ensembles})



@login_required
def users_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės peržiūrėti šio nario informacijos.")

    if request.user.role == "vadovas":
        if not user.ensembles.filter(id__in=request.user.ensembles.values_list('id', flat=True)).exists():
            return HttpResponseForbidden("Jūs galite peržiūrėti tik savo ansamblio narius.")

    return render(request, 'user_view.html', {'user': user})

#  Custom User Edit Form
class CustomUserEditForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('narys', 'Narys'),
        ('vadovas', 'Vadovas'),
        ('administratorius', 'Administratorius'),
    ]

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})

#  View to Edit a User
@login_required
def user_edit(request, user_id):
    user = get_object_or_404(User.objects.prefetch_related("ensembles"), id=user_id)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti narių.")

    if request.user.role == "vadovas":
        current_user_ensemble_ids = set(request.user.ensembles.values_list("id", flat=True))
        target_user_ensemble_ids = set(user.ensembles.values_list("id", flat=True))
        if not current_user_ensemble_ids.intersection(target_user_ensemble_ids):
            return HttpResponseForbidden("Jūs galite redaguoti tik savo ansamblio narius.")

    #  Only vadovas sees their own ensembles
    all_ensembles = (
        request.user.ensembles.all()
        if request.user.role == "vadovas"
        else Ensemble.objects.all()
    )

    if request.method == "POST":
        form_type = request.POST.get("which_form")

        if form_type == "info":
            user.username = request.POST.get("username") or user.username
            user.email = request.POST.get("email") or user.email
            user.phone_number = request.POST.get("phone_number") or user.phone_number
            user.role = request.POST.get("role") or user.role
            user.name = request.POST.get("name") or user.name
            user.surname = request.POST.get("surname") or user.surname

            selected_ids = request.POST.getlist("ensembles")

            if request.user.role == "vadovas":
                #  Only assign ensembles the user has access to
                selected = request.user.ensembles.filter(id__in=selected_ids)
            else:
                selected = Ensemble.objects.filter(id__in=selected_ids)

            user.ensembles.set(selected)
            user.save()
            messages.success(request, "Naudotojo duomenys atnaujinti sėkmingai.")
            return redirect("nariai_edit", user_id=user.id)

        elif form_type == "password":
            new_password1 = request.POST.get("new_password1")
            new_password2 = request.POST.get("new_password2")

            if new_password1 and new_password1 == new_password2:
                try:
                    validate_password(new_password1, user)
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, "Slaptažodis atnaujintas sėkmingai.")
                except ValidationError as e:
                    messages.error(request, " ".join(e.messages))
            else:
                messages.error(request, "Slaptažodžiai nesutampa arba tušti.")

            return redirect("nariai_edit", user_id=user.id)

    return render(request, "user_edit.html", {
        "user": user,
        "all_ensembles": all_ensembles
    })

def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti narių.")

    if request.user.role == "vadovas":
        if not user.ensembles.filter(id__in=request.user.ensembles.values_list('id', flat=True)).exists():
            return HttpResponseForbidden("Jūs galite ištrinti tik savo ansamblio narius.")

    if request.method == "POST":
        user.delete()
        messages.success(request, "Naudotojas sėkmingai ištrintas.")
        return redirect('nariai')

    messages.error(request, "Negalima ištrinti naudotojo.")
    return redirect('nariai')


def check_username(request):
    """Check if the username is already taken."""
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'error': 'Username parameter is required'}, status=400)

    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

from django.contrib.auth import update_session_auth_hash

@login_required
def account_edit(request):
    user = request.user
    profile_updated = False
    password_updated = False
    password_error = None

    if request.method == 'POST':
        if request.POST.get('which_form') == 'info':
            user.name = request.POST.get('name', user.name)
            user.surname = request.POST.get('surname', user.surname)
            user.email = request.POST.get('email', user.email)
            user.phone_number = request.POST.get('phone_number', user.phone_number)
            user.save()
            profile_updated = True

        elif request.POST.get('which_form') == 'password':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if new_password1 and new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)  # Stay logged in
                password_updated = True
            else:
                password_error = "Slaptažodžiai nesutampa arba tušti."

    context = {
        'user': user,
        'profile_updated': profile_updated,
        'password_updated': password_updated,
        'password_error': password_error
    }

    return render(request, 'profile_edit.html', context)
