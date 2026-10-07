"""Đẩy data/*.csv lên Google Sheet Cá Chef (mỗi CSV một tab, ghi đè).

Dùng: python3 scripts/push_sheets.py <đường-dẫn-key.json> [tab ...]
"""
import csv
import os
import sys

import gspread

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SHEET_ID = "1aoGQLY0g3UjnQRavXnufttwoigSb-Po4IkGB1z0fwno"
TABS = ["huong_dan", "nguyen_lieu", "mon_an", "mon_nguyen_lieu", "quy_tac", "gia_go"]


def cast(v):
    """Giữ số là số để Google Sheets tính toán được."""
    for conv in (int, float):
        try:
            return conv(v)
        except ValueError:
            pass
    return v


def main():
    key, tabs = sys.argv[1], sys.argv[2:] or TABS
    sh = gspread.service_account(filename=key).open_by_key(SHEET_ID)
    existing = {ws.title: ws for ws in sh.worksheets()}
    for tab in tabs:
        with open(os.path.join(DATA, f"{tab}.csv"), newline="") as f:
            rows = [[cast(v) for v in r] for r in csv.reader(f)]
        ws = existing.get(tab) or sh.add_worksheet(tab, rows=max(len(rows), 50), cols=max(len(rows[0]), 10))
        ws.clear()
        ws.update(rows, "A1", value_input_option="RAW")
        ws.format("1:1", {"textFormat": {"bold": True}, "backgroundColor": {"red": 1, "green": 0.9, "blue": 0.6}})
        ws.freeze(rows=1)
        print(f"{tab}: {len(rows) - 1} dòng")
    # Tab mặc định "Sheet1"/"Trang tính1" để trống thì xoá cho gọn.
    for title, ws in existing.items():
        if title not in TABS and not any(ws.get_all_values()):
            sh.del_worksheet(ws)
            print(f"Đã xoá tab trống: {title}")


if __name__ == "__main__":
    main()
