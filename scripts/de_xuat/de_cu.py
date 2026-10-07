"""Lọc, gộp trùng và chấm điểm món ứng viên từ bảng phân loại (đầu ra của phan_loai.py).

Dùng: python3 de_cu.py mon_phan_loai.csv ung_vien.csv
Dữ liệu Cookpad Premium chỉ để trên máy, không đưa vào kho.
"""
import csv, math, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phan_loai import concept

LOAI_BO = ["cho bé","ăn dặm","bé từ","m+","mâm cúng","cúng","cơm nhà","bữa cơm","mâm cơm","thực đơn","day ","tuần ","sp.","chay","lò nướng","nồi chiên không dầu",
           "haidilao","copycat","kfc","tự làm đậu","làm từ dấm","giảm cân","keto","eat clean","eatclean","kiểu đức","kiểu nhật","kiểu thái","thái lan","đài loan","trung hoa","campuchia","khmer","ấn","miso","phô mai","phomai","bơ tỏi","sốt cay ngọt hàn","hàn quốc"]
KHONG_HOP_TRE = ["cay","ớt","sa tế","tiết","dồi","lòng","phá lấu","mắm tôm","mắm nêm","rượu","bia","tái","sống","ngâm mắm","nhúng mẻ","tuỷ","tủy","khổ qua rừng"]
XUONG_DAM = ["cá nục","cá cơm","cá rô","cá diếc","cá trích","cá bống","cá mòi","cá linh","cá kèo","cá chép","cá trê"]
KHO_MUA = ["sấu","rươi","cá kèo","cá linh","điên điển","cá lăng","rau rút","cá chạch","cá thác lác","cù kỳ","bề bề","ốc móng tay","cá diếc","ngải cứu","hoa chuối","củ đậu","củ hũ dừa","măng tươi","bồ câu","tôm càng"]
MAT = ["canh chua","nấu chua","gỏi","nộm","cuốn","luộc","hấp","salad","trộn","bí đao","mướp","bầu","rau ngót","mồng tơi","chè","sinh tố","nước","trà","sương sáo","rau câu"]
NONG = ["lẩu","hầm","kho","cháo","om","nướng","rim","rang","phở","bún bò","sốt vang","cà ri","ram","tiêu","gừng"]

def nhiet(t):
    t = t.lower()
    if any(w in t for w in MAT): return "mat"
    if any(w in t for w in NONG): return "nong"
    return "am"

def chuan(t):  # để so trùng
    return re.sub(r"\s+", " ", concept(t)).strip()

def main(phan_loai_csv, out_csv):
    rows = [r for r in csv.DictReader(open(phan_loai_csv)) if r["mon_ngoai"] == "0"]
    nhom = {}
    for r in rows:
        t = r["ten_mon"].lower()
        if r["vai_mam"] not in ("man", "rau", "canh", "mot_to", "lau", "trang_mieng_banh", "do_uong"): continue
        if any(w in t for w in LOAI_BO): continue
        if r["vai_mam"] == "trang_mieng_banh" and not any(w in t for w in ["chè","rau câu","sữa chua","flan","sương sáo","tàu hũ","trái cây"]): continue
        k = r["khai_niem"]
        g = nhom.setdefault(k, {"r": r, "ngay": 0, "so_ct": 0})
        g["ngay"] += int(r["so_ngay_top"]); g["so_ct"] += 1
        if int(r["so_ngay_top"]) > int(g["r"]["so_ngay_top"]): g["r"] = r
    out = []
    for k, g in nhom.items():
        r = g["r"]; t = r["ten_mon"].lower()
        tre = "khong" if any(w in t for w in KHONG_HOP_TRE) else ("xuong_dam" if any(w in t for w in XUONG_DAM) else "co")
        kho = any(w in t for w in KHO_MUA)
        diem = math.log2(1 + g["ngay"]) * 2 + (1 if tre == "co" else -1) + {"luoc_hap": 1.5, "nau": 1, "tron_cuon": 1, "xao": 0.5, "chien": -1.5}.get(r["cach_nau"], 0) - (3 if kho else 0)
        out.append(dict(vai=r["vai_mam"], dam=r["nhom_dam"], ten=r["ten_mon"], khai_niem=k, nhiet=nhiet(r["ten_mon"]), cach=r["cach_nau"],
                        tre=tre, kho_mua=int(kho), ngay=g["ngay"], so_ct=g["so_ct"], diem=round(diem, 1), thang=r["thang_xuat_hien"], url=r["url"]))
    out.sort(key=lambda x: (x["vai"], x["dam"], -x["diem"]))
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    c = collections.Counter((x["vai"], x["dam"]) for x in out)
    for k, v in sorted(c.items()): print(k, v)
    print("tổng", len(out))

if __name__ == "__main__":
    main(*sys.argv[1:])
