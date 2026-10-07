"""Gộp kết quả tra cứu mùa vụ (data/de_xuat/mua_vu/*.json) thành bảng dùng được.

Vào:  data/de_xuat/mua_vu/{hai_san,nong_san,da_lat,moi}.json – mỗi mục: ma, thang[12] (0 trái mùa,
      1 có hàng, 2 rộ), tin_cay A/B/C, ghi_chu, nguon[{url, trich}]; moi.json thêm ten, nhom, vung, noi_mua.
Ra:   data/de_xuat/lich_mua_nghien_cuu.csv – lịch đã kiểm chứng, cùng cột với bảng nguyen_lieu + cột nguon
      data/de_xuat/nguon_mua_vu.csv        – từng nguồn và câu trích làm căn cứ
      data/de_xuat/de_xuat_sua_sheet.csv   – nguyên liệu trên Sheet có lịch khác kết quả tra cứu (để chủ dự án sửa tay)

Dùng: python3 scripts/de_xuat/gop_mua_vu.py
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "data", "de_xuat")
SRC = os.path.join(OUT, "mua_vu")
sys.path.insert(0, HERE)
import lo1_bac  # noqa: E402

THANG = [f"T{i}" for i in range(1, 13)]
HEADER = ["ma", "ten", "nhom", "vung", *THANG, "noi_mua", "tin_cay", "ghi_chu"]

# Hai nhóm tra cứu cho kết quả khác nhau: nghiên cứu ven bờ Ninh Thuận (vjol) ghi cá ngừ ồ, cá liệt có ở cả
# hai vụ, nên tháng ngoài mùa rộ là "có hàng" (1) chứ không phải 0.
CHINH_TAY = {
    "ca_ngu_o": dict(thang=[1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1]),
    "ca_liet": dict(thang=[2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2],
                    ghi_chu="Tuy Phong nhiều từ T10 đến Tết; ven bờ Ninh Thuận còn đánh lưới rê vụ Nam"),
}

# Tên ngắn cho nhãn trên app (tên đầy đủ vẫn ở ghi chú của nhóm tra cứu)
TEN_GON = {
    "mang_cau_ta": "Mãng cầu", "xoai_cat": "Xoài cát Cam Lâm", "chuoi_chin": "Chuối chín", "cha_la": "Chà là Ninh Thuận",
    "sau_dau": "Sầu đâu", "cu_kieu": "Củ kiệu", "tieu_moi": "Tiêu mới", "mat_ong": "Mật ong hoa cà phê",
    "ca_ngu_soc_dua": "Cá ngừ sọc dưa", "ca_ngu_o": "Cá ngừ ồ", "ca_liet": "Cá liệt", "nhum": "Nhum (cầu gai)",
    "ruoc_tuoi": "Ruốc tươi", "oc_ruoc": "Ốc ruốc", "rong_nho": "Rong nho", "hau": "Hàu", "ca_bop": "Cá bớp",
    "ca_chi_vang": "Cá chỉ vàng", "yen_sao": "Yến sào", "mac_ca": "Mắc ca",
}

def doc(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    goc = {r["ma"]: r for r in doc(os.path.join(ROOT, "data", "nguyen_lieu.csv"))}
    moi = {n[0]: dict(zip(HEADER, [n[0], n[1], n[2], n[3], *n[4], n[5], n[6], n[7]])) for n in lo1_bac.NGUYEN_LIEU}
    hien_tai = {**moi, **goc}

    muc = {}
    for ten_file in ("hai_san", "nong_san", "da_lat", "moi"):
        for x in json.load(open(os.path.join(SRC, ten_file + ".json"), encoding="utf-8")):
            if "ma" not in x: continue  # khối "de_xuat_moi" phụ
            if x["ma"] in muc and ten_file != "moi": continue  # trùng giữa các nhóm: giữ bản đầu
            muc[x["ma"]] = {**x, **CHINH_TAY.get(x["ma"], {})}

    rows, nguon_rows, sua_sheet = [], [], []
    for ma, x in muc.items():
        cu = hien_tai.get(ma)
        if cu is None and "ten" not in x:
            sys.exit(f"{ma}: mã mới nhưng thiếu tên/nhóm/vùng")
        assert len(x["thang"]) == 12 and set(x["thang"]) <= {0, 1, 2}, ma
        if cu and [int(cu[t] or 0) for t in THANG] == x["thang"] and x["tin_cay"] > cu["tin_cay"]:
            x["tin_cay"] = cu["tin_cay"]  # lịch không đổi, chỉ là không tìm thêm được nguồn: giữ mức tin cậy cũ
        ten = cu["ten"] if cu else TEN_GON.get(ma, x["ten"])
        nhom = cu["nhom"] if cu else x["nhom"]
        vung = cu["vung"] if cu else x["vung"]
        noi_mua = cu["noi_mua"] if cu else x.get("noi_mua", "chợ")
        urls = list(dict.fromkeys(n["url"] for n in x["nguon"] if n.get("url")))
        rows.append([ma, ten, nhom, vung, *x["thang"], noi_mua, x["tin_cay"], x["ghi_chu"], " | ".join(urls)])
        for n in x["nguon"]:
            nguon_rows.append([ma, n.get("url", ""), n.get("trich", "")])
        if ma in goc:
            lich_cu = [int(goc[ma][t] or 0) for t in THANG]
            if lich_cu != x["thang"] or goc[ma]["tin_cay"] != x["tin_cay"]:
                sua_sheet.append([ma, ten, "".join(map(str, lich_cu)), "".join(map(str, x["thang"])),
                                  goc[ma]["tin_cay"], x["tin_cay"], x["ghi_chu"], " | ".join(urls[:3])])

    def ghi(name, header, data):
        with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(header); w.writerows(data)

    ghi("lich_mua_nghien_cuu.csv", HEADER + ["nguon"], rows)
    ghi("nguon_mua_vu.csv", ["ma", "url", "trich"], nguon_rows)
    ghi("de_xuat_sua_sheet.csv", ["ma", "ten", "lich_tren_sheet", "lich_de_xuat", "tin_cay_cu", "tin_cay_moi",
                                  "ghi_chu", "nguon"], sua_sheet)
    moi_ma = [m for m in muc if m not in hien_tai]
    print(f"{len(rows)} mục | mã mới: {len(moi_ma)} | nguồn: {len(nguon_rows)} | đề xuất sửa Sheet: {len(sua_sheet)}")


if __name__ == "__main__":
    main()
