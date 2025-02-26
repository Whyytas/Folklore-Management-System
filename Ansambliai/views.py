from django.shortcuts import render

# Hardcoded ensembles
ENSEMBLES = [
    {"id": 1, "name": "Folk Ensemble A"},
    {"id": 2, "name": "Folk Ensemble B"},
    {"id": 3, "name": "Folk Ensemble C"},
]

# View to render a page with ensemble list
def ensembles_page(request):
    return render(request, 'ansambliai.html', {"ansambliai": ENSEMBLES})
