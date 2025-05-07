import re
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from Ensembles.models import Ensemble
from Pieces.models import Piece, Feature
from Events.models import Event
from .models import Program, ProgramPiece
import json
from django.http import JsonResponse, HttpResponseForbidden
import random

from django.core.paginator import Paginator


def programs_list(request):
    user = request.user
    is_admin = getattr(user, "role", "").lower() == "administratorius"

    selected_ensemble_id = request.GET.get("ensemble_id") or request.session.get("selected_ensemble_id")
    sort_field = request.GET.get("sort", "title")
    sort_dir = request.GET.get("dir", "asc")
    type_filter = request.GET.get("type")

    valid_sort_fields = ["title", "duration", "type"]
    if sort_field not in valid_sort_fields:
        sort_field = "title"
    sort_order = sort_field if sort_dir == "asc" else f"-{sort_field}"

    allowed_ensembles = Ensemble.objects.all() if is_admin else Ensemble.objects.filter(members=user)

    programs_qs = Program.objects.select_related("ensemble").only(
        "id", "title", "type", "ensemble_id", "duration"
    ).filter(ensemble__in=allowed_ensembles).order_by(sort_order)

    if selected_ensemble_id and allowed_ensembles.filter(id=selected_ensemble_id).exists():
        programs_qs = programs_qs.filter(ensemble_id=selected_ensemble_id)

    if type_filter:
        programs_qs = programs_qs.filter(type=type_filter)

    return render(request, 'programs_list.html', {
        'programs': programs_qs,
        'sort_field': sort_field,
        'sort_dir': sort_dir,
        'type_filter': type_filter,
        'types': Program.PROGRAM_TYPE,
        'all_ensembles': allowed_ensembles,
    })

