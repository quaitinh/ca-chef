# Cá Chef

Gợi ý món ăn theo thời tiết Phan Rang + mùa vụ Ninh Thuận / Đà Lạt.

## Chạy demo
```
CA_CHEF_KEY=/đường/dẫn/key.json python3 app/server.py 8095
```
Mở http://127.0.0.1:8095. Không có `CA_CHEF_KEY` thì app đọc `data/*.csv`.
Dữ liệu Sheet được cache 5 phút; bấm "Tải lại dữ liệu" ở chân trang để lấy bản mới.

## Dữ liệu
- Google Sheet "Cá Chef" (id `1aoGQLY0g3UjnQRavXnufttwoigSb-Po4IkGB1z0fwno`) là nơi chỉnh sửa chính.
- `scripts/build_data.py` + `scripts/recipes.py` → `data/*.csv`, `data/ca_chef_data.xlsx`.
- `scripts/push_sheets.py <key.json> [tab...]` ghi đè các tab lên Sheet – đừng chạy nếu đã sửa tay trên Sheet.
- `research/` – ghi chép kiểm chứng mùa vụ, danh mục GO!.

## Món đề xuất (`data/de_xuat/`)
Kho món mở rộng (~270 món) theo khung mâm cơm, chưa đưa lên Sheet. Khi build, `app/server.py`
gộp các file này vào dữ liệu (món đã có trên Sheet – trùng mã – thì giữ bản Sheet):
- `khung_mon.csv` – danh sách món: vai trong mâm, nhóm đạm, nguồn (link Cookpad).
- `mon_an_moi.csv`, `mon_nguyen_lieu_moi.csv`, `nguyen_lieu_moi.csv` – cùng cột với bảng gốc;
  món chưa có công thức chi tiết để trống `cach_lam`, app dẫn sang link Cookpad.
- `mon_nhan.csv` – nhãn khung mâm (vai_mam, nhom_dam, cach_nau, hop_tre_em) cho mọi món.
- `an_mon.csv` – món ẩn khỏi app (vd. món chủ nhà không thích).

Sinh lại sau khi sửa `khung_mon.csv` hoặc `scripts/de_xuat/lo1_bac.py`:
`python3 scripts/de_xuat/xuat_csv.py`
