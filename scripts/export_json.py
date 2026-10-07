"""Xuất dữ liệu ra app/static/data.json cho bản chạy tĩnh (GitHub Pages).

Có biến môi trường CA_CHEF_KEY thì đọc Google Sheet, không thì đọc data/*.csv.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app"))
from server import STATIC, get_data  # noqa: E402

payload = get_data(refresh=True)
with open(os.path.join(STATIC, "data.json"), "wb") as f:
    f.write(payload)
print(f"Đã ghi data.json ({len(payload) // 1024} KB)")
