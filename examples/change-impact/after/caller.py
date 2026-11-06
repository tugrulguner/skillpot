from api import fetch_items


def load():
    return fetch_items(limit=25)
