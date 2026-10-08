"""Lấy ảnh món ăn từ công thức Cookpad đang dùng làm nguồn tham khảo (cột nguon).

- Món có link công thức: lấy ảnh đại diện (og:image / JSON-LD) và tên người đăng.
- Món chỉ có link tìm kiếm, hoặc công thức không có ảnh: lấy kết quả tìm kiếm đầu tiên có ảnh.
Chỉ lưu mã ảnh trên CDN Cookpad (không tải file ảnh vào kho); app tự ghép URL theo cỡ cần dùng:
  https://img-global.cpcdn.com/recipes/<anh_id>/<rộng>x<cao>cq70/photo.webp

Ra: data/de_xuat/anh_mon.csv (ma_mon, anh_id, nguon_anh, tac_gia)
Dùng: python3 scripts/de_xuat/lay_anh.py [--lam-lai]   (mặc định bỏ qua món đã có ảnh)
"""
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "data", "de_xuat", "anh_mon.csv")
UA = {"User-Agent": "Mozilla/5.0 (CaChef; dự án cá nhân)"}
ANH = re.compile(r"cpcdn\.com/recipes/([0-9a-f]{12,})/")


def tai(url):
    for lan in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception:
            time.sleep(1 + lan * 2)
    return ""


def doc_cong_thuc(url):
    """(anh_id, tac_gia) của một trang công thức."""
    t = tai(url)
    anh, tac_gia = "", ""
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            d = json.loads(m.group(1))
        except ValueError:
            continue
        for x in d if isinstance(d, list) else [d]:
            if isinstance(x, dict) and x.get("@type") == "Recipe":
                img = x.get("image")
                img = img[0] if isinstance(img, list) and img else img
                m2 = ANH.search(str(img or ""))
                anh = anh or (m2.group(1) if m2 else "")
                au = x.get("author") or {}
                tac_gia = (au.get("name") if isinstance(au, dict) else str(au) or "").strip()
    if not anh:
        m2 = re.search(r'og:image" content="[^"]*?' + ANH.pattern, t)
        anh = m2.group(1) if m2 else ""
    return anh, tac_gia


def tim(tu_khoa_url, bo_qua=()):
    """Kết quả tìm kiếm đầu tiên có ảnh: (anh_id, tac_gia, url công thức)."""
    t = tai(tu_khoa_url)
    for rid in list(dict.fromkeys(re.findall(r'href="/vn/cong-thuc/(\d+)', t)))[:5]:
        url = f"https://cookpad.com/vn/cong-thuc/{rid}"
        if url in bo_qua:
            continue
        anh, tg = doc_cong_thuc(url)
        if anh:
            return anh, tg, url
    return "", "", ""


def mot_mon(r):
    ma, ten, nguon = r["ma_mon"], r["ten_mon"], r["nguon"]
    if "/cong-thuc/" in nguon:
        anh, tg = doc_cong_thuc(nguon)
        if anh:
            return [ma, anh, nguon, tg]
        tk = "https://cookpad.com/vn/tim-kiem/" + urllib.parse.quote(re.sub(r"\(.*?\)", "", ten).strip())
    else:
        tk = nguon
    anh, tg, url = tim(tk, bo_qua={nguon})
    return [ma, anh, url, tg]


def doc(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    mon = doc(os.path.join(ROOT, "data", "mon_an.csv")) + doc(os.path.join(ROOT, "data", "de_xuat", "mon_an_moi.csv"))
    cu = {r["ma_mon"]: r for r in doc(OUT)} if os.path.exists(OUT) and "--lam-lai" not in sys.argv else {}
    can = [r for r in mon if not cu.get(r["ma_mon"], {}).get("anh_id")]
    print(f"{len(mon)} món, cần lấy ảnh {len(can)}")
    with ThreadPoolExecutor(4) as ex:
        moi = list(ex.map(mot_mon, can))
    rows = {**{k: [v["ma_mon"], v["anh_id"], v["nguon_anh"], v["tac_gia"]] for k, v in cu.items()}, **{r[0]: r for r in moi}}
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ma_mon", "anh_id", "nguon_anh", "tac_gia"])
        w.writerows(sorted(rows.values()))
    thieu = [r[0] for r in rows.values() if not r[1]]
    print(f"có ảnh: {len(rows) - len(thieu)}/{len(rows)}" + (f" | chưa có: {', '.join(thieu)}" if thieu else ""))


if __name__ == "__main__":
    main()
