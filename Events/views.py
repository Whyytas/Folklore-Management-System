import io

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER

from Ensembles.models import Ensemble
from Initial.models import User
from Programs.models import Program, ProgramPiece
from .models import Event
from .forms import EventForm
from django.http import HttpResponseForbidden
import datetime  #  Correct way to import datetime module

def events_list(request):
    selected_ensemble_id = request.GET.get('ensemble_id') or request.session.get("selected_ensemble_id")
    sort_field = request.GET.get("sort", "title")
    sort_dir = request.GET.get("dir", "asc")
    program_id = request.GET.get("program_id")
    search = request.GET.get("search", "").strip()

    sort_order = sort_field if sort_dir == "asc" else f"-{sort_field}"

    events = Event.objects.select_related("ensemble", "program").all().order_by(sort_order, "-id")

    if selected_ensemble_id:
        events = events.filter(ensemble__id=selected_ensemble_id)

    if program_id:
        events = events.filter(program__id=program_id)

    if search:
        events = events.filter(title__icontains=search)

    selected_event = events.first()
    users = User.objects.filter(ensembles=selected_event.ensemble, role="narys") if selected_event else []

    return render(request, 'events_list.html', {
        'events': events,
        'sort_field': sort_field,
        'sort_dir': sort_dir,
        'program_id': program_id,
        'search': search,
        'programs': Program.objects.all(),
        'ensembles': Ensemble.objects.all(),
        'all_ensembles': Ensemble.objects.all(),  #  needed for navbar
        'selected_ensemble_id': selected_ensemble_id,
        'users': users,
        'selected_event': selected_event,
    })

def events_add(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti renginių.")

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.date = make_aware(event.date)
            event.save()
            return redirect("renginiai")

    form = EventForm()
    return render(request, "event_add.html", {"form": form})

def events_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti renginių.")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            if isinstance(form.cleaned_data["date"], str):
                naive_datetime = datetime.datetime.strptime(form.cleaned_data["date"], "%Y-%m-%d %H:%M")
                event.date = make_aware(naive_datetime)
            else:
                event.date = make_aware(form.cleaned_data["date"])
            event.save()
            return redirect('renginiai')

    event.date = event.date.strftime("%Y-%m-%d %H:%M") if event.date else ""
    form = EventForm(instance=event)

    # 🔽 Filter programs by the same ensemble as the event
    programs = Program.objects.filter(ensemble=event.ensemble)

    return render(request, "event_edit.html", {
        "event": event,
        "form": form,
        "ensembles": Ensemble.objects.all(),
        "programs": programs
    })

def event_delete(request, renginys_id):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti renginių.")

    if request.method == "POST":
        events = get_object_or_404(Event, id=renginys_id)
        events.delete()
        return redirect("renginiai")  #  Redirect to the renginiai list

    return JsonResponse({"error": "Invalid request method"}, status=400)

def publicEvents(request):
    return render(request, 'renginiaiPublic.html', )

def event_pdf_view(request, event_id):
    from reportlab.lib.styles import ListStyle

    list_style = ListStyle(
        name='TimesNumbered',
        leftIndent=20,
        bulletFontName='TimesNewRoman',
        bulletFontSize=12,
        bulletIndent=0
    )

    selected_ids = request.POST.getlist("users")
    event = get_object_or_404(Event, id=event_id)
    users = User.objects.filter(id__in=selected_ids, ensembles=event.ensemble).distinct()
    program_piece = ProgramPiece.objects.filter(program=event.program).select_related("piece")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="renginys_{event_id}.pdf"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'C:/Windows/Fonts/times.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', 'C:/Windows/Fonts/timesbd.ttf'))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterTitle', fontName='TimesNewRoman', fontSize=20, alignment=TA_CENTER, spaceAfter=20))
    styles.add(ParagraphStyle(name='NormalCustom', fontName='TimesNewRoman', fontSize=12, leading=15))
    styles.add(ParagraphStyle(name='NormalBold', fontName='TimesNewRoman-Bold', fontSize=12, leading=15))

    elements = []

    formatted_date = event.formatted_data_laikas()
    address = event.address
    title = event.title

    elements.append(Paragraph(f"{formatted_date}<br/>{address}", styles['NormalCustom']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(title, styles['CenterTitle']))
    elements.append(Spacer(1, 6))

    list_items = []
    for pk in program_piece:
        k = pk.piece

        line = f'„<font name="TimesNewRoman-Bold">{k.title}</font>“ ({k.type})'
        if k.place:
            line += f', {k.place}'
        if k.region:
            line += f' ({k.region})'

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
    for user in users:
        elements.append(Paragraph(f"{user.name} {user.surname}", styles['NormalCustom']))

    doc.build(elements)
    response.write(buffer.getvalue())
    buffer.close()
    return response

def users_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    users = User.objects.filter(ensembles__id=event.ensemble.id).distinct()


    html = render_to_string("users_checkbox_list.html", {"users": users})
    return JsonResponse({"html": html})