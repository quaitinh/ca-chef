"""Server demo Cá Chef: phục vụ giao diện tĩnh + /api/data (dữ liệu từ Google Sheet).

Dùng: CA_CHEF_KEY=/đường/dẫn/key.json python3 app/server.py [cổng]
Không có key hoặc Sheet lỗi thì đọc data/*.csv.
"""
import csv
import re
import json
import os
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC = os.path.join(ROOT, "app", "static")
DATA = os.path.join(ROOT, "data")
DE_XUAT = os.path.join(DATA, "de_xuat")
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


def read_de_xuat(name):
    path = os.path.join(DE_XUAT, name)
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return to_records(list(csv.reader(f)))


def sua_lich_mua(tabs):
    """Đè lịch mùa vụ đã tra cứu có nguồn (de_xuat_sua_sheet.csv, sinh bởi gop_mua_vu.py) lên dòng nguyên liệu
    trên Sheet. Chỉ đè khi Sheet vẫn giữ lịch cũ: chủ dự án tự sửa dòng nào trên Sheet thì giữ theo Sheet."""
    path = os.path.join(DE_XUAT, "de_xuat_sua_sheet.csv")
    if not os.path.exists(path):
        return 0
    with open(path, newline="", encoding="utf-8") as f:  # đọc nguyên chuỗi để giữ số 0 đầu của lịch "000111..."
        sua = {r["ma"]: r for r in csv.DictReader(f) if r["nguon"].strip()}
    n = 0
    for r in tabs["nguyen_lieu"]:
        moi = sua.get(r["ma"])
        if not moi:
            continue
        try:
            hien = "".join(str(int(float(r.get(f"T{i}") or 0))) for i in range(1, 13))
        except ValueError:
            continue
        if hien != moi["lich_tren_sheet"]:
            continue
        for i, v in enumerate(moi["lich_de_xuat"], 1):
            r[f"T{i}"] = int(v)
        r["tin_cay"] = moi["tin_cay_moi"]
        r["ghi_chu"] = moi["ghi_chu"]
        r["nguon"] = moi["nguon"]
        n += 1
    tabs["lich_tra_cuu"] = n
    return n


def tach_nhanh(tabs):
    """Tách nguyên liệu cha thành các nhánh (thịt heo -> ba chỉ, sườn, nạc vai...) theo nhanh_nguyen_lieu.csv.

    Nhánh mang lịch mùa vụ, nhóm (trừ khi khai nhóm riêng) của nguyên liệu cha và thêm cột cha; mac_dinh = 1 là nhánh
    được hiểu khi món chỉ ghi chung mã cha (vd. "thịt heo" là thịt nạc hoặc ba chỉ); bao_gom là các nhánh chặt ra được
    từ nhánh đó (gà nguyên con có cánh, ức, chân cổ, lòng). Dòng định lượng đang mang mã cha thì đổi
    sang mã nhánh đầu tiên có từ khóa khớp tên hiển thị; món có nguyên liệu chính là mã cha thì thay bằng các nhánh
    của dòng "chính" (không khớp nhánh nào thì giữ mã cha).
    """
    path = os.path.join(DE_XUAT, "nhanh_nguyen_lieu.csv")
    if not os.path.exists(path):
        return
    with open(path, newline="", encoding="utf-8") as f:
        nhanh = list(csv.DictReader(f))
    theo_ma = {r["ma"]: r for r in tabs["nguyen_lieu"]}
    for n in nhanh:
        cha = theo_ma.get(n["cha"])
        if cha and n["ma"] not in theo_ma:
            tabs["nguyen_lieu"].append({**cha, "ma": n["ma"], "ten": n["ten"], "cha": n["cha"], "nhom": n.get("nhom") or cha["nhom"],
                                        "mac_dinh": n.get("mac_dinh", ""), "bao_gom": n.get("bao_gom", ""), "ghi_chu": n["ghi_chu"] or cha.get("ghi_chu", "")})
    chinh = {}
    for r in tabs["mon_nguyen_lieu"]:
        ma = str(r.get("ma_nguyen_lieu") or "")
        for n in nhanh:
            if ma == n["cha"] and re.search(n["tu_khoa"], str(r.get("ten_hien_thi") or "").lower()):
                r["ma_nguyen_lieu"] = n["ma"]
                break
        if r.get("vai_tro") == "chinh":
            chinh.setdefault(r["ma_mon"], []).append(r["ma_nguyen_lieu"])
    con = {}
    for n in nhanh:
        con.setdefault(n["cha"], set()).add(n["ma"])
    for m in tabs["mon_an"]:
        ma = [c for c in str(m.get("nguyen_lieu_chinh") or "").split("|") if c]
        moi = []
        for c in ma:
            thay = [x for x in chinh.get(m["ma_mon"], []) if x in con.get(c, ())]
            moi += thay or [c]
        m["nguyen_lieu_chinh"] = "|".join(dict.fromkeys(moi))


