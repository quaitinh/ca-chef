# Cá Chef

Gợi ý món ăn theo thời tiết Phan Rang + mùa vụ Ninh Thuận / Đà Lạt.

## Chạy demo
```
CA_CHEF_KEY=/đường/dẫn/key.json python3 app/server.py 8095
```
Mở http://127.0.0.1:8095. Không có `CA_CHEF_KEY` thì app đọc `data/*.csv`.
Dữ liệu Sheet được cache 5 phút; bấm "Tải lại dữ liệu" ở chân trang để lấy bản mới.

Cài lên màn hình chính: trang Nấu gì có lời mời cài (Android/Chrome: nút "📲 Cài app"; iPhone: hướng dẫn Safari › Chia sẻ ›
"Thêm vào MH chính"; "Để sau" thì không nhắc nữa). App có `manifest.json` và service worker
(`app/static/sw.js`): `data.json` (~1 MB) tải theo mã phiên bản trong `version.json` (do `scripts/export_json.py` ghi, băm theo nội dung),
dữ liệu chưa đổi thì dùng lại bản đã lưu; app, style mạng trước, mất mạng (sóng yếu ở chợ) thì mở bằng bản đã lưu.

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
(lô 3: món đạm gà/vịt/ngan/bò/lợn/cá biển, món dưa cải chua, kim chi, 3 bữa nướng; khung món khai báo ngay trong file;
lô 4 `lo4_chu_nha.py`: món chủ nhà chọn kèm link công thức – mã trùng thì thay món cũ, món trên Sheet ghi trong `DE_SHEET`
được `app/server.py` đè lên bản Sheet qua `de_len_sheet.csv`):
`python3 scripts/de_xuat/xuat_csv.py`

Nhánh nguyên liệu (`data/de_xuat/nhanh_nguyen_lieu.csv`): gà tách lòng, chân cổ xương, cánh, ức và gà nguyên con / nửa con
(mặc định cho món ghi chung "gà"; cột `bao_gom`: tủ có gà nguyên con thì món cánh, ức, chân cổ, lòng cũng tính là có), đùi gà
tính chung với gà; thịt bò tách ba chỉ bò Mỹ (bò ta mặc định là thăn, diềm thăn thái xào); nấm tách mộc nhĩ (nấm mèo) khô,
nấm hương (đông cô) khô – nhóm hàng khô, bảo quản riêng – còn lại là nấm tươi. "Sả, ớt, gừng" tách sả, gừng, ớt tươi
(tương ớt, ớt bột, sa tế giữ mã chung; dòng ớt chuông về mã ớt chuông). Thịt heo tách thành thịt băm (nửa nạc nửa mỡ), ba chỉ, nạc vai,
thịt nạc, sườn, chân giò, xương, mỡ heo, tai, lưỡi, da (bì), thịt hộp. Món chỉ ghi chung "thịt heo" hiểu là thịt nạc hoặc
ba chỉ (cột `mac_dinh`). Khi build, `app/server.py` đổi mã các dòng định lượng đang ghi "thịt heo" sang nhánh theo từ khóa
trong tên (thứ tự trong file là thứ tự ưu tiên) và thay nguyên liệu chính của món tương ứng. Nhánh dùng lịch mùa vụ của mã cha
(trang Mùa vụ chỉ hiện mã cha). Tủ lạnh: có nhánh nào thì món dùng đúng nhánh đó được tính là có; món ghi chung "thịt heo" chỉ tính khi tủ có nạc, nạc vai
hoặc ba chỉ;
tủ ghi chung mã cha (vd. "Thịt heo") thì tính là có các nhánh cùng nhóm (tủ có nấm tươi không tính là có nấm hương khô).

Nguồn công thức ưu tiên: Món Ngon Mỗi Ngày (monngonmoingay.com, bếp chuyên nghiệp soạn, định lượng rõ) – món có bài trùng tên ở đó
dùng bài đó (27 món), không có thì dùng Cookpad. Món chủ nhà tự gửi link giữ nguyên. Ảnh lấy URL ảnh của bài (app hiện thẳng),
trang món ghi đúng nguồn.

