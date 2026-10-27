"""Typed quote contracts; the response must not expose the internal field."""
import sys
import msgspec
from dexpot import Dex


class QuoteIn(msgspec.Struct):
    customer: str
    amount: float


class QuoteOut(msgspec.Struct):
    quote_id: int
    customer: str
    amount: float


app = Dex()


@app.post("/quotes", body=QuoteIn, response=QuoteOut)
def quote(payload: QuoteIn) -> dict:
    return {"quote_id": 41, "customer": payload.customer, "amount": payload.amount,
            "internal_note": "must-not-leak"}


@app.get("/quotes/{quote_id}", response=QuoteOut)
def get_quote(quote_id: int) -> QuoteOut:
    return QuoteOut(quote_id, "Ari", 25.5)


if __name__ == "__main__":
    app.serve(host="127.0.0.1", port=int(sys.argv[1]))
