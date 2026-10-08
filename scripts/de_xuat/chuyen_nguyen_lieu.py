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

GIA_VI = r"^hành$|bơ (lạt|thực vật|nhạt|mặn)|^bơ \d|gia vị|giềng|riềng|muối|đường|nước mắm|(^|\s)mắm|hạt nêm|bột nêm|bột canh|bột ngọt|mì chính|(^|\s)tiêu|dầu ăn|dầu hào|dầu điều|dầu mè|xì dầu|nước tương|tương|giấm|dấm|(^|\s)tỏi|hành tím|hành khô|hành củ|gừng|(^|\s)sả|(^|\s)ớt|ngũ vị|quế|(^|\s)hồi|thảo quả|bột năng|bột bắp|bột mì|bột chiên|mật ong|sa tế|nước cốt chanh|(^|\s)chanh(?! dây)|(^|\s)me|rượu|màu điều|(^|\s)bơ lạt|maggi|knorr|nước lọc|nước sôi|(^|\s)nước$|đá viên|lá dứa|nước màu|sốt"
RAU_THOM = r"hành lá|hành hoa|hành ngò|(^|\s)ngò|rau mùi|rau thơm|húng|rau răm|thì là|tía tô|kinh giới|lá chanh|lá lốt|rau sống|ngò gai|lá é|rau quế"

# Tên nguyên liệu -> mã trong bảng nguyen_lieu (cụm dài/đặc thù trước)
MA = [
    (r"tôm khô|ruốc|chà bông|bánh phồng", ""), (r"tôm hùm", "tom_hum"), (r"tôm|tép", "tom_the"), (r"mực (khô|một nắng)", "muc_mot_nang"),
    (r"mực", "muc_tuoi"), (r"cá cơm khô", "ca_com_kho"), (r"cá cơm", "ca_com"), (r"cá nục", "ca_nuc"), (r"cá thu", "ca_thu"),
    (r"cá ngừ", "ca_ngu_dd"), (r"cua đồng|rạm|riêu cua|cua xay|cà ra", "cua_dong"), (r"sứa", "sua"), (r"ếch", "ech"), (r"(^|\s)dê", "thit_de"),
    (r"cừu", "thit_cuu"), (r"(^|\s)(bò|bê)(\s|$)|bắp bò|nạm|gầu", "thit_bo"), (r"đậu (hũ|phụ) trứng", "dau_phu"), (r"trứng", "trung"),
    (r"chim cút", "chim_cut"), (r"(^|\s)vịt", "vit"), (r"(^|\s)ngan(\s|$)", "ngan"), (r"(^|\s)gà", "ga_ta"),
    (r"kim ?chi", "kim_chi"), (r"dưa (cải )?(chua|muối)|dưa cải", "dua_cai_chua"), (r"cá trắm", "ca_tram"), (r"cá chép", "ca_chep"), (r"đậu (hũ|phụ)|tàu hũ|đậu non", "dau_phu"), (r"lòng|dồi", "long_heo"),
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
    (r"cá lóc|cá quả", "ca_loc"), (r"cá bạc má", "ca_bac_ma"), (r"cá chim", "ca_chim"), (r"ghẹ", "ghe"),
    (r"(^|\s)cua(\s|$)|cua biển|cua thịt|cua gạch", "cua_bien"), (r"sò điệp", "so_diep"),
    (r"nghêu|ngao|sò huyết|(^|\s)sò(\s|$)|hến", "ngheu"), (r"(^|\s)ốc", "oc"),
    (r"dưa leo|dưa chuột", "dua_leo"), (r"ngọn bí|rau bí|đọt bí", "rau_bi"), (r"rau dền", "rau_den"), (r"rau lang", "rau_lang"),
    (r"rau má", "rau_ma"), (r"(^|\s)giá(\s|$)|giá đỗ|giá sống|giá đậu", "gia_do"), (r"cà pháo", "ca_phao"),
    (r"cải (ngọt|chíp|ngồng|bẹ|xanh|bó xôi|làn|mầm)|rau cải", "cai_xanh"),
    (r"bưởi", "buoi"), (r"(^|\s)dừa|cơm dừa", "dua"), (r"(^|\s)mía", "mia"), (r"nha đam|lô hội", "nha_dam"), (r"hạt sen|(^|\s)sen(\s|$)", "hat_sen"),
    (r"đậu (xanh|đỏ|đen)", "dau_hat"), (r"(^|\s)nếp|gạo nếp", "gao_nep"), (r"sương sáo|thạch đen", "suong_sao"),
]
GV_MA = [(r"nước mắm", "mam_ca_na"), (r"muối", "muoi_ca_na"), (r"(^|\s)tỏi", "toi_pr"), (r"hành tím|hành khô|hành củ", "hanh_tim"),
         (r"(^|\s)sả|(^|\s)ớt|gừng", "sa_ot"), (r"(^|\s)chanh(?! dây)|(^|\s)me|khế", "khe_me")]


