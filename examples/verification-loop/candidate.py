import json, sys
record = json.load(sys.stdin)
# Candidate change: export only the documented core fields (regression: drops extensions).
print(json.dumps({key: record[key] for key in ("id", "name", "enabled")}, sort_keys=True, separators=(",", ":")))
