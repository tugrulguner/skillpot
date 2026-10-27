from pydantic import BaseModel, Field
from summonpot import Exactly, FromRequest, Operation, Required, Summon


class QuoteRequest(BaseModel):
    customer: str = Field(min_length=2)
    hours: int = Field(gt=0, le=40)


class InvoiceQuote(BaseModel):
    customer: str
    amount_cents: int


capability_calls: list[tuple[str, int]] = []


def calculate_quote(customer: str, hours: int) -> InvoiceQuote:
    capability_calls.append((customer, hours))
    return InvoiceQuote(customer=customer, amount_cents=hours * 12_500)


quote_operation = Operation(
    calculate_quote,
    bind={"customer": FromRequest("customer"), "hours": FromRequest("hours")},
    output=InvoiceQuote,
)
summon = Summon("invoice-quote")


@summon("/quote")
def quote(
    request: QuoteRequest,
    result=Required(quote_operation, calls=Exactly(1)),
) -> InvoiceQuote:
    """Calculate the fixed hourly invoice quotation."""
    ...
