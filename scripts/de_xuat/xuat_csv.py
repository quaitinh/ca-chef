"""Sinh các bảng đề xuất trong data/de_xuat/ từ khung món + công thức lô 1.

Vào:
  data/de_xuat/khung_mon.csv   – danh sách món theo khung mâm cơm (tên, vai, nhóm đạm, nguồn)
  scripts/de_xuat/lo1_bac.py   – công thức đầy đủ của lô 1
Ra (cùng cột với bảng gốc trong data/):
  nguyen_lieu_moi.csv, mon_an_moi.csv, mon_nguyen_lieu_moi.csv
  mon_nhan.csv – nhãn khung mâm cho mọi món (kể cả món đang có)
Món chưa có công thức chi tiết: cach_lam để trống, app dẫn sang link Cookpad ở cột nguon.

Dùng: python3 scripts/de_xuat/xuat_csv.py
"""
import csv
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "de_xuat")
sys.path.insert(0, HERE)
import lo1_bac  # noqa: E402
from phan_loai import classify  # noqa: E402

MON_AN_HEADER = ["ma_mon", "ten_mon", "loai", "nhiet", "do_nang", "dau_mo", "nguyen_lieu_chinh",
                 "thoi_tiet_hop", "khau_phan_goc", "thoi_gian_phut", "do_kho", "mo_ta_ngan",
                 "cach_lam", "do_pho_bien", "nguon", "trang_thai"]
MON_NL_HEADER = ["ma_mon", "ma_nguyen_lieu", "ten_hien_thi", "so_luong", "don_vi",
                 "kieu_tinh", "vai_tro", "ghi_chu"]
NL_HEADER = ["ma", "ten", "nhom", "vung", *[f"T{i}" for i in range(1, 13)], "noi_mua", "tin_cay", "ghi_chu"]
NHAN_HEADER = ["ma_mon", "vai_mam", "nhom_dam", "cach_nau", "hop_tre_em", "nguon_loai"]

ENUM = {"loai": {"mon_chinh", "canh", "goi", "lau", "an_vat", "trang_mieng", "do_uong"},
        "nhiet": {"mat", "am", "nong"}, "do_nang": {"nhe", "nang"}, "dau_mo": {"it", "vua", "nhieu"},
        "thoi_tiet_hop": {"nang", "mua", "moi"}, "kieu_tinh": {"theo_nguoi", "theo_noi"},
        "vai_tro": {"chinh", "phu", "gia_vi"},
        "vai_mam": {"man", "rau", "canh", "mot_to", "lau", "trang_mieng", "do_uong", "an_vat", "dua_kem"}}

# Từ khoá trong tên món -> mã nguyên liệu chính (để chấm điểm mùa vụ). Thứ tự quan trọng: cụm dài trước.
NL_TU_KHOA = [
    # trái cây, rau theo mùa trước (để "gỏi xoài tôm khô" lấy xoài làm chính)
    ("diêu hồng", ""), ("hồng giòn", "hong_gion"), ("xoài", "xoai_uc"), ("thanh long", "thanh_long"),
    ("nho", "nho_nt"), ("dâu tây", "dau_tay"), ("atiso", "atiso"), ("măng tây", "mang_tay"), ("dưa hấu", "dua_hau"),
    ("bơ", "bo_booth|bo_sap"), ("táo xanh", "tao_xanh"), ("rong sụn", "rong_sun"), ("sứa", "sua"),
    ("cá cơm khô", "ca_com_kho"), ("cá cơm", "ca_com"), ("cá nục", "ca_nuc"), ("cá thu", "ca_thu"),
    ("cá ngừ", "ca_ngu_dd"), ("cá mai", "ca_mai"), ("mực một nắng", "muc_mot_nang"), ("mực", "muc_tuoi"),
    ("tôm hùm", "tom_hum"), ("tôm", "tom_the"), ("ếch", "ech"), ("dê", "thit_de"), ("cừu", "thit_cuu"),
    ("bò", "thit_bo"), ("gà", "ga_ta"), ("vịt", "ga_ta"), ("trứng", "trung"), ("đậu phụ", "dau_phu"),
    ("đậu hũ", "dau_phu"), ("riêu cua", "cua_dong"), ("canh cua", "cua_dong"), ("rau muống", "rau_muong"),
    ("mồng tơi", "mong_toi"), ("rau ngót", "rau_ngot"), ("bí đao", "bi_dao"), ("bí đỏ", "bi_do"), ("bầu", "bau"),
    ("mướp", "muop"), ("su hào", "su_hao"), ("su su", "su_su"), ("củ cải", "cu_cai"), ("đậu bắp", "dau_bap"),
    ("đậu cô ve", "dau_co_ve"), ("đậu que", "dau_co_ve"), ("cà tím", "ca_tim"), ("khoai sọ", "khoai_mon"),
    ("khoai lang", "khoai_lang"), ("khoai tây", "khoai_tay"), ("ngô", "ngo"), ("bắp cải", "bap_cai"),
    ("súp lơ", "sup_lo"), ("cải thảo", "cai_thao"), ("cà chua", "ca_chua"), ("nấm", "nam"),
    ("sườn", "thit_heo"), ("ba chỉ", "thit_heo"), ("thịt", "thit_heo"),
]
LOAI_THEO_VAI = {"man": "mon_chinh", "rau": "mon_chinh", "canh": "canh", "mot_to": "mon_chinh", "lau": "lau",
                 "trang_mieng": "trang_mieng", "do_uong": "do_uong", "an_vat": "an_vat", "dua_kem": "goi"}
