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
Kho món mở rộng (~330 món) theo khung mâm cơm, chưa đưa lên Sheet. Khi build, `app/server.py`
gộp các file này vào dữ liệu (món đã có trên Sheet – trùng mã – thì giữ bản Sheet):
- `khung_mon.csv` – danh sách món: vai trong mâm, nhóm đạm, nguồn (link Cookpad).
- `mon_an_moi.csv`, `mon_nguyen_lieu_moi.csv`, `nguyen_lieu_moi.csv` – cùng cột với bảng gốc;
  món chưa có công thức chi tiết để trống `cach_lam`, app dẫn sang link Cookpad.
- `mon_nhan.csv` – nhãn khung mâm (vai_mam, nhom_dam, cach_nau, hop_tre_em) cho mọi món.
- `an_mon.csv` – món ẩn khỏi app (vd. món chủ nhà không thích).

Sinh lại sau khi sửa `khung_mon.csv` hoặc các lô công thức `scripts/de_xuat/lo1_bac.py`, `lo2_bac.py`, `lo3_dam.py`
(lô 3: món đạm gà/vịt/ngan/bò/lợn/cá biển, món dưa cải chua, kim chi, 3 bữa nướng; khung món khai báo ngay trong file):
`python3 scripts/de_xuat/xuat_csv.py`

Nhánh nguyên liệu (`data/de_xuat/nhanh_nguyen_lieu.csv`): thịt heo tách thành thịt băm (nửa nạc nửa mỡ), ba chỉ, nạc vai,
thịt nạc, sườn, chân giò, xương, mỡ heo, tai, lưỡi, da (bì), thịt hộp. Món chỉ ghi chung "thịt heo" hiểu là thịt nạc hoặc
ba chỉ (cột `mac_dinh`). Khi build, `app/server.py` đổi mã các dòng định lượng đang ghi "thịt heo" sang nhánh theo từ khóa
trong tên (thứ tự trong file là thứ tự ưu tiên) và thay nguyên liệu chính của món tương ứng. Nhánh dùng lịch mùa vụ của mã cha
(trang Mùa vụ chỉ hiện mã cha). Tủ lạnh: có nhánh nào thì món dùng đúng nhánh đó được tính là có; món ghi chung "thịt heo" chỉ tính khi tủ có nạc, nạc vai
hoặc ba chỉ;
tủ ghi chung "Thịt heo" thì tính là có mọi nhánh.

Lịch mùa vụ đã tra cứu (`data/de_xuat/de_xuat_sua_sheet.csv`, có nguồn) được `app/server.py` đè lên các dòng nguyên liệu
trên Sheet khi build data.json. Dòng nào chủ dự án đã tự sửa trên Sheet (khác lịch cũ) thì giữ theo Sheet.

## Giao diện (điện thoại trước)

Thanh dưới có 4 mục: **Nấu gì** (`#/`, `#/ngay-mai`), **Mùa vụ** (`#/lich`), **Món** (`#/mon`), **Tủ lạnh** (`#/tu-lanh`).
- Nấu gì: bữa trưa, tối mỗi món một dòng; ✓ để chọn giữ món, "Đổi" xoay các món còn lại; nhắc rã đông cho ngày mai.
- Trang món: thông tin nhanh; thanh phản hồi ✓ Đã nấu / 👍 Ngon / 👎 Không hợp / ♥; 3 tab Nguyên liệu / Cách làm / Mùa vụ; "Bắt đầu nấu" (`#/nau/<mã>`) hiện từng bước chữ to, giữ màn hình sáng. Bấm "Xong" ở bước cuối thì ghi là đã nấu hôm nay và hỏi cả nhà thấy thế nào.
- Món: lọc ♥ Yêu thích (♥ hoặc 👍), ✓ Đã nấu, theo vai món; `#/yeu-thich` mở thẳng danh sách yêu thích.
- Mùa vụ: chọn tháng và nhóm; Đang rộ / Sắp vào mùa / Có hàng / Trái mùa, chạm để xem nguồn và món nấu được.
- Tủ lạnh: ghi thứ đang có, ngày cho vào, ngăn mát hay ngăn đá (❄); tính hạn dùng theo bí quyết bảo quản, thứ sắp hết hạn tô màu và nhắc ở trang Nấu gì.
  Gợi ý món nấu được ngay (nút ＋Trưa / ＋Tối đưa thẳng vào bữa hôm nay, thành món đã chọn) và món thiếu 1 thứ.
  Nấu xong một món thì hỏi bỏ đồ đã dùng khỏi tủ. Thứ đang ghi ở ngăn mát không cần nhắc rã đông.
- Rã đông cho ngày mai: thịt, cá rã đông từ tối hôm trước; tôm, mực lấy từ ngăn đá nấu thẳng (chỉ nhắc một dòng);
  mỡ heo luôn để ngăn mát nên không có trong danh sách.
