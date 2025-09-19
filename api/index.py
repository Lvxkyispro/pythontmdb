from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "ok": True,
            "routes": [
                "/api/anime/by-tmdb/<tmdb_id>?type=tv",
                "/api/anime/by-tmdb/<tmdb_id>?type=movie"
            ],
            "notes": [
                "Uses TMDb API directly",
                "Append '?type=tv' for anime series, '?type=movie' for anime films",
                "Response includes titles, overview, episodes, genres, credits, images, external ids"
            ]
        }
        
        self.wfile.write(json.dumps(response).encode())
        return