MAT = ["canh chua", "nấu chua", "gỏi", "nộm", "cuốn", "luộc", "hấp", "trộn", "bí đao", "mướp", "bầu", "rau ngót",
       "mồng tơi", "chè", "sinh tố", "trà", "sương sáo", "rau câu", "sữa chua", "thạch", "ngâm", "dưa"]
NONG = ["lẩu", "hầm", "kho", "cháo", "om", "nướng", "rim", "rang", "phở", "bún bò", "sốt vang", "cà ri", "ram",
        "tiêu", "gừng", "chiên", "rán", "mì", "miến", "xôi", "súp"]
CAY = ["sả ớt", "cay", "sa tế", "mắm nhĩ", "rang me", "bún bò huế", "lòng", "tai heo", "ếch xào", "dê"]


def bo_dau(s):
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def slug(ten):
    t = re.sub(r"\(.*?\)", " ", ten)
    return re.sub(r"[^a-z0-9]+", "_", bo_dau(t).lower()).strip("_")


def nhiet_theo_ten(ten):
    t = ten.lower()
    if any(w in t for w in MAT): return "mat"
    if any(w in t for w in NONG): return "nong"
    return "am"


def nl_chinh(ten):
    t = ten.lower()
    for w, ma in NL_TU_KHOA:
        if re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", t):
            return ma
    return ""


