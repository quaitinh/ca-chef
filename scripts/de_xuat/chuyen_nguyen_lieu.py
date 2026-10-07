"""Chuyển danh sách nguyên liệu lấy từ Cookpad (cookpad_nguyen_lieu.json) thành bảng định lượng của Cá Chef.

Vào : file JSON do script trình duyệt tải về (mỗi món: ma_mon, url, khau_phan, thoi_gian, nguyen_lieu[]).
Ra  : data/de_xuat/nguyen_lieu_cookpad.csv – cùng cột với data/mon_nguyen_lieu.csv
      data/de_xuat/cookpad_bo_sung.csv   – khẩu phần gốc trên Cookpad, hệ số quy đổi, thời gian, link công thức thật
- Định lượng quy về 4 người (đồ uống 2 phần). Món không ghi khẩu phần thì giữ nguyên số lượng.
- Gia vị/nước dùng tăng chậm hơn (giống app: 1 + (hệ số - 1) * 0.6).
- Chỉ lấy nguyên liệu; cách làm vẫn để link Cookpad.

Dùng: python3 scripts/de_xuat/chuyen_nguyen_lieu.py cookpad_nguyen_lieu.json
"""
import csv
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "data", "de_xuat")
MON_NL_HEADER = ["ma_mon", "ma_nguyen_lieu", "ten_hien_thi", "so_luong", "don_vi", "kieu_tinh", "vai_tro", "ghi_chu"]

# (mẫu đơn vị, tên chuẩn, hệ số đổi sang tên chuẩn)
DON_VI = [
    (r"kg|ký|kí|ki lô|kilogram", "g", 1000), (r"lạng", "g", 100), (r"gram|gam|gr|g", "g", 1),
    (r"lít|lit|l", "ml", 1000), (r"ml", "ml", 1),
    (r"muỗng canh|thìa canh|muỗng to|mc|tbsp|m canh|mcanh|muỗng lớn", "muỗng canh", 1),
    (r"muỗng cà phê|muỗng cafe|muỗng cf|thìa cà phê|thìa cafe|mcf|tsp|m cf|muỗng nhỏ|thìa nhỏ", "muỗng cà phê", 1),
    (r"muỗng|thìa", "muỗng canh", 1),
    (r"chén|bát", "chén", 1), (r"ly|cốc", "ly", 1), (r"quả|trái", "quả", 1), (r"củ", "củ", 1), (r"tép", "tép", 1),
    (r"cây", "cây", 1), (r"nhánh", "nhánh", 1), (r"bó|mớ", "bó", 1), (r"lá", "lá", 1), (r"miếng", "miếng", 1),
    (r"con", "con", 1), (r"hộp", "hộp", 1), (r"gói", "gói", 1), (r"cái", "cái", 1), (r"khúc", "khúc", 1),
    (r"lát", "lát", 1), (r"nắm", "nắm", 1), (r"bìa|bìa đậu", "bìa", 1), (r"bắp", "bắp", 1), (r"lon", "lon", 1),
]

GIA_VI = r"^hành$|bơ (lạt|thực vật|nhạt|mặn)|^bơ \d|gia vị|giềng|riềng|muối|đường|nước mắm|(^|\s)mắm|hạt nêm|bột nêm|bột canh|bột ngọt|mì chính|(^|\s)tiêu|dầu ăn|dầu hào|dầu điều|dầu mè|xì dầu|nước tương|tương|giấm|dấm|(^|\s)tỏi|hành tím|hành khô|hành củ|gừng|(^|\s)sả|(^|\s)ớt|ngũ vị|quế|(^|\s)hồi|thảo quả|bột năng|bột bắp|bột mì|bột chiên|mật ong|sa tế|nước cốt chanh|(^|\s)chanh|(^|\s)me|rượu|màu điều|(^|\s)bơ lạt|maggi|knorr|nước lọc|nước sôi|(^|\s)nước$|đá viên|lá dứa|nước màu|sốt"
RAU_THOM = r"hành lá|hành hoa|hành ngò|(^|\s)ngò|rau mùi|rau thơm|húng|rau răm|thì là|tía tô|kinh giới|lá chanh|lá lốt|rau sống|ngò gai|lá é|rau quế"