Công thức thật (`scripts/de_xuat/cong_thuc_that.py`, `cach_lam_that.py`): 96 món trước đây Cá Chef tự soạn (nguồn chỉ là trang
tìm kiếm) nay theo một bài Cookpad cụ thể (không lấy bài Premium): tên món theo bài, link bài, ảnh và tác giả của bài, định lượng
theo bài (quy về 4 người; bài không ghi khẩu phần thì giữ số lượng gốc), cách làm viết lại bằng lời Cá Chef nhưng giữ đúng trình tự,
kỹ thuật, nguyên liệu. `xuat_csv.py` dùng các file `cong_thuc_that*.csv` đè lên công thức trong lô. Món không có bài thật bị ẩn
(`an_mon.csv`). Hiện không còn món nào nguồn là trang tìm kiếm.

Gắn mã theo tên (`data/de_xuat/gan_ma.csv`): dòng định lượng (không phải gia vị) chỉ ghi tên được `app/server.py` gắn mã theo từ khóa
(cá diêu hồng, mộc nhĩ, thơm/dứa, sữa, hẹ, lá chanh, tôm khô...) để tính trong Tủ lạnh, Mùa vụ, Đi chợ; dòng "chính" vừa có mã thì thêm
vào nguyên liệu chính của món. Nguyên liệu mới cho các mã này khai báo ở `scripts/de_xuat/lo4_chu_nha.py`. Hành lá, hành tây, bột,
đường... để trống (đồ luôn có).

Lịch mùa vụ đã tra cứu (`data/de_xuat/de_xuat_sua_sheet.csv`, có nguồn) được `app/server.py` đè lên các dòng nguyên liệu
trên Sheet khi build data.json. Dòng nào chủ dự án đã tự sửa trên Sheet (khác lịch cũ) thì giữ theo Sheet.

## Giao diện (điện thoại trước)

Thanh dưới có 5 mục: **Nấu gì** (`#/`, `#/ngay-mai`), **Mùa vụ** (`#/lich`), **Món** (`#/mon`), **Tủ lạnh** (`#/tu-lanh`), **Đi chợ** (`#/di-cho`).
- Nấu gì: bữa trưa, tối mỗi món một dòng; ✓ để chọn giữ món, "Đổi" xoay các món còn lại; nhắc rã đông cho ngày mai.
  Thèm món nào chắc chắn nấu: "🔍 Thèm món khác? Tìm và chọn" cuối mỗi bữa (gõ không dấu) – món chọn thành món đã chọn của bữa,
  các món chưa chọn ghép lại theo quy tắc. Trang món cũng có nút "＋ Trưa nay / ＋ Tối nay" (lẩu, nướng chỉ tối).
- Chế độ nấu không thêm mục lịch sử (chuyển bước, Thoát, Xong thay mục hiện tại), nên "Quay lại" ở trang món về đúng trang trước.
- Trang món: thông tin nhanh; thanh phản hồi ✓ Đã nấu / 👍 Ngon / 👎 Không hợp / ♥; 3 tab Nguyên liệu / Cách làm / Mùa vụ; "Bắt đầu nấu" (`#/nau/<mã>`) hiện từng bước chữ to, giữ màn hình sáng. Bấm "Xong" ở bước cuối thì ghi là đã nấu hôm nay và hỏi cả nhà thấy thế nào.
- Món: lọc ♥ Yêu thích (♥ hoặc 👍), ✓ Đã nấu, theo vai món; `#/yeu-thich` mở thẳng danh sách yêu thích.
- Mùa vụ: chọn tháng và nhóm; Đang rộ / Sắp vào mùa / Có hàng / Trái mùa, chạm để xem nguồn và món nấu được.
- Tủ lạnh: ghi được mọi nguyên liệu có trong món (kể cả sả, gừng, hành tây – trang Đi chợ biết là đã có); ghi thứ đang có, ngày cho vào, ngăn mát hay ngăn đá (❄); tính hạn dùng theo bí quyết bảo quản, thứ sắp hết hạn tô màu và nhắc ở trang Nấu gì.
  Gợi ý món nấu được ngay (nút ＋Trưa / ＋Tối đưa thẳng vào bữa hôm nay, thành món đã chọn) và món thiếu 1 thứ.
  Nấu xong một món thì hỏi bỏ đồ đã dùng khỏi tủ. Thứ đang ghi ở ngăn mát không cần nhắc rã đông.
