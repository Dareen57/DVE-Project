def parse_search_query(query: str):
    """
    Example query: 'Brooklyn 2022 Monday 5 killed'
    Returns a dictionary to map to dropdown values
    """
    query = query.lower()
    result = {
        "borough": None,
        "year": None,
        "month": None,
        "weekday": None,
        "hour": None,
        "metric": None
    }

    # Simple matching rules
    boroughs = ["manhattan", "brooklyn", "queens", "bronx", "staten island"]
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    metrics = {
        "persons killed": "NUMBER_OF_PERSONS_KILLED",
        "pedestrians injured": "NUMBER_OF_PEDESTRIANS_INJURED",
        "cyclists killed": "NUMBER_OF_CYCLIST_KILLED",
        "motorists killed": "NUMBER_OF_MOTORIST_KILLED",
    }

    # Extract borough
    for b in boroughs:
        if b in query:
            result["borough"] = b.title()
            break

    # Extract weekday
    for w in weekdays:
        if w in query:
            result["weekday"] = w.title()
            break

    # Extract year
    import re
    year_match = re.search(r"\b(20\d{2})\b", query)
    if year_match:
        result["year"] = int(year_match.group(1))

    # Extract hour (0-23)
    hour_match = re.search(r"\b([0-9]|1[0-9]|2[0-3])\b", query)
    if hour_match:
        result["hour"] = int(hour_match.group(1))

    # Extract metric
    for key in metrics.keys():
        if key in query:
            result["metric"] = metrics[key]
            break

    # Month (optional) using 1-12
    month_match = re.search(r"\b(1[0-2]|[1-9])\b", query)
    if month_match:
        result["month"] = int(month_match.group(1))

    return result
