"""Thay công thức Cá Chef tự soạn (lô 2, 3, 4 – nguồn chỉ là trang tìm kiếm) bằng công thức thật trên Cookpad.

Vào : JSON các công thức đã chọn (Cookpad hoặc Món Ngon Mỗi Ngày – nguồn ưu tiên khi có bài) (mỗi món: ma_mon, ten_moi, url, tac_gia, anh, khau_phan, thoi_gian, nguyen_lieu[]),
      tải từ trang công thức công khai (không lấy bài Premium). File này để ngoài kho.
Ra  : data/de_xuat/cong_thuc_that.csv       – định lượng (quy về 4 người, đồ uống 2) theo đúng bài gốc
      data/de_xuat/cong_thuc_that_nguon.csv – link bài, tên món theo bài, tác giả, mã ảnh, khẩu phần gốc, thời gian
      data/de_xuat/anh_mon.csv              – ảnh món đổi sang ảnh của đúng bài
Cách làm viết lại bằng lời của Cá Chef ở cach_lam_that.py. xuat_csv.py dùng các file này đè lên công thức trong lô.

Dùng: python3 scripts/de_xuat/cong_thuc_that.py <file JSON>
"""
import csv
import html
import json
import os
import re
import sys

from chuyen_nguyen_lieu import GIA_VI, GV_MA, MA, MON_NL_HEADER, OUT, RAU_THOM, khau_phan, lam_tron, tach

DO_UONG = {"nuoc_ep_oi", "sinh_to_gac"}
# Mã cho nguyên liệu bảng MA cũ chưa có (thêm sau này); dòng chưa khớp vẫn được server.py gắn mã theo gan_ma.csv.
THEM_MA = [(r"ớt chuông", "ot_chuong"), (r"(^|\s)vịt|thịt vit", "vit"), (r"nấm", "nam"), (r"phèo|ruột (heo|lợn|non)|lòng (heo|lợn)|(^|\s)gan |^gan$|cật|tim heo|dạ dày|bao tử", "long_heo"),
           (r"ốc (bưu|đồng|nhồi)", "oc_dong"), (r"bí ngòi", "bi_ngoi"), (r"gấc", "gac"), (r"hạt sen", "hat_sen"), (r"táo đỏ|táo tàu", "tao_do"), (r"lươn", "luon"), (r"cải chua|dưa chua|dưa cải", "dua_cai_chua"), (r"măng chua", "mang_chua"), (r"sấu", "sau"),
           (r"hoa chuối", "hoa_chuoi"), (r"chuối.*xanh", "chuoi_xanh"), (r"chuối", "chuoi_chin"), (r"khổ qua|mướp đắng", "kho_qua"),
           (r"thiên lý", "thien_ly"), (r"tim cật|cật", "long_heo"), (r"cá liệt", "ca_liet"), (r"cá (sống mũi|đội đèn)", "ca_song_mui"), (r"lá chè|chè xanh", "che_xanh"), (r"vối", "la_voi"), (r"gạo lứt", "gao_lut"), (r"đậu đen", "dau_den"), (r"hoa cúc|bông cúc|cúc khô", "hoa_cuc"), (r"atiso khô", "atiso_kho"), (r"kỷ tử|kỉ tử", "ky_tu"), (r"râu (bắp|ngô)", "ngo"), (r"cá hố", "ca_ho"), (r"cá chuồ", "ca_chuon"),
           (r"cá trích", "ca_trich"), (r"cá đục", "ca_duc"), (r"cá bớp", "ca_bop"), (r"cá đối", "ca_doi"), (r"(^|\s)hàu", "hau"),
           (r"(^|\s)ổi", "oi"), (r"đậu h[ủũ]", "dau_phu"), (r"cá rô phi", "ca_ro_phi"), (r"[dđ]iêu hồng", "ca_dieu_hong"),
           (r"(giò|dò) sống", "gio_song"), (r"hành tây", "hanh_tay"), (r"^(thơm|dứa)", "thom"), (r"^hẹ", "he"), (r"^xả", "sa")]
# Dòng bài gốc ghi định lượng lẫn lời dặn – viết lại cho tách được (giữ đúng lượng của bài).
SUA_DONG = {
    "canh_tom_nau_thom": {" Tôm tươi: 2 lạng / khẩu phần cho khoảng 4 người ăn": "200 g tôm tươi",
                          " Thơm: tùy khẩu vị nhà mình thích ăn chua nhiều hay ít thì mua": "Thơm (nhiều ít tùy thích chua)",
                          " Cà: khoảng 1 quả lớn, hoặc 2 quả nhỏ": "1 quả cà chua lớn (hoặc 2 quả nhỏ)",
                          "5-10.000 Đậu bắp: khoảng": "Đậu bắp (khoảng 5–10 nghìn đồng)"},
    "canh_dau_phu_ca_chua": {}, "vit_om_sau": {"1 lit nước: 500ml nước lọc + 500ml nước dừa": ["500 ml nước lọc", "500 ml nước dừa"]},
    "nuong_kieu_han_kim_chi": {}, "canh_bo_nau_dua_ca_chua": {"1 tô nước lọc": "Nước lọc (1 tô, 2 người)"},
}
KHONG_PHAI_NL = r"^(chảo|máy|giấy|nồi|khay|que|xiên)\b"