- Đi chợ: chọn đi hôm nay / ngày mai và mua cho 3, 4 hoặc 5 ngày. Chỉ bữa hôm nay, ngày mai có món cụ thể (sửa ở trang Nấu gì);
  danh sách mua đúng nguyên liệu các bữa đó (cho 4 người, cộng phần nấu dư, đồ đã có trong tủ tách riêng).
  Mấy ngày còn lại không gò theo món: một dòng lời khuyên theo dự báo (mưa – món hầm, om; nắng nóng – món mát) và
  "giỏ mua dư" gồm 2–3 thứ đạm khác họ (gà hoặc vịt, heo, bò, cá, hải sản...), 2 rau củ để lâu, 1 rau lá, 1 trái cây đang rộ –
  chọn theo điểm các món hợp từng ngày tới (thời tiết, mùa, chưa ăn gần đây), bỏ đồ đã có trong tủ. Tick đồ đã mua, bấm
  "Cất vào tủ lạnh": đồ cho bữa gần để ngăn mát, đạm của giỏ mua dư để ngăn đá. Sau đó Cá Chef gợi ý món theo tủ.
- Tủ sắp hết đồ (đã dùng tủ lạnh mà còn ≤ 1 thứ thịt, cá, trứng, đậu chưa quá hạn): trang Nấu gì nhắc nên đi chợ.
- Rã đông cho ngày mai: thịt, cá rã đông từ tối hôm trước; tôm, mực lấy từ ngăn đá nấu thẳng (chỉ nhắc một dòng);
  mỡ heo luôn để ngăn mát nên không có trong danh sách. Theo tủ lạnh: tủ đang ghi đồ thì chỉ nhắc thứ đang ghi ❄ ngăn đá;
  tủ trống mà hẹn đi chợ ngày mai thì không nhắc (mai mua tươi); tủ trống, không đi chợ mai thì nhắc "nếu có sẵn trong ngăn đá".
- Bí quyết chọn nguyên liệu (chọn / tránh / cất) cho 148 nguyên liệu: trên trang món (tab Nguyên liệu, phần nguyên liệu chính) và khi chạm vào nguyên liệu ở Mùa vụ.
  Nguồn: `scripts/de_xuat/bi_quyet.py` → `data/de_xuat/bi_quyet_nl.csv` (cột `mat`, `da`: số ngày để ngon ở ngăn mát / ngăn đá).

## Đồng bộ trong nhà (nhiều điện thoại dùng chung)

Tủ lạnh, món đã chọn và bữa đang gợi ý, đánh giá (đã nấu / 👍 / 👎 / ♥), món đã ăn mỗi ngày, đi chợ dùng chung giữa các máy,
lưu ở tab `dong_bo` của Google Sheet Cá Chef qua Apps Script (`scripts/apps_script/dong_bo.gs`). Chưa cài thì app chỉ lưu trên máy như cũ.

Cài một lần (người giữ Sheet):
1. Mở Google Sheet "Cá Chef" › Tiện ích mở rộng › Apps Script, dán nội dung `scripts/apps_script/dong_bo.gs`, lưu.
2. Triển khai › Tùy chọn triển khai mới › loại "Ứng dụng web"; Thực thi với tư cách: **Tôi**; Người có quyền truy cập: **Bất kỳ ai**.
   Cấp quyền khi Google hỏi. Chép URL ứng dụng web (`https://script.google.com/macros/s/…/exec`).
