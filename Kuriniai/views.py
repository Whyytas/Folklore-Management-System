from django.shortcuts import render

# Hardcoded data for Kūriniai
KURINIAI = [
    {"id": 1, "name": "Song A", "length": "3:45"},
    {"id": 2, "name": "Song B", "length": "4:20"},
    {"id": 3, "name": "Song C", "length": "5:10"},
]

def kuriniai_page(request):
    return render(request, 'kuriniai.html', {"kuriniai": KURINIAI})
