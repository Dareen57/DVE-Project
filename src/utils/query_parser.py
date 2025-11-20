# utils/query_parser.py

import re

BOROUGHS = ["MANHATTAN", "BROOKLYN", "QUEENS", "BRONX", "STATEN ISLAND"]

INJURY_KEYWORDS = {
    "pedestrian": "PEDESTRIAN",     # map to your actual column values
    "cyclist": "BICYCLE",
    "bicycle": "BICYCLE",
    "motorist": "MOTORIST",
}

VEHICLE_KEYWORDS = {
    "suv": "SPORT UTILITY / STATION WAGON",
    "truck": "TRUCK",
    "taxi": "TAXI",
    "bus": "BUS",
}

def parse_query_to_filters(query: str) -> dict:
    """
    Turn a free-text query into filter values that match your dropdowns.
    """
    if not query:
        return {}

    q = query.lower()
    filters = {}

    # Borough detection
    for b in BOROUGHS:
        if b.lower() in q:
            filters["borough"] = b
            break

    # Year (any 4-digit from 2012–2025)
    years = re.findall(r"\b(201[2-9]|202[0-5])\b", q)
    if years:
        filters["year"] = int(years[0])

    # Injury type / person type from keywords
    for kw, val in INJURY_KEYWORDS.items():
        if kw in q:
            filters["injury_type"] = val
            break

    # Vehicle type from keywords
    for kw, val in VEHICLE_KEYWORDS.items():
        if kw in q:
            filters["vehicle_type"] = val
            break

    # You can add contributing factor, severity, etc. with similar mappings

    return filters