3. Trên app: chân trang › ☁ Đồng bộ › dán URL (mã nhà tự tạo) › Bật đồng bộ.
4. Bấm "Gửi link" gửi cho người nhà; mở link trên máy đó, bấm Bật đồng bộ.

Cách gộp (`app/static/dong_bo.js`): mỗi mục (một nguyên liệu trong tủ, một món đã đánh giá, bữa của một ngày...) mang giờ sửa;
mục sửa sau cùng thắng, xóa cũng đồng bộ; món đã ăn trong ngày là bữa cuối cùng (món chỉ hiện lúc bấm Đổi không tính là đã ăn). Dữ liệu có trên máy trước khi bật được gửi lên
nhưng nhường bản trên Sheet nếu Sheet đã có. App lấy dữ liệu mới trước khi ghép bữa lúc mở, khi quay lại app và mỗi 45 giây;
sửa xong gửi sau ~1 giây, mất mạng thì giữ lại gửi sau. URL và mã nhà chỉ lưu trên máy (không nằm trong kho);
ai có cả hai mới đọc/ghi được dữ liệu nhà đó. Sửa `dong_bo.gs` thì triển khai lại (Quản lý triển khai › Sửa › Phiên bản mới) để giữ URL.

## Quy tắc ghép bữa (`app/static/app.js`, phần "Ghép bữa")

Đang áp dụng:
- Mỗi bữa: mặn + rau + canh. Bữa một món (lẩu, nướng) chỉ buổi tối: mỗi loại tối đa 1 lần/7 ngày, lẩu và nướng cách nhau
  ít nhất 3 ngày, được +3 điểm vào tối thứ 6, thứ 7, chủ nhật; hôm tối ăn lẩu/nướng thì trưa chọn món dễ nấu.
- Món mặn kho/hầm/om/rim ở bữa trưa nấu thêm phần cho tối (tối dùng tiếp, chỉ nấu thêm rau + canh).
- Không lặp nguyên liệu chính trong ngày; đạm món mặn tối khác trưa.
- Trong một bữa: tối đa 1 món **nấu lâu** (kho, om, hầm, rim, ram, bung, sốt vang – lâu nhưng ít công)
  và 1 món **cầu kì** (nướng, nhồi, cuốn, cuộn, nem, chả, viên, mọc, gỏi nhiều thứ, món khó).
- Không 2 món cùng chiên / xào / nướng trong một bữa. Canh có đạm thì khác nhóm đạm món mặn.
- Bữa nào cũng đủ 3 món. Món mặn có nhiều nước (om, bung, nấu, hầm, cà ri, bò kho, sốt vang) có thịt/cá thì canh đi kèm là
  canh nhẹ (canh rau, trứng, đậu – không thêm thịt/cá). Món có nước mà nguyên liệu chính chỉ là rau, đậu, trứng (cà tím bung đậu phụ...)
  ăn như canh: xếp vào vai canh, bữa vẫn có một món mặn thịt/cá.
- Bấm "Chọn" trên thẻ món để giữ món đó; "Đổi món còn lại" chỉ gợi ý lại các món chưa chọn.
- Cả ngày tối đa 1 món nhiều dầu mỡ.
- Món nướng (mọi vai: sườn nướng, cừu nướng, bữa nướng một nồi): cả ngày tối đa 1 món; 2 ngày trước đã có món nướng thì
  trừ 6 điểm. Bữa nướng một nồi vẫn giữ quy tắc tối đa 1 lần/7 ngày.
- Đủ đạm (tính theo nguyên liệu chính, món chưa có bảng nguyên liệu thì theo nhóm đạm): điểm đạm cả bữa ≥ 2. Món mặn thịt/cá/hải sản 2; đạm nhẹ (trứng, đậu phụ, cua đồng, đồ khô) 1;
  canh hoặc rau có thịt/cá/tôm 1, có trứng/đậu 0,5; canh cua đồng, canh rau 0. Ví dụ trứng cút rim thì canh hoặc rau phải có thịt/cá/tôm.