def doc(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def ghi(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    loi = []
    goc_mon = {r["ma_mon"]: r for r in doc(os.path.join(DATA, "mon_an.csv"))}
    goc_nl = {r["ma"] for r in doc(os.path.join(DATA, "nguyen_lieu.csv"))}
    moi_nl = {n[0] for n in lo1_bac.NGUYEN_LIEU}
    tat_ca_nl = goc_nl | moi_nl
    lo1 = {r["ma"]: r for r in lo1_bac.RECIPES}

    # Nguyên liệu mới
    nl_rows = []
    for ma, ten, nhom, vung, lich, noi_mua, tin_cay, ghi_chu in lo1_bac.NGUYEN_LIEU:
        if ma in goc_nl: loi.append(f"nguyên liệu trùng mã gốc: {ma}")
        nl_rows.append([ma, ten, nhom, vung, *lich, noi_mua, tin_cay, ghi_chu])

    mon_rows, mon_nl_rows, nhan_rows, dung = [], [], [], set(goc_mon)
    for k in doc(os.path.join(OUT, "khung_mon.csv")):
        ten, vai, dam, nguon_loai, url = k["ten_mon"], k["vai_mam"], k["nhom_dam"], k["nguon_loai"], k["nguon"]
        if vai not in ENUM["vai_mam"]: loi.append(f"{ten}: vai_mam lạ {vai}")
        cach = classify(ten)[2]
        if nguon_loai == "dang_co":
            ma = k["ma_mon"]
            if ma not in goc_mon: loi.append(f"{ten}: không thấy {ma} trong data/mon_an.csv")
        elif nguon_loai == "lo1":
            ma = k["ma_mon"]
            r = lo1[ma]
            if ma in dung: loi.append(f"trùng ma_mon {ma}")
            dung.add(ma)
            for c in r["chinh"].split("|"):
                if c and c not in tat_ca_nl: loi.append(f"{ma}: mã nguyên liệu chính lạ {c}")
            mon_rows.append([ma, r["ten"], r["loai"], r["nhiet"], r["do_nang"], r["dau_mo"], r["chinh"], r["thoi_tiet"],
                             r["khau_phan"], r["phut"], r["do_kho"], r["mo_ta"],
                             "\n".join(f"{i}. {s}" for i, s in enumerate(r["cach_lam"], 1)),
                             "" if r["pho_bien"] is None else r["pho_bien"], r["nguon"], "chua_nau_thu"])
            for ma_nl, ten_nl, sl, dv, kieu, vt in r["nguyen_lieu"]:
                for c in ma_nl.split("|"):
                    if c and c not in tat_ca_nl: loi.append(f"{ma}: mã nguyên liệu lạ {c}")
                if vt not in ENUM["vai_tro"]: loi.append(f"{ma}: vai_tro lạ {vt}")
                mon_nl_rows.append([ma, ma_nl, ten_nl, "" if sl is None else sl, dv,
                                    "theo_nguoi" if kieu == "n" else "theo_noi", vt, ""])
        else:
            ma = slug(ten)
            while ma in dung: ma += "_2"
            dung.add(ma)
            t = ten.lower()
            nh = "mat" if vai == "do_uong" else nhiet_theo_ten(ten)
            loai = "goi" if vai == "rau" and any(w in t for w in ["gỏi", "nộm", "trộn", "dưa leo"]) else LOAI_THEO_VAI[vai]
            mon_rows.append([ma, ten, loai, nh,
                             "nang" if vai in ("mot_to", "lau") or cach == "kho_om" else "nhe",
                             {"chien": "nhieu", "xao": "vua", "nuong": "vua", "kho_om": "vua"}.get(cach, "it"),
                             nl_chinh(ten), {"mat": "nang", "nong": "mua"}.get(nh, "moi"),
                             2 if vai == "do_uong" else 4, "", "", "", "", "", url, "chua_nau_thu"])
        tre = "co" if "ít cay" in ten.lower() or not any(w in ten.lower() for w in CAY) else "can_nhac"
        nhan_rows.append([ma, vai, dam, cach, tre, nguon_loai])

    # Nguyên liệu lấy từ Cookpad (chuyen_nguyen_lieu.py) cho các món chưa có công thức Cá Chef
    cp_nl = os.path.join(OUT, "nguyen_lieu_cookpad.csv")
    cp_bs = os.path.join(OUT, "cookpad_bo_sung.csv")
    if os.path.exists(cp_nl):
        co_ct = {r[0] for r in mon_rows if r[12]}
        for r in doc(cp_nl):
            if r["ma_mon"] in co_ct: continue
            for c in r["ma_nguyen_lieu"].split("|"):
                if c and c not in tat_ca_nl: loi.append(f"{r['ma_mon']}: mã nguyên liệu lạ {c}")
            mon_nl_rows.append([r[h] for h in MON_NL_HEADER])
    if os.path.exists(cp_bs):
        bs = {r["ma_mon"]: r for r in doc(cp_bs)}
        for r in mon_rows:
            b = bs.get(r[0])
            if not b: continue
            if b["thoi_gian_phut"]: r[9] = int(b["thoi_gian_phut"])
            if "/tim-kiem/" in r[14] and b["nguon_cong_thuc"]: r[14] = b["nguon_cong_thuc"]  # link tìm kiếm -> công thức thật

    for r in mon_rows:
        rec = dict(zip(MON_AN_HEADER, r))
        for f in ("loai", "nhiet", "do_nang", "dau_mo", "thoi_tiet_hop"):
            if rec[f] not in ENUM[f]: loi.append(f"{rec['ma_mon']}: {f} lạ '{rec[f]}'")
        if not str(rec["nguon"]).startswith("https://cookpad.com/"): loi.append(f"{rec['ma_mon']}: nguồn lạ")
    if loi:
        sys.exit("LỖI:\n  " + "\n  ".join(loi))

    ghi("nguyen_lieu_moi.csv", NL_HEADER, nl_rows)
    ghi("mon_an_moi.csv", MON_AN_HEADER, mon_rows)
    ghi("mon_nguyen_lieu_moi.csv", MON_NL_HEADER, mon_nl_rows)
    ghi("mon_nhan.csv", NHAN_HEADER, nhan_rows)
    co_ct = sum(1 for r in mon_rows if r[12])
    print(f"Món mới: {len(mon_rows)} ({co_ct} có công thức, {len(mon_rows) - co_ct} dẫn link Cookpad) | "
          f"nhãn: {len(nhan_rows)} món | nguyên liệu mới: {len(nl_rows)} | dòng định lượng: {len(mon_nl_rows)}")


if __name__ == "__main__":
    main()
