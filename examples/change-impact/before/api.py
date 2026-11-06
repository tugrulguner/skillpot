def fetch_items(limit=100):
    """Return up to limit items."""
    return query_items(limit)


def query_items(limit):
    return list(range(limit))


def status():
    return "ok"