# Tên nguyên liệu -> mã trong bảng nguyen_lieu (cụm dài/đặc thù trước)
MA = [
    (r"tôm khô|ruốc|chà bông", ""), (r"tôm hùm", "tom_hum"), (r"tôm|tép", "tom_the"), (r"mực (khô|một nắng)", "muc_mot_nang"),
    (r"mực", "muc_tuoi"), (r"cá cơm khô", "ca_com_kho"), (r"cá cơm", "ca_com"), (r"cá nục", "ca_nuc"), (r"cá thu", "ca_thu"),
    (r"cá ngừ", "ca_ngu_dd"), (r"cua đồng|rạm|riêu cua|cua xay|cà ra", "cua_dong"), (r"sứa", "sua"), (r"ếch", "ech"), (r"(^|\s)dê", "thit_de"),
    (r"cừu", "thit_cuu"), (r"(^|\s)(bò|bê)(\s|$)|bắp bò|nạm|gầu", "thit_bo"), (r"đậu (hũ|phụ) trứng", "dau_phu"), (r"trứng", "trung"),
    (r"(^|\s)(gà|vịt|ngan)", "ga_ta"), (r"đậu (hũ|phụ)|tàu hũ|đậu non", "dau_phu"), (r"lòng|dồi", "long_heo"),
    (r"thịt|sườn|ba chỉ|ba rọi|nạc|giò heo|chân giò|móng giò|xương heo|xương ống|mỡ heo|(^|\s)heo|lợn|tai heo|da heo", "thit_heo"),
    (r"rau muống", "rau_muong"), (r"mồng tơi", "mong_toi"), (r"rau ngót", "rau_ngot"), (r"rau đay", "rau_day"),
    (r"măng tây", "mang_tay"), (r"bí đao|bí xanh", "bi_dao"), (r"bí đỏ|bí ngô", "bi_do"), (r"(^|\s)bầu", "bau"), (r"mướp", "muop"),
    (r"su hào", "su_hao"), (r"su ?su", "su_su"), (r"củ cải|cải trắng", "cu_cai"), (r"đậu bắp", "dau_bap"), (r"đậu que|đậu cô ve|đậu ve", "dau_co_ve"),
    (r"cà tím", "ca_tim"), (r"khoai sọ|khoai môn", "khoai_mon"), (r"khoai lang", "khoai_lang"), (r"khoai tây", "khoai_tay"),
    (r"(^|\s)ngô|bắp (mỹ|nếp|non|ngọt)|hạt bắp|^bắp$", "ngo"), (r"bắp cải|cải bắp", "bap_cai"), (r"cải thảo", "cai_thao"),
    (r"súp lơ trắng|bông cải trắng", "sup_lo_trang"), (r"súp lơ|bông cải", "sup_lo"), (r"cà chua", "ca_chua"), (r"cà rốt", "ca_rot"),
    (r"cần tây", "can_tay"), (r"nấm", "nam"), (r"xà lách", "xa_lach"), (r"chuối xanh|chuối chát", "chuoi_xanh"),
    (r"xoài", "xoai_uc"), (r"thanh long", "thanh_long"), (r"(^|\s)nho", "nho_nt"), (r"dâu tây", "dau_tay"), (r"hồng giòn|(quả|trái) hồng", "hong_gion"),
    (r"dưa hấu", "dua_hau"), (r"(quả|trái) bơ|bơ (sáp|booth|chín)|^bơ$", "bo_booth|bo_sap"), (r"atiso", "atiso"), (r"chanh dây", "chanh_day"),
    (r"bún|bánh phở|phở|bánh canh|bánh hỏi|hủ tiếu|(^|\s)mì|miến|nui", "bun"), (r"bánh tráng|bánh đa nem", "banh_trang"),
    (r"đậu phộng|lạc", "dau_phong"), (r"bột gạo", "bot_gao"),
]
GV_MA = [(r"nước mắm", "mam_ca_na"), (r"muối", "muoi_ca_na"), (r"(^|\s)tỏi", "toi_pr"), (r"hành tím|hành khô|hành củ", "hanh_tim"),
         (r"(^|\s)sả|(^|\s)ớt|gừng", "sa_ot"), (r"(^|\s)chanh|(^|\s)me|khế", "khe_me")]


