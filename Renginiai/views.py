import io
import os

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf import pisa
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER

from Ansambliai.models import Ansamblis
from Initial.models import User
from Programos.models import Programa, ProgramosKurinys
from .models import Renginys
from .forms import RenginysForm
from django.http import HttpResponseForbidden
import datetime  # ✅ Correct way to import datetime module

def renginiai_list(request):
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")
    sort_field = request.GET.get("sort", "pavadinimas")
    sort_dir = request.GET.get("dir", "asc")
    programa_id = request.GET.get("programa_id")
    search = request.GET.get("search", "").strip()

    sort_order = sort_field if sort_dir == "asc" else f"-{sort_field}"

    renginiai = Renginys.objects.select_related("ansamblis", "programa").all().order_by(sort_order, "-id")

    if selected_ansamblis_id:
        renginiai = renginiai.filter(ansamblis__id=selected_ansamblis_id)
    if programa_id:
        renginiai = renginiai.filter(programa__id=programa_id)
    if search:
        renginiai = renginiai.filter(pavadinimas__icontains=search)

    paginator = Paginator(renginiai, 15)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    selected_renginys = renginiai.first()
    nariai = User.objects.filter(ansambliai=selected_renginys.ansamblis, role="narys") if selected_renginys else []

    return render(request, 'renginiai.html', {
        'renginiai': page_obj.object_list,
        'page_obj': page_obj,
        'sort_field': sort_field,
        'sort_dir': sort_dir,
        'programa_id': programa_id,
        'search': search,
        'programos': Programa.objects.all(),
        "nariai": nariai,
        "selected_renginys": selected_renginys,
    })

def renginiai_add(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti renginių.")

    if request.method == "POST":
        form = RenginysForm(request.POST)
        if form.is_valid():
            renginys = form.save(commit=False)
            renginys.data_laikas = make_aware(renginys.data_laikas)
            renginys.save()
            return redirect("renginiai")

    form = RenginysForm()
    return render(request, "renginiai_add.html", {"form": form})

def renginiai_edit(request, renginys_id):
    renginys = get_object_or_404(Renginys, id=renginys_id)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti renginių.")

    if request.method == "POST":
        form = RenginysForm(request.POST, instance=renginys)
        if form.is_valid():
            renginys = form.save(commit=False)
            if isinstance(form.cleaned_data["data_laikas"], str):
                naive_datetime = datetime.datetime.strptime(form.cleaned_data["data_laikas"], "%Y-%m-%d %H:%M")
                renginys.data_laikas = make_aware(naive_datetime)
            else:
                renginys.data_laikas = make_aware(form.cleaned_data["data_laikas"])
            renginys.save()
            return redirect('renginiai')

    renginys.data_laikas = renginys.data_laikas.strftime("%Y-%m-%d %H:%M") if renginys.data_laikas else ""
    form = RenginysForm(instance=renginys)

    return render(request, "renginiai_edit.html", {
        "renginys": renginys,
        "form": form,
        "ansambliai": Ansamblis.objects.all(),
        "programos": Programa.objects.all()
    })

def delete_renginys(request, renginys_id):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti renginių.")

    if request.method == "POST":
        renginys = get_object_or_404(Renginys, id=renginys_id)
        renginys.delete()
        return redirect("renginiai")  # ✅ Redirect to the renginiai list

    return JsonResponse({"error": "Invalid request method"}, status=400)

def publicEvents(request):
    return render(request, 'renginiaiPublic.html', )

def renginys_pdf_view(request, renginys_id):
    from reportlab.lib.styles import ListStyle

    list_style = ListStyle(
        name='TimesNumbered',
        leftIndent=20,
        bulletFontName='TimesNewRoman',
        bulletFontSize=12,
        bulletIndent=0
    )

    selected_ids = request.POST.getlist("nariai")
    renginys = get_object_or_404(Renginys, id=renginys_id)
    nariai = User.objects.filter(id__in=selected_ids, ansambliai=renginys.ansamblis).distinct()
    programos_kuriniai = ProgramosKurinys.objects.filter(programa=renginys.programa).select_related("kurinys")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="renginys_{renginys_id}.pdf"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'C:/Windows/Fonts/times.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', 'C:/Windows/Fonts/timesbd.ttf'))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterTitle', fontName='TimesNewRoman', fontSize=20, alignment=TA_CENTER, spaceAfter=20))
    styles.add(ParagraphStyle(name='NormalCustom', fontName='TimesNewRoman', fontSize=12, leading=15))
    styles.add(ParagraphStyle(name='NormalBold', fontName='TimesNewRoman-Bold', fontSize=12, leading=15))

    elements = []

    formatted_date = renginys.formatted_data_laikas()
    address = renginys.adresas
    title = renginys.pavadinimas

    elements.append(Paragraph(f"{formatted_date}<br/>{address}", styles['NormalCustom']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(title, styles['CenterTitle']))
    elements.append(Spacer(1, 6))

    list_items = []
    for pk in programos_kuriniai:
        k = pk.kurinys

        line = f'„<font name="TimesNewRoman-Bold">{k.pavadinimas}</font>“ ({k.tipas})'
        if k.vieta:
            line += f', {k.vieta}'
        if k.regionas:
            line += f' ({k.regionas})'

        list_items.append(Paragraph(line, styles['NormalCustom']))

    # elements.append(ListFlowable(list_items, bulletType='1', start=1))

    elements.append(ListFlowable(
        list_items,
        bulletType='1',
        start='1',
        bulletFormat="%s.",  # 👈 Add dot after number
        style=list_style
    ))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Dalyvaujantys nariai:", styles['NormalBold']))
    for narys in nariai:
        elements.append(Paragraph(f"{narys.vardas} {narys.pavarde}", styles['NormalCustom']))

    doc.build(elements)
    response.write(buffer.getvalue())
    buffer.close()
    return response

def nariai_for_renginys(request, renginys_id):
    renginys = get_object_or_404(Renginys, id=renginys_id)
    nariai = User.objects.filter(ansambliai__id=renginys.ansamblis.id).distinct()


    html = render_to_string("nariai_checkbox_list.html", {"nariai": nariai})
    return JsonResponse({"html": html})