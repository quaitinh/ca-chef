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
# Danh mục Món Ngon Mỗi Ngày cho trang duyệt món (tải riêng khi mở trang, không làm nặng data.json).
import csv  # noqa: E402
dm = os.path.join(os.path.dirname(STATIC), "..", "data", "de_xuat", "mnmn_danh_muc.csv")
if os.path.exists(dm):
    rows = [{k: v for k, v in r.items() if v} for r in csv.DictReader(open(dm, newline="", encoding="utf-8"))]
    with open(os.path.join(STATIC, "mnmn.json"), "w", encoding="utf-8") as f:
        json.dump({"v": v, "mon": rows}, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Đã ghi mnmn.json ({len(rows)} món)")
print(f"Đã ghi data.json ({len(payload) // 1024} KB), phiên bản {v}")
