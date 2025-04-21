import pandas as pd
import json

# Load the CSV
df = pd.read_csv("2025-04-21 2_49pm.csv")

# Optional: format timestamp column (if present)
if "timestamp_loaded" in df.columns:
    df["timestamp_loaded"] = pd.to_datetime(df["timestamp_loaded"]).astype(str)

# Convert to dictionary structure expected by your app
data = {"samples": df.to_dict(orient="records")}

# Save as JSON
with open("static_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ static_data.json created!")