- Trưa món mặn đạm nhẹ thì tối bắt buộc có món mặn thịt/cá; món mặn đạm nhẹ không nấu dư cho tối.
- Không 2 món rau lá trong một bữa (rau muống, mồng tơi, rau đay, rau ngót, cải, bắp cải...): canh rau lá thì rau là củ quả, và ngược lại.
- Canh cua đồng ăn kèm cà pháo muối xổi (không tính vào giờ nấu).
- Nguyên liệu quyết định món (sấu, măng tươi, sầu đâu, hoa thiên lý – `NL_QUYET_DINH`), kể cả là nguyên liệu phụ: tháng trái mùa
  (lịch = 0) thì trừ 3 điểm và ghi cách thay (vd. "Sấu trái mùa – dùng sấu ngâm hoặc sấu đông lạnh"). Sấu tươi chỉ có tháng 5–8.
- Lời khuyên thời tiết so tổng điểm quy tắc nghiêng món nóng / món mát và ghi lý do chính (mưa, nắng gắt...).
- Ưu tiên: bữa có rau xanh; món mặn khó ăn với trẻ (cay, nhiều xương) thì canh có đạm dễ ăn.
- Chống lặp: món gợi ý hoặc đã nấu trong 3 ngày −4, 4–7 ngày −2, 8–14 ngày −1. Món rau trừ thêm 4 điểm nếu đã ăn trong 4 ngày
  (ít món rau mát nên ngày nóng hay lặp: trước đó 14 ngày nắng T4 ra mồng tơi xào tỏi 7 lần, nay tối đa 3 lần).
  Các món điểm gần nhau được xoay theo ngày (cộng thêm 0–1,5 điểm ngẫu nhiên cố định theo ngày) để không ngày nào cũng ra cùng một nhóm món.
  Mô phỏng 14 ngày liền (tháng 10, trời mưa): 52 món khác nhau / 69 lượt, trước đó 21 món.
- Đồ trong tủ lạnh: món dùng đủ nguyên liệu chính có trong tủ +3, một phần +1; có thứ cần dùng sớm (còn ≤1 ngày, ngăn mát) thêm +2.
- Món nhiều nước ăn với bún thay cơm (`AN_BUN`, hiện có Ếch om chuối đậu): bữa đó chỉ thêm 1 món rau (ưu tiên rau xanh), không canh;
  nấu một nồi ăn cả ngày – trưa nấu thì tối ăn tiếp với 1 rau khác (không ghép lẩu, phở); danh sách đi chợ có bún.
- Phở gà trưa (một tô): nấu dư nước dùng, tối vẫn cơm đủ món – miến gà hoặc súp gà nấu từ nước dùng đó thay canh, món mặn
  tối không phải gà. Phở được chọn khi điểm không kém món mặn tốt nhất quá 2 điểm và cách lần trước hơn 7 ngày
  (mô phỏng 8 tuần trời mưa: 4 lần).
- Món thuốc bắc (tên có "thuốc bắc", vd. gà tiềm thuốc bắc): cách nhau ít nhất 14 ngày, khoảng 2 lần/tháng.
- Phản hồi của nhà (lưu trên máy, `cachef.danh_gia`): 👍 +2, ♥ +1, 👎 −6 (hầu như không gợi ý nữa).
- Quy tắc đứng trên sự mới lạ: khi bấm "Đổi" mà món chưa xem không thỏa quy tắc thì dùng lại món đã xem.

Để làm sau:
- Cân bằng nhóm đạm theo tuần từ lịch sử 7 ngày (cá/hải sản ≥3 bữa/tuần, nhóm đạm ăn ≥3 lần thì giảm điểm).
- Có món khô thì có món nước (mặn kho/chiên đi với canh thanh hoặc canh chua).
- Mỗi bữa tối đa 1 món chua và 1 món cay (cần gắn nhãn vị cho từng món).
