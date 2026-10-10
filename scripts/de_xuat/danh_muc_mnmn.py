"""Danh mục món Món Ngon Mỗi Ngày để chủ nhà duyệt tay (trang #/duyet-mon) – chỉ tên, link, ảnh, nhóm, thời gian,
khẩu phần, tên nguyên liệu; không lấy cách làm. Món được duyệt mới đưa vào app (cách làm viết lại, gắn nhãn tay).

Vào : JSONL lấy từ trang công khai (mỗi dòng: url, ten, anh, thoi_gian, khau_phan, nl[], tu_khoa) – để ngoài kho.
Ra  : data/de_xuat/mnmn_danh_muc.csv (export_json.py xuất thành app/static/mnmn.json, tải khi mở trang duyệt).
Nhóm đoán theo tên món – chỉ để lọc khi duyệt, không dùng ghép bữa.

Dùng: python3 scripts/de_xuat/danh_muc_mnmn.py <file JSONL>
"""
import csv
import json
import os
import re
import sys
import unicodedata

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "de_xuat")
THIT = r"thịt|bò|gà|heo|lợn|tôm|cá|mực|sườn|trứng|ba chỉ|ba rọi|vịt|cua|ghẹ|nghêu|sò|ốc|lươn|ếch|chả|giò|xương|tim|gan|lòng"
RAU = r"^(rau|cải|bông|hoa|đậu|bí|mướp|su su|su hào|măng|nấm|khổ qua|bầu|giá|cà tím|đọt|ngọn|mồng tơi|dền|bắp cải|súp lơ|bông cải|cà rốt|khoai|củ|cần|ngó|đậu bắp|dưa|kim chi|cà pháo)"
NHOM = [
    ("chay", r"(^|\s)chay(\s|$)"),
    ("do_uong", r"^(trà|nước|sinh tố|smoothie|sữa|soda|cà phê|cacao|ca cao|matcha|yaourt|mojito|punch|cocktail|latte)"),
    ("banh_che", r"^(bánh(?! (canh|mì|cuốn|xèo|hỏi|tráng|bột lọc|ướt|đa|khọt))|chè|kem|pudding|thạch|rau câu|flan|mousse|cookie|pancake|tàu hũ|sữa chua|mứt|xôi chè|cupcake|brulee|tart|waffle|panna)"),
    ("au", r"pasta|spaghetti|pizza|steak|bít tết|sandwich|hamburger|burger|mì ý|nui|sushi|kimbap|tokbokki|lasagna|risotto|taco|gratin|bento|salad|sốt kem|phô mai|cheese|teriyaki"),
    ("lau", r"^lẩu"),
    ("canh", r"^(canh|súp|soup)"),
    ("mot_to", r"^(bún|phở|mì|miến|hủ tiếu|hủ tíu|cháo|xôi|cơm|bánh canh|cao lầu|mì quảng|bánh đa|bánh cuốn|bánh xèo|bánh mì|nui)"),
    ("goi", r"^(gỏi|nộm)"),
]


def nhom(ten, tu_khoa):
    t = ten.lower()
    for n, re_ in NHOM:
        if re.search(re_, t) or (n == "chay" and re.search(r"(^|,\s*)(món )?chay", tu_khoa.lower())):
            return n
    if re.search(RAU, t) and not re.search(THIT, t.split(" xào ")[0].split(" luộc ")[0]):
        return "rau"
    return "man"


def plain(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode().replace("đ", "d")).strip()


def phut(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?", iso or "")
    return int(m[1] or 0) * 60 + int(m[2] or 0) if m and (m[1] or m[2]) else ""


def ten_nl(s):
    s = re.sub(r"\s{2,}.*$", "", s)  # "Thịt ba chỉ   300g" -> "Thịt ba chỉ"
    s = re.sub(r"\s*\d.*$", "", s).strip(" ,.-:")
    return "" if not s or s.isupper() or re.match(r"^(gia vị|ăn kèm|nguyên liệu|sốt|nước chấm|phần)\b", s.lower()) else s


def main(src):
    goc = os.path.join(OUT, "..", "..")
    # Món đã có trong app: theo link nguồn hoặc trùng tên.
    co_url, co_ten = set(), {}
    for f in ("cong_thuc_that_nguon.csv",):
        for r in csv.DictReader(open(os.path.join(OUT, f), newline="", encoding="utf-8")):
            co_url.add(r["url"].rstrip("/"))
    data_json = os.path.join(goc, "app", "static", "data.json")
    if os.path.exists(data_json):
        for m in json.load(open(data_json))["mon_an"]:
            co_ten[plain(m["ten_mon"])] = m["ma_mon"]
            co_url.add(str(m.get("nguon") or "").rstrip("/"))
    rows, seen = [], set()
    for line in open(src, encoding="utf-8"):
        r = json.loads(line)
        if not r.get("ten") or r.get("loi") == "tai" or r["url"] in seen:
            continue
        seen.add(r["url"])
        slug = r["url"].rstrip("/").rsplit("/", 1)[-1]
        r["ten"] = re.sub(r"\s*[-–|]\s*Món Ngon Mỗi Ngày\s*$", "", r["ten"]).strip()
        nl = [x for x in dict.fromkeys(ten_nl(x) for x in r.get("nl", [])) if x]
        trong = co_ten.get(plain(r["ten"]), "") or ("co" if r["url"].rstrip("/") in co_url else "")
        rows.append([slug, r["ten"], r["url"], r.get("anh", ""), nhom(r["ten"], r.get("tu_khoa", "")), phut(r.get("thoi_gian")),
                     r.get("khau_phan", ""), "|".join(nl[:12]), trong, "" if r.get("co_buoc", True) else "thieu_buoc"])
    rows.sort(key=lambda x: plain(x[1]))
    with open(os.path.join(OUT, "mnmn_danh_muc.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["ma", "ten", "url", "anh", "nhom", "phut", "khau_phan", "nguyen_lieu", "trong_app", "ghi_chu"])
        w.writerows(rows)
    dem = {}
    for x in rows:
        dem[x[4]] = dem.get(x[4], 0) + 1
    print(len(rows), "món |", dem, "| đã có trong app:", sum(1 for x in rows if x[8]))


if __name__ == "__main__":
    main(sys.argv[1])
