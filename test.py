import json
with open("api/static_data.json", "r") as f:
    data = json.load(f)
print("✅ JSON is valid, loaded", len(data["samples"]), "samples")