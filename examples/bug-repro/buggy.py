def page(items, limit):
    return items[:limit] if limit else items