- Bí quyết chọn nguyên liệu (chọn / tránh / cất) cho 148 nguyên liệu: trên trang món (tab Nguyên liệu, phần nguyên liệu chính) và khi chạm vào nguyên liệu ở Mùa vụ.
  Nguồn: `scripts/de_xuat/bi_quyet.py` → `data/de_xuat/bi_quyet_nl.csv` (cột `mat`, `da`: số ngày để ngon ở ngăn mát / ngăn đá).

## Quy tắc ghép bữa (`app/static/app.js`, phần "Ghép bữa")

Đang áp dụng:
- Mỗi bữa: mặn + rau + canh. Bữa một món (lẩu, nướng) chỉ buổi tối: mỗi loại tối đa 1 lần/7 ngày, lẩu và nướng cách nhau
  ít nhất 3 ngày, được +3 điểm vào tối thứ 6, thứ 7, chủ nhật; hôm tối ăn lẩu/nướng thì trưa chọn món dễ nấu.
- Món mặn kho/hầm/om/rim ở bữa trưa nấu thêm phần cho tối (tối dùng tiếp, chỉ nấu thêm rau + canh).
- Không lặp nguyên liệu chính trong ngày; đạm món mặn tối khác trưa.
- Trong một bữa: tối đa 1 món **nấu lâu** (kho, om, hầm, rim, ram, bung, sốt vang – lâu nhưng ít công)
  và 1 món **cầu kì** (nướng, nhồi, cuốn, cuộn, nem, chả, viên, mọc, gỏi nhiều thứ, món khó).
- Không 2 món cùng chiên / xào / nướng trong một bữa. Canh có đạm thì khác nhóm đạm món mặn.
- Món mặn có nhiều nước (om, bung, nấu, hầm, cà ri, bò kho, sốt vang) có thịt/cá là nguyên liệu chính thì bữa đó bỏ canh: chỉ mặn + rau
  (tiêu đề bữa ghi "không cần canh"). Món có nước mà nguyên liệu chính chỉ là rau, đậu, trứng (cà tím bung đậu phụ...) ăn như canh:
  xếp vào vai canh, bữa vẫn có một món mặn thịt/cá.
  Món kho, rim, sốt khô vẫn đi với canh.
- Bấm "Chọn" trên thẻ món để giữ món đó; "Đổi món còn lại" chỉ gợi ý lại các món chưa chọn.
- Cả ngày tối đa 1 món nhiều dầu mỡ.
- Đủ đạm (tính theo nguyên liệu chính, món chưa có bảng nguyên liệu thì theo nhóm đạm): điểm đạm cả bữa ≥ 2. Món mặn thịt/cá/hải sản 2; đạm nhẹ (trứng, đậu phụ, cua đồng, đồ khô) 1;
  canh hoặc rau có thịt/cá/tôm 1, có trứng/đậu 0,5; canh cua đồng, canh rau 0. Ví dụ trứng cút rim thì canh hoặc rau phải có thịt/cá/tôm.
- Trưa món mặn đạm nhẹ thì tối bắt buộc có món mặn thịt/cá; món mặn đạm nhẹ không nấu dư cho tối.
- Không 2 món rau lá trong một bữa (rau muống, mồng tơi, rau đay, rau ngót, cải, bắp cải...): canh rau lá thì rau là củ quả, và ngược lại.
- Canh cua đồng ăn kèm cà pháo muối xổi (không tính vào giờ nấu).
- Lời khuyên thời tiết so tổng điểm quy tắc nghiêng món nóng / món mát và ghi lý do chính (mưa, nắng gắt...).
- Ưu tiên: bữa có rau xanh; món mặn khó ăn với trẻ (cay, nhiều xương) thì canh có đạm dễ ăn.
- Chống lặp: món gợi ý hoặc đã nấu trong 3 ngày −4, 4–7 ngày −2, 8–14 ngày −1.
  Các món điểm gần nhau được xoay theo ngày (cộng thêm 0–1,5 điểm ngẫu nhiên cố định theo ngày) để không ngày nào cũng ra cùng một nhóm món.
  Mô phỏng 14 ngày liền (tháng 10, trời mưa): 52 món khác nhau / 69 lượt, trước đó 21 món.
- Đồ trong tủ lạnh: món dùng đủ nguyên liệu chính có trong tủ +2, một phần +1; có thứ cần dùng sớm (còn ≤1 ngày, ngăn mát) thêm +2.
- Phản hồi của nhà (lưu trên máy, `cachef.danh_gia`): 👍 +2, ♥ +1, 👎 −6 (hầu như không gợi ý nữa).
- Quy tắc đứng trên sự mới lạ: khi bấm "Đổi" mà món chưa xem không thỏa quy tắc thì dùng lại món đã xem.

Để làm sau:
- Cân bằng nhóm đạm theo tuần từ lịch sử 7 ngày (cá/hải sản ≥3 bữa/tuần, nhóm đạm ăn ≥3 lần thì giảm điểm).
- Có món khô thì có món nước (mặn kho/chiên đi với canh thanh hoặc canh chua).
- Mỗi bữa tối đa 1 món chua và 1 món cay (cần gắn nhãn vị cho từng món).
