import pandas as pd
import json

# Load the CSV
df = pd.read_csv("2025-04-21 2_49pm.csv")

# Clean: replace NaN with None explicitly
df = df.replace({pd.NA: None, pd.NaT: None, float('nan'): None, 'nan': None})

# Timestamp formatting if needed
if "TIMESTAMP_LOADED" in df.columns:
    df["TIMESTAMP_LOADED"] = pd.to_datetime(df["TIMESTAMP_LOADED"], errors='coerce').astype(str)

# Convert to dict structure
data = {"samples": df.to_dict(orient="records")}

# Save to JSON
with open("static_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ static_data.json created with all NaNs cleaned.")