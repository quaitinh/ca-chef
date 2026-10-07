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

# ---------- Lô B ----------
CL.update({
    "cha_muc": ("Chả mực quết dai giòn, vàng ruộm, ngọt thịt mực, trẻ con rất mê.", 60, "vua", [
        "Mực bỏ đầu, ruột, túi mực và lột da cho trắng, rồi bóp với rượu trắng, rửa lại cho hết tanh.",
        "Thấm thật khô mực, cắt nhỏ rồi xay sơ; trộn cùng nước mắm, hạt nêm, đường, hành tím và tỏi băm, để ngăn đá khoảng 30 phút cho mực se lạnh.",
        "Cho mực vào máy xay quết khoảng 5–6 phút đến khi dẻo, thêm bột khoai tây quết thêm chút cho kết dính.",
        "Xoa dầu vào tay, lấy từng thìa mực vo tròn rồi ấn dẹt.",
        "Chiên chả trong chảo dầu lửa vừa đến khi hai mặt vàng đều, vớt ra để ráo dầu, ăn với cơm hoặc xôi."]),
    "tom_hap_nuoc_dua": ("Tôm hấp nước dừa ngọt thanh, thơm mùi dừa xiêm, bày ngay trong quả dừa.", 25, "de", [
        "Tôm rửa sạch, cắt râu, để ráo; chọn tôm còn sống để khi chín không rụng đầu.",
        "Gọt vỏ dừa xiêm, vạt nắp chắt lấy nước, giữ lại quả dừa để làm bát đựng.",
        "Đun nước dừa với chút hạt nêm đến khi sôi, thả tôm vào đến khi đỏ đều thì vớt ra.",
        "Xếp tôm vào quả dừa, rót nước hấp vào, rắc cà rốt bào và ngò quanh, ăn nóng."]),
    "ghe_hap_gung_sa": ("Ghẹ hấp sả thơm lừng, thịt chắc ngọt, chấm muối tiêu chanh là đủ vị.", 25, "de", [
        "Ghẹ chà rửa sạch; sả đập dập, cắt khúc lót đáy nồi.",
        "Xếp ghẹ lên trên sả, chế bia hoặc nước lọc vào, đậy kín nắp.",
        "Hấp lửa lớn 12–15 phút tùy cỡ ghẹ, đến khi vỏ chuyển đỏ cam là chín.",
        "Gắp ghẹ ra đĩa, chấm muối tiêu chanh hoặc muối ớt chanh; phần của bé tách thịt sẵn cho dễ ăn."]),
    "so_diep_nuong_mo_hanh": ("Sò điệp nướng mỡ hành, rắc lạc rang, rưới nước mắm chua ngọt béo thơm.", 40, "vua", [
        "Rửa sạch sò điệp, ngâm nước muối loãng cho nhả cát.",
        "Đun sôi nồi nước với vài lát gừng và sả, trần sò qua để khử tanh rồi vớt ra, bỏ bớt một mảnh vỏ.",
        "Thái nhỏ hành lá, rưới dầu nóng lên làm mỡ hành; lạc rang giã dập; pha nước mắm với giấm, đường, bột nêm và tỏi đập.",
        "Nướng sò bằng lò hoặc nồi chiên không dầu 160°C khoảng 15 phút, rưới mỡ hành lên rồi nướng thêm 3 phút.",
        "Bày sò ra đĩa, rắc lạc và chan chút nước mắm lên mặt, ăn nóng."]),
    "muc_ong_nhoi_thit_sot_ca": ("Mực ống nhồi thịt mộc nhĩ, rim trong sốt cà chua sánh đậm, rất đưa cơm.", 50, "vua", [
        "Mực làm sạch, giữ nguyên ống, râu băm nhỏ; mộc nhĩ ngâm nở, thái nhỏ.",
        "Phi thơm hành tỏi, xào sơ thịt xay với mộc nhĩ và râu mực, nêm nước mắm, tiêu, trộn thêm hành lá.",
        "Nhồi nhân vào ống mực chừng hai phần ba, gài tăm miệng rồi hấp 10 phút, giữ lại nước hấp.",
        "Xào cà chua băm đến khi nhừ, cho mực và nước hấp vào rim 5 phút, nêm nước mắm, hạt nêm.",
        "Hòa chút bột năng với nước, đổ vào cho sốt sánh lại rồi tắt bếp; thái khoanh mực khi dọn ra."]),
    "cua_rang_me": ("Cua rang me chua ngọt sền sệt, gạch cua béo ngậy, chấm bánh mì cực bắt.", 50, "kho", [
        "Ướp lạnh cua sống khoảng 30 phút cho cua lịm, tách mai, bỏ yếm và phổi, thân chặt đôi, càng đập dập.",
        "Khều gạch cua ra bát riêng; ngâm me với nước ấm, bóp tan rồi lọc lấy nước.",
        "Chiên cua với ít dầu ở lửa lớn đến khi vỏ đỏ, vớt ra.",
        "Phi hành khô, cho gạch cua vào xào sệt, nêm nước mắm và đường rồi đổ nước me vào đun sôi.",
        "Cho cua vào rim lửa vừa, đảo đều đến khi sốt me sánh bám vào cua.",
        "Múc phần của trẻ ra trước, phần còn lại mới thêm ớt tươi thái nhỏ."]),
    "nom_ga_rau_thom": ("Nộm gà xé trộn hành tây, rau răm, rau mùi chua ngọt, thanh mát ngày hè.", 60, "de", [
        "Luộc gà chín đều, vớt ra để nguội rồi xé hoặc cắt sợi vừa ăn.",
        "Hành tây thái lát, trần qua nước sôi hoặc nước luộc gà khoảng 10 phút cho bớt hăng mà vẫn giòn, vớt ra để ráo.",
        "Nhặt xà lách, rau răm, rau mùi, ngâm nước muối loãng rồi rửa sạch, để ráo.",
        "Bóp gà với bột canh, đường, nước cốt chanh và ớt thái nhỏ cho ngấm, nêm lại cho vừa.",
        "Cho hành tây và rau thơm vào trộn nhẹ tay, bày lên đĩa lót xà lách; phần của bé để riêng trước khi cho ớt."]),
    "canh_ga_nuong_sa": ("Cánh gà nướng sả vàng óng, thơm sả, mặn ngọt đậm đà.", 150, "de", [
        "Cánh gà rửa sạch, thấm khô; sả lấy phần non, bào mỏng rồi trộn với chút dầu ăn.",
        "Trộn dầu hào, gia vị, tiêu, nước tương và đường, cho cánh gà vào ướp khoảng 2 tiếng.",
        "Làm nóng lò, xếp cánh gà lên khay, rải sả bào lên mặt.",
        "Nướng 180–200°C khoảng 20–25 phút, giữa chừng trở mặt và quét lại phần nước ướp đến khi gà vàng đều."]),
    "thit_ga_sot_chua_ngot": ("Gà chiên giòn đảo sốt cà chua ớt chuông chua ngọt, màu sắc bắt mắt.", 40, "vua", [
        "Má đùi gà cắt miếng vừa ăn, ướp chút muối khoảng 10 phút.",
        "Lăn gà qua bột chiên giòn, chiên ngập dầu đến khi vàng giòn rồi vớt ra để ráo.",
        "Ớt chuông và cà chua cắt hạt vuông.",
        "Phi nóng dầu mè, xào cà chua đến mềm rồi cho ớt chuông vào, nêm giấm, đường, muối thành sốt chua ngọt vừa miệng.",
        "Trút gà vào đảo nhanh cho sốt áo đều, bày ra đĩa và rắc mè đen."]),
    "vit_chay_toi": ("Ngan chiên vàng ướp ngũ vị, phủ tỏi phi giòn rụm, thơm nức cả nhà.", 70, "vua", [
        "Ngan bóp với gừng, rượu và muối rồi rửa sạch, để ráo, chặt miếng vừa ăn; tỏi chia hai phần, một phần băm, một phần thái lát.",
        "Ướp ngan với tỏi băm, gừng băm, ngũ vị hương, rượu mai quế lộ, hạt nêm, đường, nước tương khoảng 30 phút.",
        "Đun nóng dầu, chiên ngan đến khi chín vàng, vớt ra để ráo dầu.",
        "Tắt bếp, thả tỏi lát vào dầu còn nóng chiên đến khi vàng giòn rồi vớt ra.",
        "Xếp ngan ra đĩa, phủ tỏi phi lên, ăn kèm rau húng, ngò gai và nước mắm gừng; ớt để riêng cho người lớn."]),
    "ga_xao_ngo": ("Gà chiên bột đảo cùng ngô ngọt và xúc xích trong sốt bơ mặn ngọt, trẻ con rất thích.", 40, "de", [
        "Tách hạt ngô, luộc sơ cùng xúc xích thái khoanh rồi vớt ra.",
        "Gà cắt miếng nhỏ, lăn qua bột bắp, chiên vàng rồi vớt ra để ráo dầu.",
        "Cho bơ vào chảo, xào ngô và xúc xích đến khi thơm.",
        "Pha sốt gồm đường, tương ớt, nước mắm và khoảng 150ml nước, đổ vào chảo đun sôi.",
        "Cho gà vào đảo đến khi sốt sánh lại và áo đều miếng gà; nhà có bé thì giảm tương ớt."]),
    "canh_ga_chien_nuoc_mam": ("Cánh gà chiên hai lần giòn rụm, áo nước mắm tỏi chua ngọt bóng đẹp.", 60, "vua", [
        "Cánh gà rửa sạch, chặt đôi, ướp với tiêu, hạt nêm và gừng xay khoảng 30 phút.",
        "Cho gà vào túi cùng bột khoai tây và bột năng, lắc đều cho bột bám kín.",
        "Phi tỏi vàng rồi vớt ra; thêm dầu, chiên cánh gà vàng đều, sau đó chiên lại lần nữa cho giòn hơn.",
        "Pha nước mắm, đường, nước cốt chanh, ớt xay với nửa bát nước, đun trong chảo đến khi sánh.",
        "Trút cánh gà và tỏi phi vào đảo nhanh cho sốt bám đều, rắc hành lá; phần của bé bỏ ớt."]),
    "vit_nau_thom": ("Vịt nấu thơm với nước dừa, khoai, nấm và huyết, nước dùng chua ngọt đậm đà.", 120, "kho", [
        "Vịt chặt miếng, ướp với sa tế, nước mắm, đường, bột ngọt, tiêu, hành tỏi xay và gừng sợi khoảng 1 tiếng.",
        "Thơm, cà rốt, khoai tây cắt miếng; sả đập dập; nấm đông cô ngâm mềm; huyết vịt cắt miếng.",
        "Phi hành tỏi, sả và gừng với dầu ăn và dầu điều, cho vịt vào xào lửa lớn 7–10 phút cho săn.",
        "Đổ nước dừa và thêm nước lọc xăm xắp, nêm muối, đường rồi hầm đến khi vịt mềm.",
        "Lần lượt cho nấm, cà rốt, khoai tây, cách nhau 5 phút; sau đó thêm thơm, huyết và hành tím, nấu thêm 10 phút.",
        "Nêm lại vừa miệng, rắc ngò gai, ăn với bún hoặc bánh mì; nhà có bé thì giảm sa tế."]),
    "cha_uc_ga_nam_huong": ("Chả ức gà nấm hương mềm mọng, lẫn rau củ nhiều màu, hợp cho bé.", 60, "de", [
        "Luộc chín nấm hương và rau củ đông lạnh, thái hạt lựu; hành lá thái nhỏ.",
        "Băm nhỏ ức gà, trộn với rau củ, nấm, hành lá và đậu hũ non bóp nhuyễn.",
        "Nêm xì dầu, hắc xì dầu, rượu nấu ăn, dầu hào, tiêu, muối và bột bắp, trộn đều rồi ướp 30 phút.",
        "Nặn hỗn hợp thành miếng chả dẹt vừa ăn.",
        "Rán chả với ít dầu ở lửa vừa đến khi hai mặt vàng đều và chín tới bên trong."]),
    "dui_ga_rut_xuong_ap_chao": ("Đùi gà rút xương áp chảo da giòn, thơm sả ớt, ăn kèm salad mỡ gà.", 60, "vua", [
        "Ướp đùi gà với nước mắm, muối, xì dầu cùng một nửa hành, tỏi, sả, ớt băm trong 30 phút.",
        "Nướng gà trong nồi chiên không dầu 180°C khoảng 15 phút, mặt thịt hướng lên.",
        "Phi thơm phần hành, tỏi, sả, ớt còn lại, cho gà vào áp chảo lửa vừa 10 phút, cuối cùng tăng lửa cho da giòn.",
        "Lấy gà ra thái miếng, giữ lại mỡ gà trong chảo.",
        "Trộn xà lách, dưa chuột, cà chua với chút mỡ gà, bày ra đĩa rồi xếp gà lên trên; phần của bé bớt ớt."]),
    "ga_kho_gung": ("Gà kho gừng mặn ngọt, thơm ấm, thịt săn thấm vị, ăn với cơm nóng.", 50, "de", [
        "Gà chặt miếng, ướp với nước mắm, nước tương, tiêu, hạt nêm và đường khoảng 30 phút; gừng thái sợi.",
        "Phi thơm đầu hành và gừng, cho gà vào đảo đến khi thịt săn lại.",
        "Thêm nước xăm xắp, đậy nắp kho lửa vừa đến khi gà mềm và nước sánh.",
        "Nêm lại cho vừa, thả hành lá cắt khúc, múc ra đĩa và rắc tiêu."]),
    "ga_om_nam": ("Gà om nấm đông cô với nước dừa, ngọt dịu, nước sốt thơm béo.", 50, "de", [
        "Gà cắt miếng vừa ăn, ướp với bột hành, bột tỏi và gia vị khoảng 20 phút.",
        "Nấm đông cô ngâm nở, rửa sạch, cắt đôi; cà rốt thái miếng.",
        "Hấp gà đến khi vừa chín tới.",
        "Phi thơm hành tím và tỏi, cho gà, nấm, cà rốt vào đảo sơ, đổ nước dừa vào om lửa nhỏ đến khi gà mềm và nước hơi sánh.",
        "Nêm lại, rắc hành lá, ngò và tiêu rồi tắt bếp."]),
    "ca_ri_ga": ("Cà ri gà ít cay, nước cốt dừa béo ngậy, khoai cà rốt bùi mềm, hợp cả nhà.", 80, "vua", [
        "Gà chặt miếng, ướp với muối, đường, bột canh, nước mắm, ngũ vị hương, tiêu, sả băm, hành tỏi băm khoảng 30 phút.",
        "Cà rốt, khoai tây, hành tây cắt miếng vuông; sả còn lại cắt khúc đập dập; dừa nạo ngâm nước ấm rồi vắt lấy nước cốt.",
        "Phi thơm hành tỏi, cho gà vào xào săn, đổ nước xăm xắp, thả sả vào đun sôi.",
        "Cho cà rốt vào trước, sôi lại thì thêm khoai tây và hành tây, nấu đến khi khoai vừa mềm.",
        "Thêm nước cốt dừa, sữa tươi, chút sữa đặc và cà ri, nêm vừa ăn rồi đun thêm 10 phút; múc ra bát rắc rau thơm, ăn với bánh mì hoặc bún."]),
    "vit_luoc_cham_mam_gung": ("Vịt luộc da vàng, thịt ngọt, chấm nước mắm gừng cay ấm đúng vị Bắc.", 70, "de", [
        "Gừng giã dập trộn rượu trắng, xát khắp con vịt để khử mùi, rồi rửa lại nhiều lần.",
        "Cho vịt vào nồi nước lạnh cùng gừng, chút muối và hạt nêm, luộc lửa vừa đến khi chín thì tắt bếp ủ thêm 10 phút.",
        "Vớt vịt ra để nguội rồi chặt miếng; nước luộc giữ lại nấu canh.",
        "Pha nước mắm với nước, đường, gừng giã, chút chanh và ớt làm nước chấm; bát của bé không cho ớt."]),
    "bo_xao_luc_lac": ("Bò lúc lắc mềm, xém cạnh, xào cùng ớt chuông và hành tây nhiều màu.", 50, "vua", [
        "Thịt bò rửa sạch, thấm khô, thái quân cờ khoảng 2cm, ướp bột canh và hạt tiêu 30 phút.",
        "Hành tây và ớt chuông bỏ hạt, thái miếng vuông cỡ miếng bò; tỏi băm.",
        "Xào bò với chút dầu ở lửa lớn khoảng 3 phút cho se mặt rồi trút ra.",
        "Phi tỏi, cho hành tây và ớt chuông vào xào đến khi gần chín.",
        "Trút bò trở lại, đảo nhanh tay lửa to, nêm vừa ăn rồi tắt bếp; ăn với cơm hoặc bánh mì."]),
    "bo_kho": ("Bò kho mềm nhừ, thơm quế hồi, nước sốt cà chua sánh, chấm bánh mì rất ngon.", 120, "vua", [
        "Khoai tây và cà rốt gọt vỏ, cắt miếng to; khoai ngâm nước cho khỏi thâm; hành tây, sả cắt khúc đập dập.",
        "Thịt bò cắt miếng vuông, phi thơm hành tây và sả rồi cho bò vào xào săn, nêm chút muối.",
        "Rắc bột mì vào đảo đều, thêm cà chua cô đặc xào cho ngấm màu.",
        "Đổ khoảng 1,5 lít nước, thả quế, hồi, thảo quả, lá nguyệt quế; sôi thì hớt bọt rồi hạ lửa liu riu 1–1,5 tiếng đến khi bò mềm.",
        "Cho cà rốt rồi khoai tây vào nấu đến khi chín mềm, nêm Knorr, đường, tiêu vừa ăn.",
        "Múc ra bát, rắc hành lá, ăn kèm bánh mì hoặc bún."]),
    "bap_bo_ngam_chua_ngot": ("Bắp bò luộc thái mỏng ngâm nước mắm chua ngọt gừng tỏi, giòn sần sật.", 75, "de", [
        "Bắp bò rửa sạch, khứa nhẹ quanh miếng nếu quá dày; gừng cạo vỏ.",
        "Luộc bắp bò với phần lớn gừng đập dập, tiêu hạt và bột canh đến khi xiên đũa không còn nước đỏ chảy ra; không luộc quá lâu kẻo bò dai.",
        "Pha sốt từ nước mắm, nước lạnh, đường, gừng còn lại giã nhỏ, tỏi băm, ớt, nước chanh và nước quất.",
        "Thái bắp bò thật mỏng, xếp vào đĩa sâu lòng rồi chan sốt lên.",
        "Để ngấm khoảng 15 phút rồi dọn ăn; múc phần của bé ra trước khi cho ớt."]),
    "bap_bo_hap_sa_gung": ("Bắp bò hấp sả gừng thơm dịu, thái mỏng chấm nước mắm gừng tỏi.", 40, "de", [
        "Bắp bò rửa với nước muối; sả cắt khúc đập dập, một củ gừng thái lát.",
        "Đun sôi nồi hấp, lót sả và gừng lát lên xửng, đặt bắp bò lên trên.",
        "Hấp khoảng 15–20 phút, xiên đũa thấy không còn nước đỏ là chín, vớt ra để ráo.",
        "Băm tỏi và gừng còn lại, pha với nước sôi, nước mắm, đường, giấm hoặc chanh và chút ớt băm làm nước chấm.",
        "Thái bắp bò lát mỏng, bày ra đĩa, ăn kèm nước chấm."]),
    "bo_xao_mang_tay": ("Bò xào măng tây xanh giòn, thịt mềm, thơm tỏi phi, làm nhanh trong 20 phút.", 20, "de", [
        "Thịt bò thái lát mỏng, ướp dầu hào, nước tương và chút dầu ăn; măng tây bỏ gốc già, cắt khúc.",
        "Phi thơm tỏi băm, cho bò vào xào nhanh lửa lớn rồi trút ra đĩa.",
        "Cho măng tây vào chảo, thêm chút nước, nước tương và hạt nêm, xào đến khi măng vừa chín còn xanh.",
        "Trút bò vào đảo đều, rắc tiêu và tỏi phi rồi tắt bếp."]),
    "bo_xao_hanh_tay": ("Bò xào hành tây mềm ngọt, đậm vị xì dầu, món nhanh cho bữa tối.", 20, "de", [
        "Thịt bò thái lát mỏng ngang thớ; hành tây bổ múi cau; tỏi đập dập.",
        "Phi tỏi với dầu ăn cho thơm, cho bò vào xào lửa lớn đến khi vừa tái.",
        "Nêm xì dầu, muối hồng, chút bột ngọt, tiêu rồi cho hành tây vào đảo nhanh tay.",
        "Khi hành tây vừa chín tới, nêm lại cho vừa, múc ra đĩa và rắc tiêu."]),
    "bo_vien_sot_ca_chua": ("Bò viên mềm áp chảo xém cạnh, om sốt cà chua húng quế thơm kiểu Ý.", 60, "vua", [
        "Hành tây thái hạt lựu; vụn bánh mì ngâm sữa; cà chua bỏ vỏ, xay với ít nước; tỏi và parsley băm, basil thái chỉ.",
        "Phi một nửa tỏi với dầu, cho một nửa hành tây và chút ớt bột vào đảo chín, để nguội.",
        "Trộn bò xay với vụn bánh mì, hành xào, parsley, muối, tiêu, nhồi kỹ rồi vo viên và chiên xém cạnh.",
        "Phi tỏi và hành tây còn lại, cho cà chua xay, tương cà, paprika, muối, tiêu, chút đường và basil vào nấu sôi.",
        "Thả bò viên vào sốt, hạ lửa om khoảng 20–30 phút đến khi sốt sánh; nhà có bé thì bỏ bớt ớt bột."]),
    "trung_chien_nuoc_mam": ("Trứng ốp lòng đào rim sốt nước mắm sền sệt, mặn ngọt, cực tốn cơm.", 15, "de", [
        "Pha nước mắm, đường, tương ớt và nước lọc trong bát, khuấy tan; hành lá thái nhỏ.",
        "Đun nóng dầu, đập trứng vào ốp lòng đào, rắc hành lá lên mặt.",
        "Rưới sốt mắm vào chảo, đun lửa nhỏ đến khi sốt sánh lại và bám vào trứng thì tắt bếp.",
        "Ăn nóng với cơm; phần của bé có thể bỏ tương ớt."]),
    "trung_chung_ca_chua": ("Trứng chưng cà chua mềm mướt, chua dịu, món quen của mâm cơm Bắc.", 15, "de", [
        "Cà chua băm nhỏ; hành khô băm, hành lá thái nhỏ; trứng đập ra bát đánh tan.",
        "Phi thơm hành khô, cho cà chua vào xào lửa nhỏ khoảng 1–2 phút đến khi mềm.",
        "Đổ trứng từ từ vào chảo, để vài giây cho mặt trứng se rồi mới đảo nhẹ, nêm nước mắm.",
        "Đảo khoảng 3 phút cho trứng chín mềm thành từng mảng, thêm nhúm đường và hành lá.",
        "Múc ra đĩa, rắc chút hạt tiêu, ăn với cơm nóng."]),
    "dau_hu_nhoi_thit_sot_ca_chua": ("Đậu nhồi thịt mộc nhĩ áp chảo, rim sốt cà chua đỏ au, món quen nhà Bắc.", 60, "vua", [
        "Ngâm mộc nhĩ cho nở rồi băm nhỏ; trộn thịt xay với hành tây băm, hành lá, mộc nhĩ, nước mắm và tiêu, ướp 15 phút.",
        "Khoét nhẹ phần giữa mỗi miếng đậu, chừa thành và đáy đủ dày; nhồi nhân vào vừa đầy, không ép chặt.",
        "Áp chảo mặt có nhân xuống trước cho thịt săn, rồi lật nhẹ các mặt còn lại đến khi vàng.",
        "Phi tỏi, xào cà chua đến khi nhừ, nêm nước mắm, tương cà và thêm chút nước.",
        "Xếp đậu vào sốt, rim lửa nhỏ khoảng 10 phút, thỉnh thoảng rưới sốt lên mặt rồi dọn ăn với cơm."]),
    "dau_hu_trung_sot_nam": ("Đậu hũ trứng mềm mịn phủ sốt nấm rơm, nấm hương thơm bơ, hợp cho bé.", 35, "de", [
        "Đậu hũ trứng ngâm nước muối loãng 10 phút rồi cắt khoanh; nấm hương ngâm mềm, cùng nấm rơm rửa sạch và thái hạt lựu.",
        "Đun chảy bơ, phi thơm hành tím và tỏi băm.",
        "Cho nấm vào xào lửa lớn đến khi vừa chín, nêm dầu hào chay, hạt nêm nấm, chút bột ngọt, tiêu và đường.",
        "Thêm nước xăm xắp, đun sôi rồi xếp đậu vào, để lửa nhỏ khoảng 3 phút.",
        "Nhẹ tay gắp đậu ra đĩa, chan sốt nấm lên trên, rắc vài nhánh ngò."]),
    "nam_rom_kho_dau_hu": ("Nấm rơm kho đậu hũ xì dầu đậm đà, món chay mềm ngọt đưa cơm.", 30, "de", [
        "Nấm rơm cắt gốc, rửa sạch, để ráo; đậu hũ cắt miếng vừa ăn; boa rô thái nhỏ.",
        "Phi thơm boa rô với dầu ăn, cho nấm rơm vào đảo cùng xì dầu, đường, tiêu và chút bột ngọt.",
        "Khi nước sôi thì hớt bọt, thả đậu hũ vào kho lửa nhỏ khoảng 15 phút cho thấm.",
        "Nêm lại vừa miệng, múc ra đĩa, rắc ngò rí và tiêu; ớt băm để riêng cho người lớn."]),
    "trung_cut_rim_nuoc_mam": ("Trứng cút chiên vàng rim nước mắm tỏi ớt, mặn ngọt, trẻ con ăn mãi không chán.", 30, "de", [
        "Luộc chín trứng cút, ngâm nước lạnh rồi bóc vỏ, chiên sơ đến khi vàng mặt.",
        "Pha nước mắm, nước lọc, đường, tiêu và tỏi băm vào bát, khuấy tan; ớt băm để riêng.",
        "Chắt bớt dầu trong chảo, đổ nước mắm vào, đảo cho trứng thấm đều.",
        "Rim lửa nhỏ đến khi nước sốt gần cạn và bám bóng lên trứng thì tắt bếp, rắc chút ngò."]),
    "dau_phu_ran_cham_mam_hanh": ("Đậu phụ rán vàng ngâm mắm hành thơm, món dân dã đúng chất Hà Nội.", 25, "de", [
        "Chọn đậu mơ hoặc đậu non mịn, cắt miếng vuông; hành lá thái nhỏ, hành khô băm.",
        "Pha nước mắm với nước lọc và đường cho vừa miệng, cho hành khô băm vào.",
        "Rán đậu trong chảo dầu nóng đến khi vàng đều các mặt, vớt ra để ráo dầu.",
        "Thả đậu còn nóng vào bát mắm hành, rắc hành lá, ngâm vài phút cho thấm.",
        "Vớt đậu ra đĩa, rải hành từ bát nước chấm lên mặt rồi dọn ăn."]),
    "cuu_nuong": ("Sườn cừu ướp sả tỏi nướng thơm lừng, đặc sản đất Ninh Thuận.", 90, "vua", [
        "Thịt hoặc sườn cừu 1kg rửa sạch, chà muối và gừng để khử mùi, thấm khô rồi cắt miếng vừa ăn.",
        "Ướp cừu với sả, tỏi, hành tím băm, dầu hào, nước mắm, mật ong, chút ngũ vị hương và tiêu khoảng 1 tiếng.",
        "Nướng trên than hoa hoặc lò 200°C khoảng 25–30 phút, trở mặt và quét lại nước ướp cho thịt vàng đều.",
        "Pha chao hoặc muối tiêu chanh làm nước chấm, ăn kèm rau thơm, dưa leo và bánh tráng; phần của bé thái nhỏ, bỏ tiêu ớt."]),
    "kho_qua_xao_trung": ("Khổ qua xào trứng đắng nhẹ, bùi thơm, món thanh mát cho ngày nóng.", 25, "de", [
        "Khổ qua bổ đôi, nạo bỏ ruột và hạt, thái lát mỏng; hành khô, tỏi băm; hành lá cắt khúc.",
        "Đánh tan trứng với chút nước mắm, tiêu và hạt nêm.",
        "Phi thơm hành tỏi, cho khổ qua vào xào lửa lớn nếu thích giòn, nêm muối, dầu hào, hạt nêm.",
        "Đổ trứng vào, để trứng se lại rồi đảo nhẹ cho bám đều quanh khổ qua.",
        "Nêm lại vừa ăn, thả hành lá, rắc tiêu rồi tắt bếp; bột ớt để riêng cho người lớn."]),
    "bap_cai_xao_trung": ("Bắp cải xào trứng ngọt giòn, vàng xanh đẹp mắt, nấu nhanh trong 15 phút.", 15, "de", [
        "Bắp cải thái sợi, ngâm nước muối loãng, rửa sạch, để ráo; hành tỏi băm nhỏ.",
        "Phi thơm hành tỏi với mỡ hoặc dầu, cho bắp cải vào xào lửa lớn cho giòn và không ra nước.",
        "Nêm dầu hào, muối, đường, bột nêm nấm, đảo khoảng 3 phút cho ngấm.",
        "Đập trứng vào, đảo đều đến khi trứng chín bám quanh sợi bắp cải.",
        "Thêm hành lá, múc ra đĩa, rắc chút tiêu."]),
    "bap_cai_xao_toi": ("Bắp cải xào tỏi giòn ngọt, thơm tỏi, món rau đơn giản ngày nào cũng hợp.", 15, "de", [
        "Bắp cải thái sợi, ngâm nước muối loãng rồi rửa sạch, để ráo; tỏi đập dập băm nhỏ; hành lá cắt khúc.",
        "Phi tỏi với dầu ăn cho thơm, cho bắp cải vào xào lửa lớn.",
        "Nêm dầu hào, chút mắm, muối, bột ngọt, đảo đều khoảng 3 phút đến khi bắp cải vừa chín còn giòn.",
        "Thả hành lá, rắc tiêu, đảo nhanh rồi múc ra đĩa."]),
    "dau_co_ve_xao_toi": ("Đậu cô ve xào tỏi xanh mướt, giòn ngọt, thơm mùi dầu hào.", 20, "de", [
        "Đậu cô ve tước xơ, ngâm nước muối, rửa sạch rồi cắt khúc vừa ăn.",
        "Chần đậu qua nước sôi có chút muối, vớt ra xả nước lạnh để giữ màu xanh.",
        "Phi thơm tỏi, cho đậu vào xào lửa lớn, nêm dầu hào, chút nước mắm, muối và bột ngọt.",
        "Đảo nhanh tay đến khi đậu chín tới, nêm lại, thêm hành lá rồi tắt bếp."]),
    "su_hao_xao_ca_rot_nam_meo": ("Su hào xào cà rốt mộc nhĩ giòn sần sật, ngọt thanh, nhiều màu sắc.", 25, "de", [
        "Mộc nhĩ ngâm nở, rửa sạch; su hào, cà rốt và mộc nhĩ thái sợi.",
        "Trộn rau củ với chút muối và hạt nêm, để 10 phút cho hơi mềm.",
        "Đun nóng dầu, xào hỗn hợp ở lửa vừa khoảng 5 phút đến khi su hào chín tới còn giòn; thích mềm thì xào thêm 2–3 phút.",
        "Tắt bếp, rắc rau mùi, đảo đều rồi múc ra đĩa."]),
    "goi_buoi": ("Gỏi bưởi tôm thịt chua ngọt, giòn mát, ăn kèm bánh phồng tôm.", 60, "vua", [
        "Bưởi bóc vỏ, tách tép; hành tây thái khoanh mỏng; cà rốt và dưa leo bỏ ruột thái sợi hoặc lát mỏng.",
        "Luộc thịt ba rọi với chút nước mắm, hạt nêm và đường đến khi chín, để nguội rồi thái lát mỏng; tôm luộc chín, bóc vỏ, chẻ đôi.",
        "Pha nước trộn gỏi từ đường, nước mắm, nước cốt tắc hoặc chanh, chút tương ớt và tỏi băm, nêm chua ngọt vừa miệng; phi hành tỏi, giữ lại dầu phi.",
        "Trộn thịt, rau củ với nước trộn, tỏi phi, dầu phi và dừa bào; tôm trộn riêng cho thấm rồi mới cho bưởi vào trộn nhẹ tay cuối cùng.",
        "Bày ra đĩa, rắc hành phi và dừa bào, ăn kèm bánh phồng tôm hoặc bánh tráng; phần của bé bớt ớt."]),
})

