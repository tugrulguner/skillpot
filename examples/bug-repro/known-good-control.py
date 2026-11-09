def page(items, limit):
    return items if limit is None else items[:limit]
