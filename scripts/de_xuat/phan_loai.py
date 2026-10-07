"""Phân loại tên món Cookpad theo khung mâm cơm (heuristic theo từ khoá).

Dùng: python3 phan_loai.py cookpad_rankings.csv mon_phan_loai.csv
  vào: file xếp hạng (ngay, hang, ma_cong_thuc, ten_mon, url)
  ra : mỗi công thức một dòng – vai trong mâm, nguồn đạm, cách nấu, số ngày lọt top.
Dữ liệu Cookpad Premium chỉ để trên máy, không đưa vào kho.
"""
import csv, re, sys, collections, unicodedata

def has(t, *ws):
    """Có từ/cụm từ nào trong t (khớp trọn từ, không khớp 'cá' trong 'cánh')."""
    return any(re.search(r"(?<!\w)" + re.escape(w.strip()) + r"(?!\w)", t) for w in ws if w.strip())

PROT = {
  "hai_san": ["tôm","mực","cua","ghẹ","ốc","nghêu","ngao","sò","hàu","sứa","bạch tuộc","hến","tép","bề bề","cù kỳ"],
  "ca": ["cá"],
  "ga": ["gà","vịt","ngan","bồ câu"],
  "bo": ["bò","bê"],
  "heo": ["heo","lợn","ba chỉ","ba rọi","sườn","giò","chả lụa","nạc","thịt băm","thịt bằm","thịt xay","dồi","lòng","tai heo","thịt kho","thịt luộc","thịt rang","thịt quay","xá xíu","khâu nhục","thịt đông","pate","xúc xích","lạp xưởng","thịt nướng"],
  "trung_dau": ["trứng","đậu hũ","đậu phụ","tàu hũ","đậu hấp"],
  "khac": ["ếch","lươn","dê","cừu","thỏ"],
}
NGOAI = ["hàn quốc","nhật","thái","kiểu ý","ấn độ","pasta","pizza","spaghetti","kimchi","kimbap","tokbokki","tteok","sushi","ramen",
         "masala","cookie","cinnamon","cheesecake","tiramisu","brownie","muffin","croissant","sandwich","burger","salad","teriyaki","bibimbap","kombucha","latte","smoothie","âu)","kiểu âu","mochi","dimsum","há cảo","sủi cảo"]

