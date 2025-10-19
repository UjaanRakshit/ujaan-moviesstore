def calculate_cart_total(cart, movies_in_cart):
    total = 0
    for movie in movies_in_cart:
        quantity = cart[str(movie.id)]
        total += movie.price * int(quantity)
    return total


# Minimal ISO2 to ISO3 mapping for common countries
ISO2_TO_ISO3 = {
    'US': 'USA', 'CA': 'CAN', 'GB': 'GBR', 'UK': 'GBR', 'IN': 'IND', 'AU': 'AUS',
    'DE': 'DEU', 'FR': 'FRA', 'BR': 'BRA', 'JP': 'JPN', 'CN': 'CHN', 'MX': 'MEX',
    'ES': 'ESP', 'IT': 'ITA', 'KR': 'KOR'
}


def iso2_to_iso3(code2: str | None) -> str | None:
    if not code2:
        return None
    return ISO2_TO_ISO3.get(code2.upper())


def derive_region_code(request) -> str | None:
    """
    Determine the best region code (ISO A3) for this request.
    Priority: query ?region= -> session preferred_region_code -> Accept-Language country -> None
    """
    # 1) Query param
    region_from_query = (request.GET.get('region') or '').strip().upper()
    if region_from_query:
        # If someone passed ISO2, try to map to ISO3
        if len(region_from_query) == 2:
            mapped = iso2_to_iso3(region_from_query)
            return (mapped or region_from_query).upper()
        return region_from_query[:3].upper()

    # 2) Session
    preferred = (request.session.get('preferred_region_code') or '').strip().upper()
    if preferred:
        if len(preferred) == 2:
            mapped = iso2_to_iso3(preferred)
            return (mapped or preferred).upper()
        return preferred[:3].upper()

    # 3) Accept-Language header e.g., 'en-US,en;q=0.9'
    lang = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if lang:
        # take the first token and extract country portion
        first = lang.split(',')[0]
        if '-' in first:
            parts = first.split('-')
            if len(parts) >= 2:
                country2 = parts[-1].upper()
                mapped = iso2_to_iso3(country2)
                if mapped:
                    return mapped.upper()
                # Fallback to 2-letter if unknown
                return country2.upper()
    return None