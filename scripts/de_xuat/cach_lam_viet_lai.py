"""Cách làm do Cá Chef viết lại (bằng lời riêng, rút gọn) cho các món lấy nguyên liệu từ Cookpad.

Nguồn tham khảo: link Cookpad ở cột nguon của từng món. Không chép nguyên văn.
CL[ma_mon] = (mô tả ngắn, thời gian phút, độ khó de/vua/kho, [các bước])
"""
CL = {}

# ---------- Lô A ----------
CL.update({
    "dau_hu_non_sot_thit_bam": ("Đậu hũ non mềm mịn rim trong sốt cà chua thịt băm – món quen của mâm cơm nhà.", 35, "de", [
        "Cà chua bỏ hạt, thái hạt lựu; hành lá thái nhỏ, để riêng phần đầu trắng; đậu hũ cắt khối vừa ăn.",
        "Ướp thịt băm với chút đường, hạt nêm, nước mắm và đầu hành khoảng 15 phút.",
        "Phi thơm hành tím, xào thịt đến khi săn; cho cà chua cùng khoảng 200ml nước, thêm tương ớt, tương cà, đun đến khi sốt sánh.",
        "Nêm lại, thả đậu hũ vào, trở thật nhẹ tay cho khỏi nát, đun liu riu thêm 5–7 phút rồi rắc hành lá."]),
    "thit_bam_rang_man_ngot": ("Thịt băm rang xém cạnh, mặn ngọt đậm đà – rất đưa cơm, trẻ nhỏ dễ ăn.", 20, "de", [
        "Ướp thịt băm với hạt nêm, nước mắm, đường, tiêu khoảng 10 phút.",
        "Phi thơm hành tím với ít dầu, cho thịt vào đảo tơi.",
        "Rang lửa vừa đến khi thịt khô lại, vàng và hơi xém cạnh; nêm lại, rắc hành lá, tiêu."]),
    "ba_chi_rang_chay_canh": ("Ba chỉ rang ra mỡ, vàng xém cạnh rồi áo nước mắm đường.", 25, "de", [
        "Thái ba chỉ miếng nhỏ cỡ đốt ngón tay, đều nhau.",
        "Chảo nóng với chút dầu, rang thịt lửa vừa đến khi vàng các mặt và ra mỡ; chắt bớt mỡ để dành xào rau.",
        "Cho nước mắm và đường vào đảo đến khi thịt áo đều, bóng; thêm hành lá cắt khúc và tiêu rồi tắt bếp."]),
    "thit_ba_chi_rim_man_ngot": ("Ba chỉ rim nước mắm đường đến khi sệt bóng.", 35, "de", [
        "Ba chỉ cắt miếng vừa ăn, chần qua nước sôi rồi rửa lại.",
        "Phi thơm tỏi, cho thịt vào đảo đến khi săn.",
        "Thêm nước mắm, đường và chút nước, rim lửa nhỏ đến khi nước sệt lại, thịt bóng đẹp; rắc tiêu, ớt nếu thích."]),
    "ca_tim_om_thit_bam": ("Cà tím chiên mềm om cùng thịt băm sốt dầu hào tương ớt.", 35, "de", [
        "Cà tím cắt khúc, ngâm nước muối loãng 15 phút rồi vắt ráo; tỏi, ớt, hành lá băm.",
        "Chiên cà tím trong ít dầu đến khi mềm, vớt ra.",
        "Dùng chảo đó phi tỏi, xào thịt băm cho chín; pha sốt dầu hào, nước tương, tương ớt, chút đường, hạt nêm với vài thìa nước rồi đổ vào.",
        "Cho cà tím vào đảo nhẹ 2 phút cho thấm sốt, rắc hành lá."]),
    "khoai_tay_xao_thit_bam": ("Khoai tây chiên sơ xào thịt băm sốt nước tương – bùi, mặn ngọt.", 30, "de", [
        "Khoai tây gọt vỏ, cắt hạt lựu to, để ráo; hành lá chia phần đầu và phần lá.",
        "Ướp thịt với chút muối, tiêu, đường, dầu hào và đầu hành 15 phút; pha sốt nước tương, tương ớt, ít đường và nước.",
        "Chiên khoai trong ít dầu đến khi vàng các mặt, vớt ra.",
        "Xào thịt cho săn, cho khoai vào cùng sốt, đun lửa vừa 4–5 phút cho thấm; thêm hành lá rồi tắt bếp."]),
    "cha_gio_re": ("Chả giò cuốn bánh tráng rế, nhân thịt khoai môn mộc nhĩ – nướng nồi chiên không dầu cho ít dầu.", 60, "vua", [
        "Mộc nhĩ ngâm nở thái sợi; khoai môn bào sợi; miến ngâm mềm cắt ngắn.",
        "Trộn tất cả với thịt xay, nêm muối, đường, hạt nêm, tiêu, hành phi.",
        "Cuốn nhân vào bánh tráng rế, quét lòng trắng trứng ở mép cho dính.",
        "Quét lớp dầu mỏng, nướng nồi chiên không dầu 200°C khoảng 20 phút, trở mặt nướng thêm 5 phút đến khi vàng giòn (hoặc chiên ngập dầu lửa vừa)."]),
    "thit_heo_mot_nang_chien": ("Thịt heo ướp sả ớt, phơi một nắng rồi chiên – đặc sản miền Trung, hợp trời nắng Phan Rang.", 300, "vua", [
        "Thịt cắt miếng dài, rửa nước muối loãng, để thật ráo.",
        "Xay sả, tỏi, ớt; trộn với hạt nêm, đường, nước mắm, ngũ vị hương, dầu điều, chút rượu; ướp thịt ít nhất 2 tiếng trong ngăn mát.",
        "Xâu thịt, phơi chỗ nắng gắt 4–5 tiếng đến khi mặt thịt se khô (chỉ làm hôm nắng to).",
        "Chiên vàng 2 mặt hoặc nướng nồi chiên không dầu; thái miếng, ăn với dưa leo và nước mắm chua ngọt."]),
    "suon_xao_chua_ngot": ("Sườn chiên vàng rồi đảo với sốt chua ngọt tỏi phi.", 45, "vua", [
        "Chần sườn trong nước sôi 3–4 phút, vớt ra để ráo.",
        "Chiên sườn lửa nhỏ đến khi chín vàng.",
        "Pha sốt: nước mắm, nước tương, đường, chút tương ớt, nước cốt chanh và ít nước lọc.",
        "Chắt bớt dầu, phi thơm nhiều tỏi băm, cho sườn và sốt vào đảo đến khi sốt sệt, áo đều miếng sườn; rắc mè nếu thích."]),
    "suon_non_kho_thom": ("Sườn non kho nước dừa với thơm và trứng cút – chua ngọt, thơm mùi dứa.", 70, "de", [
        "Thơm bỏ lõi, cắt miếng dày; sườn rửa sạch, ướp với một nửa phần sốt kho (hoặc nước mắm, đường) 30 phút.",
        "Phi hành tỏi, đảo sườn cho săn, đổ nước dừa xâm xấp, hớt bọt, kho lửa nhỏ 30 phút.",
        "Thêm thơm, trứng cút, ớt, tiêu xanh và phần sốt còn lại, kho thêm 15 phút; thiếu nước thì thêm chút nước lọc."]),
    "thit_ba_chi_sot_ca_chua": ("Ba chỉ rang xém rồi rim với cà chua – nhanh, đưa cơm.", 25, "de", [
        "Ba chỉ thái miếng vừa ăn; cà chua bổ múi cau.",
        "Rang thịt với chút dầu và gia vị đến khi xém vàng cạnh.",
        "Cho cà chua vào đảo đến khi mềm, quyện với thịt; nêm lại, thêm hành lá và tiêu."]),
    "thit_dong": ("Móng giò, ba chỉ nấu với nấm hương mộc nhĩ rồi để đông – món Tết miền Bắc.", 120, "vua", [
        "Móng giò chặt miếng nhỏ, chần sạch, ninh mềm (nồi áp suất khoảng 20 phút) với nước và chút muối, hạt nêm.",
        "Ba chỉ có bì thái vuông 2cm, cho vào ninh cùng thêm khoảng 15 phút.",
        "Nấm hương, mộc nhĩ ngâm nở thái nhỏ; cà rốt tỉa hoa, thái lát mỏng; cho vào nồi đun thêm 10 phút, thêm tiêu.",
        "Xếp hoa cà rốt, rau mùi dưới đáy bát, múc thịt và nước dùng vào; để nguội rồi cho vào tủ lạnh đến khi đông, úp ra đĩa."]),
    "thit_luoc_cham_mam_dua_leo": ("Thịt đùi luộc thái mỏng, chấm nước mắm hành, ăn kèm dưa leo – món mát, đơn giản.", 40, "de", [
        "Thịt bóp muối rửa sạch; luộc với chút muối, hạt nêm và vài củ hành tím đập dập đến khi chín (xiên không ra nước hồng).",
        "Vớt thịt ngâm nước nguội cho trắng, thái mỏng; nước luộc dùng nấu canh.",
        "Pha nước chấm: nước mắm, đường, nước lọc, chanh, tiêu và hành tím thái mỏng; ăn kèm dưa leo."]),
    "thit_vien_sot_ca_chua": ("Thịt viên trộn nấm hương mộc nhĩ, rán vàng rồi om sốt cà chua – trẻ em rất thích.", 40, "de", [
        "Nấm hương, mộc nhĩ ngâm mềm, băm nhỏ, trộn với thịt xay, chút gia vị và 1–2 thìa bột mì cho viên dễ kết dính.",
        "Viên thành từng viên nhỏ, rán sơ đến khi hơi vàng.",
        "Phi hành, cho cà chua bổ múi cau vào xào nát với chút nước mắm, đường, thêm ít nước.",
        "Thả thịt viên vào om lửa nhỏ đến khi chín và thấm sốt; rắc hành lá."]),
    "suon_ram_man_ngot": ("Sườn non ram nước màu, mặn ngọt sệt bóng.", 40, "de", [
        "Thắng 1 thìa đường với dầu đến khi màu cánh gián, cho hành tỏi băm vào.",
        "Cho sườn vào đảo đến khi săn và xém các mặt, thêm ít nước.",
        "Nêm nước mắm, đường, chút muối, tiêu; khi sôi hạ lửa nhỏ, ram đến khi nước cạn sệt, sườn bóng; nêm lại cho vừa."]),
    "cha_la_lot": ("Thịt băm trộn lá lốt thái nhỏ, nặn viên rán vàng – thơm mùi lá lốt.", 35, "de", [
        "Lá lốt ngâm nước muối, rửa sạch, thái nhỏ; hành tây băm.",
        "Trộn thịt băm với lá lốt, hành tây, chút hạt nêm, tiêu, nước mắm và 1 quả trứng.",
        "Nặn thành viên dẹt, rán lửa vừa đến khi chín vàng hai mặt; ăn nóng với cơm."]),
    "thit_heo_kho_tieu": ("Thịt heo kho tiêu đậm vị, nước kho sệt cay nhẹ.", 40, "de", [
        "Thịt thái lát mỏng, ướp nước mắm, đường, hành tỏi băm, nhiều tiêu khoảng 15 phút.",
        "Phi thơm hành tỏi, cho thịt vào đảo săn.",
        "Thêm chút nước, kho lửa nhỏ đến khi thịt chín mềm, nước sệt lại; rắc tiêu, hành lá."]),
    "ca_loc_kho_to": ("Cá lóc kho tộ với ba chỉ, gừng, riềng – nước kho sánh, đậm đà.", 60, "vua", [
        "Cá lóc làm sạch, cắt khúc; ướp với gia vị kho cá (hoặc nước mắm, đường, tiêu) 15–20 phút.",
        "Chiên sơ cá cho săn, cuối cùng phi vàng hành tỏi cùng.",
        "Lót ba chỉ thái miếng dày dưới đáy nồi đất, rải gừng, riềng thái lát, ớt, hành tỏi phi; xếp cá lên trên.",
        "Đổ nước ngập mặt cá cùng phần nước ướp, kho lửa nhỏ đến khi nước gần cạn, sánh lại; thả hành lá, đậy nắp 5 phút."]),
    "ca_kho_rieng": ("Cá kho riềng sả kiểu Bắc, kho lửa nhỏ nhiều lần cho chắc thịt, thấm vị.", 90, "vua", [
        "Cá làm sạch, cắt khúc; riềng thái lát, sả đập dập, gừng đập, ớt băm; ba chỉ thái lát.",
        "Ướp cá với gia vị kho riềng (hoặc nước mắm, đường, chút muối) cùng một phần riềng sả gừng ít nhất 45 phút.",
        "Làm nước màu; xếp lần lượt riềng sả gừng, ba chỉ, cá và phần riềng sả còn lại vào nồi.",
        "Đổ nước ngập cá, sôi thì hạ lửa thật nhỏ, kho 30–40 phút; không đảo để cá khỏi nát; để nguội rồi kho thêm lần nữa cho đậm."]),
    "ca_hoi_sot_ca_chua": ("Cá hồi áp chảo rồi rim trong sốt cà chua nước mắm.", 30, "de", [
        "Cá hồi rửa nhanh, thấm khô, cắt khúc vừa ăn.",
        "Áp chảo cá lửa vừa, rán kỹ phần da cho giòn, phần thịt vừa chín tới để khỏi khô.",
        "Thấm bớt dầu, phi hành tỏi, cho cà chua băm vào xào mềm.",
        "Hòa nước mắm, đường với ít nước rưới vào, đậy nắp rim lửa nhỏ, thỉnh thoảng trở cá, đến khi sốt sệt; rắc tiêu."]),
    "ca_dieu_hong_hap_nam_kim_cham": ("Cá diêu hồng hấp gừng với nấm kim châm, rau thơm – thanh nhẹ.", 35, "de", [
        "Cá làm sạch bằng muối, giấm; khứa thân cá; chà gừng băm lên cá.",
        "Ướp cá với chút nước mắm và dầu ăn, xếp lên đĩa, rải nấm kim châm xung quanh.",
        "Hấp cách thủy khoảng 20 phút đến khi cá chín.",
        "Rắc hành lá, thì là, rau răm và tiêu, hấp thêm 2 phút rồi ăn nóng."]),
    "ca_chim_hap_xi_dau": ("Cá chim ướp xì dầu, hấp cùng gừng hành – thơm, ngọt thịt.", 60, "vua", [
        "Cá làm sạch, ngâm nước muối loãng rồi rửa lại, để ráo; hành tím, tỏi thái lát; gừng, ớt thái sợi.",
        "Phi vàng hành, tỏi, gừng băm, chắt ráo dầu.",
        "Pha sốt xì dầu, dầu hào, chút đường, dầu mè, cho thêm hành tỏi lát, một nửa gừng sợi và một nửa phần phi; xoa đều lên cá, ướp 30 phút.",
        "Hấp cách thủy 20 phút, rải gừng, ớt sợi, hành tây, hành lá lên, hấp thêm 3 phút; rưới nốt phần hành gừng phi."]),
    "ca_bac_ma_kho_thom": ("Cá bạc má kho với thơm và ớt – chua ngọt, thơm, ăn với cơm nóng.", 45, "de", [
        "Cá bóp muối giấm rửa sạch, cắt đôi; ướp với muối và đầu hành 30 phút rồi chắt bỏ nước.",
        "Phi thơm đầu hành, cho cá cùng nước mắm, đường, hạt nêm và khoảng 1 chén nước vào kho.",
        "Khi nước hơi cạn, thêm thơm thái miếng và ớt, kho tiếp đến khi thấm; rắc hành lá, tiêu."]),
    "ca_thu_nuong_muoi_tieu": ("Cá thu ướp muối tiêu nướng vàng – đơn giản, giữ vị ngọt cá biển.", 45, "de", [
        "Cá thu rửa sạch, thấm khô, ướp muối tiêu ít nhất 30 phút.",
        "Nướng than hoặc lò/nồi chiên không dầu 200°C khoảng 25–30 phút, trở mặt giữa chừng đến khi vàng đều.",
        "Ăn kèm dưa leo, rau luộc và nước mắm chanh ớt."]),
    "cha_ca_sot_ca_chua": ("Chả cá chiên sơ rồi rim sốt cà chua – nhanh gọn, trẻ em thích.", 25, "de", [
        "Chả cá cắt miếng vừa ăn, chiên sơ vàng 2 mặt.",
        "Xay cà chua với tương cà, tương ớt, đường, nước mắm, hạt nêm (không có máy xay thì băm nhỏ cà chua).",
        "Phi thơm tỏi trong chảo vừa chiên, đổ sốt cà chua vào đun sôi.",
        "Cho chả cá và vài lát ớt vào rim 5 phút cho thấm; nêm lại, rắc hành lá, ngò."]),
    "kho_ca_chi_vang_rim_chua_ngot": ("Khô cá chỉ vàng rim với hành sả tỏi và nước mắm chua ngọt – món hàng khô cho mùa biển động.", 20, "de", [
        "Khô cá cắt miếng nhỏ; hành, sả, tỏi băm.",
        "Phi thơm hành sả tỏi với ít dầu, cho cá vào đảo lửa nhỏ khoảng 2 phút.",
        "Rưới nước mắm chua ngọt (nước mắm, đường, chanh, nước), tăng lửa đảo nhanh đến khi sốt bám đều và cạn."]),
    "ca_thu_sot_ca_chua": ("Cá thu chiên vàng rồi rim sốt cà chua hành tỏi.", 35, "de", [
        "Cá thu ướp chút muối 15 phút, chiên vàng 2 mặt rồi gắp ra.",
        "Phi hành tỏi, cho cà chua thái hạt lựu vào xào cùng nửa chén nước, nêm nước mắm, đường cho vừa.",
        "Cho cá trở lại chảo, rim lửa nhỏ, trở mặt sau 5 phút để cá thấm sốt; rắc hành lá, tiêu."]),
    "ca_ngu_kho_tieu": ("Cá ngừ chiên sơ rồi kho tiêu đậm đà, nước kho sệt.", 45, "de", [
        "Cá ngừ rửa sạch, cắt miếng; phi hành tỏi rồi chiên sơ cá cho săn.",
        "Ướp cá với nước mắm, đường, dầu hào và nhiều tiêu khoảng 10 phút.",
        "Thêm 1 chén nước, kho lửa vừa, trở đều 2 mặt; khi nước rút thì thêm hành lá, ớt và hạ lửa thật nhỏ 10 phút cho thấm."]),
    "ca_nuc_kho_ca_chua": ("Cá nục kho cà chua – món quen của dân biển, cá chắc, nước kho chua ngọt.", 40, "de", [
        "Cá nục chà muối, rửa sạch, để ráo; cà chua cắt múi; hành tím, tỏi băm.",
        "Chiên sơ cá 2 mặt, cho hành tỏi vào phi thơm rồi xếp cà chua xen giữa cá.",
        "Pha 2 thìa nước mắm, 1 thìa đường, chút hạt nêm và vài thìa nước, rưới vào, kho lửa nhỏ đến khi nước sệt; rắc tiêu, hành lá."]),
    "cha_ca_thu_chien": ("Chả cá thu quết mỏng chiên vàng – đặc sản biển Nha Trang, Phan Rang.", 30, "de", [
        "Trộn chả cá thu với hành tím băm, tiêu, chút muối, bột nêm; để 15 phút cho thấm.",
        "Nhúng tay qua dầu, quết chả thành miếng tròn mỏng.",
        "Chiên lửa vừa đến khi vàng 2 mặt; ăn với cơm hoặc bánh mì."]),
    "ca_com_kho_rim_dau_phong": ("Cá cơm khô rang giòn rim chua ngọt, thêm đậu phộng và lá chanh – hàng khô cất được lâu.", 25, "de", [
        "Rang cá cơm khô cho vàng giòn, sàng bớt vụn; rang đậu phộng riêng.",
        "Pha nước rim: đường, nước mắm, chút nước cốt chanh, tương ớt và ít nước.",
        "Phi tỏi, cho cá và nước rim vào đảo lửa nhỏ đến khi cạn, bám đều; thêm đậu phộng, lá chanh thái chỉ rồi tắt bếp."]),
    "ca_thu_chien_sa": ("Cá thu chiên mỡ với gừng sả, giòn mặt, không tanh.", 25, "de", [
        "Cá thu rửa với nước pha giấm muối, thấm thật khô, xoa chút muối 2 mặt.",
        "Đun nóng mỡ heo, phi sơ gừng và sả đập dập cho thơm.",
        "Cho cá vào chiên, đặt lát gừng lên mặt cá; vàng một mặt thì lật, chiên lửa hơi lớn không đậy nắp cho giòn; để lên giấy thấm dầu."]),
    "dau_hap_tom_thit_sot_chua_ngot": ("Đậu phụ non xếp lớp với nhân tôm thịt nấm, hấp chín rồi rưới sốt chua ngọt.", 50, "vua", [
        "Đậu phụ thái lát ngang; tôm thái hạt lựu; nấm hương ngâm nở thái chỉ.",
        "Trộn thịt xay, tôm, nấm, trứng với chút hạt nêm, tiêu.",
        "Xếp xen kẽ lớp đậu, lớp nhân trên đĩa; hấp lửa vừa 20–30 phút đến khi nhân chín.",
        "Phi hành tỏi, đun sốt đường, dầu hào, nước tương, giấm hoặc chanh với ít nước đến khi sánh; rưới lên đậu, ăn nóng."]),
    "muc_xao_dua": ("Mực khứa vảy rồng xào dứa, cà chua, cần tỏi – chua ngọt giòn.", 25, "de", [
        "Mực làm sạch, khứa chéo mặt trong, thái miếng 2cm.",
        "Dứa thái lát mỏng, cà chua bổ múi cau, cần tây và tỏi tây cắt khúc.",
        "Xào cà chua và dứa lửa to đến khi dứa hơi trong.",
        "Cho mực vào, nêm hạt nêm, tiêu, đảo nhanh đến khi mực vừa trắng; thêm cần tỏi đảo đều rồi tắt bếp."]),
    "tom_thit_rim_man_ngot": ("Tôm và thịt ba chỉ rim nước màu – món mặn quen thuộc miền Nam.", 40, "de", [
        "Thịt cắt miếng nhỏ, xào cho ra bớt mỡ và săn lại.",
        "Tôm cắt râu, rút chỉ; ướp với hành băm, chút muối, hạt nêm 30 phút.",
        "Cho tôm vào chảo thịt cùng nước màu, nước mắm, đường; rim đến khi tôm thịt keo lại, bóng.",
        "Nêm lại, thêm hành lá, tiêu."]),
    "sua_tron_mam_nhi": ("Sứa trụng giòn trộn cà pháo và sốt mắm nhĩ chua cay – món mát mùa sứa (tháng 3–6).", 40, "vua", [
        "Nấu sốt: đường, mắm nhĩ, nước lọc, nước chanh, tương ớt, bột ớt khuấy đều đun sôi; để thật nguội (giữ tủ lạnh được 1 tuần).",
        "Sứa trụng nhanh qua nước sôi rồi thả ngay vào nước đá.",
        "Cà pháo thái mỏng, ngâm nước chanh muối loãng.",
        "Trộn sứa, cà pháo với sốt, thêm tắc, ớt nếu ăn cay; ngâm 20 phút rồi ăn."]),
    "ngheu_hap_sa": ("Nghêu hấp sả gừng, chấm nước mắm gừng chanh ớt.", 30, "de", [
        "Ngâm nghêu với nước vo gạo và vài lát ớt 1–2 tiếng cho nhả cát, rửa sạch.",
        "Sả cắt khúc đập dập, gừng thái lát, ớt cắt lát; lót dưới đáy nồi, xếp nghêu lên.",
        "Thêm chút nước, nước mắm, dầu ăn, đậy nắp hấp lửa lớn đến khi nghêu mở miệng.",
        "Giã gừng, tỏi, ớt với đường, pha nước mắm và chanh làm nước chấm."]),
    "muc_hap_hanh_gung": ("Mực nang hấp hành gừng, giòn ngọt, chấm nước mắm gừng.", 30, "de", [
        "Mực làm sạch (bỏ túi mực, nội tạng, xương), chà nước muối loãng rồi rửa lại.",
        "Lót gừng thái lát, hành lá cắt khúc dưới khay, đặt mực lên, phủ phần hành gừng còn lại và chút rượu trắng.",
        "Hấp khoảng 15–20 phút đến khi mực chín vừa (hấp lâu sẽ dai).",
        "Thái mực thành lát, chấm nước mắm gừng hoặc mắm ruốc, ăn kèm rau sống."]),
    "oc_huong_luoc": ("Ốc hương luộc sả lá chanh, chấm mắm gừng hoặc muối ớt xanh.", 25, "de", [
        "Ốc hương rửa sạch; nên luộc trong ngày mua.",
        "Đun sôi nước với sả đập dập; sôi bùng thì cho ốc vào, đậy nắp lửa lớn.",
        "Nước trào thì hạ lửa vừa, thêm lá chanh, ớt, đảo một lần; khoảng 5 phút lấy tăm khều thử thấy ruột ra dễ là chín.",
        "Pha mắm gừng: gừng ớt giã, nước mắm, đường, vắt tắc; hoặc muối ớt xanh."]),
    "tom_rang_muoi": ("Tôm rang muối hột với sả ớt lá chanh – thơm, đậm vị.", 25, "de", [
        "Tôm làm sạch, để thật ráo; sả cắt khúc, ớt thái nhỏ.",
        "Rang muối hột trong chảo nóng đến khi muối hơi vàng.",
        "Thêm sả, ớt, lá chanh đảo dậy mùi, cho tôm vào đảo liên tục lửa lớn đến khi tôm chín đỏ, thấm muối.",
        "Bày ra đĩa, chấm muối ớt xanh."]),
})