def merge_de_xuat(tabs):
    """Gộp món đề xuất (data/de_xuat/) vào dữ liệu Sheet/CSV và ẩn các món trong an_mon.csv.

    Món/nguyên liệu đã có trên Sheet (trùng mã) thì giữ bản trên Sheet.
    """
    an = {r["ma_mon"] for r in read_de_xuat("an_mon.csv")}
    sua_lich_mua(tabs)
    # Món chủ nhà đổi sang công thức khác (de_len_sheet.csv, sinh từ lo4_chu_nha.py): bỏ bản Sheet để lấy bản đề xuất.
    de = {r["ma_mon"] for r in read_de_xuat("de_len_sheet.csv")} if os.path.exists(os.path.join(DE_XUAT, "de_len_sheet.csv")) else set()
    tabs["mon_an"] = [r for r in tabs["mon_an"] if r["ma_mon"] not in de]
    tabs["mon_nguyen_lieu"] = [r for r in tabs["mon_nguyen_lieu"] if r["ma_mon"] not in de]
    co_nl = {r["ma"] for r in tabs["nguyen_lieu"]}
    tabs["nguyen_lieu"] += [r for r in read_de_xuat("nguyen_lieu_moi.csv") if r["ma"] not in co_nl]
    co_mon = {r["ma_mon"] for r in tabs["mon_an"]}
    moi = [r for r in read_de_xuat("mon_an_moi.csv") if r["ma_mon"] not in co_mon]
    them = {r["ma_mon"] for r in moi}
    tabs["mon_an"] = [r for r in tabs["mon_an"] + moi if r["ma_mon"] not in an]
    tabs["mon_nguyen_lieu"] = [r for r in tabs["mon_nguyen_lieu"] if r["ma_mon"] not in an] + \
        [r for r in read_de_xuat("mon_nguyen_lieu_moi.csv") if r["ma_mon"] in them]
    tabs.setdefault("mon_nhan", [r for r in read_de_xuat("mon_nhan.csv") if r["ma_mon"] not in an])
    tach_nhanh(tabs)
    # Ảnh món: mã ảnh trên CDN Cookpad (lay_anh.py). Đọc nguyên chuỗi: mã hex như "8e12…" không được đổi thành số.
    path = os.path.join(DE_XUAT, "anh_mon.csv")
    if "anh_mon" not in tabs and os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            tabs["anh_mon"] = list(csv.DictReader(f))
    # Bí quyết chọn và bảo quản nguyên liệu (bi_quyet.py): mat/da là số ngày để ngon ở ngăn mát/ngăn đá.
    path = os.path.join(DE_XUAT, "bi_quyet_nl.csv")
    if "bi_quyet" not in tabs and os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            tabs["bi_quyet"] = list(csv.DictReader(f))
    return len(moi)


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
    de_xuat = merge_de_xuat(tabs)
    payload = json.dumps({"source": source, "error": error, "fetched_at": time.strftime("%H:%M %d/%m/%Y"),
                          "de_xuat": de_xuat, **tabs}, ensure_ascii=False).encode()
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
