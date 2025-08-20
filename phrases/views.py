from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import *
from .utils import normalize_text

import json
from rapidfuzz import process, fuzz


def match_concept(user_input, correct_concept_pk, cutoff_score=85):
    normalized = normalize_text(user_input)
    rapidfuzz_function = fuzz.WRatio
    try:
        correct_concept = MedicalConcept.objects.get(pk=correct_concept_pk)
    except MedicalConcept.DoesNotExist:
        return {"message": "error", "message": "Invalid concept id"}

    # Get only variants related to the expected concept
    correct_variants_qs = correct_concept.variants.all()
    correct_variant_texts = [v.text for v in correct_variants_qs]

    # 1. Exact match to correct variants
    if normalized in correct_variant_texts:
        return {"message": "correct", "matched_variant": normalized}

    # 2. Check if it matches another known concept
    all_variant_texts = TermVariant.objects.values_list("text", flat=True)
    if normalized in all_variant_texts:
        wrong_variant = TermVariant.objects.get(text=normalized)
        return {"message": "incorrect", "matched_variant": wrong_variant.concept.name}

    # 3. Fuzzy match within correct variants
    if correct_variant_texts:
        # match, score, _ = process.extractOne(normalized, correct_variant_texts, scorer=fuzz.token_sort_ratio)
        for text_var in correct_variant_texts:
            score = rapidfuzz_function(normalized, text_var)
            if score > cutoff_score:
                unmapped, created = UnmappedTerm.objects.get_or_create(
                    text=normalized,  # <-- only search by this
                    defaults={
                        "score": int(score),
                        "concept": correct_concept,
                        "matched_term": TermVariant.objects.get(text=text_var),
                    },
                )
                if not created:
                    unmapped.seen_count += 1
                    unmapped.save()
                return {"message": "partially_correct", "matched_variant": text_var}

    # 4. Fuzzy match within all variants
    other_match, other_score, _ = process.extractOne(
        normalized, all_variant_texts, scorer=rapidfuzz_function
    )

    if other_score > cutoff_score:
        wrong_variant = TermVariant.objects.get(text=other_match)
        unmapped, created = UnmappedTerm.objects.get_or_create(
            text=normalized,  # <-- only search by this
            defaults={
                "score": int(score),
                "concept": correct_concept,
                "matched_term": TermVariant.objects.get(text=text_var),
                "common_similarity": False,
            },
        )
        if not created:
            unmapped.seen_count += 1
            unmapped.save()
        return {
            "message": "wrong_concept",
            "matched_variant": other_match,
            "matched_concept": wrong_variant.concept.name,
        }

    # 5. Log unknown
    unmapped, created = UnmappedTerm.objects.get_or_create(
        text=normalized,  # <-- only search by this
        defaults={
            "score": int(score),
            "concept": correct_concept,
            "matched_term": TermVariant.objects.get(text=text_var),
            "common_similarity": False,
        },
    )
    if not created:
        unmapped.seen_count += 1
        unmapped.save()

    return {"message": "unknown", "matched_variant": None}


@require_http_methods(["GET", "POST"])
def mono_text_check(request):
    payload = json.loads(request.body or "{}")
    user_input = (payload.get("input_text") or "").strip()
    concept_id = payload.get("concept_id")

    if not user_input:
        return JsonResponse(
            {"status": "error", "message": "No answer provided."}, status=400
        )

    result = match_concept(user_input, concept_id)

    # JSON response for frontend usage
    # if request.headers.get("Accept") == "application/json":
    #     return JsonResponse(result)

    if result["message"] == "correct":
        return JsonResponse(
            {"message": "درسته!", "backColor": "#d4edda", "color": "#155724"}
        )
    elif result["message"] == "partially_correct":
        matched_variant = result["matched_variant"]
        return JsonResponse(
            {
                "message": f"درسته.\nالبته احتمالا منظورت <b>{matched_variant}</b> بوده!",
                "backColor": "#d4edda",
                "color": "#155724",
            }
        )
    elif result["message"] == "wrong_concept":
        return JsonResponse(
            {"message": "اشتباهه!", "backColor": "#f8d7da", "color": "#721c24"}
        )
    elif result["message"] == "unknown":
        return JsonResponse(
            {
                "message": "سیستم ما این عبارت رو نمی‌شناسه.\nاگر فکر می‌کنی پاسخت درسته، ما اون رو بررسی می‌کنیم و امتیازش رو بهت می‌دیم.",
                "backColor": "#fff3cd",
                "color": "#856404",
            }
        )
    else:
        return JsonResponse(
            {"message": "خطای ناشناخته", "backColor": "#fff3cd", "color": "#856404"}
        )
