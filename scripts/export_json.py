"""Xuất dữ liệu ra app/static/data.json (+ version.json: mã phiên bản) cho bản chạy tĩnh (GitHub Pages).

Có biến môi trường CA_CHEF_KEY thì đọc Google Sheet, không thì đọc data/*.csv.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app"))
from server import STATIC, get_data  # noqa: E402

payload = get_data(refresh=True)
with open(os.path.join(STATIC, "data.json"), "wb") as f:
    f.write(payload)
# Mã phiên bản theo nội dung (bỏ giờ lấy dữ liệu): app tải data.json?v=<mã>, dữ liệu không đổi thì dùng lại bản đã lưu.
d = json.loads(payload)
d.pop("fetched_at", None)
v = hashlib.sha1(json.dumps(d, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]
with open(os.path.join(STATIC, "version.json"), "w") as f:
    json.dump({"v": v}, f)
print(f"Đã ghi data.json ({len(payload) // 1024} KB), phiên bản {v}")
