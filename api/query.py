import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Allow all CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load static data once
try:
    with open("api/static_data.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)["samples"]
except Exception as e:
    print("❌ Failed to load static_data.json:", e)
    raw_data = []

# Normalize keys to expected lowercase for frontend re-mapping
def normalize(sample):
    return {
        "title": sample.get("TITLE") or sample.get("title"),
        "youtube_url": sample.get("YOUTUBE_URL") or sample.get("youtube_url"),
        "start_time": sample.get("START_TIME") or sample.get("start_time"),
        "end_time": sample.get("END_TIME") or sample.get("end_time"),
        "sample_type": sample.get("SAMPLE_TYPE") or sample.get("sample_type"),
        "description": sample.get("DESCRIPTION") or sample.get("description"),
        "genre": sample.get("GENRE") or sample.get("genre"),
        "decade": sample.get("DECADE") or sample.get("decade"),
        "start_seconds": sample.get("START_SECONDS") or sample.get("start_seconds"),
        "end_seconds": sample.get("END_SECONDS") or sample.get("end_seconds"),
        "duration": sample.get("DURATION") or sample.get("duration"),
        "chatgpt_prompt": sample.get("CHATGPT_PROMPT") or sample.get("chatgpt_prompt"),
        "query_used": sample.get("QUERY_USED") or sample.get("query_used"),
        "timestamp_loaded": sample.get("TIMESTAMP_LOADED") or sample.get("timestamp_loaded"),
        "youtube_rank": sample.get("YOUTUBE_RANK") or sample.get("youtube_rank"),
    }

@app.get("/api/query.py")
async def get_samples(prompt_filter: str = Query(default=None)):
    try:
        if prompt_filter:
            filtered = [
                normalize(sample)
                for sample in raw_data
                if prompt_filter.lower() in (sample.get("QUERY_USED") or "").lower()
            ]
            return JSONResponse(content={"samples": filtered})

        # Return all normalized samples
        normalized = [normalize(sample) for sample in raw_data]
        return JSONResponse(content={"samples": normalized})
    except Exception as e:
        print("❌ API error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})