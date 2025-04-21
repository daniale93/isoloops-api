from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from snowflake_api import query_snowflake
import json

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        try:
            query_components = parse_qs(urlparse(self.path).query)
            prompt_filter = query_components.get("prompt_filter", [None])[0]

            base_sql = """
                SELECT
                    title,
                    youtube_url,
                    start_time,
                    end_time,
                    sample_type,
                    description,
                    genre,
                    decade,
                    start_seconds,
                    end_seconds,
                    duration,
                    video_duration,
                    view_count,
                    like_count,
                    comment_count,
                    resolution,
                    chatgpt_prompt
                FROM SAMPLED_SONGS_ENRICHED
            """

            if prompt_filter:
                # Sanitize single quotes for Snowflake safety
                prompt_filter_safe = prompt_filter.replace("'", "''")
                base_sql += f" WHERE chatgpt_prompt = '{prompt_filter_safe}'"

            results = query_snowflake(base_sql)

            columns = [
                "title", "youtube_url", "start_time", "end_time", "sample_type",
                "description", "genre", "decade", "start_seconds", "end_seconds", "duration",
                "video_duration", "view_count", "like_count", "comment_count", "resolution",
                "chatgpt_prompt"
            ]
            data = [dict(zip(columns, row)) for row in results]

            self._set_headers()
            self.wfile.write(json.dumps({"samples": data}, indent=2).encode())

        except Exception as e:
            self._set_headers(status=500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())