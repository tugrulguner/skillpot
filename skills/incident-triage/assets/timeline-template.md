# Incident timeline

Use one row per evidenced event or collection/notification action. Preserve source timestamps verbatim, including precision and timezone; never normalize an unknown clock into guessed UTC.

| ID | Source ID/locator | Timestamp as recorded | Precision/timezone/clock | Kind: event, collection, notification | Event or bounded interval | Ordering relation / uncertainty |
|---|---|---|---|---|---|---|

## Ordering notes
- State clock offsets, unknown clocks and partial orders explicitly; do not impose an order without evidence.
- Concurrent log/trace spans do not by themselves establish causal relation.
- Missing, truncated, mixed-generation or changing records are gaps, not timeline events.
- Link every event to inspected source evidence. Do not invent events to fill silence.