# ---------- Lô C ----------
CL.update({
    "dua_leo_tron": ("Dưa leo đập giòn mát, sốt chua ngọt tỏi ớt thơm dầu mè, ăn kèm món mặn rất đưa cơm.", 55, "de", [
        "Rửa dưa leo, cắt hai đầu, đập dập nhẹ bằng bản dao rồi cắt khúc vừa ăn.",
        "Rắc khoảng 15g đường và chút muối vào dưa, xóc đều, để 25 phút rồi chắt bỏ nước tiết ra cho dưa giòn.",
        "Giã dập tỏi, ớt; khuấy cùng xì dầu, tương ớt, đường còn lại, dầu mè và nước cốt chanh đến khi tan, nếm lại cho hài hòa.",
        "Đổ sốt vào dưa, thêm ngò rí cắt ngắn, trộn đều và để 15–20 phút cho thấm (nên để ngăn mát).",
        "Phần cho bé thì múc riêng trước khi cho ớt, chỉ trộn nhẹ xì dầu, đường, chanh."]),
    "mang_tay_xao_toi": ("Măng tây xanh giòn ngọt xào nhanh lửa lớn, rưới tỏi phi vàng thơm lừng.", 15, "de", [
        "Bẻ bỏ phần gốc già của măng tây, rửa sạch, cắt đôi; tỏi bóc vỏ đập dập.",
        "Làm nóng chảo dầu, cho măng tây vào đảo nhanh trên lửa lớn, nêm chút muối, xào 2–3 phút đến khi xanh bóng rồi bày ra đĩa.",
        "Thêm ít dầu vào chảo, phi tỏi đến vàng thơm.",
        "Rưới tỏi phi cùng dầu lên măng tây, dọn ăn nóng."]),
    "dot_su_su_xao_toi": ("Ngọn su su xanh giòn xào tỏi cùng giá, thoảng mùi dầu mè, món rau nhanh gọn ngày thường.", 15, "de", [
        "Nhặt đọt su su lấy phần non, rửa sạch; giá rửa sạch để ráo; tỏi băm.",
        "Phi tỏi với dầu ăn cho dậy mùi.",
        "Cho đọt su su vào đảo lửa lớn đến khi gần chín thì thêm giá, xào thêm 1 phút.",
        "Nêm muối, hạt nêm, chút đường, rắc tiêu và vài giọt dầu mè, đảo đều rồi tắt bếp.",
        "Ăn kèm chao hoặc nước tương tùy thích."]),
    "rau_bi_xao_toi": ("Ngọn bí mềm ngọt, xanh mướt xào tỏi, thêm tỏi phi rắc mặt cho dậy mùi.", 20, "de", [
        "Tước sạch vỏ xơ ở thân rau bí, tách riêng lá, ngọn và thân.",
        "Vò nhẹ rau với chút muối cho hết lông rồi rửa kỹ nhiều lần, để ráo.",
        "Đun sôi nồi nước có chút muối, chần rau bí qua cho mềm, vớt ra.",
        "Phi tỏi đập dập với dầu đến vàng, múc ra một nửa; cho rau vào chảo xào nhanh, nêm bột nêm, thêm chút nước nếu khô.",
        "Bày rau ra đĩa, rắc phần tỏi phi đã để riêng lên trên."]),
    "cai_chip_xao": ("Cải chíp chần giòn xanh, xào tỏi và xì dầu đậm đà, trẻ con cũng dễ ăn.", 15, "de", [
        "Rửa sạch cải chíp, chần qua nước sôi rồi thả vào bát nước lạnh, vớt ra để ráo.",
        "Phi thơm tỏi băm, múc ra khoảng 2/3 để rắc lên sau.",
        "Cho cải vào chảo đảo với phần tỏi còn lại, nêm hạt nêm, bột canh, thêm chút nước và xì dầu.",
        "Đậy nắp, để lửa nhỏ khoảng 3 phút cho cải thấm vị, bày ra đĩa và rắc tỏi phi lên."]),
    "muop_xao": ("Mướp hương ngọt mềm xào thịt băm cùng mộc nhĩ, miến, món nhà quen thuộc mùa hè.", 25, "de", [
        "Ngâm nở mộc nhĩ (nấm mèo) và miến; mộc nhĩ thái sợi, miến cắt ngắn. Mướp gọt vỏ, cắt khúc.",
        "Phi thơm tỏi đập dập, cho thịt băm vào xào đến khi săn lại.",
        "Thêm mướp vào đảo đều, khi mướp mềm thì nêm gia vị cho vừa.",
        "Cho mộc nhĩ và miến vào xào thêm đến khi mọi thứ mềm, tắt bếp, rắc tiêu lên mặt."]),
    "bau_xao_nam_bao_ngu": ("Bầu non ngọt mát xào nấm bào ngư mềm thơm, nhẹ nhàng mà vẫn đưa cơm.", 20, "de", [
        "Rửa sạch bầu, có thể để nguyên vỏ, bổ đôi rồi thái lát mỏng.",
        "Ngâm nấm bào ngư trong nước muối loãng, rửa lại và vắt ráo, xé miếng vừa ăn.",
        "Phi thơm tỏi băm với dầu, cho bầu vào xào lửa lớn, nêm hạt nêm và nước tương.",
        "Thêm nấm, đảo cho thấm rồi tắt bếp, đậy nắp vài phút để bầu và nấm chín bằng hơi nóng.",
        "Mở nắp, rưới vài giọt dầu mè, rắc hành lá, dọn ăn với cơm nóng."]),
    "goi_du_du_tom_thit": ("Gỏi đu đủ giòn sần sật với tôm, thịt ba chỉ, rau thơm và nước trộn chua ngọt.", 60, "vua", [
        "Đu đủ và cà rốt gọt vỏ, bào sợi, ngâm vào thau nước đá pha chút đường và nước cốt chanh, cất ngăn mát 15–30 phút cho giòn.",
        "Luộc thịt ba chỉ với chút muối và một củ hành tím đến chín, vớt ra thái mỏng; dùng nồi nước đó luộc tôm, bóc vỏ, bỏ chỉ lưng.",
        "Pha nước trộn: đường và nước mắm bằng nhau, thêm nước cốt chanh, tỏi ớt băm, khuấy tan rồi nếm lại.",
        "Trộn tôm thịt với vài thìa nước trộn, để 5–10 phút; vắt thật ráo đu đủ, cà rốt rồi trộn chung với tôm thịt, rau răm, húng quế thái nhỏ.",
        "Bày ra đĩa, rắc lạc rang và hành phi, ăn kèm bánh phồng tôm; phần của bé trộn riêng không ớt."]),
    "goi_xoai_tom_kho": ("Xoài xanh chua giòn trộn tôm khô rim ngọt mặn, rau răm thơm, ăn là nhớ.", 35, "de", [
        "Ngâm tôm khô nước ấm 15–30 phút, rửa sạch cát. Phi thơm hành khô, cho tôm vào xào, nêm chút nước mắm và đường, rim lửa nhỏ đến khi tôm săn.",
        "Giã tỏi và ớt, hòa với nước mắm và đường đến khi tan để làm nước trộn (xoài đã chua nên không cần chanh).",
        "Xoài gọt vỏ, thái sợi; trộn với một nửa nước trộn trong 5 phút rồi chắt bỏ nước.",
        "Cho phần nước trộn còn lại, tôm rim và rau răm thái nhỏ vào xoài, trộn đều, rắc thêm tôm lên mặt khi dọn."]),
    "ca_tim_nuong_mo_hanh": ("Cà tím nướng mềm, phủ mỡ hành dầu hào béo thơm, món chay mặn đều hợp.", 40, "de", [
        "Thái mỏng hành khô, phi vàng thơm; cho hành lá thái nhỏ, ớt, dầu hào, chút nước mắm và đường vào đảo đều làm mỡ hành.",
        "Bổ đôi cà tím, nướng ở 210°C khoảng 20–25 phút đến khi ruột mềm.",
        "Dùng dĩa dàn ruột cà tím ra, rưới mỡ hành lên trên, rắc chút hạt thì là.",
        "Cho vào lò nướng thêm 4–5 phút cho thấm rồi dọn ăn nóng; phần cho bé bỏ ớt."]),
    "dau_ha_lan_xao_tau_hu_ky_nam_meo": ("Đậu Hà Lan xanh giòn xào tàu hũ ky, mộc nhĩ, nấm bào ngư và cà rốt, đủ màu đủ vị.", 30, "de", [
        "Nhặt xơ đậu Hà Lan, rửa sạch, xẻ đôi; ngâm mềm tàu hũ ky và nấm mèo rồi cắt sợi; cà rốt thái sợi.",
        "Chần đậu Hà Lan 2–3 phút rồi xả nước lạnh; chần qua cà rốt và nấm mèo, để ráo.",
        "Xào nấm bào ngư với chút dầu cho săn lại.",
        "Cho tàu hũ ky, nấm mèo, cà rốt, đậu Hà Lan vào chảo, nêm muối, hạt nêm chay, xào lửa vừa khoảng 5 phút cho thấm, nếm lại rồi tắt bếp."]),
    "rau_lang_luoc_cham_kho_quet": ("Rau củ luộc chấm kho quẹt tôm khô thịt ba chỉ mặn ngọt sánh, cực kỳ hao cơm.", 40, "de", [
        "Thắng mỡ heo lấy tóp, tóp vàng thì vớt ra.",
        "Chừa ít mỡ trong nồi, phi thơm hành tỏi băm, cho tôm khô và thịt ba chỉ thái nhỏ vào xào đến khi xém cạnh.",
        "Thêm nước mắm, đường, tiêu, đun lửa nhỏ đến khi hỗn hợp sánh lại; múc riêng một ít cho bé rồi mới thêm ớt cho người lớn. Rắc tóp mỡ và hành lá.",
        "Luộc rau lang và các loại rau củ khác vừa chín tới, vớt ra, chấm cùng kho quẹt."]),
    "cai_ngot_xao_toi": ("Cải ngọt xào tỏi bằng mỡ thêm tóp mỡ giòn, xanh mướt và ngọt rau.", 15, "de", [
        "Nhặt, rửa sạch cải ngọt, cắt khúc, để ráo.",
        "Đun nóng mỡ, phi tỏi đập dập đến khi dậy mùi.",
        "Cho cải vào xào lửa lớn, nêm muối, đảo đều đến khi rau vừa chín, còn xanh giòn.",
        "Nêm lại, cho tóp mỡ vào, đảo nhanh rồi bày ra đĩa."]),
    "rau_den_luoc": ("Rau dền luộc mềm ngọt, chấm nước mắm tỏi ớt, có cả bát nước luộc mát lành.", 15, "de", [
        "Nhặt rau dền, tước bỏ vỏ xơ ở thân, rửa sạch với nước muối loãng.",
        "Đun sôi mạnh nồi nước với chút muối, cho rau vào luộc khoảng 3 phút đến khi mềm.",
        "Vớt rau ra đĩa; nếu giữ nước luộc làm canh thì nêm thêm chút bột ngọt cho vừa.",
        "Pha nước mắm với đường, tỏi, ớt băm (bát riêng cho bé không ớt) để chấm rau."]),
    "cai_thao_xao_nam": ("Cải thảo ngọt mềm xào nấm hương thơm, gừng hành dậy mùi, đậm đà dầu hào.", 25, "de", [
        "Ngâm nấm hương khô vào nước nóng đến khi nở mềm, cắt bỏ chân, thái miếng; cải thảo rửa sạch, cắt nhỏ.",
        "Phi gừng và hành tím thái lát với dầu cho thơm.",
        "Cho nấm hương vào xào trước 3–4 phút, rồi thêm cải thảo đảo chung.",
        "Nêm dầu hào và hạt nêm, xào đến khi cải vừa chín tới thì thêm hành lá, rắc tiêu lên mặt."]),
    "gia_xao_he": ("Giá đỗ giòn xào hẹ xanh thơm, món rau nhanh gọn chỉ vài phút là có.", 10, "de", [
        "Nhặt bỏ rễ giá, rửa sạch để ráo; hẹ rửa sạch, cắt khúc khoảng 4cm.",
        "Phi thơm tỏi băm với chút dầu.",
        "Cho giá vào đảo nhanh trên lửa lớn khoảng 1 phút, nêm chút muối, hạt nêm.",
        "Thêm hẹ, đảo thêm 30 giây đến khi hẹ vừa chuyển màu thì tắt bếp ngay để giá còn giòn."]),
    "bap_cai_luoc_cham_trung_dam_nuoc_mam": ("Bắp cải luộc ngọt chấm trứng dầm nước mắm, món quê đơn giản mà ai cũng mê.", 25, "de", [
        "Rửa sạch bắp cải, bổ đôi hoặc tách lá; rửa sạch vỏ trứng.",
        "Cho bắp cải và trứng vào nồi cùng nước, đun lửa lớn khoảng 15 phút đến khi sôi được một lúc thì tắt bếp.",
        "Vớt bắp cải ra đĩa; giữ nước luộc làm canh, nêm chút muối.",
        "Bóc trứng, dầm nhuyễn với nước mắm (có thể vắt thêm chanh) để chấm bắp cải."]),
    "dau_que_luoc_cham_muoi_me": ("Đậu que luộc xanh giòn ngọt, chấm muối vừng hay nước mắm chanh tỏi đều ngon.", 15, "de", [
        "Chọn đậu non, ngắt hai đầu và tước xơ hai bên sống cho đỡ dai, rửa sạch.",
        "Đun nước thật sôi, thêm chút muối và chút đường để đậu giữ màu xanh và ngọt hơn.",
        "Thả đậu vào luộc khoảng 3 phút để còn giòn, vớt ra để ráo.",
        "Rang vừng giã với muối làm muối vừng, hoặc pha nước mắm chanh tỏi rưới lên đậu để thấm."]),
    "nom_dua_chuot_ca_rot": ("Nộm dưa chuột cà rốt cuộn xinh, chua ngọt giòn mát, rắc lạc rang bùi béo.", 30, "vua", [
        "Cắt đầu dưa chuột, xát cho hết nhựa, rửa sạch rồi nạo lát mỏng; cà rốt gọt vỏ, nạo lát mỏng. Lạc rang xát vỏ, giã dập; tỏi ớt băm nhỏ.",
        "Đặt lát dưa chuột, phủ lát cà rốt so le lên trên rồi cuộn tròn, cố định bằng tăm; làm đến hết.",
        "Pha nước trộn với nước cốt chanh, tỏi ớt băm, chút đường và bột canh cho vừa miệng.",
        "Rưới nước trộn lên các cuộn cho ngấm, bày ra đĩa và rắc lạc giã lên trên; phần của bé bớt ớt."]),
    "xa_lach_tron_dau_giam": ("Xà lách trộn dầu giấm kiểu Bắc, chua dịu ngọt nhẹ, ăn kèm thịt rán hay bò xào rất hợp.", 15, "de", [
        "Nhặt xà lách, rửa sạch, ngâm nước muối loãng rồi vẩy thật ráo; cà chua thái múi cau, hành tây thái mỏng ngâm nước đá cho bớt hăng.",
        "Pha nước trộn: giấm, đường, chút muối, khuấy tan rồi thêm dầu ăn và tỏi băm, đánh đều.",
        "Ngay trước khi ăn mới rưới nước trộn lên xà lách, cà chua, hành tây và trộn nhẹ tay để rau không bị úng.",
        "Rắc chút tiêu, có thể thêm trứng luộc thái lát cho bé dễ ăn."]),
    "mong_toi_xao_toi": ("Mồng tơi xào tỏi mềm mướt, thấm vị dầu hào, đĩa rau xanh nhanh mà ngon.", 15, "de", [
        "Nhặt mồng tơi bỏ cọng già, ngâm và rửa sạch, để ráo; tỏi bóc vỏ đập dập.",
        "Hòa bột nêm, bột ngọt, dầu hào với ít nước thành bát gia vị.",
        "Phi tỏi với dầu đến vàng thơm, vớt riêng ra; đổ bát gia vị vào chảo đun sôi.",
        "Cho mồng tơi vào xào lửa lớn đến khi vừa chín, còn xanh thì bày ra đĩa, rắc tỏi phi và tiêu lên."]),
    "cai_ngong_luoc": ("Cải ngồng luộc giòn ngọt chấm trứng dầm nước mắm, bữa cơm nhà thanh nhẹ.", 20, "de", [
        "Nhặt cải ngồng bỏ phần già, rửa sạch, ngâm nước muối loãng khoảng 15–30 phút rồi rửa lại.",
        "Đun sôi nồi nước với chút muối, cho cải vào luộc đến khi vừa chín, đừng để quá mềm, vớt ra để ráo.",
        "Dùng nồi nước luộc rau luộc trứng khoảng 10 phút, bóc vỏ.",
        "Dầm trứng với nước mắm, thêm ớt đỏ thái lát cho người lớn, chấm cùng cải ngồng."]),
    "ngo_xao_tom_kho": ("Ngô ngọt xào tôm khô và bơ thơm lừng, hạt bắp mềm dẻo, trẻ con rất thích.", 35, "de", [
        "Ngâm tôm khô cho mềm, rửa sạch, để ráo rồi giã hoặc xay sơ cho tơi.",
        "Luộc ngô chín rồi tách lấy hạt (hoặc tách hạt trước rồi luộc), để ráo.",
        "Đun chảy bơ trong chảo, phi đầu hành lá cho thơm, cho tôm khô vào xào trước rồi thêm hạt ngô.",
        "Nêm hạt nêm, xào lửa nhỏ đến khi ngô khô ráo thì cho hành lá thái nhỏ vào, đảo đều rồi tắt bếp."]),
    "su_su_luoc_cham_muoi_vung": ("Su su luộc xanh ngọt chấm muối vừng bùi thơm, món luộc giản dị cho cả nhà.", 20, "de", [
        "Gọt vỏ su su (ngâm trong nước hoặc đeo găng để khỏi dính nhựa), bổ miếng vừa ăn, rửa sạch.",
        "Đun sôi nồi nước, cho chút muối để su su giữ màu xanh và ngọt.",
        "Thả su su vào luộc khoảng 5 phút đến khi vừa chín, vớt ra để ráo.",
        "Rang vừng vàng, giã cùng chút muối và đường làm muối vừng để chấm."]),
    "mang_tay_luoc_cham_xi_dau_trung": ("Măng tây luộc giòn ngọt chấm xì dầu dầm trứng lòng đào, nhanh gọn và bổ dưỡng.", 20, "de", [
        "Bẻ bỏ gốc già của măng tây, rửa sạch; trứng rửa sạch vỏ.",
        "Luộc trứng khoảng 7–8 phút cho lòng đỏ vừa chín dẻo, thả vào nước lạnh rồi bóc vỏ.",
        "Đun sôi nước với chút muối, chần măng tây 1–2 phút đến khi xanh bóng, vớt ra ngâm nước lạnh để giữ độ giòn.",
        "Dầm trứng với xì dầu, chút đường và vài giọt chanh, dùng làm nước chấm măng tây."]),
    "canh_ga_rau_cu": ("Canh gà hầm khoai tây, cà rốt, hành tây ngọt nước, mềm nhừ hợp khẩu vị trẻ nhỏ.", 60, "de", [
        "Làm sạch cổ, cánh, chân gà, chặt miếng vừa ăn; hầm với nước, bột canh, hạt nêm, chút nước mắm và mì chính.",
        "Khoai tây, hành tây thái miếng vuông khoảng 2cm; cà rốt thái miếng dày 1cm; hành hoa thái khúc.",
        "Khi gà chín, cho khoai tây và cà rốt vào hầm đến khi mềm.",
        "Thêm hành tây, đun thêm 5 phút cho vừa chín tới rồi tắt bếp, cho hành hoa vào.",
        "Múc ra bát, rắc tiêu; ớt thái nhỏ chỉ thêm vào bát người lớn."]),
    "canh_moc_nam_huong": ("Canh nấm hương quết mọc nước dùng gà ngọt thanh, thêm bông cải và cà rốt xinh mắt.", 35, "vua", [
        "Rửa sạch nấm hương, cắt bỏ chân, để ráo; cà rốt và bông cải xanh cắt miếng vừa ăn.",
        "Trộn giò sống với tiêu, quết một lớp lên mặt trong của từng tai nấm.",
        "Đun sôi nước hầm gà, cho cà rốt vào nấu 3 phút.",
        "Thả nấm quết mọc vào, nấu lửa vừa khoảng 5 phút đến khi mọc chín.",
        "Thêm bông cải xanh, nêm muối và nước mắm, nấu thêm 2 phút rồi rắc hành lá, mùi ta."]),
    "canh_kho_qua_nhoi_thit": ("Khổ qua nhồi thịt nấm mèo hầm mềm, nước canh trong ngọt, đắng nhẹ thanh mát.", 60, "vua", [
        "Ngâm nở nấm mèo, băm nhỏ; trộn cùng thịt xay, đầu hành băm, hạt nêm, tiêu và dầu ăn cho dẻo.",
        "Rửa khổ qua, cắt đầu, khoét bỏ ruột hạt rồi nhồi nhân thật chặt; dùng lá hành chần mềm buộc quanh cho khỏi bung.",
        "Đun sôi nước, thả khổ qua cùng ít rễ ngò vào, hầm lửa nhỏ.",
        "Nêm nước mắm, đường, hạt nêm cho vừa; hầm tiếp đến khi khổ qua mềm.",
        "Múc ra tô, rắc hành lá và ngò rí thái nhỏ."]),
    "canh_rong_bien_thit_bam": ("Canh rong biển thịt băm ngọt mát, nấu nhanh, bé dễ ăn và giàu khoáng chất.", 20, "de", [
        "Ngâm rong biển cho nở mềm, rửa sạch, cắt đoạn ngắn cho dễ ăn.",
        "Cho thịt xay cùng chút hạt nêm vào nồi nước, đun sôi và hớt bọt.",
        "Thả rong biển vào, nêm muối và hạt nêm cho vừa.",
        "Khi nước sôi lại thì cho hành ngò thái nhỏ vào và tắt bếp."]),
    "canh_cai_cuc_thit_bam": ("Canh cải cúc thịt băm thơm mùi tần ô đặc trưng, ngọt nước, nấu chỉ 15 phút.", 15, "de", [
        "Nhặt cải cúc, rửa sạch, cắt khúc.",
        "Băm nhỏ thịt nạc, ướp với hành tím băm, chút muối, nước mắm và tiêu.",
        "Đun sôi nước, cho thịt vào khuấy tơi, hớt bọt.",
        "Thả cải cúc vào, nêm lại cho vừa, nước sôi lại là tắt bếp ngay để rau giữ màu."]),
    "canh_suon_nau_ngo": ("Canh sườn nấu ngô ngọt lịm, nước trong, sườn mềm, bé nào cũng thích.", 45, "de", [
        "Rửa sạch sườn, chặt miếng vừa ăn, ướp với chút muối, nước mắm, tiêu và hành tỏi băm.",
        "Bóc vỏ, bỏ râu ngô, rửa sạch rồi cắt khúc.",
        "Phi thơm hành tỏi, cho sườn vào xào săn, thêm chút nước để không bị cháy.",
        "Đổ nước vào, cho ngô vào hầm khoảng 20–30 phút, hớt bọt, nêm lại vừa ăn rồi múc ra tô."]),
    "canh_su_hao_nau_suon": ("Canh su hào sườn non ngọt thanh kiểu Bắc, su hào mềm bở, nước trong vắt.", 50, "de", [
        "Gọt vỏ su hào, cắt khúc hoặc thái miếng; lá su hào non cắt khúc để riêng. Sườn non chặt miếng vừa ăn.",
        "Hầm sườn với nước và chút muối, hớt bọt, đến khi sườn mềm.",
        "Cho su hào vào, đậy nắp đun đến khi su hào mềm.",
        "Thả lá su hào vào đảo đều, nêm gia vị cho vừa, tắt bếp và rắc tiêu."]),
    "canh_ca_ngu_nau_ca_thom": ("Canh cá ngừ nấu cà chua, dứa chua ngọt dịu, cá chắc thịt thấm đậm.", 35, "de", [
        "Rửa sạch cá ngừ, cắt khúc; ướp với chút hạt nêm, muối, nước mắm, hành tím băm và tiêu.",
        "Cà chua bổ múi, dứa (thơm) thái miếng; hành lá, ngò cắt khúc.",
        "Phi thơm hành tím với dầu, cho cà chua và dứa vào xào cùng chút hạt nêm, đường đến khi mềm rồi đổ nước vào.",
        "Nước sôi thì thả cá vào, sôi lại nêm cho vị chua ngọt vừa phải, cho hành ngò vào và tắt bếp.",
        "Pha bát nước mắm ớt riêng cho người lớn chấm cá."]),
    "canh_ca_nau_ngot": ("Canh đầu đuôi cá nấu cà chua và cần tây, chua nhẹ thanh ngọt, tận dụng cá khéo léo.", 35, "de", [
        "Làm sạch đầu và đuôi cá, rán qua cho săn và hết tanh.",
        "Phi thơm đầu hành, cho cà chua bổ múi vào đảo đến khi mềm, đổ nước vào đun sôi rồi thả cá vào.",
        "Cần tây rửa sạch, cắt khúc.",
        "Khi nước sôi lại, cho cần tây vào, nêm muối, hạt nêm, rắc tiêu và chút tỏi phi rồi tắt bếp."]),
    "canh_chua_tom": ("Canh chua tôm với bạc hà, đậu bắp, dứa, cà chua, chua ngọt thanh mát ngày hè.", 30, "de", [
        "Bóc vỏ tôm, bỏ chỉ lưng; rửa sạch và cắt gọn bạc hà, đậu bắp, cà chua, dứa, giá và rau ngổ.",
        "Phi thơm đầu hành với chút dầu, cho tôm vào xào săn rồi đổ nước vào đun sôi.",
        "Lần lượt cho cà chua, dứa, đậu bắp, bạc hà vào nồi.",
        "Nêm cho vị chua ngọt vừa miệng, thêm giá và rau ngổ rồi tắt bếp; ớt để riêng cho người lớn."]),
    "canh_ngheu_nau_rau_ngot": ("Canh ngao nấu rau ngót ngọt nước, thanh mát, bữa cơm nhà nào cũng hợp.", 45, "de", [
        "Rửa sạch nghêu, ngâm nước khoảng 30 phút cho nhả cát, rửa lại.",
        "Luộc nghêu với chút muối đến khi há miệng, vớt ra lấy thịt; để nước luộc lắng cặn. Ướp thịt nghêu với chút hạt nêm và hành.",
        "Tuốt lấy lá rau ngót, rửa sạch, vò nhẹ.",
        "Phi hành với mỡ, cho thịt nghêu vào đảo nhanh, đổ phần nước luộc trong vào đun sôi.",
        "Thả rau ngót vào, nêm gia vị cho vừa, sôi lại là tắt bếp."]),
    "canh_cai_xanh_nau_tom": ("Canh cải xanh nấu tôm băm ngọt nước, cải hơi đắng nhẹ, rất giải nhiệt.", 20, "de", [
        "Rửa sạch cải xanh, thái nhỏ.",
        "Băm tôm nõn, xào sơ với dầu, hành tím băm và chút muối.",
        "Đun sôi nồi nước, cho tôm và cải vào, nêm gia vị.",
        "Khi canh sôi lại, nêm lần cuối rồi tắt bếp."]),
    "canh_bo_ham_khoai_tay_ca_rot": ("Canh bò hầm khoai tây cà rốt mềm nhừ, nước sánh ngọt đậm, ấm bụng cả nhà.", 90, "vua", [
        "Chần thịt bò qua nước sôi cho sạch, vớt ra để ráo rồi thái miếng vuông ngang thớ.",
        "Ướp bò với tỏi băm, chút bột canh, tiêu, nước mắm và dầu ăn khoảng 30 phút.",
        "Trong lúc chờ, cắt khoai tây, cà rốt miếng vừa ăn; chiên sơ khoai tây cho vàng hai mặt để khoai thơm, không nát.",
        "Xào bò trong nồi đến khi chín tới, cho cà chua vào đảo đến khi mềm; đổ khoảng 1 lít nước, thêm gừng đập dập và gia vị, hầm lửa nhỏ đến khi bò gần nhừ.",
        "Cho cà rốt vào nấu 4 phút, rồi thêm khoai tây đun 3 phút nữa; tắt bếp, cho hành lá, mùi ta và nêm lại."]),
    "canh_dau_hu_he_nam_rom": ("Canh đậu hũ non, nấm rơm và hẹ thanh ngọt, mềm mịn dễ ăn cho trẻ.", 25, "de", [
        "Thái khoanh đậu hũ trứng; hẹ cắt khúc ngắn; nấm rơm cắt gốc, rửa sạch, bổ nhỏ.",
        "Đun nóng dầu, xào nấm lửa lớn đến khi mềm, hạ lửa và nêm chút hạt nêm, bột ngọt cho thấm.",
        "Đổ khoảng 1 lít nước vào, khi sôi thì thả đậu hũ và chút đường, nêm phần hạt nêm còn lại.",
        "Nước sôi lại thì cho hẹ vào, hẹ vừa đổi màu là tắt bếp, thêm dầu mè và tiêu."]),
    "canh_ga_nau_bi_do": ("Canh gà nấu bí đỏ bùi ngọt, nước dùng trong, bí mềm tan hợp cho bé.", 40, "de", [
        "Rửa sạch gà với muối, chặt miếng; cho vào nồi cùng nước, chút muối và đường, đun sôi.",
        "Hớt bọt cho nước trong, đậy nắp nấu thêm khoảng 10 phút để gà mềm.",
        "Bí đỏ gọt vỏ, bỏ hạt, cắt miếng dày 3–4cm.",
        "Thả bí vào nồi gà đang sôi, đảo đều rồi tắt bếp, đậy kín ủ 5–10 phút cho bí chín mềm.",
        "Bật lại bếp, nêm gia vị cho vừa, cho hành lá và ngò rí, rắc tiêu rồi múc ra tô."]),
})

