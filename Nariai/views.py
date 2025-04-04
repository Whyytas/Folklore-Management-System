from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from Ansambliai.models import Ansamblis
from django.contrib.auth import get_user_model

User = get_user_model()  # ✅ Ensure you're using the correct model


ROLE_ORDER = {
    'administratorius': 1,
    'vadovas': 2,
    'narys': 3
}

from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def nariai_list(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės peržiūrėti narių.")

    selected_ansamblis_id = request.session.get("selected_ansamblis_id")
    role_filter = request.GET.get("role", "")
    search = request.GET.get("search", "").strip()
    sort = request.GET.get("sort", "username")

    valid_sort_fields = ['username', '-username', 'vardas', '-vardas', 'pavarde', '-pavarde', 'role', '-role']
    if sort not in valid_sort_fields:
        sort = "username"

    users_qs = User.objects.all()

    if selected_ansamblis_id:
        users_qs = users_qs.filter(ansambliai__id=selected_ansamblis_id).distinct()

    if role_filter:
        users_qs = users_qs.filter(role=role_filter)

    if search:
        users_qs = users_qs.filter(
            Q(username__icontains=search) |
            Q(vardas__icontains=search) |
            Q(pavarde__icontains=search)
        )

    users_qs = users_qs.order_by(sort)

    paginator = Paginator(users_qs, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'nariai.html', {
        'page_obj': page_obj,
        'users': page_obj.object_list,
        'all_ansambliai': Ansamblis.objects.all(),
        'selected_ansamblis_id': selected_ansamblis_id,
        'role_filter': role_filter,
        'search_query': search,
        'sort_param': sort,
    })
# ✅ Custom Form for Creating a User
class CustomUserCreationForm(UserCreationForm):
    vardas = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pavarde = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    ansambliai = forms.ModelMultipleChoiceField(
        queryset=Ansamblis.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'vardas', 'pavarde', 'email', 'phone_number', 'role', 'password1', 'password2', 'ansambliai']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})# ✅ View to Add a New User
@login_required
def nariai_add(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti narių.")

    if request.user.role == "vadovas":
        all_ansambliai = request.user.ansambliai.all()
    else:
        all_ansambliai = Ansamblis.objects.all()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.vardas = form.cleaned_data['vardas']
            user.pavarde = form.cleaned_data['pavarde']
            user.save()

            selected_ansambliai_ids = request.POST.getlist("ansambliai")
            selected_ansambliai = Ansamblis.objects.filter(id__in=selected_ansambliai_ids)

            if request.user.role == "vadovas":
                selected_ansambliai = selected_ansambliai.filter(id__in=request.user.ansambliai.values_list('id', flat=True))

            user.ansambliai.set(selected_ansambliai)
            messages.success(request, "Naujas vartotojas sėkmingai pridėtas!")
            return redirect('nariai')

    else:
        form = CustomUserCreationForm()

    return render(request, 'nariai_add.html', {'form': form, 'all_ansambliai': all_ansambliai})



@login_required
def nariai_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės peržiūrėti šio nario informacijos.")

    if request.user.role == "vadovas":
        if not user.ansambliai.filter(id__in=request.user.ansambliai.values_list('id', flat=True)).exists():
            return HttpResponseForbidden("Jūs galite peržiūrėti tik savo ansamblio narius.")

    return render(request, 'nariai_view.html', {'user': user})

# ✅ Custom User Edit Form
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

# ✅ View to Edit a User
@login_required
def nariai_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti narių.")

    if request.user.role == "vadovas":
        if not user.ansambliai.filter(id__in=request.user.ansambliai.values_list('id', flat=True)).exists():
            return HttpResponseForbidden("Jūs galite redaguoti tik savo ansamblio narius.")

    all_ansambliai = Ansamblis.objects.all()

    if request.method == 'POST':
        form_type = request.POST.get('which_form')

        # ✅ 1. User Info Update Only
        if form_type == 'info':
            user.username = request.POST.get('username', user.username)
            user.email = request.POST.get('email', user.email)
            user.phone_number = request.POST.get('phone_number', user.phone_number)
            user.role = request.POST.get('role', user.role)
            user.vardas = request.POST.get('vardas', user.vardas)
            user.pavarde = request.POST.get('pavarde', user.pavarde)

            selected_ansambliai_ids = request.POST.getlist('ansambliai')

            if request.user.role == "vadovas":
                selected_ansambliai = Ansamblis.objects.filter(id__in=selected_ansambliai_ids).intersection(
                    Ansamblis.objects.filter(id__in=request.user.ansambliai.values_list('id', flat=True))
                )
            else:
                selected_ansambliai = Ansamblis.objects.filter(id__in=selected_ansambliai_ids)

            user.ansambliai.set(selected_ansambliai)
            user.save()
            messages.success(request, "Vartotojo duomenys atnaujinti sėkmingai.")
            return redirect('nariai_edit', user_id=user.id)

        # ✅ 2. Password Update Only
        elif form_type == 'password':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

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

            return redirect('nariai_edit', user_id=user.id)

    return render(request, 'nariai_edit.html', {'user': user, 'all_ansambliai': all_ansambliai})
def nariai_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti narių.")

    if request.user.role == "vadovas":
        if not user.ansambliai.filter(id__in=request.user.ansambliai.values_list('id', flat=True)).exists():
            return HttpResponseForbidden("Jūs galite ištrinti tik savo ansamblio narius.")

    if request.method == "POST":
        user.delete()
        messages.success(request, "Vartotojas sėkmingai ištrintas.")
        return redirect('nariai')

    messages.error(request, "Negalima ištrinti vartotojo.")
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
def profilis_edit(request):
    user = request.user
    profile_updated = False
    password_updated = False
    password_error = None

    if request.method == 'POST':
        if request.POST.get('which_form') == 'info':
            user.vardas = request.POST.get('vardas', user.vardas)
            user.pavarde = request.POST.get('pavarde', user.pavarde)
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
                update_session_auth_hash(request, user)  # ✅ Stay logged in
                password_updated = True
            else:
                password_error = "Slaptažodžiai nesutampa arba tušti."

    context = {
        'user': user,
        'profile_updated': profile_updated,
        'password_updated': password_updated,
        'password_error': password_error
    }

    return render(request, 'profilis_edit.html', context)
