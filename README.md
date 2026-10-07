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