# ---------- Lô D ----------
CL.update({
    "canh_dau_phu_ca_chua": ("Canh đậu phụ cà chua chua dịu, mềm mát, bát canh quen thuộc của mâm cơm Bắc.", 20, "de", [
        "Cà chua bổ múi cau, đậu phụ cắt miếng vuông vừa ăn, hành lá thái nhỏ, tách riêng đầu hành.",
        "Phi thơm đầu hành với chút dầu, cho cà chua vào xào cùng ít muối đến khi cà nhuyễn, ra màu đỏ.",
        "Đổ khoảng 1,2 lít nước, đun sôi rồi thả đậu phụ vào, để lửa vừa 3–4 phút cho đậu ngấm.",
        "Nêm nước mắm, hạt nêm vừa miệng, rắc hành lá rồi tắt bếp, múc ra bát khi còn nóng."]),
    "canh_rau_den_nau_tom": ("Canh rau dền đỏ nấu tôm, nước canh hồng ngọt, mát ruột ngày hè.", 20, "de", [
        "Nhặt lấy lá và ngọn non rau dền, rửa kỹ vài lượt nước rồi để ráo.",
        "Tôm bóc vỏ, rút chỉ đen; phi thơm tỏi với chút dầu, cho tôm vào xào săn, nêm ít hạt nêm và tiêu.",
        "Đổ nước vào nồi tôm, đun sôi rồi thả rau dền vào, đảo nhẹ cho rau chìm đều.",
        "Rau vừa mềm, nước ngả hồng thì nêm muối cho vừa, tắt bếp, rắc chút tiêu khi múc ra bát."]),
    "canh_rau_lang": ("Canh rau lang nấu tôm băm, thanh mát, dễ ăn cho cả nhà.", 20, "de", [
        "Nhặt phần ngọn non rau lang, rửa sạch, để ráo và cắt khúc ngắn.",
        "Tôm bóc vỏ, băm nhỏ, ướp với chút hạt nêm và hành tím băm khoảng 10 phút.",
        "Phi thơm hành tím với ít dầu, cho tôm vào xào săn rồi đổ nước, đun sôi.",
        "Thả rau lang vào, nêm nước mắm, hạt nêm vừa ăn; rau chín mềm thì tắt bếp.",
        "Rắc hành lá, ngò rí và chút tiêu lên trên, dọn ăn cùng cơm nóng."]),
    "canh_rong_bien_dau_hu": ("Canh rong biển đậu hũ thịt băm thanh nhẹ, mềm mịn, trẻ nhỏ rất dễ ăn.", 25, "de", [
        "Ngâm rong biển trong nước cho nở, rửa lại vài lần rồi để ráo.",
        "Cắt đậu hũ thành khối vuông nhỏ, thịt băm nêm sơ chút muối, tiêu.",
        "Phi thơm hành tím với ít dầu, cho rong biển vào đảo nhanh rồi đổ nước, đun sôi.",
        "Thả thịt băm vào, dùng muôi khuấy tơi; thịt chín thì cho đậu hũ vào, nêm hạt nêm cho vừa.",
        "Đun thêm 2–3 phút cho đậu ngấm, rắc hành lá rồi tắt bếp."]),
    "canh_su_su_ca_rot_thit_bam": ("Canh su su cà rốt thịt băm ngọt nước, màu sắc tươi, bé nào cũng thích.", 25, "de", [
        "Thịt nạc rửa sạch, băm nhỏ, ướp với chút nước mắm, muối, tiêu và hành tím băm.",
        "Su su và cà rốt gọt vỏ, rửa sạch, thái lát hoặc miếng vừa ăn.",
        "Phi thơm hành tím với ít dầu, cho thịt vào xào săn rồi đổ nước, đun sôi và hớt bọt.",
        "Cho cà rốt vào trước, khoảng 3 phút sau thêm su su, nấu đến khi rau củ mềm.",
        "Nêm lại nước mắm, hạt nêm cho vừa, rắc hành lá thái nhỏ rồi tắt bếp."]),
    "canh_ngao_nau_chua": ("Canh ngao nấu chua mẻ kiểu Bắc, chua thanh, ngọt nước, thơm rau răm.", 35, "vua", [
        "Ngâm ngao cho nhả cát, rửa sạch rồi luộc đến khi há miệng; tách lấy thịt, để nước luộc lắng cặn.",
        "Cà chua bổ múi cau, dứa thái miếng mỏng; phi thơm hành khô, cho cà chua cùng chút nước mắm vào xào mềm.",
        "Trút thịt ngao vào đảo săn, thêm dứa rồi gạn phần nước ngao trong vào nồi, đun sôi.",
        "Lọc nước mẻ, cho từ từ vào nồi đến khi đủ độ chua; nêm lại mắm muối, để lửa nhỏ 5 phút.",
        "Tắt bếp, thả hành lá và rau răm thái nhỏ vào là dọn được."]),
    "canh_khoai_mo_nau_tom": ("Canh khoai mỡ tôm băm sánh mịn, bùi béo, thơm ngò om ngò gai.", 30, "de", [
        "Khoai mỡ gọt vỏ (đeo găng tay để đỡ ngứa), rửa sạch rồi bào hoặc nạo nhỏ.",
        "Tôm bóc vỏ, băm nhỏ, ướp chút hạt nêm và tiêu.",
        "Phi thơm ít dầu, cho tôm vào xào săn, thêm khoai mỡ đảo cùng rồi đổ nước xâm xấp mặt.",
        "Nấu lửa vừa khoảng 10 phút cho khoai nhừ, dùng muôi dằm thêm cho canh sánh, nêm lại vừa ăn.",
        "Thả hành lá, ngò om, ngò gai thái nhỏ vào rồi tắt bếp, ăn nóng với cơm."]),
    "canh_khoai_tay_thit_bam": ("Canh khoai tây thịt băm bùi ngọt, nấu nhanh, hợp khẩu vị trẻ nhỏ.", 35, "de", [
        "Khoai tây gọt vỏ, cắt miếng vừa ăn, ngâm nước cho bớt nhựa; hành tím đập dập thái nhỏ, hành lá thái nhỏ.",
        "Phi hành tím với chút dầu cho thơm, cho thịt băm vào đảo tơi, nêm chút nước mắm và muối.",
        "Đổ nước vào nồi, đun sôi khoảng 10 phút cho ngọt nước, nhớ hớt bọt.",
        "Thả khoai tây vào nấu thêm khoảng 10 phút đến khi khoai chín mềm, nêm lại bột nêm vừa miệng.",
        "Rắc hành lá rồi tắt bếp, múc ra bát."]),
    "canh_muc_nau_chua": ("Canh mực nấu chua ngọt dứa cà, mực giòn sần sật, thơm cần tây.", 25, "de", [
        "Mực làm sạch, cắt khoanh vừa ăn, để ráo; cà chua bổ múi cau, dứa thái miếng, hành tây thái múi, cần tây cắt khúc.",
        "Phi thơm hành tỏi băm, cho hành tây và cà chua vào đảo sơ, thêm dứa xào cùng.",
        "Đổ khoảng một tô lớn nước, đun sôi bùng rồi nêm nước mắm, muối, đường cho vừa chua ngọt.",
        "Thả mực vào, đun đến khi mực vừa co lại, trắng đục là chín, không nấu lâu kẻo dai.",
        "Cho cần tây vào rồi tắt bếp, múc ra tô ăn nóng."]),
    "canh_cai_thao_dau_hu_nam": ("Canh cải thảo đậu hũ nấm ngọt thanh, nhẹ bụng, hợp bữa tối cả nhà.", 25, "de", [
        "Cải thảo rửa sạch, cắt khúc vừa ăn; đậu hũ cắt miếng vuông; nấm cắt chân, rửa sạch, xé hoặc thái nhỏ.",
        "Phi thơm hành tím với ít dầu, cho nấm vào xào sơ cho dậy mùi.",
        "Đổ khoảng 1,2 lít nước, đun sôi rồi cho phần cuống cải thảo vào trước, nấu 3 phút.",
        "Thêm lá cải và đậu hũ, nêm muối, hạt nêm vừa ăn, đun thêm 2–3 phút cho cải mềm.",
        "Rắc hành lá, chút tiêu rồi tắt bếp."]),
    "canh_dua_chua_nau_suon": ("Canh dưa chua nấu sườn kiểu Bắc, chua dịu, sườn mềm, thơm thì là.", 50, "vua", [
        "Dưa chua vắt bớt nước, thái nhỏ; cà chua bổ múi; sườn và da heo chần qua nước sôi có muối rồi rửa lại, da heo thái miếng.",
        "Cho sườn vào nồi với khoảng 1 lít nước, nêm chút hạt nêm và nước mắm, ninh 15–20 phút cho sườn mềm, thêm da heo đun tiếp 5 phút.",
        "Phi vàng hành tím, cho cà chua vào đảo một phút rồi thêm dưa chua xào khoảng 3 phút cho dưa ngấm vị.",
        "Trút dưa cà vào nồi sườn, đun sôi lại và nêm nếm vừa khẩu vị.",
        "Múc ra tô, rắc hành lá, thì là thái nhỏ và chút tiêu."]),
    "canh_ga_nau_nam": ("Canh gà nấu nấm thơm ngọt, bổ dưỡng, ấm bụng cho cả nhà.", 50, "vua", [
        "Nấm tươi cắt chân, ngâm nước muối loãng 10 phút rồi rửa sạch; gói nấm khô Vân Nam ngâm nước ấm khoảng 20 phút (riêng kỷ tử để sau).",
        "Băm hành khô và gừng, phi thơm với dầu, cho thịt gà vào xào săn với chút nước mắm.",
        "Đổ khoảng 1,5 lít nước, đun sôi, hớt bọt rồi cho nấm khô và táo đỏ vào ninh khoảng 20 phút.",
        "Nêm gia vị vừa miệng, thả nấm tươi cắt vừa ăn và kỷ tử vào, đun thêm 7–10 phút.",
        "Rắc hành lá thái nhỏ rồi tắt bếp."]),
    "canh_ca_thu_nau_chua": ("Canh cá thu nấu chua dứa cà, cá chắc thịt, không tanh, thơm thì là.", 35, "vua", [
        "Cá thu rửa sạch, thấm khô rồi rán sơ hai mặt cho săn; cà chua bổ múi cau, dứa bỏ mắt thái miếng, hành và thì là cắt khúc.",
        "Phi thơm hành, cho dứa và cà chua vào xào đến khi cà mềm.",
        "Đun sôi nồi nước, cho cá cùng dứa cà vào, nêm muối và hạt nêm, để lửa nhỏ và hớt bọt.",
        "Khi canh dậy vị chua ngọt, thêm chút nước mắm, hành, thì là và hạt tiêu rồi tắt bếp.",
        "Gỡ xương cá cẩn thận trước khi chia cho trẻ nhỏ."]),
    "canh_cai_be_xanh_thit_bam": ("Canh cải bẹ xanh thịt băm thơm gừng, đậm đà, giải nhiệt tốt.", 20, "de", [
        "Cải bẹ xanh rửa sạch, cắt khúc; gừng cạo vỏ, thái sợi nhỏ; hành tím bóc vỏ, băm nhỏ.",
        "Ướp thịt xay với hạt nêm và tiêu; phi thơm hành tím, cho thịt vào xào săn.",
        "Đổ nước vào nồi, đun sôi và hớt bọt cho canh trong.",
        "Thả cải và gừng vào, nêm nước mắm vừa ăn; cải vừa chín tới thì tắt bếp để giữ màu xanh.",
        "Múc ra tô, rắc thêm tiêu."]),
    "canh_tom_nau_thom": ("Canh tôm nấu thơm chua ngọt tự nhiên, nước trong, thơm mùi dứa chín.", 25, "de", [
        "Tôm bóc vỏ, rút chỉ, ướp chút hạt nêm và tiêu; dứa gọt vỏ, bỏ mắt, thái miếng mỏng; cà chua bổ múi cau.",
        "Phi thơm hành tím với ít dầu, cho tôm vào xào săn rồi gắp ra bát.",
        "Cho dứa và cà chua vào nồi xào mềm, đổ khoảng 1,2 lít nước rồi đun sôi.",
        "Thả tôm trở lại nồi, nêm nước mắm, đường, muối cho vừa vị chua ngọt, đun thêm 2 phút.",
        "Rắc hành lá, ngò gai thái nhỏ rồi tắt bếp."]),
    "xoi_lac": ("Xôi lạc nếp cái hoa vàng dẻo thơm, bùi béo, ăn sáng no lâu.", 60, "vua", [
        "Vo sạch gạo nếp, ngâm nước lạnh 6–8 tiếng hoặc qua đêm; lạc nhặt bỏ hạt lép, ngâm riêng khoảng 4 tiếng.",
        "Để ráo gạo, trộn đều với lạc và chút muối, dàn vào chõ hấp, chọc vài lỗ cho hơi bốc đều, lót thêm lá dứa cho thơm.",
        "Hấp khoảng 30 phút, giữa chừng xới nhẹ vài lần cho xôi chín đều.",
        "Khi xôi gần chín, rưới dầu dừa lên, đảo nhẹ và hấp thêm 5 phút.",
        "Xới xôi ra đĩa, rắc dừa bào và muối vừng lạc lên trên."]),
    "banh_mi_chao": ("Bánh mì chảo sốt cà chua nóng hổi, trứng lòng đào, pate béo ngậy.", 25, "de", [
        "Cà chua chần qua nước sôi, bóc vỏ rồi xay nhuyễn; thái xúc xích, thịt hộp miếng vừa ăn.",
        "Đun cà chua xay với dầu hào và hạt nêm, hòa chút bột ngô với nước rồi khuấy vào cho sốt sánh lại.",
        "Xếp pate, thịt hộp, xúc xích ra chảo nhỏ, đập trứng vào giữa rồi rưới sốt cà chua lên.",
        "Đậy vung, đun lửa nhỏ đến khi lòng trắng chín, lòng đỏ còn hơi mềm (nấu chín hẳn cho bé nếu cần).",
        "Rắc hành lá, rau mùi thái nhỏ, ăn kèm bánh mì nướng giòn."]),
    "banh_cuon": ("Bánh cuốn nhân thịt mộc nhĩ làm nhanh từ bánh tráng, mềm mướt, thơm hành phi.", 45, "vua", [
        "Thịt heo băm nhuyễn; mộc nhĩ, nấm hương ngâm nở, rửa sạch, băm nhỏ; hành khô băm nhỏ.",
        "Phi thơm hành khô, cho thịt vào đảo tơi, nêm hạt nêm và chút nước mắm; thịt săn thì thêm mộc nhĩ, nấm hương, đảo đến khi chín rồi rắc tiêu.",
        "Pha một đĩa nước với vài giọt chanh và chút dầu; nhúng từng lá bánh tráng khoảng 1 phút cho mềm, trải ra, cho nhân vào giữa rồi cuộn lại.",
        "Xếp bánh vào đĩa, hấp cách thủy 5–7 phút cho bánh trong và mềm.",
        "Rắc hành phi, dọn kèm nước chấm chua ngọt và rau sống."]),
    "xoi_dau_den": ("Xôi đậu đen nếp cái hoa vàng tím bóng, dẻo bùi, thơm dừa.", 90, "vua", [
        "Đậu đen nhặt bỏ hạt lép, rửa sạch, ngâm nước khoảng 2 tiếng.",
        "Nấu đậu với chút muối và baking soda đến khi đậu chín mềm nhưng còn nguyên hạt, giữ lại nước luộc đậu.",
        "Vo sạch gạo nếp, ngâm vào nước đậu đã nguội khoảng 30 phút cho gạo lên màu, rồi để ráo.",
        "Trộn gạo với đậu và dầu dừa, cho vào nồi cơm điện, thêm nước đậu thấp hơn mặt gạo khoảng 1 cm; nấu khoảng 45 phút, giữa chừng đảo đều.",
        "Xôi chín thì xới tơi, rắc dừa bào lên, ăn kèm muối vừng và chút đường."]),
    "xoi_man": ("Xôi mặn thập cẩm đủ lạp xưởng, chả lụa, trứng, chà bông, rưới mỡ hành thơm lừng.", 60, "vua", [
        "Vo sạch gạo nếp, ngâm ít nhất 2 tiếng (hoặc qua đêm), để ráo rồi hấp chín trong chõ, giữa chừng xới đều cho xôi chín đều.",
        "Lạp xưởng thái lát, áp chảo lửa nhỏ không cần dầu đến khi ra mỡ và hơi xém cạnh.",
        "Đánh tan trứng, tráng thành lớp mỏng rồi cuộn lại, thái sợi; chả lụa thái sợi nhỏ.",
        "Hành lá thái nhỏ, cho vào bát rồi rưới dầu nóng lên làm mỡ hành.",
        "Xới xôi ra đĩa, xếp lạp xưởng, chả lụa, trứng sợi và chà bông lên trên, rưới mỡ hành và chút nước tương."]),
    "nui_xao_bo": ("Nui xào bò mềm thơm, sốt dầu hào đậm vị, rau củ giòn ngọt.", 35, "vua", [
        "Luộc nui 10–12 phút, xả nước lạnh, để ráo rồi trộn chút dầu cho khỏi dính.",
        "Thịt bò thái mỏng, ướp với chút nước tương, dầu hào, tiêu, dầu mè và một thìa nhỏ tinh bột khoai tây.",
        "Pha sốt gồm dầu hào, nước tương, đường, tương ớt và tỏi băm, khuấy cho tan.",
        "Phi thơm tỏi, xào bò lửa lớn vừa tái thì trút ra đĩa; dùng lại chảo xào hành tây, cà rốt với một nửa sốt.",
        "Cho nui và phần sốt còn lại vào đảo đều, trút bò vào đảo nhanh rồi tắt bếp, rắc hành lá và rau ngò."]),
    "mi_hoanh_thanh": ("Mì hoành thánh chay nước dùng rau củ ngọt thanh, hoành thánh chiên giòn.", 60, "kho", [
        "Hấp chín khoai môn và khoai lang, tán nhuyễn với chút muối và bơ, trộn thêm nấm mèo băm nhỏ làm nhân.",
        "Múc nhân vào từng lá hoành thánh, chấm nước vào mép rồi gấp kín, chiên vàng giòn hai mặt.",
        "Hầm nước dùng với củ cải trắng, củ sắn, mướp, bắp và hành tây khoảng 30 phút, thêm nấm rơm, nấm đông cô rồi nêm muối vừa ăn.",
        "Trụng mì tươi qua nước sôi khoảng 25 giây, nhúng nhanh nước lạnh rồi trụng nóng lại cho sợi dai.",
        "Cho mì ra bát cùng rau tần ô, hẹ, đậu hũ chiên, chả chay và hoành thánh, chan nước dùng nóng."]),
    "com_rang_thap_cam": ("Cơm rang thập cẩm tơi hạt, đủ lạp xưởng, thịt, rau củ, đầy màu sắc.", 35, "vua", [
        "Cà rốt, đậu cô ve, hành tây thái hạt lựu; lạp xưởng luộc qua 10 phút, bóc vỏ, thái hạt lựu; thịt xào săn.",
        "Đánh trứng rồi trộn đều với cơm nguội cho từng hạt áo trứng.",
        "Xào cà rốt và lạp xưởng khoảng 5 phút, thêm hành tây, đậu cô ve và thịt, nêm chút bột nêm rồi trút ra đĩa.",
        "Lau chảo, cho dầu nóng rồi rang cơm, nêm bột nêm, muối, tiêu, đảo đến khi hạt cơm săn và tơi.",
        "Trút rau củ vào trộn đều, rang thêm vài phút, rắc hành lá và hành phi rồi tắt bếp."]),
    "bun_rieu_cua": ("Bún riêu cua đồng chua dịu, riêu xốp béo, đậu rán vàng, đậm vị Hà Nội.", 75, "kho", [
        "Cua xay hòa với nước lạnh, lọc qua rây lấy nước, phần bã lọc thêm lần nữa; giữ riêng gạch cua.",
        "Đun nước cua lửa vừa, khuấy nhẹ đến khi riêu nổi thành mảng thì hạ lửa, vớt riêu ra bát.",
        "Trộn riêu với thịt xay và trứng vịt; cà chua bổ múi, xào với hành tím phi, gạch cua và chút mắm đến khi mềm rồi đổ vào nồi nước.",
        "Đậu hũ cắt miếng, rán vàng rồi thả vào nồi; múc từng thìa hỗn hợp riêu thả vào, đun lửa nhỏ đến khi chín; nêm mắm, giấm bỗng cho vừa chua.",
        "Trụng bún, cho ra bát, xếp riêu và đậu lên, chan nước dùng, dọn kèm rau sống, chanh, ớt, mắm tôm."]),
    "sup_ga_ngo_ngot": ("Súp gà ngô ngọt sánh mịn, gà xé mềm, trứng vân đẹp, bé ăn rất thích.", 40, "de", [
        "Luộc chín ức gà, vớt ra để nguội rồi xé sợi nhỏ, giữ lại nước luộc.",
        "Cà rốt thái hạt lựu, nấm hương thái nhỏ, ngô rửa sạch, rau mùi thái nhỏ.",
        "Cho ngô, cà rốt, nấm vào nồi nước luộc gà, nêm muối, nước mắm vừa ăn, đun đến khi rau củ chín rồi thêm gà xé.",
        "Hòa bột năng với nước nguội, vừa đổ từ từ vào nồi vừa khuấy cho súp sánh.",
        "Đánh tan trứng, rót thành dòng mảnh vào nồi và khuấy nhẹ cho tạo vân; tắt bếp, rắc tiêu và rau mùi."]),
    "pho_ga": ("Phở gà nước dùng trong ngọt, thịt gà xé mềm, trứng non béo bùi.", 60, "vua", [
        "Ức gà xát muối, rửa sạch; rau thơm, giá nhặt rửa, để ráo.",
        "Đun nồi nước hầm xương với vài lát gừng và củ hành nướng, cho ức gà vào luộc chín, nêm hạt nêm và chút đường cho vừa.",
        "Vớt gà ra để nguội rồi xé sợi; thả trứng non vào nồi nước dùng luộc khoảng 3 phút.",
        "Trụng nóng bánh phở, cho ra bát, xếp gà và trứng non lên, chan nước dùng thật sôi.",
        "Rắc hành lá, ngò rí, tiêu; dọn kèm giá, rau quế, ngò gai, tương ớt và tương đen."]),
    "chao_suon": ("Cháo sườn nấu nhừ từ cơm nguội, sánh mịn, ngọt nước sườn, hợp bé ăn sáng.", 100, "de", [
        "Sườn non chặt khúc, chần qua nước sôi khoảng 5 phút, rửa lại nước lạnh rồi ướp với hạt nêm, chút đường, nước mắm và hành khô.",
        "Cho cơm nguội, sườn và khoảng 2 lít nước vào nồi, ninh lửa nhỏ (hoặc nồi cơm điện chế độ cháo) khoảng 1 tiếng rưỡi đến khi cháo nhừ.",
        "Cà rốt thái hạt lựu, cho vào nồi khi cháo gần xong, nêm lại cho vừa miệng.",
        "Múc cháo ra bát, thêm giá trụng, hành ngò thái nhỏ, hành phi và chút tiêu."]),
    "bun_cha_ca_nha_trang": ("Bún chả cá Nha Trang nước dùng thanh ngọt dứa cà, chả cá dai thơm.", 75, "vua", [
        "Rửa sạch và nhặt các loại rau, bắp cải thái nhỏ, để ráo.",
        "Xương gà rửa với muối, chần qua rồi hầm cùng vài lát gừng khoảng 45 phút lấy nước ngọt.",
        "Cho dứa vào nồi nấu khoảng 10 phút, thêm cà chua đun 3 phút, nêm hạt nêm, nước mắm, đường hơi nhạt một chút.",
        "Chả cá cắt miếng vừa ăn, thả vào nồi nước dùng cho nóng lại.",
        "Trụng bún, cho ra bát cùng chả cá, chan nước dùng, rắc hành ngò, tiêu; ăn kèm rau sống, chanh, ớt và mắm tôm tùy thích."]),
    "bun_thit_nuong": ("Bún thịt nướng chả giò, nước mắm chua ngọt, mỡ hành, đậu phộng giòn bùi.", 90, "kho", [
        "Trộn thịt xay với cà rốt thái sợi, nấm mèo băm, trứng, chút hạt nêm và tiêu; cuốn bằng bánh tráng rồi chiên vàng thành chả giò.",
        "Thịt thái lát mỏng, ướp với hành tím, tỏi băm, nước mắm, hạt nêm, chút đường và dầu ăn khoảng 30 phút rồi nướng than hoặc nướng lò đến khi xém cạnh.",
        "Pha nước mắm: hòa đường với nước ấm và nước mắm, để nguội rồi thêm tỏi ớt băm và chanh.",
        "Đu đủ xanh và cà rốt bào sợi, ngâm nước giấm đường muối làm đồ chua; hành lá trần dầu nóng làm mỡ hành.",
        "Cho rau sống xuống đáy bát, xếp bún, thịt nướng, chả giò cắt khúc, đồ chua lên trên, rưới mỡ hành, rắc đậu phộng và chan nước mắm."]),
    "com_tam_suon": ("Cơm tấm sườn nướng thơm lừng, mỡ hành béo, nước mắm sánh ngọt.", 90, "vua", [
        "Sườn non để nguyên tảng hoặc xẻ theo từng dẻ, ướp với hỗn hợp gia vị ít nhất 2 tiếng, tốt nhất qua đêm.",
        "Xếp sườn lên khay lót giấy bạc, rưới nước dừa và nước ướp, nướng lò khoảng 220–250°C mỗi mặt 25–30 phút đến khi vàng thơm.",
        "Đun nước mắm, đường và nước dừa đến khi hơi sánh, tắt bếp rồi cho tỏi ớt băm vào.",
        "Hành lá thái nhỏ cho vào bát, rưới dầu nóng lên, trộn đều làm mỡ hành.",
        "Xới cơm ra đĩa, xếp sườn, dưa leo, đồ chua, thêm trứng ốp la nếu thích, rưới mỡ hành và dọn kèm nước mắm."]),
    "bun_bo_hue": ("Bún bò Huế ít cay cho cả nhà, nước dùng thơm sả, ngọt xương, màu điều đẹp mắt.", 120, "kho", [
        "Xương heo, bắp giò, bắp bò rửa sạch, chần qua nước sôi có muối rồi rửa lại.",
        "Cho xương và thịt vào nồi cùng 1,7 lít nước, sả đập dập, hành tím, hành tây; đun sôi rồi hạ lửa nhỏ, ninh mở nắp khoảng 60 phút, nêm muối, hạt nêm, đường phèn.",
        "Hòa mắm ruốc với 500 ml nước, đun sôi rồi để lắng, chỉ lấy phần nước trong đổ vào nồi dùng.",
        "Trộn thịt xay với hành tím băm, muối, tiêu và chút màu điều, vo viên hoặc múc từng miếng thả vào nồi làm chả; phần màu điều còn lại cho vào nước dùng, nấu thêm 30 phút.",
        "Vớt thịt bò, giò heo ra thái lát; trụng bún, xếp thịt, chả, chan nước dùng, thêm hành tây, rau răm, ngò, hành lá. Để riêng sa tế cho người lớn."]),
    "chao_ngao": ("Cháo ngao ngọt thanh, thơm tía tô, ấm bụng, hợp bữa sáng hay khi trời lạnh.", 50, "vua", [
        "Ngao ngâm nhả cát, rửa sạch rồi luộc vừa há miệng; tách lấy thịt, để nước luộc lắng trong.",
        "Dùng nước ngao nấu cháo với gạo (rang sơ cho thơm) đến khi hạt gạo nở bung, nhừ mịn.",
        "Tía tô, hành lá thái nhỏ; hành khô băm, phi thơm rồi cho thịt ngao vào xào nhanh, nêm chút nước mắm cho vừa.",
        "Cho ngao xào vào nồi cháo, đun sôi lại và nêm nếm; nếu thích có thể thêm trứng vịt lộn.",
        "Múc ra bát, rắc tía tô, hành lá và chút tiêu."]),
    "mi_quang_ga": ("Mì Quảng gà vàng nghệ, nước nhân sánh đậm, giòn bùi đậu phộng, bánh tráng.", 90, "kho", [
        "Gà chặt miếng nhỏ, ướp với củ nén và nghệ giã nhuyễn, nước mắm, muối, tiêu, chút ớt bột và sả đập dập khoảng 30 phút.",
        "Hầm xương gà với củ cải trắng và khoảng 2 lít nước trong 1 tiếng, hớt bọt kỹ, nêm vừa ăn.",
        "Phi thơm hành tím với dầu phộng, cho gà vào đảo săn, thêm nước xâm xấp rồi rim đến khi gà thấm vị, trút vào nồi nước dùng.",
        "Pha nước mắm với tỏi, ớt giã nhỏ để chấm (để ớt riêng cho trẻ).",
        "Trụng mì, cho ra bát với rau sống, xếp gà lên, chan ít nước dùng, rắc đậu phộng, hành lá và bánh tráng nướng bẻ nhỏ."]),
    "banh_mi_op_la": ("Bánh mì ốp la trứng chín mềm, rưới xì dầu, ăn sáng nhanh gọn.", 10, "de", [
        "Đun nóng ít dầu trong chảo, đập trứng vào rồi hạ lửa nhỏ.",
        "Đậy nắp khoảng 3–4 phút cho lòng trắng chín, tắt bếp (để lâu hơn nếu muốn lòng đỏ chín hẳn cho bé).",
        "Rưới chút nước tương lên trứng, thêm ớt xay cho người lớn.",
        "Dưa leo thái lát mỏng, húng lủi rửa sạch, ăn cùng trứng và bánh mì nướng nóng."]),
    "chao_trung_thit_bam": ("Cháo trứng thịt băm mềm mịn, có rau củ, bữa sáng bổ dưỡng cho bé.", 45, "de", [
        "Vo gạo, cho vào nồi nước lạnh và nấu đến khi cháo nhừ; nếu dùng cháo gói thì đun sôi nước rồi cho cháo vào.",
        "Cà rốt thái hạt lựu nhỏ; phi thơm hành tỏi băm, cho thịt xay vào xào cùng cà rốt, bắp, nêm chút nước mắm, muối, đường.",
        "Trút phần thịt xào vào nồi cháo, khuấy đều, nêm lại hạt nêm cho vừa.",
        "Đập trứng vào bát đánh tan, rót từ từ vào nồi cháo vừa rót vừa khuấy nhẹ cho trứng chín thành vân.",
        "Múc ra bát, rắc hành lá, ngò rí và chút tiêu."]),
    "bun_moc": ("Bún mọc Hà Nội nước dùng sườn trong ngọt, viên mọc mềm thơm nấm hương.", 75, "vua", [
        "Sườn non chần qua nước sôi, rửa sạch rồi hầm với nước khoảng 40 phút làm nước dùng.",
        "Măng khô ngâm mềm, xé sợi, xào nhanh với chút dầu và hạt nêm; nấm hương rửa sạch, khía hoa rồi thả vào nồi nước dùng.",
        "Trộn giò sống với vài cây nấm hương băm nhỏ, múc từng viên thả vào nồi đang sôi lăn tăn, nấu khoảng 3 phút đến khi mọc nổi.",
        "Cho măng vào nồi, nêm lại nước mắm, hạt nêm cho vừa.",
        "Trụng bún và giá, cho ra bát, xếp sườn, mọc, măng, nấm, chan nước dùng; rắc hành ngò, tiêu, dọn kèm rau sống, chanh ớt."]),
    "com_chien_trung": ("Cơm chiên trứng vàng ươm, tơi hạt, thơm tỏi phi, làm nhanh từ cơm nguội.", 20, "de", [
        "Tách lòng đỏ và lòng trắng; trộn lòng đỏ với cơm nguội cùng chút hạt nêm cho hạt cơm áo vàng đều.",
        "Phi thơm tỏi băm với dầu, cho cơm vào chiên, đảo đều tay đến khi hạt cơm săn lại, rưới chút nước mắm quanh chảo.",
        "Đánh tan lòng trắng, đổ vào một góc chảo có ít dầu, khuấy nhanh cho tơi rồi đảo lẫn vào cơm.",
        "Rắc hành lá và chút tiêu, đảo đều rồi tắt bếp, xới ra đĩa."]),
    "mien_ga": ("Miến gà nước dùng ngọt thanh, gà xé, nấm đông cô, rau xanh đủ chất.", 50, "de", [
        "Luộc chín ức gà, vớt ra xé sợi, giữ nước luộc làm nước dùng.",
        "Cà rốt thái miếng, hành tây bổ múi cau, nấm đông cô cắt đôi, cải bó xôi cắt khúc.",
        "Đun sôi lại nước luộc gà, cho cà rốt, hành tây, nấm vào nấu đến khi cà rốt mềm, nêm muối, nước mắm, chút đường cho vừa.",
        "Ngâm miến cho mềm rồi trụng qua nước sôi; chần sơ cải bó xôi và giá.",
        "Xếp giá, cải, miến, gà xé vào bát, chan nước dùng cùng rau củ, rắc hành lá và tiêu."]),
    "chao_ca_thu": ("Cháo cá thu thơm gừng, thịt cá ngọt bùi, nhiều đạm cho bé lớn nhanh.", 45, "de", [
        "Vo sạch gạo rồi nấu cháo đến khi hạt gạo nở nhừ.",
        "Cá thu rửa sạch, ướp với chút nước mắm, tiêu, gừng thái sợi và đầu hành.",
        "Thả cá vào nồi cháo, đun đến khi cá chín thì vớt ra, gỡ bỏ hết xương rồi dằm thịt cá cho vào lại.",
        "Nêm cháo với nước mắm, muối cho vừa khẩu vị.",
        "Múc ra bát, rắc hành ngò thái nhỏ và chút tiêu."]),
    "chao_tom_hum_binh_ba": ("Cháo tôm hùm ngọt đậm từ vỏ tôm, thịt tôm chắc, món đãi cả nhà dịp đặc biệt.", 75, "kho", [
        "Tôm hùm làm sạch, luộc chín rồi tách lấy thịt, để riêng đầu và vỏ.",
        "Rang gạo cho thơm, nấu cùng đầu và vỏ tôm đến khi cháo nhừ (dùng nồi áp suất cho nhanh), sau đó vớt bỏ vỏ.",
        "Hành khô băm nhỏ, phi thơm rồi cho thịt tôm vào xào, nêm vừa ăn và thêm vài giọt dầu mè.",
        "Cho thịt tôm vào nồi cháo, đun lửa nhỏ thêm khoảng 15 phút, nêm lại gia vị.",
        "Múc ra bát, rắc gừng thái sợi và hành hoa thái nhỏ."]),
})