def program_generate(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės generuoti programų.")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            type = data.get("type")
            pieces_data = data.get("pieces", [])

            if not title or not type or not pieces_data:
                return JsonResponse({"error": "Trūksta reikiamų laukų arba kūrinių!"}, status=400)

            program = Program.objects.create(
                title=title,
                type=type,
                description=data.get("description", ""),
                duration=data.get("duration", ""),
                ensemble_id=data.get("ensemble")
            )

            pieces_ids = [item["id"] for item in pieces_data]
            pieces_qs = Piece.objects.filter(id__in=pieces_ids)
            pieces_map = {k.id: k for k in pieces_qs}

            total_seconds = 0
            program_pieces = []

            for item in pieces_data:
                kid = int(item["id"])
                queue = int(item.get("queue", 0))
                piece = pieces_map.get(kid)

                if piece and queue is not None:
                    program_pieces.append(
                        ProgramPiece(
                            program=program,
                            piece=piece,
                            queue=queue
                        )
                    )
                    # Calculate total duration
                    if piece.duration and ":" in piece.duration:
                        m, s = map(int, piece.duration.split(":"))
                        total_seconds += m * 60 + s

            Program.objects.filter(id=program.id).update(
                duration=f"{total_seconds // 60:02}:{total_seconds % 60:02}"
            )

            ProgramPiece.objects.bulk_create(program_pieces)

            return JsonResponse({"redirect": "/programos"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    ensembles = Ensemble.objects.all()
    types = Program.PROGRAM_TYPE

    return render(request, "program_generate.html", {
        "type": types,
        "ensembles": ensembles
    })

def program_create(request):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės pridėti programų.")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            type = data.get("type")
            description = data.get("description", "")
            ensemble_id = data.get("ensemble")
            pieces_data = data.get("pieces", [])
            manual_duration = data.get("duration", "").strip()

            if not title or not type or not pieces_data:
                return JsonResponse({"error": "Trūksta reikiamų laukų arba kūrinių!"}, status=400)

            program = Program.objects.create(
                title=title,
                type=type,
                description=description,
                ensemble_id=ensemble_id or None
            )

            piece_ids = [item["id"] for item in pieces_data]
            pieces_qs = Piece.objects.filter(id__in=piece_ids)
            pieces_map = {k.id: k for k in pieces_qs}

            total_seconds = 0
            programs_pieces = []

            for item in pieces_data:
                kid = int(item["id"])
                queue = item.get("queue")
                piece = pieces_map.get(kid)

                if piece and queue is not None:
                    programs_pieces.append(
                        ProgramPiece(
                            program=program,
                            piece=piece,
                            queue=queue
                        )
                    )
                    if piece.duration and ":" in piece.duration:
                        try:
                            minutes, seconds = map(int, piece.duration.split(":"))
                            total_seconds += minutes * 60 + seconds
                        except ValueError:
                            pass  # skip invalid duration

            # Use manual duration if provided and valid, else use calculated
            if manual_duration and ":" in manual_duration:
                try:
                    m, s = map(int, manual_duration.split(":"))
                    program.duration = f"{m:02}:{s:02}"
                except ValueError:
                    program.duration = f"{total_seconds // 60:02}:{total_seconds % 60:02}"
            else:
                program.duration = f"{total_seconds // 60:02}:{total_seconds % 60:02}"

            program.save()
            ProgramPiece.objects.bulk_create(programs_pieces)

            return JsonResponse({"redirect": "/programos"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    ensembles = Ensemble.objects.all()
    types = Program.PROGRAM_TYPE

    return render(request, "program_add.html", {
        "types": types,
        "ensembles": ensembles
    })

def program_edit(request, pk):
    program = get_object_or_404(Program, pk=pk)

    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės redaguoti programų.")

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            program.title = data["title"]
            program.type = data["type"]
            program.description = data.get("description", "")
            program.duration = data["duration"]

            ensemble_id = data.get("ensemble")
            if ensemble_id:
                program.ensemble_id = ensemble_id

            program.save()

            ProgramPiece.objects.filter(program=program).delete()
            for k_data in data.get("pieces", []):
                ProgramPiece.objects.create(
                    program=program,
                    piece_id=k_data["id"],
                    queue=k_data.get("queue", 0)
                )

            return JsonResponse({"redirect": "/programos"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    selected_pieces = ProgramPiece.objects.filter(program=program).order_by("queue")
    context = {
        "program": program,
        "selected_pieces": selected_pieces,
        "selected_pieces_ids": [pk.piece.id for pk in selected_pieces],
        "types": Program.PROGRAM_TYPE,
        "ensembles": Ensemble.objects.all(),
    }
    return render(request, "program_edit.html", context)

def program_delete(request, pk):
    if request.user.role == "narys":
        return HttpResponseForbidden("Jūs neturite teisės ištrinti programų.")

    program = get_object_or_404(Program, pk=pk)

    if request.method == "POST":
        program.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def programs_pieces_view(request, pk):
    program = get_object_or_404(Program, pk=pk)

    # Retrieve all Kūriniai in the correct queue (`queue`)
    program_pieces = ProgramPiece.objects.filter(program=program).order_by("queue")

    return render(request, 'program_pieces.html', {
        "program": program,
        "program_pieces": program_pieces
    })

def generate_pieces(request):
    try:
        data = json.loads(request.body)
        feature = data.get("feature")
        duration = data.get("duration")
        ensemble_id = int(data.get("ensemble", 0))
        santykis = data.get("santykis", "")
        include_balfolk = data.get("include_balfolk", True)

        if not feature or not duration or not ensemble_id:
            return JsonResponse({"error": "Trūksta duomenų."}, status=400)

        m, s = map(int, duration.split(":"))
        target_seconds = m * 60 + s

        all_pieces = Piece.objects.filter(ensembles__id=ensemble_id)

        if feature == "Susidainavimams":
            feature = Feature.objects.filter(title__iexact="Susidainavimams").first()
            if not feature:
                return JsonResponse([], safe=False)

            filtered = all_pieces.filter(features=feature).exclude(preparation__in=["Archyvas", "Naujas"])
            return JsonResponse(_select_up_to_duration(filtered, target_seconds), safe=False)

        elif feature == "Vakaronei":
            feature = Feature.objects.filter(title__iexact="Vakaronei").first()
            if not feature:
                return JsonResponse([], safe=False)

            filtered = all_pieces.filter(features=feature).exclude(preparation__in=["Archyvas", "Naujas"])

            # Check if we need to exclude Balfolk pieces
            if not include_balfolk:
                balfolk_feature = Feature.objects.filter(title__iexact="Balfolk").first()
                if balfolk_feature:
                    filtered = filtered.exclude(features=balfolk_feature)

            groups = {"Lėtas": [], "Vidutinis": [], "Greitas": []}
            for k in filtered:
                if k.duration and k.speed and ":" in k.duration:
                    groups[k.speed].append(k)

            for g in groups:
                random.shuffle(groups[g])

            result = []
            total = 0
            cycle = ["Lėtas", "Vidutinis", "Greitas"]
            i = 0
            while total < target_seconds and any(groups.values()):
                group = cycle[i % 3]
                if groups[group]:
                    k = groups[group].pop()
                    m, s = map(int, k.duration.split(":"))
                    dur = m * 60 + s
                    if total + dur <= target_seconds:
                        result.append(k)
                        total += dur
                i += 1

            return JsonResponse(_pieces_to_json(result), safe=False)

        else:
            used_pradzia_id = _recent_program_pradzia_piece()
            pradzia_pozymis = Feature.objects.filter(title__iexact="Pradžia").first()
            pradzia_candidates = all_pieces.exclude(preparation__in=["Archyvas", "Naujas"])

            if pradzia_pozymis:
                pradzia_candidates = pradzia_candidates.filter(features=pradzia_pozymis)

            if used_pradzia_id:
                pradzia_candidates = pradzia_candidates.exclude(id=used_pradzia_id)

            pradzia_piece = next(
                (k for k in pradzia_candidates if k.duration and ":" in k.duration),
                None
            )

            # fallback if santykis is missing or invalid
            if not santykis or ":" not in santykis:
                return JsonResponse(_pieces_to_json([pradzia_piece] if pradzia_piece else []), safe=False)

            try:
                d, s_, k = map(int, santykis.split(":"))
            except Exception:
                return JsonResponse({
                    "error": "Neteisingas santykio formatas. Pvz: 3:2:1"
                }, status=400)

            feature_obj = Feature.objects.filter(title__iexact=feature).first()
            if not feature_obj:
                return JsonResponse({"error": f"Požymis '{feature}' nerastas."}, status=404)

            available = all_pieces.filter(
                features=feature_obj,
                duration__contains=":"
            ).exclude(preparation__in=["Archyvas", "Naujas"]).distinct()

            print("🔍 available.count():", available.count())
            print("🔍 available types:", available.values_list("type", flat=True).distinct())

            if pradzia_piece:
                available = available.exclude(id=pradzia_piece.id)

            groups = {"Daina": [], "Šokis": [], "Instrumentalas": []}
            for kur in available:
                if kur.type in groups and ":" in kur.duration:
                    groups[kur.type].append(kur)

            for g in groups:
                random.shuffle(groups[g])

            cycle = ["Daina"] * d + ["Šokis"] * s_ + ["Instrumentalas"] * k
            total_result = []
            total_time = 0

            # Sort each group by shortest duration first
            for group_name in groups:
                groups[group_name].sort(
                    key=lambda k: sum(int(x) * 60 ** i for i, x in enumerate(reversed(k.duration.split(":")))))

            first_group_added = False

            while True:
                group = []
                group_time = 0
                for group_name in cycle:
                    if not groups[group_name]:
                        group = []
                        break

                    kur = groups[group_name].pop(0)
                    m, s = map(int, kur.duration.split(":"))
                    dur = m * 60 + s
                    group.append((kur, dur))
                    group_time += dur

                if not group:
                    break

                if not first_group_added:
                    total_result.extend([k for k, _ in group])
                    total_time += group_time
                    first_group_added = True
                    continue

                if total_time + group_time > target_seconds:
                    # Try to build shortest possible group
                    short_group = []
                    short_time = 0
                    for group_name in cycle:
                        for candidate in groups[group_name]:
                            if ":" not in candidate.duration:
                                continue
                            m, s = map(int, candidate.duration.split(":"))
                            dur = m * 60 + s
                            short_group.append((candidate, dur))
                            short_time += dur
                            break

                    if short_group and total_time + short_time <= target_seconds:
                        total_result.extend([k for k, _ in short_group])
                    break

                total_result.extend([k for k, _ in group])
                total_time += group_time

            sort_order = {"Daina": 1, "Instrumentalas": 2, "Šokis": 3}
            sorted_result = sorted(total_result, key=lambda x: sort_order.get(x.type, 99))

            final_result = []
            if pradzia_piece:
                final_result.append(pradzia_piece)
            final_result.extend(sorted_result)

            return JsonResponse(_pieces_to_json(final_result), safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def _pieces_to_json(pieces):
    return [
        {
            "id": k.id,
            "title": k.title,
            "duration": k.duration,
            "type": k.type,
            "regionas": k.region or "",
        }
        for k in pieces
    ]


def _select_up_to_duration(queryset, max_seconds):
    valid = [k for k in queryset if k.duration and ":" in k.duration]
    for k in valid:
        m, s = map(int, k.duration.split(":"))
        k.seconds = m * 60 + s
    random.shuffle(valid)

    selected = []
    total = 0
    for k in valid:
        if total + k.seconds > max_seconds:
            continue
        selected.append(k)
        total += k.seconds
    return _pieces_to_json(selected)


def _recent_program_pradzia_piece():
    recent_renginys = Event.objects.filter(
        date__lt=datetime.now(),
        program__isnull=False
    ).order_by("-date").first()

    if not recent_renginys or not recent_renginys.program:
        return None

    program = recent_renginys.program
    last = ProgramPiece.objects.filter(program=program, piece__type="Pradžia").first()

    return last.piece.id if last else None


def _duration_in_seconds(duration_str):
    m, s = map(int, duration_str.split(":"))
    return m * 60 + s

def get_programs_by_ensemble(request, ensemble_id):
    programs = Program.objects.filter(ensemble_id=ensemble_id).values("id", "title")
    return JsonResponse(list(programs), safe=False)