def classify(title):
    title = unicodedata.normalize("NFC", title)
    t = " " + title.lower() + " "
    if has(t, "nước chấm","nước mắm chua","pha nước mắm","nước mắm tỏi","nước sốt","sốt chấm","tương ớt","muối ớt","muối tôm","mỡ hành","siro","sa tế","cách pha","dầu điều","chà bông","ruốc"):
        vai = "cham_gia_vi"
    elif has(t, "dưa góp","đồ chua","dưa muối","cà pháo","kim chi","kimchi ","ngâm dấm","ngâm giấm","dưa cải","muối chua","củ kiệu"):
        vai = "dua_kem"
    elif has(t, " trà ","trà ","nước ép","sinh tố","smoothie","kombucha","cà phê","cafe","coffee","detox","nước sâm","nước mía","latte","matcha latte","soda","mojito","sữa ngô","sữa bắp","sữa đậu","sữa hạt","sữa gạo","nước gạo","nước chanh","nước cam","nước dừa","đồ uống","nước uống","nước bí","nước rau má","nước nha đam","sương sáo"):
        vai = "do_uong"
    elif has(t, "lẩu"):
        vai = "lau"
    elif has(t, "chè","rau câu","thạch","flan","kem ","pudding","sữa chua","yaourt","cheesecake","cookie","mứt","tart","cake","bông lan","su kem","tiramisu","brownie","muffin","bánh quy","bánh bò","bánh da lợn","bánh flan","bánh pía","bánh trung thu","bánh dẻo","bánh chuối","bánh khoai","bánh bí","bánh gato","bánh kem","bánh su","bánh tình","bánh bột lọc","bánh ít","bánh tét","bánh chưng","bánh giò","bánh ú","bánh in","bánh mì quế","bánh mì sữa","bánh mì ngọt","bánh cuộn","mochi","sữa chua","trái cây","hoa quả","rượu"):
        vai = "trang_mieng_banh"
    elif has(t, "phở","bún","miến","mì ","mì quảng","hủ tiếu","hủ tíu","cháo","xôi","bánh mì","bánh cuốn","bánh canh","cơm chiên","cơm rang","cơm tấm","cơm gà","cơm cuộn","cơm nắm","cơm trộn","cơm hến","cơm lam","nui","pasta","spaghetti","súp","bánh xèo","bánh căn","kimbap","sandwich","pizza","burger","bánh đa","bánh hỏi","bánh bèo","bánh khọt","bánh ướt","bánh tráng nướng","mì xào","ramen","udon","tokbokki","bánh bao","bánh giò"):
        vai = "mot_to"
    elif has(t, "canh","súp","hầm","nấu chua","nấu ngót","riêu"):
        vai = "canh"
    else:
        prot = [k for k, ws in PROT.items() if has(t, *ws)]
        if prot:
            vai = "man"
        elif has(t, "nộm","gỏi","salad","rau","cải","su su","bí ","bầu","mướp","đậu que","đậu cô ve","đậu bắp","đậu hà lan","măng","nấm","giá ","khổ qua","mồng tơi","súp lơ","bông cải","bắp cải","cà tím","dưa leo","dưa chuột","rau muống","cà rốt","khoai","ngô","bắp","su hào","cần","đậu đũa","rong"):
            vai = "rau"
        elif has(t, "khô ","snack","bỏng","bắp rang","chân gà","bánh tráng trộn","ăn vặt","nem chua","hạt điều","đậu phộng","lạc rang","khoai tây chiên","xiên"):
            vai = "an_vat"
        else:
            vai = "khac"
    prot = [k for k, ws in PROT.items() if has(t, *ws)]
    if vai in ("canh","mot_to","lau") or vai == "man":
        pass
    cach = next((c for c, ws in [
        ("chien", ["chiên","rán","nồi chiên"]), ("nuong", ["nướng","quay"]),
        ("kho_om", ["kho","rim","om","rang","ram","sốt","um","ngũ vị","khìa","lúc lắc"]),
        ("xao", ["xào","áp chảo"]), ("luoc_hap", ["luộc","hấp","chần","trụng"]),
        ("nau", ["canh","nấu","hầm","lẩu","súp","cháo"]), ("tron_cuon", ["gỏi","nộm","trộn","cuốn","salad","ngâm","tái"]),
    ] if has(t, *ws)), "")
    ngoai = has(t, *NGOAI) or (title.isascii() and len(title) > 3)
    return vai, (prot[0] if prot else ""), cach, ngoai

STOP = r"\(.*?\)|\[.*?\]|#\S+|[^\w\s,\-&/]|\b(siêu|cực|ngon|đơn giản|dễ làm|nhà làm|cách làm|cách|món|tại nhà|chuẩn vị|đậm đà|thơm ngon|hao cơm|bắt cơm|nhức nách|lười|nhanh|cấp tốc|cho bé|cho cả nhà|kiểu mới|mới|healthy|eatclean|eat clean)\b"
def concept(title):
    t = re.sub(STOP, " ", unicodedata.normalize("NFC", title).lower())
    t = re.split(r"\s[-–:|]\s|,", t)[0]
    t = t.replace("đậu hũ","đậu phụ").replace("tàu hũ","đậu phụ").replace("thịt bằm","thịt băm").replace("lợn","heo").replace("bắp","ngô")
    return re.sub(r"\s+", " ", t).strip()

if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    agg = {}
    for r in rows:
        a = agg.setdefault(r["ma_cong_thuc"], {"ten": unicodedata.normalize("NFC", r["ten_mon"]), "ngay": [], "hang": []})
        a["ngay"].append(r["ngay"]); a["hang"].append(int(r["hang"]))
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ma_cong_thuc","ten_mon","khai_niem","vai_mam","nhom_dam","cach_nau","mon_ngoai","so_ngay_top","hang_tot_nhat","thang_xuat_hien","url"])
        for k, a in sorted(agg.items(), key=lambda kv: -len(kv[1]["ngay"])):
            vai, dam, cach, ngoai = classify(a["ten"])
            thang = sorted({int(d[5:7]) for d in a["ngay"]})
            w.writerow([k, a["ten"], concept(a["ten"]), vai, dam, cach, int(ngoai), len(a["ngay"]), min(a["hang"]),
                        " ".join(map(str, thang)), f"https://cookpad.com/vn/cong-thuc/{k}"])
