"""Sửa tay sau khi sinh bảng đề xuất (xuat_csv.py áp dụng trước khi ghi CSV), để chạy lại không mất.

Đợt đánh giá 14/10/2026: món mặn có nguyên liệu chính ghi nhầm thành rau/gia vị (cá hồi ghi "phụ", nước dừa,
măng tây… ghi "chính"), cá trứng gắn nhầm mã trứng gà, cá cơm than gắn vào lòng trắng trứng.
"""

# Nguyên liệu mới. Cá trứng: hàng đông lạnh có quanh năm ở GO! (catalog sieuthi-go.vn 07/10/2026,
# research/go_catalog_2026-10-07.csv: 8 loại 200–600g, 43.000–119.000đ).
NGUYEN_LIEU = [
    ("ca_trung", "Cá trứng (đông lạnh)", "hải sản", "nhập khẩu", [1] * 12, "GO!/siêu thị", "B",
     "Cá trứng đông lạnh đóng gói, có quanh năm ở GO! (8 loại 200–600g, 43.000–119.000đ – catalog sieuthi-go.vn 07/10/2026)"),
    # Chủ nhà đi chợ 15/10/2026 mua về mà dữ liệu chưa có mã riêng.
    ("gio_lua", "Giò lụa (chả lụa)", "thịt", "chung", [1] * 12, "chợ/GO!", "C", "Giò Bắc làm từ thịt lợn, miền Nam gọi chả lụa; hàng làm sẵn, có quanh năm"),
    ("la_e", "Lá é", "rau củ", "chung", [1] * 12, "chợ", "C", "Chưa có nguồn riêng"),
    ("hanh_la", "Hành lá", "rau củ", "chung", [1] * 12, "chợ/GO!", "C", "Có quanh năm; dùng chung như rau thơm"),
]

# Cột nguyen_lieu_chinh của món.
NL_CHINH = {
    "thit_ba_chi_sot_ca_chua": "thit_heo|ca_chua", "thit_kho_cu_cai": "thit_heo|cu_cai", "thit_vien_sot_ca_chua": "thit_heo|ca_chua",
    "bo_xao_mang_tay": "thit_bo|mang_tay", "ca_dieu_hong_sot_ca_chua": "ca_dieu_hong|ca_chua", "ca_kho_chuoi_xanh": "ca_cam|chuoi_xanh",
    "ca_hoi_chien_mam_dua": "ca_hoi", "ca_hoi_chien_sot_chanh": "ca_hoi", "ca_hoi_kho_nuoc_tuong": "ca_hoi", "ca_hoi_ngu_sac": "ca_hoi",
    "ca_hoi_xot_cay": "ca_hoi", "ca_hoi_sot_ca_chua": "ca_hoi|ca_chua", "ca_com_than_chien_ca_ri": "ca_com",
    "ca_trung_cham_tuong_me": "ca_trung", "canh_ga_la_e": "ga_ta|la_e", "cha_lua_kho_trung_cut": "gio_lua|trung", "ca_trung_chien_bo_toi": "ca_trung", "ca_trung_chien_gion": "ca_trung",
}
CA_HOI = {"ca_hoi_chien_mam_dua", "ca_hoi_chien_sot_chanh", "ca_hoi_kho_nuoc_tuong", "ca_hoi_ngu_sac", "ca_hoi_xot_cay",
          "ca_hoi_sot_ca_chua", "canh_chua_dau_ca_hoi", "chao_ca_hoi"}
CA_TRUNG = {"ca_trung_cham_tuong_me", "ca_trung_chien_bo_toi", "ca_trung_chien_gion"}
VE_PHU = {("ca_hoi_chien_mam_dua", "dua"), ("ca_hoi_kho_nuoc_tuong", "mang_tay"), ("ca_hoi_ngu_sac", "khoai_tay"), ("ca_hoi_xot_cay", "hanh_tay")}
LEN_CHINH = {("ca_dieu_hong_sot_ca_chua", "ca_dieu_hong"), ("ca_kho_chuoi_xanh", "ca_cam")}
# Món ăn chơi giữa buổi, không phải món mặn trong bữa (chủ nhà 16/10/2026).
AN_VAT = {"chan_ga_sa_tac"}
# Nhóm đạm: ếch như các món ếch khác.
NHOM_DAM = {"cha_ech_la_lot_chien": "khac"}


def sua_dong(r):
    """r: dòng mon_nguyen_lieu (ma_mon, ma_nguyen_lieu, ten_hien_thi, so_luong, don_vi, kieu_tinh, vai_tro, ghi_chu)."""
    ma, nl, ten = r[0], r[1], r[2].lower()
    if ma in CA_HOI and not nl and "cá hồi" in ten:
        r[1], r[6] = "ca_hoi", "chinh"
    elif ma in CA_TRUNG and nl == "trung" and ten.startswith("cá trứng"):
        r[1] = "ca_trung"
    elif ma == "ca_com_than_chien_ca_ri" and not nl and ten.startswith("cá cơm than"):
        r[1], r[6] = "ca_com", "chinh"
    elif ma == "ca_com_than_chien_ca_ri" and nl == "trung":
        r[6] = "phu"
    elif ma == "canh_ga_la_e" and nl == "rau_thom" and ten.startswith("lá é"):
        r[1], r[6] = "la_e", "chinh"
    elif ma == "cha_lua_kho_trung_cut" and not nl and ten.startswith("chả lụa"):
        r[1], r[6] = "gio_lua", "chinh"
    elif (ma, nl) in VE_PHU:
        r[6] = "phu"
    elif (ma, nl) in LEN_CHINH:
        r[6] = "chinh"


def ap_dung(mon_rows, mon_nl_rows, nhan_rows):
    for r in mon_rows:
        if r[0] in NL_CHINH: r[6] = NL_CHINH[r[0]]
        if r[0] in AN_VAT: r[2] = "an_vat"
    for r in mon_nl_rows: sua_dong(r)
    for r in nhan_rows:
        if r[0] in NHOM_DAM: r[2] = NHOM_DAM[r[0]]
        if r[0] in AN_VAT: r[1] = "an_vat"