# Món mà trang Cookpad liệt kê thiếu/gộp nguyên liệu: Cá Chef tự điền (định lượng 4 người, đồ uống 2 phần).
SUA_TAY = {
    "canh_cai_be_xanh_thit_bam": ["300 g cải bẹ xanh", "150 g thịt heo xay", "1 nhánh gừng", "2 củ hành tím",
                                  "1 muỗng canh nước mắm", "1 muỗng cà phê hạt nêm", "Tiêu"],
    "hu_tieu_kho": ["600 g hủ tiếu", "300 g thịt heo xay", "200 g tôm", "4 quả trứng cút", "200 g giá", "Hẹ, xà lách",
                    "4 tép tỏi", "3 muỗng canh nước tương", "1 muỗng canh dầu hào", "1 muỗng cà phê đường", "Hành phi"],
    "cuu_nuong": ["1 kg thịt cừu", "3 cây sả", "1 củ tỏi", "2 củ hành tím", "2 muỗng canh dầu hào",
                  "1 muỗng canh nước mắm", "1 muỗng canh mật ong", "1 muỗng cà phê tiêu", "2 muỗng canh dầu ăn",
                  "Muối ớt chanh"],
    "gia_xao_he": ["400 g giá đỗ", "1 bó hẹ", "2 tép tỏi", "1 muỗng canh dầu ăn", "1 muỗng cà phê hạt nêm"],
    "xa_lach_tron_dau_giam": ["300 g xà lách", "2 quả cà chua", "1 củ hành tây", "2 quả trứng gà",
                              "2 muỗng canh giấm", "2 muỗng canh dầu ăn", "1 muỗng canh đường", "Muối, tiêu"],
    "mang_tay_luoc_cham_xi_dau_trung": ["500 g măng tây", "2 quả trứng gà", "3 muỗng canh xì dầu",
                                        "1 muỗng cà phê đường", "Muối"],
    "canh_dau_phu_ca_chua": ["2 bìa đậu phụ", "3 quả cà chua", "2 cây hành lá", "1 củ hành tím",
                             "1 muỗng canh nước mắm", "1 muỗng cà phê hạt nêm", "1 muỗng canh dầu ăn"],
    "canh_cai_thao_dau_hu_nam": ["400 g cải thảo", "2 bìa đậu phụ", "150 g nấm rơm", "1 củ hành tím",
                                 "1 muỗng cà phê hạt nêm", "1 muỗng canh nước mắm", "Hành lá"],
    "canh_tom_nau_thom": ["200 g tôm", "1/4 quả dứa", "2 quả cà chua", "1 củ hành tím", "Hành lá, ngò gai",
                          "1 muỗng canh nước mắm", "1 muỗng cà phê hạt nêm"],
    # Trang Cookpad thiếu nguyên liệu có trong tên món (đậu phộng, rau lang, muối vừng): điền đủ cho khớp tên.
    "ca_com_kho_rim_dau_phong": ["150 g cá cơm khô", "100 g đậu phộng", "3 tép tỏi", "2 muỗng canh đường", "2 muỗng canh nước mắm",
                                 "1 muỗng canh nước cốt chanh", "1 muỗng canh tương ớt", "5 lá chanh", "Tiêu"],
    "rau_lang_luoc_cham_kho_quet": ["500 g rau lang", "150 g thịt ba chỉ", "50 g mỡ heo", "30 g tôm khô", "4 tép tỏi", "2 củ hành tím",
                                    "2 muỗng canh nước mắm", "1 muỗng canh đường", "Hành lá", "Ớt", "Tiêu"],
    "dau_que_luoc_cham_muoi_me": ["400 g đậu que", "2 muỗng canh vừng (mè) rang", "1 muỗng cà phê muối", "1 muỗng cà phê đường"],
    # Trang Cookpad không ghi lượng nguyên liệu chính: điền lượng cho 4 người, giữ đúng nguyên liệu của công thức gốc.
    "suon_xao_chua_ngot": ["600 g sườn non", "4 tép tỏi", "2 muỗng canh giấm", "3 muỗng canh đường", "2 muỗng canh nước mắm",
                           "2 muỗng canh tương cà", "1 muỗng canh dầu ăn"],
    "thit_heo_kho_tieu": ["600 g thịt heo", "1 muỗng cà phê tiêu", "2 quả ớt", "4 tép tỏi", "2 củ hành tím",
                          "3 muỗng canh nước mắm", "2 muỗng canh đường"],
    "ca_kho_rieng": ["1 kg cá trắm", "150 g thịt ba chỉ", "1 củ riềng", "2 cây sả", "1 nhánh gừng", "2 quả ớt",
                     "3 muỗng canh nước mắm", "2 muỗng canh đường"],
    "ngheu_hap_sa": ["1,5 kg nghêu", "4 cây sả", "1 nhánh gừng", "4 tép tỏi", "2 quả ớt", "1 quả chanh", "200 ml nước lọc",
                     "1 muỗng cà phê hạt nêm"],
    "tom_hap_nuoc_dua": ["600 g tôm tươi", "1 trái dừa xiêm", "1 muỗng cà phê hạt nêm", "Ngò, cà rốt trang trí"],
    "ga_om_nam": ["1 kg gà", "10 tai nấm đông cô", "1 củ cà rốt", "300 ml nước dừa", "2 muỗng canh dầu ăn", "Hành lá, ngò, tiêu",
                  "2 củ hành tím", "3 tép tỏi", "1 muỗng canh nước mắm", "1 muỗng cà phê hạt nêm"],
    "trung_cut_rim_nuoc_mam": ["30 quả trứng cút", "4 tép tỏi", "2 quả ớt", "3 muỗng canh nước mắm", "2 muỗng canh đường",
                               "1 muỗng canh dầu ăn"],
    "dau_phu_ran_cham_mam_hanh": ["4 bìa đậu mơ", "3 cây hành lá", "2 củ hành khô", "3 muỗng canh mắm", "1 muỗng canh đường",
                                  "Dầu ăn để rán"],
    "goi_buoi": ["1 trái bưởi da xanh", "250 g tôm sú", "250 g thịt ba rọi", "3 trái dưa leo", "1 củ hành tây", "2 củ cà rốt",
                 "50 g dừa bào sợi", "Rau quế", "2 muỗng canh đậu phộng", "Ớt, tỏi, tỏi phi, hành phi", "2 muỗng canh nước mắm",
                 "2 muỗng canh đường", "Bánh phồng tôm"],
    "cai_chip_xao": ["600 g cải chíp", "4 tép tỏi", "1 muỗng canh xì dầu", "1 muỗng cà phê hạt nêm", "1 muỗng canh dầu ăn"],
    "goi_du_du_tom_thit": ["300 g thịt ba chỉ", "300 g tôm sú", "1 trái đu đủ xanh", "1 củ cà rốt", "Rau răm, húng quế",
                           "3 tép tỏi", "2 quả ớt", "2 củ hành tím", "1 quả chanh", "3 muỗng canh đường", "3 muỗng canh nước mắm",
                           "Hành phi", "2 muỗng canh đậu phộng rang", "Bánh phồng tôm"],
    "ca_tim_nuong_mo_hanh": ["4 quả cà tím", "3 củ hành khô", "4 cây hành lá", "1 muỗng cà phê hạt thì là", "1 quả ớt",
                             "1 muỗng canh dầu hào", "3 muỗng canh dầu ăn"],
    "rau_den_luoc": ["600 g rau dền", "1 muỗng cà phê muối", "1 tép tỏi", "1 trái ớt", "2 muỗng canh nước mắm", "1/2 muỗng cà phê đường"],
    "canh_rau_den_nau_tom": ["400 g rau dền đỏ", "200 g tôm thẻ", "2 tép tỏi", "1 muỗng cà phê hạt nêm", "Muối"],
    "banh_mi_chao": ["4 ổ bánh mì", "100 g pate", "1 hộp thịt hộp", "4 cây xúc xích", "4 quả trứng", "2 quả cà chua", "Rau mùi, hành lá",
                     "1 muỗng canh dầu hào", "1 muỗng cà phê hạt nêm"],
    "com_rang_thap_cam": ["800 g cơm nguội", "150 g thịt nạc xay", "2 cây lạp xưởng", "1 củ cà rốt", "100 g đậu cô ve", "2 quả trứng vịt",
                          "1 củ hành tây", "Hành lá, hành tím phi", "1 muỗng cà phê hạt nêm", "Muối, tiêu"],
    "chao_suon": ["600 g sườn non", "400 g cơm nguội", "1 củ cà rốt", "100 g giá", "Hành lá, ngò", "2 muỗng canh nước mắm",
                  "1 muỗng cà phê đường", "1 muỗng cà phê hạt nêm", "Tiêu, hành phi"],
    "banh_mi_op_la": ["4 ổ bánh mì", "8 quả trứng gà", "1 quả dưa leo", "Rau húng lủi", "2 muỗng canh nước tương", "Ớt xay",
                      "2 muỗng canh dầu ăn"],
    "mien_ga": ["300 g miến", "500 g ức gà", "1 củ cà rốt", "200 g cải bó xôi", "1 củ hành tây", "6 tai nấm đông cô", "100 g giá",
                "Hành lá", "2 lít nước luộc gà", "2 muỗng canh nước mắm", "1 muỗng cà phê đường", "Muối"],
    "bo_nhung_giam": ["800 g bắp bò", "1 trái dừa non", "2 quả táo", "1 củ hành tây", "3 cây sả", "1/2 quả dứa", "Ớt",
                      "Rau mùi, rau mùi tàu", "2 củ hành khô", "1 lít nước dừa", "500 ml nước khoáng có ga", "80 ml giấm gạo",
                      "20 g đường", "5 g muối", "Cà rốt, dưa chuột", "Xà lách, cải thảo, nấm", "Bún", "Bánh tráng cuốn",
                      "Đậu rán", "Quẩy"],
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
        url = rec.get("url") or rec.get("url_goc") or ""
        if "/tao-moi" in url: url, tg = "", ""  # crawl rơi vào trang "tạo món mới": không phải công thức
        bo_sung.append([ma, kp or "", round(hs, 2), tg, url])
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
