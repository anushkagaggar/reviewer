def normalize_item(item, default_title="Observation"):
    """
    Convert strings/dicts into standard ReviewItem format
    """

    # Case 1: Already a string
    if isinstance(item, str):
        return {
            "title": default_title,
            "description": item,
            "impact": None,
            "suggestion": None
        }

    # Case 2: Dict-like object
    if isinstance(item, dict):

        title = (
            item.get("title")
            or item.get("assumption")
            or item.get("information")
            or item.get("issue")
            or default_title
        )

        description = (
            item.get("description")
            or item.get("impact")
            or item.get("evaluation")
            or item.get("reasoning")
            or ""
        )

        impact = item.get("impact")
        suggestion = item.get("suggestion") or item.get("fix")

        return {
            "title": title,
            "description": description,
            "impact": impact,
            "suggestion": suggestion
        }

    # Fallback
    return {
        "title": default_title,
        "description": str(item),
        "impact": None,
        "suggestion": None
    }


def normalize_list(items, default_title):
    if not isinstance(items, list):
        return []

    return [
        normalize_item(item, default_title)
        for item in items
    ]
