import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load static data once
with open("static_data.json") as f:
    static_samples = json.load(f)

@app.get("/api/query.py")
async def get_samples(prompt_filter: str = None):
    if prompt_filter:
        filtered = [
            s for s in static_samples["samples"]
            if prompt_filter.lower() in s.get("query_used", "").lower()
        ]
        return JSONResponse(content={"samples": filtered})
    return JSONResponse(content=static_samples)