from django.shortcuts import render

# Hardcoded data for Programos
PROGRAMOS = [
    {"id": 1, "name": "Program A"},
    {"id": 2, "name": "Program B"},
    {"id": 3, "name": "Program C"},
]

def programos_page(request):
    return render(request, 'programos.html', {"programos": PROGRAMOS})
