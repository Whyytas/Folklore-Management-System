from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import json

from django.urls import reverse
from django.utils.timezone import now

from Pieces.models import Piece
from Rehearsals.models import Rehearsal, RehearsalPiece
from Ensembles.models import Ensemble  #  Import Ansamblis


from django.core.paginator import Paginator

@login_required
def rehearsals_list(request):
    selected_ensemble_id = request.session.get("selected_ensemble_id")
    sort_param = request.GET.get("sort", "date")
    show_all = request.GET.get("show", "") == "all"

    if sort_param not in ["date", "-date", "title", "-title"]:
        sort_param = "date"

    rehearsals = (
        Rehearsal.objects
        .select_related("ensemble")
        .prefetch_related("pieces")  # preload M2M
        .only("id", "title", "date", "ensemble__title")  # narrow field load
    )

    if not show_all:
        rehearsals = rehearsals.filter(date__gte=now())

    if selected_ensemble_id:
        rehearsals = rehearsals.filter(ensemble_id=selected_ensemble_id)

    rehearsals = rehearsals.order_by(sort_param)

    return render(request, 'rehearsals_list.html', {
        'rehearsals': rehearsals,
        'all_ensembles': Ensemble.objects.only("id", "title"),
        'sort_param': sort_param,
        'show_all': show_all,
    })

@login_required
def rehearsal_create(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės kurti repeticijų.")

    if request.method == 'POST':
        try:
            if request.content_type != "application/json":
                return JsonResponse({"error": "Netinkamas užklausos tipas."}, status=400)

            data = json.loads(request.body)
            title = data.get("title", "").strip()
            date = data.get("date", "").strip()
            pieces_ids = data.get("pieces", [])
            ensemble_id = data.get("ensemble")

            if not title or not date or not pieces_ids or not ensemble_id:
                return JsonResponse({"error": "Prašome užpildyti visus laukus ir pasirinkti kūrinius."}, status=400)

            try:
                data_datetime = datetime.strptime(date[:16], '%Y-%m-%d %H:%M')
            except ValueError:
                return JsonResponse({"error": "Netinkamas datos formatas."}, status=400)

            selected_ensemble = get_object_or_404(Ensemble, id=ensemble_id)
            rehearsal = Rehearsal.objects.create(
                title=title,
                date=data_datetime,
                ensemble=selected_ensemble
            )

            # Save RehearsalPiece with order preserved
            relations = []
            for index, piece_id in enumerate(pieces_ids):
                piece = get_object_or_404(Piece, id=piece_id)
                relations.append(
                    RehearsalPiece(
                        rehearsal=rehearsal,
                        piece=piece,
                        order=index
                    )
                )

            RehearsalPiece.objects.bulk_create(relations)

            return JsonResponse({"redirect": reverse("rehearsals")}, status=201)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": f"Serverio klaida: {str(e)}"}, status=500)

    # GET → show form
    ensembles = Ensemble.objects.all()
    return render(request, "rehearsal_add.html", {
        "ensembles": ensembles
    })

@login_required
def rehearsal_edit(request, pk):
    rehearsal = get_object_or_404(Rehearsal, pk=pk)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti repeticijų.")

    if request.method == "POST":
        if request.content_type != "application/json":
            return HttpResponseBadRequest("Netinkamas užklausos tipas.")

        try:
            data = json.loads(request.body)

            rehearsal.title = data.get("title", rehearsal.title)
            date_value = data.get("date")
            if date_value:
                rehearsal.date = datetime.strptime(date_value.strip()[:16], '%Y-%m-%d %H:%M')

            ensemble_id = data.get("ensemble")
            if ensemble_id:
                rehearsal.ensemble = get_object_or_404(Ensemble, id=ensemble_id)

            rehearsal.save()

            pieces_ids = data.get("pieces", [])

            with transaction.atomic():
                rehearsal.rehearsalpiece_set.all().delete()
                for order, kid in enumerate(pieces_ids):
                    piece = Piece.objects.get(id=kid)
                    RehearsalPiece.objects.create(
                        rehearsal=rehearsal,
                        piece=piece,
                        order=order
                    )

            return JsonResponse({"redirect": reverse("rehearsals")})

        except Exception as e:
            return JsonResponse({"error": f"Klaida: {str(e)}"}, status=500)

    # GET method
    ordered_pieces = rehearsal.pieces.through.objects.filter(
        rehearsal=rehearsal
    ).select_related('piece').order_by('order')

    all_pieces = Piece.objects.filter(ensembles=rehearsal.ensemble)
    ensembles = Ensemble.objects.all()

    return render(request, "rehearsal_edit.html", {
        "rehearsal": rehearsal,
        "ordered_pieces": [rk.piece for rk in ordered_pieces],
        "all_pieces": all_pieces,
        "ensembles": ensembles
    })
@login_required
def rehearsal_delete(request, pk):
    rehearsal = get_object_or_404(Rehearsal, pk=pk)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti repeticijų.")

    if request.method == "POST":
        rehearsal.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@login_required
def rehearsal_detail(request, pk):
    rehearsal = get_object_or_404(
        Rehearsal.objects.prefetch_related(
            Prefetch(
                "pieces",
                queryset=Piece.objects.all().order_by("rehearsalpiece__order")
            )
        ),
        pk=pk
    )
    return render(request, 'rehearsal_detail.html', {'rehearsal': rehearsal})