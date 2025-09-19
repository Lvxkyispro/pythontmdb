from http.server import BaseHTTPRequestHandler
import json
import os
import requests
from urllib.parse import urlparse, parse_qs

# Set your TMDB API key directly here
TMDB_KEY = "8452fead25d0dd27fd24c19fefdde496"  # Replace with your actual key
TMDB_BASE = "https://api.themoviedb.org/3"

def fetch_tmdb(tmdb_id: int, media_type: str = "tv"):
    url = f"{TMDB_BASE}/{media_type}/{tmdb_id}"
    params = {
        "api_key": TMDB_KEY,
        "language": "en-US",
        "append_to_response": "credits,images,external_ids"
    }
    r = requests.get(url, params=params, timeout=15)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # Get media type from query params (default to tv)
        media_type = query_params.get('type', ['tv'])[0]
        if media_type not in ("tv", "movie"):
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "type must be tv or movie"
            }).encode())
            return
        
        try:
            # Extract TMDB ID from path (the filename is [tmdb_id].py)
            tmdb_id = int(os.path.basename(__file__).replace('.py', ''))
            
            # Fetch data from TMDb
            data = fetch_tmdb(tmdb_id, media_type=media_type)
            if not data:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "matched": False, 
                    "message": "No TMDb match found"
                }).encode())
                return
            
            # Return successful response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "matched": True,
                "tmdb_id": tmdb_id,
                "tmdb_type": media_type,
                "tmdb_data": data
            }).encode())
            
        except ValueError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Invalid TMDB ID format"
            }).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": f"Internal server error: {str(e)}"
            }).encode())