def phut(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?", iso or "")
    return int(m[1] or 0) * 60 + int(m[2] or 0) if m and (m[1] or m[2]) else ""


def main(src):
    data = json.load(open(src, encoding="utf-8"))
    rows, nguon = [], []
    for rec in data:
        ma = rec["ma_mon"]
        goc = 2 if ma in DO_UONG else 4
        kp = khau_phan(rec.get("khau_phan"))
        hs = goc / kp if kp else 1.0
        ds = []
        for d in rec["nguyen_lieu"]:
            x = SUA_DONG.get(ma, {}).get(d, d)
            ds += x if isinstance(x, list) else [x]
        for dong in map(html.unescape, ds):
            # Món Ngon Mỗi Ngày ghi "Sườn non: 400g", "Tỏi băm : 2M" (M = muỗng canh, m = muỗng cà phê) -> "400g Sườn non".
            m = re.match(r"^\s*([^:\d][^:]*?)\s*:\s*(\d[\d.,/\-]*)\s*(?:(M|m)\b)?\s*(.*)$", dong)
            if m:
                don_vi = {"M": " muỗng canh", "m": " muỗng cà phê"}.get(m[3] or "", "")
                dong = f"{m[2]}{don_vi} {m[4]} {m[1]}".replace("  ", " ")
            dong = re.sub(r"(?i)^(\d+ gói đậu hũ non):.*$", r"\1", dong)
            dong = re.sub(r"^(\S+(?:-\S+)? gr thịt ba chỉ) tùy sức ăn\..*$", r"\1", dong)
            dong = re.sub(r"(?i)(?<![^\W\d_])tcfe?\b", " muỗng cà phê", re.sub(r"(?i)(?<![^\W\d_])tbs\b", " muỗng canh", dong))
            qty, unit, name, ghi = tach(dong)
            name = re.sub(r"\s*(LISA|AJI-NO-MOTO®?|Aji-ngon®?|AJI-QUICK®?|“?Phú Sĩ”?|\"Phú Sĩ\"|Ajinomoto)\b", "", name, flags=re.I).strip()
            t = name.lower()
            if re.search(KHONG_PHAI_NL, t):
                continue
            if not name or (qty is None and t.endswith(":")) or re.match(r"^(phần|nguyên liệu|nước chấm|sốt|ướp|gia vị)\b.*:?$", t) and qty is None and len(t) < 25:
                continue
            if "," in name and qty is None and re.search(GIA_VI, t):
                vai, code = "gia_vi", ""
            elif any(re.search(p, t) for p, _ in THEM_MA):  # trước rau thơm: "bí ngòi" chứa "ngò"
                vai, code = "phu", next(c for p, c in THEM_MA if re.search(p, t))
            elif re.search(RAU_THOM, t):
                vai, code = "phu", "rau_thom"
            elif t.startswith("gia vị") or (re.search(GIA_VI, t) and not re.search(r"thịt|cá|tôm|mực|gà|bò|trứng|đậu|rau|cải", t)):
                vai, code = "gia_vi", next((c for p, c in GV_MA if re.search(p, t)), "")
            else:
                vai, code = "phu", next((c for p, c in THEM_MA + MA if re.search(p, t)), "")
            kieu = "theo_noi" if vai == "gia_vi" or unit in ("muỗng canh", "muỗng cà phê") else "theo_nguoi"
            if qty is not None and hs != 1:
                qty *= hs if kieu == "theo_nguoi" else 1 + (hs - 1) * 0.6
            rows.append([ma, code, name[:1].upper() + name[1:], "" if qty is None else lam_tron(qty, unit),
                         unit if qty is not None else "vừa đủ", kieu, vai, ghi[:60]])
        nguon.append([ma, rec.get("ten_moi", ""), rec["url"], rec.get("tac_gia", ""), rec.get("anh", ""), kp or "", round(hs, 2), phut(rec.get("thoi_gian"))])
    with open(os.path.join(OUT, "cong_thuc_that.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n"); w.writerow(MON_NL_HEADER); w.writerows(rows)
    with open(os.path.join(OUT, "cong_thuc_that_nguon.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["ma_mon", "ten_moi", "url", "tac_gia", "anh_id", "khau_phan_cookpad", "he_so", "thoi_gian_phut"]); w.writerows(nguon)
    # Ảnh món: lấy đúng ảnh của bài đã chọn (trước đây là kết quả tìm kiếm đầu tiên – có thể là món khác).
    p = os.path.join(OUT, "anh_mon.csv")
    anh = list(csv.reader(open(p, newline="")))
    moi = {n[0]: [n[0], n[4], n[2], n[3]] for n in nguon if n[4]}
    anh = [moi.pop(r[0], r) if r and r[0] in moi else r for r in anh] + list(moi.values())
    with open(p, "w", newline="") as f:
        csv.writer(f, lineterminator="\r\n").writerows(anh)
    print(f"{len(nguon)} món, {len(rows)} dòng nguyên liệu, {sum(1 for n in nguon if not n[5])} món không ghi khẩu phần (giữ số lượng gốc)")


if __name__ == "__main__":
    main(sys.argv[1])