# Món mà trang Cookpad liệt kê thiếu/gộp nguyên liệu: Cá Chef tự điền (định lượng 4 người, đồ uống 2 phần).
SUA_TAY = {
    "canh_cai_be_xanh_thit_bam": ["300 g cải bẹ xanh", "150 g thịt heo xay", "1 nhánh gừng", "2 củ hành tím",
                                  "1 muỗng canh nước mắm", "1 muỗng cà phê hạt nêm", "Tiêu"],
    "hu_tieu_kho": ["600 g hủ tiếu", "300 g thịt heo xay", "200 g tôm", "4 quả trứng cút", "200 g giá", "Hẹ, xà lách",
                    "4 tép tỏi", "3 muỗng canh nước tương", "1 muỗng canh dầu hào", "1 muỗng cà phê đường", "Hành phi"],
    "nuoc_chanh_muoi": ["2 quả chanh muối", "2 muỗng canh đường", "400 ml nước lọc", "1 ly đá viên"],
}


def so(txt):
    """Đọc số đầu dòng: 1, 1.5, 1,5, 1/2, 1 1/2, 2-3 (lấy trung bình), ½."""
    txt = txt.replace("½", "1/2").replace("¼", "1/4").replace("¾", "3/4")
    m = re.match(r"\s*(\d+)\s+(\d+)/(\d+)", txt)
    if m: return int(m[1]) + int(m[2]) / int(m[3]), txt[m.end():]
    m = re.match(r"\s*(\d+)/(\d+)", txt)
    if m: return int(m[1]) / int(m[2]), txt[m.end():]
    m = re.match(r"\s*(\d+(?:[.,]\d+)?)\s*(?:-|–|~|đến)\s*(\d+(?:[.,]\d+)?)", txt)
    if m: return (float(m[1].replace(",", ".")) + float(m[2].replace(",", "."))) / 2, txt[m.end():]
    m = re.match(r"\s*(\d+(?:[.,]\d+)?)", txt)
    if m: return float(m[1].replace(",", ".")), txt[m.end():]
    return None, txt


def tach(dong):
    """'300 gram thịt bằm (thịt xay)' -> (300, 'g', 'thịt bằm', 'thịt xay')"""
    s = unicodedata.normalize("NFC", dong).strip().strip("-•*+_").strip()
    ghi = "; ".join(x.strip() for x in re.findall(r"\(([^)]*)\)", s))
    s = re.sub(r"\([^)]*\)", " ", s)
    qty, rest = so(s)
    unit = ""
    if qty is not None:
        for pat, chuan, hs in DON_VI:
            m = re.match(r"\s*(" + pat + r")(?![^\W\d_])\.?\s*", rest, re.I)
            if m:
                unit, qty, rest = chuan, qty * hs, rest[m.end():]
                break
    name = re.sub(r"\s+", " ", rest).strip(" ,.:;")
    if qty is None:  # "Thịt ba chỉ 300g" – số lượng nằm cuối
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*(kg|gr|gram|g|ml|lít|l)\s*$", name, re.I)
        if m:
            qty = float(m[1].replace(",", "."))
            u = m[2].lower()
            unit, qty = ("g", qty * 1000) if u == "kg" else ("ml", qty * 1000) if u in ("lít", "l") else ("ml" if u == "ml" else "g", qty)
            name = name[:m.start()].strip(" ,.:;")
    return qty, unit, name, ghi


def khau_phan(txt):
    m = re.search(r"(\d+)", txt or "")
    return int(m[1]) if m else None


def lam_tron(v, unit):
    if unit in ("g", "ml"):
        return int(round(v / 10) * 10) if v >= 100 else int(round(v / 5) * 5) or round(v)
    v = round(v) if v >= 2 else max(0.5, round(v * 2) / 2)  # đơn vị đếm: từ 2 trở lên làm tròn số nguyên
    return int(v) if v == int(v) else v


