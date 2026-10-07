"""Server demo Cá Chef: phục vụ giao diện tĩnh + /api/data (dữ liệu từ Google Sheet).

Dùng: CA_CHEF_KEY=/đường/dẫn/key.json python3 app/server.py [cổng]
Không có key hoặc Sheet lỗi thì đọc data/*.csv.
"""
import csv
import json
import os
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC = os.path.join(ROOT, "app", "static")
DATA = os.path.join(ROOT, "data")
SHEET_ID = "1aoGQLY0g3UjnQRavXnufttwoigSb-Po4IkGB1z0fwno"
TABS = ["nguyen_lieu", "mon_an", "mon_nguyen_lieu", "quy_tac", "gia_go"]
CACHE_SECONDS = 300

_cache = {"at": 0, "payload": None}


def cast(v):
    for conv in (int, float):
        try:
            return conv(v)
        except ValueError:
            pass
    return v


def to_records(rows):
    header, *body = rows
    return [{h: cast(v) for h, v in zip(header, r)} for r in body if any(r)]


def load_sheet():
    import gspread
    sh = gspread.service_account(filename=os.environ["CA_CHEF_KEY"]).open_by_key(SHEET_ID)
    ranges = sh.values_batch_get(TABS)["valueRanges"]
    return {tab: to_records(r.get("values", [[]])) for tab, r in zip(TABS, ranges)}


def load_csv():
    out = {}
    for tab in TABS:
        with open(os.path.join(DATA, f"{tab}.csv"), newline="") as f:
            out[tab] = to_records(list(csv.reader(f)))
    return out


def get_data(refresh=False):
    if not refresh and _cache["payload"] and time.time() - _cache["at"] < CACHE_SECONDS:
        return _cache["payload"]
    source, error = "csv", None
    if os.environ.get("CA_CHEF_KEY"):
        try:
            tabs, source = load_sheet(), "sheet"
        except Exception as e:  # Sheet lỗi mạng/quyền -> vẫn chạy được bằng CSV
            error = str(e)
            tabs = load_csv()
    else:
        tabs = load_csv()
    payload = json.dumps({"source": source, "error": error, "fetched_at": time.strftime("%H:%M %d/%m/%Y"),
                          **tabs}, ensure_ascii=False).encode()
    _cache.update(at=time.time(), payload=payload)
    return payload


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=STATIC, **kw)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path in ("/api/data", "/data.json"):
            body = get_data(refresh="refresh" in parse_qs(url.query))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8095
    print(f"Cá Chef đang chạy: http://127.0.0.1:{port}  (nguồn dữ liệu: {'Sheet' if os.environ.get('CA_CHEF_KEY') else 'CSV'})")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
