"""Lô 5: món chủ nhà duyệt tay từ danh mục Món Ngon Mỗi Ngày (trang #/duyet-mon), nguon_loai = DOT ("mnmn_duyet_1").

Khung món (vai mâm, nhóm đạm, nhãn ghép bữa) ở data/de_xuat/mnmn_duyet.csv – gắn nhãn khi thêm món, duyệt lại được.
Định lượng theo bài (cong_thuc_that.csv), cách làm viết lại (cach_lam_mnmn.py) – xuat_csv.py đè lên như lô 4.
Gỡ cả đợt: xóa các dòng có cột dot tương ứng trong mnmn_duyet.csv rồi chạy lại xuat_csv.py.
"""
import csv
import os

DOT = "mnmn_duyet_1"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "de_xuat")
NGUYEN_LIEU = []
RECIPES, KHUNG = [], []  # KHUNG: (mã, vai mâm, nhóm đạm, nguon_loai)

_p = os.path.join(OUT, "mnmn_duyet.csv")
if os.path.exists(_p):
    for r in csv.DictReader(open(_p, newline="", encoding="utf-8")):
        RECIPES.append(dict(ma=r["ma_mon"], ten=r["ten_mon"], loai=r["loai"], nhiet=r["nhiet"], do_nang=r["do_nang"],
                            dau_mo=r["dau_mo"], chinh="", thoi_tiet=r["thoi_tiet_hop"], khau_phan=4,
                            phut=int(r["thoi_gian_phut"]) if r["thoi_gian_phut"] else "", do_kho=r["do_kho"], mo_ta="",
                            cach_lam=[], pho_bien=None, nguon=r["url"], nguyen_lieu=[]))
        KHUNG.append((r["ma_mon"], r["vai_mam"], r["nhom_dam"], r["dot"] or DOT))
