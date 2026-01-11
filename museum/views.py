from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import ArtObject

def object_list(request):
    q = (request.GET.get("q") or "").strip()
    per_page = request.GET.get("per_page", "12")

    FILTER_FIELDS = {
        "objectName": "Tip obiect",
        "medium": "Material / Tehnică",
        "classification": "Clasificare",
    }

    # citim ce a ales user
    filter_field = (request.GET.get("filter_field") or "").strip()
    filter_value = (request.GET.get("filter_value") or "").strip()

    # securitate: dacă cineva trimite alt câmp în URL, îl ignorăm
    if filter_field not in FILTER_FIELDS:
        filter_field = ""
        filter_value = ""

    try:
        per_page = max(1, min(100, int(per_page)))
    except ValueError:
        per_page = 12

    qs = ArtObject.objects.all().order_by("id")

    # daca a ales, filtreaza rezultatele
    if filter_field and filter_value:
        qs = qs.filter(**{f"data__{filter_field}": filter_value})

    if q:
        qs = qs.filter(
            Q(data__title__icontains=q) |
            Q(data__artistDisplayName__icontains=q) |
            Q(data__department__icontains=q) |
            Q(data__classification__icontains=q) |
            Q(data__culture__icontains=q) |
            Q(data__objectName__icontains=q) |
            Q(data__medium__icontains=q)
        )

    # valori posibile pentru al doilea dropdown in funcție de camp
    filter_values = []
    if filter_field:
        filter_values = (
            ArtObject.objects
            .exclude(**{f"data__{filter_field}__isnull": True})
            .exclude(**{f"data__{filter_field}": ""})
            .values_list(f"data__{filter_field}", flat=True)
            .distinct()
            .order_by(f"data__{filter_field}")
        )
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "museum/object_list.html", {
        "page_obj": page_obj,
        "q": q,
        "per_page": per_page,
        "FILTER_FIELDS": FILTER_FIELDS,
        "filter_field": filter_field,
        "filter_value": filter_value,
        "filter_values": filter_values,
    })
def object_detail(request, pk):
    obj = get_object_or_404(ArtObject, pk=pk)

    # afisam pagina
    return render(request, "museum/object_detail.html", {"obj": obj})
