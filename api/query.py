import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load static data safely on startup
try:
    with open("api/static_data.json", "r", encoding="utf-8") as f:
        static_samples = json.load(f)
except Exception as e:
    print("❌ Failed to load static_data.json:", e)
    static_samples = {"samples": []}

@app.get("/api/query.py")
async def get_samples(prompt_filter: str = Query(default=None)):
    try:
        if prompt_filter:
            filtered = [
                s for s in static_samples["samples"]
                if prompt_filter.lower() in (s.get("QUERY_USED") or "").lower()
            ]
            return JSONResponse(content={"samples": filtered})
        return JSONResponse(content=static_samples)
    except Exception as e:
        print("❌ Error serving data:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})