def main(src):
    data = json.load(open(src, encoding="utf-8"))
    mon = {r["ma_mon"]: r for r in csv.DictReader(open(os.path.join(OUT, "mon_an_moi.csv")))}
    rows, bo_sung, bo_qua = [], [], 0
    for rec in data:
        ma = rec["ma_mon"]
        if ma in SUA_TAY:
            rec = {**rec, "nguyen_lieu": SUA_TAY[ma], "khau_phan": ""}
        if ma not in mon: continue
        goc = 2 if mon[ma]["loai"] == "do_uong" else 4
        kp = khau_phan(rec.get("khau_phan"))
        hs = goc / kp if kp else 1.0
        tg = ""
        m = re.search(r"(?:(\d+)\s*tiếng)?\s*(?:(\d+)\s*phút)?", rec.get("thoi_gian") or "")
        if m and (m[1] or m[2]): tg = int(m[1] or 0) * 60 + int(m[2] or 0)
        bo_sung.append([ma, kp or "", round(hs, 2), tg, rec.get("url") or rec.get("url_goc")])
        ten_mon = mon[ma]["ten_mon"].lower()
        chinh_ma = set(filter(None, mon[ma]["nguyen_lieu_chinh"].split("|")))
        chinh_ma |= {c for p, c in MA if c and c not in ("bun", "dau_phong") and re.search(p, ten_mon)}  # nguyên liệu có trong tên món
        mon_rows = []
        for dong in rec["nguyen_lieu"]:
            qty, unit, name, ghi = tach(dong)
            t = name.lower()
            if not name or (qty is None and t.endswith(":")) or re.match(r"^(phần|nguyên liệu|nước chấm|sốt|ướp|gia vị)\b.*:?$", t) and qty is None and len(t) < 25:
                bo_qua += 1
                continue
            if "," in name and qty is None and re.search(GIA_VI, t):  # "Hạt nêm, đường, nước mắm..."
                vai, code = "gia_vi", ""
            elif re.search(RAU_THOM, t):
                vai, code = "phu", "rau_thom"
            elif t.startswith("gia vị") or (re.search(GIA_VI, t) and not re.search(r"thịt|cá|tôm|mực|gà|bò|trứng|đậu|rau|cải", t)):
                vai, code = "gia_vi", next((c for p, c in GV_MA if re.search(p, t)), "")
            else:
                vai, code = "phu", next((c for p, c in MA if re.search(p, t)), "")
            kieu = "theo_noi" if vai == "gia_vi" or unit in ("muỗng canh", "muỗng cà phê") else "theo_nguoi"
            if qty is not None and hs != 1:
                qty *= hs if kieu == "theo_nguoi" else 1 + (hs - 1) * 0.6
            ten = name[:1].upper() + name[1:]
            mon_rows.append([ma, code, ten, "" if qty is None else lam_tron(qty, unit), unit if qty is not None else "vừa đủ",
                             kieu, vai, ghi[:60]])
        # Nguyên liệu chính: dòng có mã trùng nguyên liệu chính của món; không có thì dòng phụ đầu tiên có mã.
        def trong_ten(r):  # 2 chữ đầu của nguyên liệu có trong tên món (vd. "cá lóc" trong "Cá lóc kho tộ")
            w = re.sub(r"[^\w\s]", " ", r[2].lower()).split()[:2]
            return r[6] != "gia_vi" and len(w) == 2 and " ".join(w) in ten_mon
        idx = [i for i, r in enumerate(mon_rows) if (r[1] and r[6] != "gia_vi" and set(r[1].split("|")) & chinh_ma) or trong_ten(r)]
        if not idx:
            idx = [i for i, r in enumerate(mon_rows) if r[6] == "phu" and r[1] and r[1] != "rau_thom"][:1] or \
                  [i for i, r in enumerate(mon_rows) if r[6] == "phu" and r[1] != "rau_thom"][:1] or [0][:len(mon_rows)]
        for i in idx: mon_rows[i][6] = "chinh"
        rows += mon_rows
    with open(os.path.join(OUT, "nguyen_lieu_cookpad.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(MON_NL_HEADER); w.writerows(rows)
    with open(os.path.join(OUT, "cookpad_bo_sung.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["ma_mon", "khau_phan_cookpad", "he_so", "thoi_gian_phut", "nguon_cong_thuc"]); w.writerows(bo_sung)
    print(f"{len(bo_sung)} món, {len(rows)} dòng nguyên liệu (bỏ {bo_qua} dòng tiêu đề), "
          f"{sum(1 for b in bo_sung if not b[1])} món không ghi khẩu phần")


if __name__ == "__main__":
    main(sys.argv[1])
