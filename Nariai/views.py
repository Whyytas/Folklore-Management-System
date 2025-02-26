from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Hardcoded nariai
NARIAI = [
    {"id": 1, "name": "Jonas", "surname": "Jonaitis"},
    {"id": 2, "name": "Ona", "surname": "Onaite"},
    {"id": 3, "name": "Petras", "surname": "Petraitis"},
]

# View to render the Nariai page
def nariai_page(request):
    return render(request, 'nariai.html', {"nariai": NARIAI})
