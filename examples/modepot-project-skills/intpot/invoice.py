from intpot import App
app = App('invoice')
@app.tool()
def quote(quantity: int, unit_price_cents: int, discount_cents: int = 0) -> int:
    """Calculate an invoice total in cents; reject invalid amounts."""
    if quantity <= 0 or unit_price_cents < 0 or discount_cents < 0:
        raise ValueError('amounts must be positive quantity and nonnegative cents')
    subtotal = quantity * unit_price_cents
    if discount_cents > subtotal:
        raise ValueError('discount exceeds subtotal')
    return subtotal - discount_cents

