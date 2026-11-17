import json, sys
record = json.load(sys.stdin)
# Previous exporter round-trips extension fields users may depend on.
print(json.dumps(record, sort_keys=True, separators=(",", ":")))
