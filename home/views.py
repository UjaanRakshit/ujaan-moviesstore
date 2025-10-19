from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from cart.models import Item, Order
from cart.utils import iso2_to_iso3
def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {
        'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request,
                  'home/about.html',
                  {'template_data': template_data})

def local_popularity_map(request):
    template_data = {}
    template_data['title'] = 'Local Popularity Map'
    template_data['preferred_region'] = request.session.get('preferred_region_code')
    # No precomputed popularity; the frontend will fetch via API
    country_popularity = {}

    # Pass empty seed; template JS will hydrate via /api/region-popularity
    return render(request,
                  'home/local_popularity_map.html',
                  {
                      'template_data': template_data,
                      'country_popularity': country_popularity,
                  })


@require_http_methods(["GET"])
def api_region_popularity(request):
    """
    Returns purchase popularity per region as a mapping of ISO A3 code -> total quantity purchased.
    """
    qs = (
        Item.objects
        .filter(order__region_code__isnull=False)
        .values("order__region_code")
        .annotate(total=Sum("quantity"))
        .order_by()
    )
    data = {(row["order__region_code"] or "").upper(): row["total"] for row in qs}
    return JsonResponse({"regions": data})


@require_http_methods(["GET"])
def api_region_top(request, region_code: str):
    """
    Returns top movies for a given region code with aggregated purchase counts.
    Query param: limit (default 5)
    """
    try:
        limit = int(request.GET.get("limit", 5))
    except ValueError:
        limit = 5

    rc = (region_code or "").upper()
    qs = (
        Item.objects
        .filter(order__region_code=rc)
        .values("movie__id", "movie__name")
        .annotate(total=Sum("quantity"))
        .order_by("-total", "movie__name")[:limit]
    )
    top = [
        {"movie_id": row["movie__id"], "title": row["movie__name"], "count": row["total"]}
        for row in qs
    ]
    return JsonResponse({"region": rc, "top": top})


@csrf_exempt
@require_http_methods(["POST"])
def api_set_region(request):
    """
    Sets the preferred region code (ISO A3) into session for tagging future purchases.
    Body: {"region_code": "USA"}
    """
    try:
        import json
        payload = json.loads(request.body or b"{}")
        raw = (payload.get("region_code") or "").strip()
        if not raw:
            return JsonResponse({"success": False, "message": "region_code is required"}, status=400)
        raw_up = raw.upper()
        region = None
        # Accept ISO3 directly
        if len(raw_up) == 3 and raw_up.isalpha():
            region = raw_up
        # Map ISO2 to ISO3
        elif len(raw_up) == 2 and raw_up.isalpha():
            mapped = iso2_to_iso3(raw_up)
            region = (mapped or raw_up).upper()
        # Reject full country names instead of truncating
        if not region or len(region) != 3:
            return JsonResponse({"success": False, "message": "region_code must be ISO2 or ISO3"}, status=400)
        request.session["preferred_region_code"] = region
        return JsonResponse({"success": True, "region_code": region})
    except Exception:
        return JsonResponse({"success": False, "message": "Invalid payload"}, status=400)