from django.shortcuts import render
from apis.models import Padalinys

def index(request):
    padalinys_list = Padalinys.objects.all()  # Query all Padalinys objects
    context = {
        "padalinys_list": padalinys_list,
    }
    return render(request, "index.html", context)

