from django.shortcuts import render

# Hardcoded data for Instrumentai
INSTRUMENTAI = [
    {"id": 1, "name": "Violin"},
    {"id": 2, "name": "Flute"},
    {"id": 3, "name": "Drum"},
]

def instrumentai_page(request):
    return render(request, 'instrumentai.html', {"instrumentai": INSTRUMENTAI})