# ---------- Lô E ----------
CL.update({
    "lau_nam_thap_cam": ("Nồi lẩu ngọt thanh từ rau củ hầm, đủ loại nấm, hải sản và bò nhúng, cả nhà quây quần.", 90, "vua", [
        "Cho cà rốt, su su, bắp mỹ, bắp cải, hành tây và thơm cắt khúc vào nồi với khoảng 3 lít nước, hầm lửa vừa 45 phút cho ngọt nước.",
        "Lọc lấy nước dùng, nêm nước mắm, hạt nêm, đường, bột ngọt vừa miệng; vo chả cá thác lác thành viên nhỏ thả vào nồi.",
        "Trong lúc chờ, làm sạch mực, tôm, thái mỏng thịt bò; cắt gốc các loại nấm; rửa cải thảo, tần ô, để ráo và bày ra đĩa cùng bún.",
        "Đổ nước dùng vào nồi lẩu, đun sôi rồi nhúng nấm, hải sản, bò và rau theo lượt; trẻ nhỏ gắp phần nấm, tôm chín kỹ chấm nước mắm nhạt."]),
    "lau_hai_san": ("Lẩu hải sản chua nhẹ vị thơm cà, nước ngọt từ vỏ tôm, mực giòn và bò mềm.", 60, "vua", [
        "Bóc vỏ tôm, giữ lại vỏ; lột da mực, khía và cắt lát; thái mỏng thịt bò; xếp từng loại ra đĩa riêng.",
        "Luộc vỏ tôm với khoảng 2 lít nước chừng 10 phút, lọc lấy nước làm nước lẩu.",
        "Phi thơm hành với chút dầu, cho cà chua và thơm cắt lát vào xào mềm rồi trút vào nồi nước lẩu, nêm nước mắm, muối, tiêu cho đậm vừa.",
        "Rửa sạch cải và mùng tơi, cắt hành ngò; bắc nồi lẩu lên bếp, nhúng mực, tôm, bò rồi đến rau, ăn kèm bún."]),
    "bo_nhung_giam": ("Bò nhúng giấm chua ngọt thơm nước dừa, cuốn bánh tráng cùng rau sống và dưa leo.", 120, "kho", [
        "Rửa sạch nạm bò, luộc với chút muối và hạt nêm khoảng 50 phút đến khi mềm, ủ thêm 15 phút rồi ngâm nước lạnh và thái mỏng.",
        "Phi thơm hành khô băm, xào cùng sả đập dập và vài miếng dứa, thêm táo thái miếng và chút nước, đun đến khi táo mềm rồi lọc lấy nước.",
        "Đổ nước dừa và nước khoáng có ga vào phần nước vừa lọc, thêm giấm, dừa non, hành tây, nêm muối, đường cho chua ngọt hài hòa; cho rau mùi, ớt vào sau cùng (để riêng phần cho trẻ).",
        "Bày bắp bò sống thái mỏng, bò chín, đậu rán, quẩy, nấm, xà lách, cải thảo, cà rốt, dưa chuột ra đĩa.",
        "Nhúng bò vào nồi giấm sôi, cuốn bánh tráng với bún và rau, chấm mắm nêm hoặc nước mắm pha; nhúng chín kỹ phần cho trẻ."]),
    "lau_rieu_cua": ("Lẩu riêu cua đồng gạch vàng ươm, chua dịu vị cà chua mẻ, nhúng bò và rau tươi.", 90, "kho", [
        "Ninh xương ống lấy nước dùng khoảng 1 giờ. Tách mai cua, khều gạch để riêng, giã nhỏ phần thân cua rồi lọc với nước lấy nước cua.",
        "Hòa nước cua với chút muối và mắm tôm, đun lửa vừa, khuấy nhẹ một chiều để gạch không dính đáy; khi riêu đóng mảng thì hớt riêng ra bát.",
        "Phi thơm hành khô, cho cà chua bổ cau xào nát, thêm gạch cua đảo cùng, nêm chút mắm rồi đổ vào nồi nước cua cùng nước xương, thêm mẻ lọc cho chua dịu.",
        "Cho riêu cua trở lại nồi lẩu, bày bắp bò thái mỏng, mọc viên, nấm và rau xanh ra đĩa, nhúng dần khi ăn."]),
    "lau_muc": ("Lẩu mực kiểu Phan Rang chua ngọt vị me thơm, mực ống giòn sần sật.", 45, "de", [
        "Làm sạch mực ống, bỏ túi mực, cắt khoanh vừa ăn; cà chua bổ múi, thơm thái lát.",
        "Phi thơm tỏi với chút dầu rồi vớt tỏi ra bát để riêng.",
        "Đun nước dùng gà với thơm, cà chua và me chín, khi sôi lọc bớt bã me, nêm mắm, muối, đường cho chua ngọt vừa miệng.",
        "Thả mực vào nồi đến khi vừa chín, nêm lại hơi đậm để nhúng rau, rắc tỏi phi, ngò tàu và hành ngò; ăn kèm bún, ớt để riêng cho người lớn."]),
    "che_dau_xanh_bot_bang": ("Chè đậu xanh nấu nhừ sánh mịn, bột báng dẻo trong, ngọt dịu dễ ăn cho trẻ.", 60, "de", [
        "Ngâm đậu xanh cà vỏ khoảng 2 tiếng (hoặc qua đêm) cho nở mềm, đãi sạch; ngâm bột báng 30 phút.",
        "Nấu đậu với 900ml nước khoảng 30 phút đến khi nhừ, dùng muôi đánh cho đậu tan bớt.",
        "Cho đường vào khuấy tan, để lửa vừa và khuấy thường xuyên để chè không trào hay bén đáy.",
        "Thả bột báng vào, hạ lửa nhỏ, khuấy đều thêm khoảng 5 phút đến khi bột báng trong là tắt bếp; có thể chan chút nước cốt dừa khi ăn."]),
    "banh_flan": ("Bánh flan mềm mịn béo sữa, lớp caramen đắng nhẹ, món tráng miệng trẻ con mê.", 75, "vua", [
        "Đánh tan trứng theo một chiều bằng phới lồng, tránh tạo bọt; thêm sữa tươi, sữa đặc, whipping cream, vani và nhúm muối, khuấy đều rồi lọc qua rây.",
        "Cho đường cùng khoảng 30ml nước vào nồi nhỏ, đun lửa vừa không khuấy đến khi đường ngả vàng thì hạ lửa.",
        "Vắt nước cốt chanh và phần nước còn lại vào, lắc nhẹ, đun đến màu cánh gián thì tắt bếp, chia nhanh vào đáy các hũ một lớp mỏng.",
        "Đợi caramen đông thì rót hỗn hợp sữa trứng vào, đậy nắp, hấp lửa thật nhỏ khoảng 30 phút; mặt bánh se lại và chọc tăm thấy sạch là chín.",
        "Để nguội rồi cất ngăn mát vài tiếng hoặc qua đêm cho bánh chắc và lạnh mới ăn."]),
    "rau_cau_dua": ("Rau câu dừa hai lớp: lớp trong ngọt nước dừa xiêm, lớp trắng béo nước cốt dừa.", 60, "vua", [
        "Trộn đều 10g bột rau câu với 150g đường, đổ nước dừa xiêm vào (thiếu thì thêm nước lọc cho đủ khoảng 1,2 lít), nấu lửa nhỏ, khuấy liên tục đến khi sôi và rau câu tan trong.",
        "Đổ lớp nước dừa vào khuôn, để yên cho se mặt.",
        "Trộn 5g bột rau câu với 100g đường, nấu cùng 350ml nước đến sôi; thêm nước cốt dừa và bát tinh bột đậu xanh đã hòa với 20ml nước, khuấy nhẹ đến khi sôi lại.",
        "Rót từ từ lớp nước cốt dừa lên mặt lớp rau câu trong để hai lớp bám vào nhau, để nguội rồi cho vào ngăn mát vài tiếng.",
        "Khi rau câu đông cứng, lấy ra khỏi khuôn, cắt miếng vừa ăn."]),
    "che_troi_nuoc": ("Chè trôi nước viên nếp dẻo nhân đậu xanh bùi, nước đường gừng ấm, rắc mè rang và cốt dừa.", 120, "kho", [
        "Ngâm đậu xanh 1 tiếng, nấu chín bằng nồi cơm điện với nhiều nước, tán nhuyễn cùng chút đường và muối rồi vo thành viên nhỏ.",
        "Để riêng khoảng 50g bột nếp làm bột áo; phần còn lại nhào với nước ấm từ từ đến khi mịn, không dính tay, đậy kín ủ 30 phút.",
        "Chia bột thành miếng dẹt, đặt viên nhân vào giữa, bọc kín và vê tròn, lăn qua bột áo; rang mè vàng, gừng gọt vỏ thái sợi.",
        "Luộc các viên chè trong nồi nước sôi, viên nổi lên thì vớt ngay sang thau nước lạnh.",
        "Nấu 1 lít nước với đường vàng, đường trắng, gừng và lá dứa đến khi đường tan, thả viên chè vào đun thêm 5 phút cho thấm.",
        "Vắt dừa nạo lấy nước cốt, nấu với chút đường và bột năng cho sánh; múc chè ra bát, chan cốt dừa, rắc mè. Cho trẻ ăn viên nhỏ, cắt đôi cho dễ nuốt."]),
    "che_hat_sen_duong_phen": ("Chè hạt sen đường phèn thanh mát, hạt sen bở bùi, ngọt nhẹ giải nhiệt.", 60, "de", [
        "Rửa sạch hạt sen, bỏ tim để chè không bị đắng.",
        "Đun sôi khoảng 1 lít nước, cho hạt sen vào, khi sôi lại thì hạ lửa liu riu và để mở vung cho hạt không bị nứt.",
        "Nấu 30–40 phút đến khi hạt sen mềm bở, cho đường phèn vào, giữ lửa nhỏ thêm 15 phút rồi tắt bếp.",
        "Để nguội, ăn với đá hoặc cất ngăn mát; phần cho trẻ nên ăn ở nhiệt độ thường."]),
    "sua_chua_nha_lam": ("Sữa chua nhà làm dẻo mịn chua ngọt vừa phải, ủ bằng nồi cơm điện tiện lợi.", 40, "vua", [
        "Để hũ sữa chua cái ra ngoài cho bớt lạnh. Cho sữa đặc, sữa tươi và nước lọc (đong bằng lon sữa) vào nồi, khuấy tan, đun nóng già rồi tắt bếp.",
        "Để sữa nguội còn ấm tay (khoảng 40–45°C); hòa sữa chua cái với một muôi sữa ấm cho tan rồi lọc qua rây vào nồi, khuấy nhẹ.",
        "Rót vào hũ sạch, đậy nắp, xếp vào nồi cơm điện không cắm điện, phủ khăn và ủ khoảng 8–10 tiếng, tuyệt đối không xê dịch.",
        "Khi sữa chua đông đặc và mịn thì chuyển vào ngăn mát; ăn kèm trái cây hoặc cấp đông làm sữa chua đá."]),
    "che_buoi": ("Chè bưởi cùi giòn sần sật, đỗ xanh bùi, nước chè sánh thơm, rưới cốt dừa béo ngậy.", 150, "kho", [
        "Gọt lấy cùi trắng của bưởi, bỏ vỏ xanh và lớp xơ sát múi, thái hạt lựu; ngâm đỗ xanh ít nhất 2 tiếng.",
        "Ngâm cùi trong nước sôi khoảng 10 phút rồi vắt kiệt, lặp lại vài lần đến khi cùi hết đắng và vắt không còn phồng lại; xả lại nước sạch.",
        "Thắng một ít đường đến màu cánh gián, thêm nước và đường đun sôi, để nguội ấm thì trộn cùi bưởi vào, rồi lăn cùi qua bột năng cho áo đều.",
        "Luộc cùi trong nước sôi đến khi nổi và trong thì vớt ngay vào thau nước đá, để ráo. Đỗ xanh hấp hoặc nấu chín vừa tới, còn nguyên hạt.",
        "Dùng nồi nước luộc cùi, thêm đường, khuấy bột năng hòa nước lạnh vào cho sánh, cho đỗ xanh vào; để nguội bớt rồi trút cùi bưởi vào trộn đều.",
        "Đun nước cốt dừa với chút đường và bột năng cho sánh; múc chè ra bát, rưới cốt dừa, thêm đá cho người lớn."]),
    "che_bo": ("Chè bơ đông mát béo mịn, ngọt dịu sữa, ăn kèm nước cốt dừa hay sữa tươi.", 30, "de", [
        "Bơ chín bổ đôi, bỏ hạt, nạo lấy thịt.",
        "Hòa gelatin với chút nước, đun hoặc quay lò vi sóng khoảng 40 giây cho tan rồi để nguội bớt.",
        "Xay bơ với sữa tươi, sữa đặc pha nước và whipping cream đến khi thật mịn, có thể lọc qua rây.",
        "Trộn gelatin vào hỗn hợp bơ, đổ khuôn và cất ngăn mát vài tiếng cho đông; nhúng dao qua nước nóng để cắt và lấy chè ra dễ."]),
    "thach_rau_cau_bo": ("Thạch rau câu bơ dẻo mịn, béo vị sữa và cốt dừa, màu xanh mát mắt.", 40, "de", [
        "Cắt bơ thành miếng, xay nhuyễn cùng 4 thìa sữa đặc và 1 hộp sữa tươi.",
        "Đun sôi 700ml nước, thêm phần sữa đặc và sữa tươi còn lại, rây bột rau câu và bột cốt dừa vào, khuấy đều trên lửa nhỏ, nêm đường vừa ngọt.",
        "Đun lăn tăn khoảng 5 phút rồi tắt bếp, để nguội 5 phút cho đỡ nóng.",
        "Đổ bơ xay vào khuấy đều, rót qua rây vào các hũ cho mịn mặt, cất ngăn mát đến khi đông."]),
    "trai_cay_lac": ("Trái cây lắc chua ngọt mặn cay, nước mắm đường sánh quyện muối tôm, ăn chơi cực vui miệng.", 20, "de", [
        "Gọt vỏ xoài, cóc hoặc táo, cắt miếng dài vừa ăn.",
        "Pha nước mắm đường lắc theo tỉ lệ 2 phần nước mắm, 4 phần đường vàng, 1 phần nước; đun sôi lửa vừa, không khuấy, đến khi hơi sánh rồi để nguội.",
        "Cho trái cây vào hộp có nắp, thêm nước mắm đường, muối tôm, đường và ớt bột, đậy kín rồi lắc đều cho thấm.",
        "Với trẻ nhỏ, bớt ớt bột và muối tôm hoặc chấm chút muối đường thôi."]),
    "che_dau_do": ("Chè đậu đỏ nấu bở mềm, ngọt bùi, chan nước cốt dừa thơm vani.", 90, "de", [
        "Rửa sạch đậu đỏ, ngâm vài tiếng hoặc qua đêm cho nhanh mềm.",
        "Nấu đậu với nhiều nước (hoặc dùng nồi cơm điện, sôi rồi ủ) đến khi hạt bở mềm.",
        "Cho đường vào đậu, khuấy nhẹ và nấu thêm vài phút cho thấm, nêm độ ngọt tùy ý.",
        "Đun nước cốt dừa lửa nhỏ với chút đường, tắt bếp thì cho vani; múc chè ra bát, chan cốt dừa lên."]),
    "che_xoai": ("Chè xoài nhiều tầng: thạch xoài sữa chua, xoài tươi, bột báng, thạch đen và cốt dừa béo.", 60, "vua", [
        "Xay 2–3 quả xoài với hộp sữa chua. Ngâm bột rau câu với khoảng 100ml nước 15 phút, đun sôi rồi hạ nhỏ lửa, cho xoài xay vào khuấy đều, đổ khuôn để đông.",
        "Thả bột báng vào nồi nước sôi đun 20 phút, tắt bếp ủ thêm 20 phút, xả nước lạnh rồi trộn với 1–2 thìa đường.",
        "Pha nước cốt dừa với lượng nước tương đương, thêm sữa đặc, khuấy bột năng vào và đun đến khi hơi sánh.",
        "Cắt thạch xoài, xoài tươi và thạch đen thành hạt lựu, xếp vào bát cùng bột báng, rưới nước cốt dừa và thêm đá."]),
    "thach_nho_ninh_thuan": ("Thạch nho Ninh Thuận tím đẹp mắt, chua ngọt tự nhiên, trẻ nhỏ thích mê.", 30, "de", [
        "Rửa sạch nho, bỏ hạt rồi xay nhuyễn với chút nước, lọc qua rây lấy nước nho.",
        "Rắc bột gelatin vào nước nho, để vài phút cho bột nở.",
        "Đun lửa nhỏ, khuấy đều đến khi gelatin tan hoàn toàn, không để sôi lớn.",
        "Rót vào khuôn yêu thích, để nguội rồi cất ngăn mát đến khi đông lại là ăn được."]),
    "sua_chua_nep_cam": ("Sữa chua nếp cẩm dẻo thơm, chua ngọt mát lạnh, vừa ăn vặt vừa tốt cho tiêu hóa.", 60, "de", [
        "Ngâm nếp cẩm khoảng 8 tiếng hoặc qua đêm, vo lại và thay nước sạch.",
        "Nấu nếp với 800ml nước bằng nồi cơm điện đến khi chín dẻo, để nguội.",
        "Múc nếp cẩm vào cốc, trộn chút đường nếu thích ngọt, thêm sữa chua lên trên.",
        "Cho đá bào hoặc ướp lạnh, khi ăn khuấy đều cho nếp quyện sữa chua."]),
    "hong_gion_tron_sua_chua": ("Hồng giòn trộn sữa chua mát lạnh, ngọt thanh, tráng miệng nhẹ nhàng sau bữa cơm.", 15, "de", [
        "Gọt vỏ hồng giòn, rửa sạch, để ráo rồi cắt miếng vừa ăn.",
        "Trộn hồng với sữa chua và sữa đặc cho đều.",
        "Chia ra cốc, cất ngăn mát khoảng 30 phút cho lạnh rồi ăn."]),
    "sua_ngo": ("Sữa ngô ngọt tự nhiên từ ngô và chà là, thơm béo, không cần thêm đường.", 40, "de", [
        "Luộc ngô ngọt âm ỉ 15–20 phút cho nước đậm ngọt, vớt ra tách hạt, giữ lại nước luộc.",
        "Để nước luộc nguội bớt, cho hạt ngô, nước luộc và vài quả chà là bỏ hạt vào máy xay, xay thật kỹ.",
        "Lọc qua rây mịn hoặc túi lọc, thêm một nhúm muối cho tròn vị; uống ấm hoặc ướp lạnh."]),
    "nuoc_nha_dam_la_dua": ("Nước nha đam lá dứa thanh mát, ngọt nhẹ đường phèn, nha đam giòn mát.", 30, "de", [
        "Gọt bỏ vỏ xanh nha đam, rửa sạch nhựa, cắt hạt lựu, ngâm nước muối loãng 10 phút rồi xả lại thật kỹ cho hết nhớt.",
        "Đun 500ml nước với đường phèn và lá dứa buộc túm đến khi sôi và đường tan.",
        "Cho nha đam vào đun thêm khoảng 3 phút, vớt lá dứa ra.",
        "Để nguội rồi cất ngăn mát, dùng trong vòng 2 ngày."]),
    "tra_chanh_day": ("Trà chanh dây chua thơm mát lạnh, vị trà đen dịu, giải khát ngày nóng.", 15, "de", [
        "Cắt đôi chanh dây, nạo lấy ruột rồi lọc qua rây lấy nước cốt, bỏ hạt.",
        "Hãm túi trà đen với nước sôi vài phút, bỏ túi trà và để nguội bớt.",
        "Đổ nước cốt chanh dây vào trà, thêm nước đường, nếm và gia giảm cho vừa.",
        "Cho đá vào, khuấy đều rồi rót ra ly."]),
    "sinh_to_thanh_long_chuoi": ("Sinh tố thanh long chuối táo ngọt dịu, mịn mượt, hợp cả bé đang ăn dặm.", 15, "de", [
        "Rửa sạch, gọt vỏ thanh long, chuối và táo, thái nhỏ.",
        "Với bé mới tập ăn dặm, hấp sơ táo và thanh long vài phút cho mềm; bé lớn hơn có thể dùng tươi.",
        "Xay tất cả cùng sữa công thức hoặc sữa mẹ đến khi mịn.",
        "Lọc lại qua rây nếu bé chưa quen ăn thô, rót ra cốc dùng ngay."]),
    "sua_dau_xanh": ("Sữa đậu xanh nấu bằng máy làm sữa hạt, bùi thơm, ngọt thanh từ chà là và táo đỏ.", 35, "de", [
        "Rửa sạch đậu xanh và đậu nành, ngâm nước qua đêm rồi để ráo.",
        "Rửa táo đỏ, chà là, kỷ tử; bỏ hạt táo đỏ và chà là.",
        "Cho tất cả vào máy làm sữa hạt cùng nước lọc, chọn chế độ nấu sữa khoảng 25 phút.",
        "Lọc lại nếu muốn sữa mịn hơn, uống ấm hoặc để nguội cất ngăn mát."]),
    "nuoc_ep_ca_rot_tao": ("Nước ép cà rốt táo xanh ngọt mát, thêm chút chanh cho tươi vị, giàu vitamin.", 15, "de", [
        "Rửa sạch cà rốt và táo xanh, gọt vỏ cà rốt, bỏ lõi táo, cắt miếng vừa ống máy ép.",
        "Ép lần lượt cà rốt và táo bằng máy ép chậm.",
        "Vắt thêm chút nước cốt chanh, khuấy đều và uống ngay để giữ trọn vitamin."]),
    "suong_sao": ("Sương sáo đen dai mềm thơm dầu chuối, ăn kèm nước đường hoặc cốt dừa giải nhiệt.", 30, "de", [
        "Hòa bột sương sáo vào 800ml nước lọc, vừa đổ vừa khuấy cho tan hết, để ngâm khoảng 5 phút.",
        "Bắc lên bếp lửa vừa, thêm đường, khuấy liên tục để sương sáo chín đều và không cháy đáy.",
        "Khi hỗn hợp sánh đặc lại thì tắt bếp, nhỏ vài giọt dầu chuối khuấy đều.",
        "Đổ ra khuôn, để nguội cho đông, cắt miếng và ăn cùng nước đường, đá hoặc cốt dừa."]),
    "tra_dao_cam_sa": ("Trà đào cam sả thơm nồng sả, chua ngọt cam đào, mát lạnh sảng khoái.", 25, "de", [
        "Đập dập sả, đun sôi cùng nước khoảng 5 phút; cắt một lát cam để trang trí, phần còn lại vắt lấy nước.",
        "Cho túi trà vào ly hoặc bình, đổ nước sả nóng vào, hãm 10 phút rồi vớt túi trà ra.",
        "Cho nước cam, nước đào ngâm và đường hoặc siro vào trà, lắc hoặc khuấy đều cùng đá.",
        "Rót ra ly, thêm đào miếng, lát cam và một khúc sả lên trên."]),
    "nuoc_chanh_muoi": ("Nước chanh muối mặn ngọt thanh, mát họng, dễ uống sau bữa ăn.", 5, "de", [
        "Lấy quả chanh muối, bỏ hạt và dầm nhẹ trong cốc.",
        "Thêm đường và chút nước, khuấy cho tan.",
        "Đổ nước lọc và đá viên vào, nếm lại độ mặn ngọt rồi uống."]),
    "nuoc_rau_ma": ("Nước rau má xanh mát, thanh nhiệt, thêm chút đường cho dễ uống.", 20, "de", [
        "Nhặt bỏ lá úa, rửa sạch rau má, ngâm nước muối loãng 10 phút rồi rửa lại và để ráo.",
        "Xay rau má với nước sôi để nguội, khoảng 100g rau với 1 cốc nước.",
        "Lọc qua túi vải vắt kiệt, hớt bỏ bọt, thêm đường nếu thích.",
        "Uống với đá hoặc cất chai thủy tinh trong ngăn mát, dùng trong 24 giờ."]),
    "sinh_to_xoai": ("Sinh tố xoài sánh mịn, ngọt thơm sữa đặc, thoang thoảng chanh dây.", 10, "de", [
        "Gọt vỏ xoài chín, cắt miếng bỏ hạt.",
        "Cho xoài, đường, sữa đặc, sữa tươi và siro chanh dây vào máy xay, xay đến khi nhuyễn mịn.",
        "Thêm đá viên nhỏ hoặc đá bào, xay tiếp đến khi hỗn hợp đều và sánh.",
        "Rót ra ly uống ngay."]),
    "nuoc_ep_dua_hau": ("Nước ép dưa hấu đỏ mát, điểm lát xoài vàng, trẻ con thích thú.", 10, "de", [
        "Gọt vỏ dưa hấu, bỏ bớt hạt, cắt miếng rồi ép hoặc xay và lọc lấy nước.",
        "Tỉa lát xoài thành hình ngôi sao, đặt vào ly cùng đá.",
        "Rót nhẹ nước dưa hấu vào ly và uống ngay cho mát."]),
    "nuoc_mia_lau_re_tranh": ("Nước mía lau rễ tranh nấu kiểu xưa, ngọt thanh mát, giải nhiệt ngày hè.", 60, "de", [
        "Rửa sạch mía lau, chặt khúc và chẻ mỏng; rễ tranh rửa sạch cắt khúc; rau má nhặt rửa kỹ.",
        "Xếp mía lau dưới đáy nồi, cho rễ tranh và rau má lên trên, đổ nước ngập.",
        "Đun sôi rồi hạ lửa nhỏ, nấu khoảng 40 phút cho ra hết vị ngọt.",
        "Lọc lấy nước, để nguội rồi cất ngăn mát, uống dần trong ngày."]),
    "thit_heo_gia_bo_kho": ("Thịt heo giả bò khô xé sợi cay ngọt, thơm sả ớt, nhâm nhi hay ăn vặt đều hợp.", 180, "kho", [
        "Thái thịt nạc thành miếng dài theo thớ, luộc vừa chín tới, để nguội rồi xé sợi vừa phải, không xé quá nhỏ.",
        "Giã nhỏ tỏi, gừng và phần lớn sả, trộn với ớt bột, tương ớt, đường, gia vị, nghệ, dầu hào, ngũ vị hương, gia vị bò kho và bột điều.",
        "Trộn hỗn hợp gia vị với thịt xé, ướp 1–2 tiếng cho ngấm.",
        "Cho thịt vào nồi cùng chút nước xâm xấp, thêm sả còn lại và ớt tươi bổ dọc, đun sôi rồi hạ lửa nhỏ, đảo thỉnh thoảng đến khi cạn nước.",
        "Chuyển thịt sang chảo, rang lửa nhỏ, đảo liên tục đến khi thịt săn khô, ngả nâu đậm; để nguội rồi cho vào hũ kín. Phần cho trẻ nên bớt ớt."]),
    "muc_rim_me": ("Mực khô rim me chua ngọt sền sệt, ăn kèm ớt chuông giòn mát.", 30, "vua", [
        "Nướng mực khô cho chín thơm, đập dập rồi xé sợi nhỏ.",
        "Rửa ớt chuông, cắt miếng vừa ăn, ngâm đá cho giòn.",
        "Phi vàng tỏi và ớt băm với dầu, cho mực xé vào đảo, nêm đường, ớt bột, nước mắm và chút bột ngọt.",
        "Đổ nước cốt me đã lọc hạt vào, rim lửa nhỏ đến khi sốt sệt bám đều sợi mực; ăn kèm ớt chuông."]),
    "do_chua_ca_rot_cu_cai": ("Đồ chua cà rốt củ cải giòn sần sật, chua ngọt vừa, ăn kèm thịt nướng hay bánh mì.", 40, "de", [
        "Gọt vỏ cà rốt và củ cải trắng, bào sợi hoặc thái que, cho chung vào âu.",
        "Bóp với muối, để 15 phút cho ra nước rồi vắt thật ráo.",
        "Trộn giấm và đường vào, để khoảng 15 phút là ăn được; phần dư cho vào hũ kín cất ngăn mát, dùng trong vài ngày."]),
    "ca_phao_muoi_xoi": ("Cà pháo muối xổi giòn tan, chua cay mặn ngọt, ăn với cơm canh ngày nào cũng hợp.", 150, "de", [
        "Chọn cà pháo vừa tới, rửa sạch, cắt cuống rồi bổ đôi hoặc bổ ba.",
        "Ngâm cà trong nước muối pha nửa quả chanh khoảng 30 phút cho ra hết nhựa, rửa lại và để ráo.",
        "Giã hoặc băm tỏi ớt, pha với nước mắm, đường và nước cốt chanh cho chua mặn ngọt vừa miệng.",
        "Trộn cà với nước mắm vừa pha, cho vào hũ đậy kín, để nhiệt độ phòng 1–2 tiếng là ăn được, sau đó cất ngăn mát."]),
    "dua_cai_muoi_chua": ("Dưa cải muối chua giòn vàng ươm, thơm hành, ăn kèm cơm, kho cá hay xào thịt.", 60, "vua", [
        "Cắt bớt lá cải, phơi héo khoảng 3 tiếng nếu có thời gian; rửa sạch, cắt miếng vừa ăn và để ráo. Hành bắc bóc vỏ, rửa sạch.",
        "Đun sôi 2 lít nước, tráng hũ và nắp bằng nước sôi; hòa muối và đường vào phần nước còn lại, để nguội.",
        "Trộn cải, hành với nước muối trong thau lớn khoảng 30 phút cho cải hơi héo.",
        "Xếp cải vào hũ, đổ nước muối ngập, dùng vỉ tre hoặc đĩa nén chặt; đậy nắp, để 3–4 ngày là dưa chua vàng."]),
    "hu_tieu_kho": ("Hủ tiếu khô kiểu Nam Vang sợi dai trộn sốt mặn ngọt, tôm thịt đầy đặn, kèm chén nước dùng ngọt xương.", 90, "vua", [
        "Hầm xương heo khoảng 1 giờ với hành tây nướng, hớt bọt kỹ, nêm muối, chút đường phèn cho nước trong ngọt.",
        "Luộc thịt nạc vai và gan heo trong nồi nước dùng đến chín, vớt ra thái mỏng; thả tôm vào chần chín, bóc vỏ.",
        "Phi vàng tỏi băm, vớt bớt tỏi phi để riêng; cho thịt băm vào xào săn, nêm chút nước mắm và tiêu.",
        "Pha sốt: nước tương, dầu hào, đường và chút nước dùng đun sôi đến hơi sánh, thêm dầu tỏi phi.",
        "Trụng sợi hủ tiếu và giá qua nước sôi, để ráo, trộn với sốt trong bát; xếp thịt băm, tôm, thịt và gan lên trên, rắc hẹ cắt khúc, tỏi phi, hành phi.",
        "Múc chén nước dùng nóng có hành ngò ăn kèm; phần cho trẻ cắt sợi ngắn, bớt sốt."]),
})
