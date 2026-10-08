// Cá Chef – gợi ý bữa trưa, tối theo thời tiết Phan Rang và mùa vụ (hôm nay, ngày mai), giao diện cho điện thoại.
const LAT = 11.56, LON = 108.99;
const WEATHER_URL = `https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}` +
  "&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m" +
  "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum," +
  "precipitation_probability_max,wind_speed_10m_max,uv_index_max" +
  "&timezone=Asia%2FHo_Chi_Minh&forecast_days=2";
const HISTORY_KEY = "cachef.history";
const CHON_KEY = "cachef.chon";

const LABEL = {
  loai: { mon_chinh: "Món chính", canh: "Canh", goi: "Gỏi", lau: "Lẩu", an_vat: "Ăn vặt", trang_mieng: "Tráng miệng", do_uong: "Đồ uống" },
  nhiet: { mat: "Mát", am: "Ấm", nong: "Nóng" },
  do_nang: { nhe: "Nhẹ bụng", nang: "No lâu" },
  dau_mo: { it: "Ít dầu", vua: "Dầu vừa", nhieu: "Nhiều dầu" },
  do_kho: { de: "Dễ", vua: "Vừa", kho: "Khó" },
  vai_mam: { man: "Món mặn", rau: "Món rau", canh: "Canh", mot_to: "Món một tô (sáng)", lau: "Lẩu", nuong: "Bữa nướng",
    trang_mieng: "Tráng miệng, chè", do_uong: "Đồ uống", an_vat: "Ăn vặt", dua_kem: "Dưa, đồ ăn kèm" },
};

const S = { data: null, weather: null, ing: {}, prices: {}, ingByDish: {}, nhan: {}, query: "", ranked: [], rankedTomorrow: [], meals: [null, null], shown: [{ trua: new Set(), toi: new Set() }, { trua: new Set(), toi: new Set() }], servings: {}, chon: {}, anh: {}, bq: {} };

// Món đã chọn trong bữa (giữ nguyên khi bấm Đổi các món còn lại), lưu theo ngày để tải lại trang vẫn còn.
function readChon() {
  try { return JSON.parse(localStorage.getItem(CHON_KEY) || "{}"); } catch { return {}; }
}
// Giữ trong phiên (S.chon) là chính; localStorage chỉ để tải lại trang vẫn còn.
function chonOf(day) {
  const ngay = dayStr(day);
  if (!S.chon[ngay]) {
    const k = readChon()[ngay] || {};
    S.chon[ngay] = { trua: new Set(k.trua || []), toi: new Set(k.toi || []) };
  }
  return S.chon[ngay];
}
function saveChon(day, chon) {
  S.chon[dayStr(day)] = chon;
  try {
    const all = readChon(), giu = new Set([dayStr(0), dayStr(1)]);
    for (const d of Object.keys(all)) if (!giu.has(d)) delete all[d];
    all[dayStr(day)] = { trua: [...chon.trua], toi: [...chon.toi] };
    localStorage.setItem(CHON_KEY, JSON.stringify(all));
  } catch { /* trình duyệt chặn lưu: lựa chọn chỉ còn trong phiên này */ }
}
// Món đã chọn của một ngày, lấy từ danh sách đã chấm điểm (bỏ qua mã không còn trong dữ liệu).
function monDaChon(ranked, day) {
  const k = chonOf(day), tim = (ma) => ranked.find((d) => d.ma_mon === ma);
  return { trua: [...k.trua].map(tim).filter(Boolean), toi: [...k.toi].map(tim).filter(Boolean) };
}
// Bữa đang hiện (sau khi bấm Đổi) và các món đã xem, lưu theo ngày để F5 không gợi ý lại từ đầu.
const BUA_KEY = "cachef.bua";
function saveBua(day) {
  const m = S.meals[day];
  if (!m) return;
  try {
    const all = JSON.parse(localStorage.getItem(BUA_KEY) || "{}"), giu = new Set([dayStr(0), dayStr(1)]);
    for (const d of Object.keys(all)) if (!giu.has(d)) delete all[d];
    const ma = (l) => l.map((d) => d.ma_mon);
    all[dayStr(day)] = { trua: ma(m.trua), toi: ma(m.toi), lau: m.lau, du: m.du,
      shown: { trua: [...S.shown[day].trua], toi: [...S.shown[day].toi] } };
    localStorage.setItem(BUA_KEY, JSON.stringify(all));
  } catch { /* chặn lưu: F5 sẽ gợi ý lại */ }
}
// Khôi phục bữa đã lưu nếu mọi món còn trong dữ liệu; không thì null để ghép bữa mới.
function readBua(ranked, day) {
  try {
    const b = JSON.parse(localStorage.getItem(BUA_KEY) || "{}")[dayStr(day)];
    if (!b) return null;
    const tim = (ma) => ranked.find((d) => d.ma_mon === ma);
    const trua = b.trua.map(tim), toi = b.toi.map(tim);
    if (!trua.length || [...trua, ...toi].some((d) => !d)) return null;
    S.shown[day] = { trua: new Set(b.shown?.trua || []), toi: new Set(b.shown?.toi || []) };
    return { trua, toi, lau: !!b.lau, du: b.du || null };
  } catch { return null; }
}
const $app = document.getElementById("app");
// Bỏ dấu tiếng Việt để tìm kiếm không cần gõ dấu.
const plain = (s) => String(s ?? "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toLowerCase();
const hasRecipe = (d) => String(d.cach_lam ?? "").trim() !== "";
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const today = () => new Date().toLocaleDateString("sv-SE", { timeZone: "Asia/Ho_Chi_Minh" });
// Ngày (YYYY-MM-DD, giờ Việt Nam) cách hôm nay `i` ngày; tháng tương ứng.
const dayStr = (i = 0) => new Date(Date.parse(today()) + i * 86400000).toISOString().slice(0, 10);
const month = (i = 0) => Number(dayStr(i).slice(5, 7));

// ---------- Dữ liệu ----------
async function load() {
  const [data, weather] = await Promise.all([
    fetch(`data.json?t=${Date.now()}`).then((r) => r.json()),
    fetch(WEATHER_URL).then((r) => r.json()).catch(() => null),
  ]);
  S.data = data;
  S.weather = weather;
  for (const n of data.nguyen_lieu) {
    n.thang = Array.from({ length: 12 }, (_, i) => Number(n[`T${i + 1}`]) || 0);
    S.ing[n.ma] = n;
  }
  for (const p of data.gia_go) S.prices[p.ma_nguyen_lieu] = p;
  for (const r of data.mon_nguyen_lieu) (S.ingByDish[r.ma_mon] ??= []).push(r);
  for (const r of data.mon_nhan || []) S.nhan[r.ma_mon] = r;
  for (const r of data.anh_mon || []) if (r.anh_id) S.anh[r.ma_mon] = r;
  for (const r of data.bi_quyet || []) S.bq[r.ma] = r;
  S.ranked = rankDishes(0);
  S.meals[0] = readBua(S.ranked, 0) || pickMeals(S.ranked, 0, monDaChon(S.ranked, 0));
  saveBua(0);
  recordHistory(mealDishes(S.meals[0]).map((d) => d.ma_mon));
  S.rankedTomorrow = rankDishes(1); // sau recordHistory để không gợi ý lại món của hôm nay
  S.meals[1] = readBua(S.rankedTomorrow, 1) || pickMeals(S.rankedTomorrow, 1, monDaChon(S.rankedTomorrow, 1));
  saveBua(1);
  document.getElementById("foot").innerHTML =
    `Dữ liệu: ${data.source === "sheet" ? "Google Sheet" : "file CSV"} (${esc(data.fetched_at)})` +
    `${data.error ? " – Sheet lỗi, đang dùng CSV" : ""} · Thời tiết: Open-Meteo · ` +
    `<a href="#" id="refresh">Tải lại dữ liệu</a>`;
  document.getElementById("refresh").onclick = async (e) => {
    e.preventDefault();
    await fetch("data.json?refresh=1");
    location.reload();
  };
}

// Giá trị mùa của 1 hoặc nhiều mã (a|b): lấy cao nhất.
function seasonOf(codes, m = month()) {
  const vals = String(codes || "").split("|").filter(Boolean).map((c) => S.ing[c]?.thang[m - 1] ?? 1);
  return vals.length ? Math.max(...vals) : 1;
}

// ---------- Phản hồi của gia đình (lưu trên máy) ----------
// { ma_mon: { nau: ["YYYY-MM-DD", ...], y: 1 (ngon) | -1 (không hợp) | 0, tim: true (yêu thích) } }
const DG_KEY = "cachef.danh_gia";
function danhGia() {
  if (!S.dg) { try { S.dg = JSON.parse(localStorage.getItem(DG_KEY) || "{}"); } catch { S.dg = {}; } }
  return S.dg;
}
const dgMon = (ma) => danhGia()[ma] || {};
function saveDanhGia(ma, sua) {
  const all = danhGia();
  all[ma] = { ...(all[ma] || {}), ...sua };
  if (all[ma].nau) all[ma].nau = [...new Set(all[ma].nau)].sort().slice(-20);
  try { localStorage.setItem(DG_KEY, JSON.stringify(all)); } catch { /* chặn lưu: chỉ giữ trong phiên */ }
  // Chấm lại điểm để lần gợi ý sau phản ánh ngay; bữa đang hiện giữ nguyên.
  S.ranked = rankDishes(0);
  S.rankedTomorrow = rankDishes(1);
}
const DIEM_DG = { ngon: 2, khongHop: -6, tim: 1 };

// ---------- Chấm điểm ----------
// Số ngày từ lần gợi ý gần nhất trước ngày `ref` (ngày mai thì tính cả món gợi ý hôm nay).
function readHistory() {
  try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || "{}"); } catch { return {}; }
}

function daysSinceSuggested(ma, ref = today()) {
  const hist = readHistory();
  const t = new Date(ref);
  let best = Infinity;
  for (const [date, list] of Object.entries(hist)) {
    if (date >= ref || !list.includes(ma)) continue;
    best = Math.min(best, Math.round((t - new Date(date)) / 86400000));
  }
  for (const date of dgMon(ma).nau || []) // món đã nấu cũng tính là vừa ăn
    if (date < ref) best = Math.min(best, Math.round((t - new Date(date)) / 86400000));
  return best;
}

function recordHistory(list) {
  try {
    const hist = JSON.parse(localStorage.getItem(HISTORY_KEY) || "{}");
    hist[today()] = [...new Set([...(hist[today()] || []), ...list])]; // mọi món đã hiện trong ngày
    const keep = Object.keys(hist).sort().slice(-14);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(Object.fromEntries(keep.map((k) => [k, hist[k]]))));
  } catch {}
}

function compare(x, op, ng) {
  if (op === "between") {
    const [a, b] = String(ng).split("-").map(Number);
    return x >= a && x < b;
  }
  ng = Number(ng);
  return { ">=": x >= ng, "<=": x <= ng, ">": x > ng, "<": x < ng, "=": x === ng }[op] ?? false;
}

// Quy tắc thời tiết khớp với dự báo của ngày thứ `i` (0 = hôm nay, 1 = ngày mai).
function weatherRulesHit(i = 0) {
  const d = S.weather?.daily;
  if (!d || d.time.length <= i) return [];
  const w = Object.fromEntries(Object.keys(d).map((k) => [k, d[k][i]]));
  return S.data.quy_tac.filter((r) => {
    if (!(r.bien in w) || !compare(w[r.bien], r.toan_tu, r.nguong)) return false;
    // R09: khả năng mưa cao chỉ tính khi chưa đủ mưa để kích hoạt quy tắc "Có mưa".
    if (r.bien === "precipitation_probability_max" && w.precipitation_sum >= 3) return false;
    return true;
  });
}

function scoreDish(dish, weatherHits, day = 0) {
  let score = 0;
  const reasons = [];
  for (const r of weatherHits) {
    const [field, val] = String(r.ap_dung_cho).split("=");
    if (dish[field] === val) {
      score += Number(r.diem);
      reasons.push({ text: r.ten, diem: Number(r.diem) });
    }
  }
  const season = seasonOf(dish.nguyen_lieu_chinh, month(day));
  const since = daysSinceSuggested(dish.ma_mon, dayStr(day));
  for (const r of S.data.quy_tac) {
    let hit = false;
    if (r.bien === "lich_thang") hit = compare(season, r.toan_tu, r.nguong);
    else if (r.bien === "so_ngay_tu_lan_cuoi") hit = compare(since, r.toan_tu, r.nguong);
    if (hit) {
      score += Number(r.diem);
      reasons.push({ text: r.ten, diem: Number(r.diem) });
    }
  }
  // Chống lặp theo tuần: ngoài quy tắc "vừa gợi ý" (≤3 ngày) trên Sheet, trừ dần đến 14 ngày.
  const them = (text, diem) => { score += diem; reasons.push({ text, diem }); };
  if (since > 3 && since <= 7) them("Đã gợi ý trong tuần", -2);
  else if (since > 7 && since <= 14) them("Đã gợi ý 2 tuần qua", -1);
  const dg = dgMon(dish.ma_mon);
  if (dg.y === 1) them("Nhà khen ngon", DIEM_DG.ngon);
  if (dg.y === -1) them("Nhà thấy không hợp", DIEM_DG.khongHop);
  if (dg.tim) them("Yêu thích", DIEM_DG.tim);
  // Lẩu, nướng là bữa quây quần: ưu tiên tối thứ 6, thứ 7, chủ nhật.
  if (MOT_NOI.includes(vaiOf(dish)) && [0, 5, 6].includes(new Date(dayStr(day) + "T00:00:00Z").getUTCDay())) them("Cuối tuần, cả nhà quây quần", 3);
  // Đồ có sẵn trong tủ: món dùng hết nguyên liệu chính trong tủ +2, dùng một phần +1; có thứ sắp quá hạn thêm +2.
  const c = chinhCua(dish), co = c.filter(trongTu);
  if (co.length) {
    them(co.length === c.length ? "Có sẵn trong tủ" : "Có một phần trong tủ", co.length === c.length ? 2 : 1);
    if (co.some((x) => canDungSom(trongTu(x)))) them("Đồ trong tủ cần dùng sớm", 2);
  }
  return { ...dish, score, reasons, season };
}

// Xáo theo ngày: món chênh nhau dưới XAO_DIEM điểm đổi chỗ cho nhau mỗi ngày, để món sát điểm cũng được lên.
const XAO_DIEM = 1.5;
function dayHash(s, day = 0) {
  let h = 0;
  for (const c of dayStr(day) + s) h = (h * 31 + c.charCodeAt(0)) | 0;
  return h;
}

function rankDishes(day = 0) {
  const hits = weatherRulesHit(day);
  return S.data.mon_an
    .map((d) => scoreDish(d, hits, day))
    .map((d) => ({ ...d, xep: d.score + XAO_DIEM * ((dayHash(d.ma_mon, day) >>> 0) % 1000) / 1000 }))
    .sort((a, b) => b.xep - a.xep);
}

// Bữa một món (lẩu, nướng) là bữa lớn: mỗi loại tối đa 1 lần/7 ngày, hai loại cách nhau ít nhất 3 ngày.
const MOT_NOI = ["lau", "nuong"];
const motNoi = (d) => MOT_NOI.includes(vaiOf(d));
const LAU_CACH_NGAY = 7, MOT_NOI_CACH_NGAY = 3;
function ganDay(day, vai, soNgay) {
  const ref = dayStr(day), loai = Object.fromEntries(S.data.mon_an.map((m) => [m.ma_mon, m.loai]));
  return Object.entries(readHistory()).some(([date, list]) =>
    date < ref && (new Date(ref) - new Date(date)) / 86400000 < soNgay && list.some((ma) => loai[ma] === vai));
}
const duocMotNoi = (day, vai) => !ganDay(day, vai, LAU_CACH_NGAY) && !MOT_NOI.some((v) => v !== vai && ganDay(day, v, MOT_NOI_CACH_NGAY));
const tenMotNoi = (meals) => meals.toi.some((d) => vaiOf(d) === "nuong") ? "nướng" : "lẩu";

// ---------- Ghép bữa ----------
// Quy tắc:
//  - Lẩu chỉ ăn buổi tối (tối đa 1 lần/7 ngày). Hôm tối ăn lẩu thì trưa gợi ý món dễ nấu.
//  - Trưa: mặn + rau + canh. Món mặn kho/hầm/om/rim thì nấu dư, tối ăn lại -> tối chỉ nấu thêm rau + canh.
//  - Không lặp nguyên liệu chính trong ngày (rau thơm, gia vị dùng chung được); đạm tối khác đạm trưa.
//  - Trong một bữa: tối đa 1 món nấu lâu (kho/om/hầm/rim...) và 1 món cầu kì (nướng, nhồi, cuốn, chả...);
//    không 2 món cùng chiên/xào/nướng; canh có đạm thì khác nhóm đạm của món mặn.
//  - Món mặn có nhiều nước (om, bung, nấu, cà ri...) thì bữa đó bỏ canh: chỉ mặn + rau.
//  - Cả ngày tối đa 1 món nhiều dầu mỡ.
//  - Đủ đạm: điểm đạm cả bữa ≥ 2 (món mặn thịt/cá/hải sản 2, đạm nhẹ như trứng, đậu, cua đồng, đồ khô 1;
//    canh hoặc rau có thịt/cá/tôm 1, có trứng/đậu 0,5; canh cua đồng, canh rau 0).
//  - Trưa món mặn đạm nhẹ thì tối phải có món mặn thịt/cá (và không nấu dư món đạm nhẹ cho tối).
//  - Không 2 món rau lá trong một bữa (canh rau lá thì rau là củ quả, và ngược lại).
//  - Canh cua đồng ăn kèm cà pháo muối.
//  - Ưu tiên (bỏ được khi hết món): bữa có rau xanh; món mặn khó ăn với trẻ (cay, nhiều xương) thì canh có đạm dễ ăn.
const VAI_TU_LOAI = { canh: "canh", lau: "lau", nuong: "nuong", goi: "rau", trang_mieng: "trang_mieng", do_uong: "do_uong", an_vat: "an_vat", mon_chinh: "man" };
// Món mặn có nhiều nước mà nguyên liệu chính không có thịt/cá (cà tím bung đậu, ...) ăn như canh: xếp vào vai canh.
const vaiOf = (d) => {
  const v = S.nhan[d.ma_mon]?.vai_mam || VAI_TU_LOAI[d.loai] || "man";
  return v === "man" && NUOC_TEN.test(d.ten_mon) && damNL(d) === 1 ? "canh" : v;
};
const NUOC_TEN = /(^|\s)(om|bung|nấu|hầm|sốt vang|cà ri)(\s|$)|bò kho|riêu/i;
// Mức đạm theo nguyên liệu chính của món: 2 có thịt/cá/hải sản, 1 chỉ có đạm nhẹ (trứng, đậu phụ, cua đồng, đồ khô),
// 0 không có; null khi món chưa có bảng nguyên liệu.
const NHOM_DAM = new Set(["thịt", "hải sản", "thủy sản"]);
const NL_DAM_NHE = new Set(["cua_dong", "ca_com_kho", "ruoc_tuoi", "trung", "dau_phu", "xuong_heo"]);
const NL_KHONG_DAM = new Set(["rong_sun", "rong_nho", "sua", "mo_heo"]);
const _damNL = {};
function damNL(d) {
  if (d.ma_mon in _damNL) return _damNL[d.ma_mon];
  const rows = (S.ingByDish[d.ma_mon] || []).filter((r) => r.vai_tro === "chinh");
  let m = rows.length ? 0 : null, chuaMa = false;
  for (const r of rows) for (const c of String(r.ma_nguyen_lieu || "").split("|")) {
    if (!S.ing[c]) chuaMa = true; // nguyên liệu chưa có mã (cá hồi, cá diêu hồng...): không đoán được từ bảng
    else if (NL_DAM_NHE.has(c)) m = Math.max(m, 1);
    else if (NHOM_DAM.has(S.ing[c].nhom) && !NL_KHONG_DAM.has(c)) m = 2;
  }
  return (_damNL[d.ma_mon] = m === 2 || !chuaMa ? m : null);
}
const hopTre = (d) => S.nhan[d.ma_mon]?.hop_tre_em !== "can_nhac";
const cachNau = (d) => S.nhan[d.ma_mon]?.cach_nau || "";
const damOf = (d) => { const n = S.nhan[d.ma_mon]?.nhom_dam; return n && n !== "khac" ? n : ""; };
// Món dễ nấu (cho bữa trưa hôm tối ăn lẩu): không hầm, không nướng, không khó, không quá 60 phút (nếu biết).
const deNau = (d) => !(Number(d.thoi_gian_phut) > 60) && d.do_kho !== "kho" &&
  cachNau(d) !== "nuong" && !/hầm/i.test(d.ten_mon);
// Nấu lâu: để lửa nhỏ lâu nhưng ít công (thịt kho tàu, bò hầm). Món mặn loại này trưa nấu dư cho tối.
const nauLau = (d) => /(^|\s)(kho|hầm|om|rim|ram|bung|sốt vang)(\s|$)/i.test(d.ten_mon);
const khoHam = (d) => vaiOf(d) === "man" && nauLau(d);
// Cầu kì: nhiều công đoạn hoặc sơ chế lâu – nướng, nhồi, cuốn, viên, chả, gỏi nhiều thứ, món khó.
const cauKi = (d) => cachNau(d) === "nuong" || d.do_kho === "kho" || (cachNau(d) === "tron_cuon" && d.do_kho === "vua") ||
  /nướng|nhồi|cuốn|cuộn|(^|\s)(nem|chả|viên|mọc)(\s|$)|chả giò|hoành thánh|tẩm bột/i.test(d.ten_mon);
// Món mặn có nhiều nước (om, bung, nấu, hầm, cà ri, bò kho, sốt vang): bữa đó không cần thêm canh.
const coNuoc = (d) => vaiOf(d) === "man" && NUOC_TEN.test(d.ten_mon);
const CACH_KHONG_LAP = new Set(["chien", "xao", "nuong"]);
// Đạm nhẹ: trứng, đậu, cua đồng (chủ yếu lọc lấy nước), đồ khô ăn ít (cá khô, mực khô, ruốc, mắm).
// Điểm đạm: tính theo nguyên liệu chính; món chưa có bảng nguyên liệu thì theo nhóm đạm đã gắn nhãn.
// Thịt chỉ là nguyên liệu phụ (cà bung có ít thịt ba chỉ) tính như đạm nhẹ. Đồ khô, ruốc, mắm tối đa là đạm nhẹ.
function damMuc(d) {
  const dm = S.nhan[d.ma_mon]?.nhom_dam || "", nl = damNL(d);
  let m = nl === null ? (!dm || dm === "khac" ? 0 : dm === "trung_dau" ? 1 : 2) : nl || (dm && dm !== "khac" ? 1 : 0);
  if (m === 2 && /(^|\s)khô|ruốc/i.test(d.ten_mon)) m = 1;
  return m;
}
const damNhe = (d) => damMuc(d) < 2;
function damDiem(d) {
  const v = vaiOf(d), m = damMuc(d);
  if (v === "man") return m;
  if (v === "canh" || v === "rau") {
    if (m === 2) return 1;
    if (m === 1) return String(d.nguyen_lieu_chinh || "").split("|").includes("cua_dong") ? 0 : 0.5; // canh cua đồng: chủ yếu nước
    return 0;
  }
  return 0;
}
const DAM_DU = 2;
const damBua = (bua) => bua.reduce((s, d) => s + damDiem(d), 0);
// Bữa đã đủ vai (canh được bỏ khi món mặn có nước) – lúc này mới xét đủ đạm.
const duVai = (bua) => ["man", "rau", "canh"].every((v) => bua.some((d) => vaiOf(d) === v) || (v === "canh" && bua.some(coNuoc)));
const RAU_LA = new Set(["rau_muong", "mong_toi", "rau_day", "rau_ngot", "cai_xanh", "cai_thao", "bap_cai", "rau_bi", "rau_den",
  "rau_lang", "rau_ma", "xa_lach", "sau_dau", "rau_cai"]);
function rauLa(d) {
  const t = d.ten_mon.toLowerCase();
  return String(d.nguyen_lieu_chinh || "").split("|").some((c) => RAU_LA.has(c)) ||
    NL_TEN.some(([re, key]) => RAU_LA.has(key) && re.test(t));
}
// Món x có hợp với các món đã có trong bữa không (bua gồm cả món ăn lại từ trưa).
function hopBua(x, bua, ctx) {
  if (vaiOf(x) === "canh" && bua.some(coNuoc)) return false;
  if (coNuoc(x) && bua.some((d) => vaiOf(d) === "canh")) return false;
  if (nauLau(x) && bua.some(nauLau)) return false;
  if (cauKi(x) && bua.some(cauKi)) return false;
  if (CACH_KHONG_LAP.has(cachNau(x)) && bua.some((d) => cachNau(d) === cachNau(x))) return false;
  const dam = damOf(x), canhVsMan = (d) => (vaiOf(x) === "canh") !== (vaiOf(d) === "canh");
  if (dam && bua.some((d) => canhVsMan(d) && damOf(d) === dam)) return false;
  if (x.dau_mo === "nhieu" && ctx.mo >= 1) return false;
  const vx = vaiOf(x);
  if ((vx === "rau" || vx === "canh") && rauLa(x) && bua.some((d) => ["rau", "canh"].includes(vaiOf(d)) && rauLa(d))) return false;
  if (vx === "man" && ctx.damChinh && damDiem(x) < 2) return false;
  if (["man", "rau", "canh"].includes(vx) && duVai([...bua, x]) && damBua([...bua, x]) < DAM_DU) return false;
  return true;
}
const RAU_XANH = new Set(["rau_muong", "mong_toi", "rau_day", "rau_ngot", "cai_xanh", "cai_thao", "bap_cai", "rau_bi", "rau_den",
  "rau_lang", "rau_ma", "sup_lo", "mang_tay", "dau_co_ve", "kho_qua", "su_hao", "gia"]);
const coRauXanh = (d) => [...nlChinh(d)].some((k) => RAU_XANH.has(k));
// Ưu tiên mềm: rau xanh; món mặn không hợp trẻ thì canh có đạm dễ ăn (trứng, đậu, thịt heo, gà) và hợp trẻ.
function uaThich(x, bua, vai) {
  if (vai === "rau" && !coRauXanh(x)) return false;
  if (vai === "canh" && !bua.some(coRauXanh) && !coRauXanh(x)) return false;
  const man = bua.find((d) => vaiOf(d) === "man");
  if (vai === "canh" && man && !hopTre(man) && !(hopTre(x) && ["trung_dau", "heo", "ga"].includes(damOf(x)))) return false;
  return true;
}
// Chọn lần lượt các vai cho một bữa; điều kiện nới dần khi không còn món thỏa.
// ex.da_xem: món đã hiện (khi bấm Đổi) – chỉ dùng lại khi món chưa xem không thỏa quy tắc;
// ex.cam: món đã có trong ngày hoặc vừa hiện – không bao giờ chọn.
function pickBua(ranked, vais, ex, used, ctx, bua = [], them = {}) {
  // Món đầu (thường là món mặn) quyết định các món sau: nếu bữa phải nới quy tắc thì thử lại với món đầu khác.
  let best = null;
  const boQua = new Set();
  for (let lan = 0; lan < 4; lan++) {
    const u = new Set(used), c = { ...ctx }, b = [...bua];
    const r = ghepBua(ranked, vais, { da_xem: ex.da_xem, cam: [...ex.cam, ...boQua] }, u, c, b, them);
    if (!best || r.no < best.no) best = { ...r, u, c, b };
    if (!r.no || !r.out[0]) break;
    boQua.add(r.out[0].ma_mon);
  }
  best.u.forEach((k) => used.add(k));
  Object.assign(ctx, best.c);
  bua.splice(0, bua.length, ...best.b);
  return best.out;
}
// no: số món phải nới quy tắc cứng (trùng nguyên liệu hoặc phạm quy tắc bữa).
function ghepBua(ranked, vais, ex, used, ctx, bua, them) {
  const cam = new Set(ex.cam), out = [];
  let no = 0;
  for (const vai of vais) {
    if (vai === "canh" && bua.some(coNuoc)) continue;
    const t = them[vai] || (() => true), cung = (x) => khongTrung(x, used) && hopBua(x, bua, ctx);
    const pool2 = ranked.filter((d) => d.score > -3 && vaiOf(d) === vai && !cam.has(d.ma_mon));
    const pool1 = pool2.filter((d) => !ex.da_xem.has(d.ma_mon));
    const muc = [(x) => cung(x) && t(x) && uaThich(x, bua, vai), (x) => cung(x) && t(x), cung, (x) => khongTrung(x, used), () => true];
    let d = null;
    for (let i = 0; i < muc.length && !d; i++) {
      const c = pool1.filter(muc[i]).concat(pool2.filter(muc[i]));
      if (c.length) { d = c.find((x) => hopTre(x) && pool1.includes(x)) || c.find(hopTre) || c[0]; if (i >= 3) no += i - 2; }
    }
    if (!d) continue;
    out.push(d); bua.push(d); cam.add(d.ma_mon); dungNL(d, used);
    if (d.dau_mo === "nhieu") ctx.mo++;
  }
  return { out, no };
}
// Món vừa hiện ở lần trước (3 món cuối trong danh sách đã xem) để bấm Đổi luôn ra bữa khác.
const vuaHien = (daXem) => [...daXem].slice(-3);

// Nguyên liệu chính của món: lấy từ bảng định lượng, món chưa có thì đoán theo tên.
const NL_TEN = [
  [/tôm|hải sản/, "tom"], [/mực|hải sản/, "muc"], [/cua|ghẹ/, "cua"], [/nghêu|ngao|sò|ốc|hến/, "so_oc"], [/sứa/, "sua"],
  [/(^|\s)cá(\s|$)|chả cá/, "ca"], [/ếch/, "ech"], [/(^|\s)dê(\s|$)/, "de"], [/cừu/, "cuu"], [/(^|\s)(bò|bê)(\s|$)/, "bo"],
  [/(^|\s)(gà|vịt|ngan)(\s|$)/, "ga"], [/trứng/, "trung"], [/đậu (phụ|hũ)|tàu hũ/, "dau_phu"],
  [/thịt(?! (bò|gà|vịt|dê|cừu|ếch))|sườn|ba chỉ|ba rọi|(^|\s)giò(\s|$)|(^|\s)heo|lợn|nem|chả lá lốt|chả giò/, "heo"],
  [/khoai tây/, "khoai_tay"], [/cà rốt/, "ca_rot"], [/bí đỏ|bí ngô/, "bi_do"], [/bí đao|bí xanh/, "bi_dao"], [/(^|\s)bầu/, "bau"],
  [/mướp/, "muop"], [/cà tím|cà bung/, "ca_tim"], [/cà chua|sốt cà/, "ca_chua"], [/su su|đọt su/, "su_su"], [/su hào/, "su_hao"],
  [/củ cải/, "cu_cai"], [/bắp cải/, "bap_cai"], [/đậu que|đậu cô ve/, "dau_co_ve"], [/đậu bắp/, "dau_bap"], [/ngô|(?<!đậu )bắp(?! (cải|bò))/, "ngo"],
  [/nấm/, "nam"], [/xoài/, "xoai_uc"], [/măng tây/, "mang_tay"], [/rau muống/, "rau_muong"], [/mồng tơi/, "mong_toi"],
  [/rau ngót/, "rau_ngot"], [/khổ qua|mướp đắng/, "kho_qua"], [/khoai sọ|khoai môn/, "khoai_mon"], [/khoai lang|rau lang/, "khoai_lang"],
  [/khoai mỡ/, "khoai_mo"], [/rong biển/, "rong_bien"], [/(^|\s)giá(\s|$)/, "gia"], [/cải thảo/, "cai_thao"], [/súp lơ|bông cải/, "sup_lo"],
  [/đậu hà lan/, "dau_ha_lan"], [/rau dền/, "rau_den"], [/cải (ngọt|chíp|bẹ|xanh|cúc|ngồng)/, "cai_xanh"], [/dưa (leo|chuột)/, "dua_leo"],
  [/đu đủ/, "du_du"], [/bưởi/, "buoi"], [/chuối xanh/, "chuoi_xanh"], [/lươn/, "luon"], [/(^|\s)ốc(\s|$)/, "so_oc"],
  [/hoa chuối/, "hoa_chuoi"], [/dứa|(^|\s)thơm(\s|$)/, "thom"], [/lòng (heo|lợn)|lưỡi heo/, "heo"],
];
const NL_MA = { thit_heo: "heo", long_heo: "heo", ba_chi: "heo", suon_heo: "heo", chan_gio: "heo", xuong_heo: "heo", thit_bam: "heo",
  nac_vai: "heo", thit_nac: "heo", mo_heo: "heo", vit: "ga", ngan: "ga", chim_cut: "ga", tom_the: "tom", tom_hum: "tom", muc_tuoi: "muc", muc_mot_nang: "muc",
  thit_bo: "bo", ga_ta: "ga", thit_de: "de", thit_cuu: "cuu", cua_dong: "cua", sup_lo_trang: "sup_lo", bo_booth: "bo_trai", bo_sap: "bo_trai",
  ghe: "cua", cua_bien: "cua", ngheu: "so_oc", oc: "so_oc", oc_dong: "so_oc", so_diep: "so_oc", gia_do: "gia" };
const NL_CHUNG = new Set(["rau_thom", "sa_ot", "toi_pr", "hanh_tim", "mam_ca_na", "muoi_ca_na", "khe_me", "dau_phong", "bun", "banh_trang", "bot_gao", "xa_lach"]);
const _keys = {};
function nlChinh(d) {
  if (_keys[d.ma_mon]) return _keys[d.ma_mon];
  const k = new Set(), t = d.ten_mon.toLowerCase();
  for (const [re, key] of NL_TEN) if (re.test(t)) k.add(key);
  for (const r of S.ingByDish[d.ma_mon] || []) {
    if (r.vai_tro === "gia_vi") continue;
    if (motNoi(d) && r.vai_tro !== "chinh") continue; // lẩu, nướng: rau, bún đi kèm không tính là nguyên liệu chính
    for (const c of String(r.ma_nguyen_lieu || "").split("|").filter(Boolean))
      if (!NL_CHUNG.has(c)) k.add(NL_MA[c] || (c.startsWith("ca_") && !["ca_rot", "ca_chua", "ca_tim", "ca_phao"].includes(c) ? "ca" : c));
  }
  return (_keys[d.ma_mon] = k);
}
const khongTrung = (d, used) => ![...nlChinh(d)].some((k) => used.has(k));
const dungNL = (d, used) => nlChinh(d).forEach((k) => used.add(k));

// Món điểm cao nhất theo vai; thử lần lượt các điều kiện từ chặt đến lỏng, ưu tiên món hợp trẻ em.
function pickRole(ranked, vai, exclude, ...conds) {
  const pool = ranked.filter((d) => d.score > -3 && vaiOf(d) === vai && !exclude.has(d.ma_mon));
  for (const ok of [...conds, () => true]) {
    const c = pool.filter(ok);
    if (c.length) return c.find(hopTre) || c[0];
  }
  return null;
}

// giu: món đã chọn của bữa – giữ nguyên; chỉ gợi ý các vai còn thiếu, phải hợp quy tắc với món đã chọn.
const VAI_BUA = ["man", "rau", "canh"];
const conThieu = (giu) => VAI_BUA.filter((v) => !giu.some((d) => vaiOf(d) === v));
const THU_TU_VAI = ["lau", "nuong", "man", "rau", "canh", "dua_kem", "trang_mieng"];
// Canh cua đồng ăn kèm cà pháo muối cho giòn miệng (nếu bữa chưa có đồ ăn kèm).
const MA_CA_PHAO = "ca_phao_muoi_xoi";
function themKem(ranked, bua, cam) {
  const canhCua = bua.some((d) => vaiOf(d) === "canh" && String(d.nguyen_lieu_chinh || "").split("|").includes("cua_dong"));
  if (!canhCua || bua.some((d) => vaiOf(d) === "dua_kem") || cam.includes(MA_CA_PHAO)) return bua;
  const k = ranked.find((d) => d.ma_mon === MA_CA_PHAO);
  return k ? [...bua, k] : bua;
}
const theoVai = (list) => [...list].sort((a, b) => THU_TU_VAI.indexOf(vaiOf(a)) - THU_TU_VAI.indexOf(vaiOf(b)));

function pickTrua(ranked, daXem, cam, used, ctx, deThoi, giu = []) {
  const de = deThoi ? { man: deNau, rau: deNau, canh: deNau } : {};
  const ex = { da_xem: daXem, cam: [...cam, ...giu.map((d) => d.ma_mon), ...vuaHien(daXem)] };
  return theoVai(themKem(ranked, [...giu, ...pickBua(ranked, conThieu(giu), ex, used, ctx, [...giu], de)], ex.cam));
}

function pickToi(ranked, daXem, used, ctx, trua, du, giu = []) {
  const coSan = du ? [du, ...giu] : giu;
  const ex = { da_xem: daXem, cam: [...trua.map((d) => d.ma_mon), ...giu.map((d) => d.ma_mon), ...vuaHien(daXem)] };
  const damTrua = damOf(trua.find((d) => vaiOf(d) === "man") || {});
  return theoVai(themKem(ranked, [...coSan, ...pickBua(ranked, conThieu(coSan), ex, used, ctx, [...coSan],
    { man: (x) => !damTrua || damOf(x) !== damTrua })], ex.cam));
}

// keep.trua / keep.toi: các món giữ nguyên (món đã chọn, hoặc cả bữa còn lại khi bấm Đổi một bữa).
function pickMeals(ranked, day, keep = {}) {
  const sh = S.shown[day], used = new Set();
  const kTrua = keep.trua || [], kToi = keep.toi || [];
  const ctx = { mo: [...kTrua, ...kToi].filter((d) => d.dau_mo === "nhieu").length };
  [...kTrua, ...kToi].forEach((d) => dungNL(d, used));
  // Bữa tối một món (lẩu, nướng): giữ nếu đã chọn; nếu tối chưa có món nào giữ thì xét gợi ý
  // (không trùng nguyên liệu bữa trưa, điểm không thua món mặn tốt nhất).
  let toi = kToi.some(motNoi) ? [...kToi] : null;
  if (!toi && !kToi.length) {
    const bestMan = ranked.find((d) => d.score > -3 && vaiOf(d) === "man");
    const ung = MOT_NOI.filter((v) => duocMotNoi(day, v))
      .map((v) => pickRole(ranked, v, new Set([...sh.toi, ...kTrua.map((d) => d.ma_mon)]), (x) => khongTrung(x, used)))
      .filter((l) => l && khongTrung(l, used) && l.score >= (bestMan?.score ?? -99))
      .sort((a, b) => ranked.indexOf(a) - ranked.indexOf(b));
    if (ung.length) { toi = [ung[0]]; dungNL(ung[0], used); }
  }
  if (toi) {
    if (!toi.some((d) => vaiOf(d) === "trang_mieng")) {
      const tm = pickRole(ranked, "trang_mieng", new Set([...sh.toi, ...kTrua.map((d) => d.ma_mon)]), (x) => khongTrung(x, used));
      if (tm) { toi.push(tm); dungNL(tm, used); }
    }
    const trua = pickTrua(ranked, sh.trua, toi.map((d) => d.ma_mon), used, ctx, true, kTrua);
    return { trua, toi: theoVai(toi), lau: true, du: null };
  }
  const trua = pickTrua(ranked, sh.trua, kToi.map((d) => d.ma_mon), used, ctx, false, kTrua);
  const manTrua = trua.find((d) => vaiOf(d) === "man");
  const du = manTrua && khoHam(manTrua) && !damNhe(manTrua) && !kToi.some((d) => vaiOf(d) === "man") ? manTrua : null;
  ctx.damChinh = !manTrua || damDiem(manTrua) < 2; // trưa đạm nhẹ: tối phải có thịt/cá
  const toiMoi = pickToi(ranked, sh.toi, used, ctx, trua, du, kToi);
  return { trua, toi: toiMoi, lau: false, du: du?.ma_mon ?? null };
}
// Món phải nấu (món ăn lại từ trưa không tính 2 lần).
const mealDishes = (m) => [...m.trua, ...m.toi.filter((d) => d.ma_mon !== m.du)];

// ---------- Thời tiết ----------
function wmo(code) {
  if (code === 0) return ["☀️", "Trời quang, nắng"];
  if (code <= 2) return ["🌤️", "Ít mây"];
  if (code === 3) return ["☁️", "Nhiều mây"];
  if (code <= 48) return ["🌫️", "Sương mù"];
  if (code <= 57) return ["🌦️", "Mưa phùn"];
  if (code <= 67) return ["🌧️", "Mưa"];
  if (code <= 82) return ["🌧️", "Mưa rào"];
  return ["⛈️", "Dông"];
}


// Đồ tươi sống (thịt, hải sản) của các món ngày mai – thường để ngăn đá, cần rã đông từ tối nay.
const FROZEN_GROUPS = ["thịt", "hải sản"];
const NOT_FROZEN = ["rong_sun", "sua", "muc_mot_nang", "mo_heo"]; // rong khô, sứa ngâm, mực phơi: không cần rã đông lâu
const FROZEN_WORDS = /chả cá|xương|sườn|giò heo/i;
const NAU_THANG = new Set(["tom_the", "tom_hum", "muc_tuoi"]); // tôm, mực: lấy từ ngăn đá nấu thẳng, không rã đông
const MO_HEO = /^mỡ/i; // mỡ heo (mỡ phần, mỡ nước) luôn để ngăn mát – không tính "thịt nửa nạc nửa mỡ"
// thang: nhận tên các thứ nấu thẳng từ ngăn đá (tôm, mực) để nhắc riêng.
function thawList(meals, thang = []) {
  const out = [];
  for (const d of mealDishes(meals)) {
    const f = d.ma_mon === meals.du ? 2 : 1; // nấu dư cho bữa tối
    for (const r of S.ingByDish[d.ma_mon] || []) {
      if (r.vai_tro === "gia_vi") continue;
      if (motNoi(d) && r.vai_tro !== "chinh") continue; // lẩu, nướng: rau, bún đi kèm không tính là nguyên liệu chính
      if (MO_HEO.test(r.ten_hien_thi)) continue;
      const codes = String(r.ma_nguyen_lieu || "").split("|").filter(Boolean);
      if (codes.length && codes.every((c) => NAU_THANG.has(c))) { if (!thang.includes(r.ten_hien_thi)) thang.push(r.ten_hien_thi); continue; }
      const frozen = codes.length
        ? codes.some((c) => FROZEN_GROUPS.includes(S.ing[c]?.nhom) && !NOT_FROZEN.includes(c))
        : FROZEN_WORDS.test(r.ten_hien_thi);
      if (frozen && codes.length && codes.every((c) => trongTu(c) && !tuLanh()[trongTu(c)].da)) continue; // tủ lạnh ghi đang ở ngăn mát
      if (frozen) out.push({ ten: r.ten_hien_thi, mon: d.ten_mon + (f > 1 ? " (gồm phần cho bữa tối)" : ""), qty: scaleQty(r, f) });
    }
  }
  return out;
}


// Số lượng theo khẩu phần: "theo_nguoi" nhân thẳng, "theo_noi" tăng chậm hơn (60%).
function scaleQty(row, factor) {
  const q = Number(row.so_luong);
  if (!row.so_luong && row.so_luong !== 0 || isNaN(q)) return row.don_vi || "";
  const f = row.kieu_tinh === "theo_noi" ? 1 + (factor - 1) * 0.6 : factor;
  let v = q * f;
  const unit = row.don_vi;
  if (["g", "ml"].includes(unit)) v = v >= 100 ? Math.round(v / 10) * 10 : Math.round(v);
  else v = Math.max(0.5, Math.round(v * 2) / 2);
  if (unit === "g" && v >= 1000) return `${fmt(v / 1000)} kg`;
  if (unit === "ml" && v >= 1000) return `${fmt(v / 1000)} lít`;
  return `${fmt(v)} ${unit}`;
}
const fmt = (v) => (Math.round(v * 100) / 100).toLocaleString("vi-VN");


// ---------- Giao diện chung ----------
const THU = ["Chủ nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"];
function ngayVN(i = 0) {
  const [y, m, d] = dayStr(i).split("-").map(Number);
  return `${THU[new Date(Date.UTC(y, m - 1, d)).getUTCDay()]}, ${d}/${m}`;
}

// Thanh trên: ngày + thời tiết gói trong một nhãn.
function headerBar() {
  document.getElementById("today").textContent = ngayVN(0);
  const d = S.weather?.daily, c = S.weather?.current, wx = document.getElementById("wx");
  if (!d) { wx.hidden = true; return; }
  const [icon] = wmo(c ? c.weather_code : d.weather_code[0]);
  wx.textContent = `${icon} ${Math.round(c ? c.temperature_2m : d.temperature_2m_max[0])}° · mưa ${d.precipitation_probability_max[0]}%`;
}

// Lời khuyên theo thời tiết: so tổng điểm các quy tắc nghiêng về món nóng với món mát, kèm lý do chính.
function loiKhuyen(day) {
  const d = S.weather.daily, hits = weatherRulesHit(day);
  const theo = (h) => hits.filter((r) => r.ap_dung_cho === `nhiet=${h}` && Number(r.diem) > 0);
  const tong = (h) => theo(h).reduce((t, r) => t + Number(r.diem), 0);
  if (!tong("nong") && !tong("mat")) return null;
  const huong = tong("nong") >= tong("mat") ? "nong" : "mat";
  const r = theo(huong).sort((a, b) => b.diem - a.diem)[0];
  const lyDo = {
    precipitation_sum: `dự báo mưa ${d.precipitation_sum[day]} mm`,
    precipitation_probability_max: `khả năng mưa ${d.precipitation_probability_max[day]}%`,
    temperature_2m_max: `${r.ten.toLowerCase()}, cao nhất ${Math.round(d.temperature_2m_max[day])}°`,
    uv_index_max: `UV ${Math.round(d.uv_index_max[day])}`,
  }[r.bien] || r.ten.toLowerCase();
  return { huong, text: huong === "nong" ? "Ưu tiên món nóng, ấm bụng" : "Ưu tiên món mát, ít dầu", lyDo };
}

// Dự báo trong ngày (khớp với lời khuyên) + lời khuyên; chạm để xem chi tiết.
function weatherTip(day) {
  const d = S.weather?.daily;
  if (!d || d.time.length <= day) return `<div class="tip">Không lấy được thời tiết – gợi ý chỉ theo mùa vụ.</div>`;
  const c = day === 0 ? S.weather.current : null;
  const [icon, desc] = wmo(d.weather_code[day]);
  const lk = loiKhuyen(day);
  return `<details class="tip ${lk ? (lk.huong === "nong" ? "rain" : "hot") : ""}">
    <summary><span class="t1">${icon} ${day ? "Ngày mai" : "Hôm nay"}: ${desc.toLowerCase()} · ${Math.round(d.temperature_2m_min[day])}–${Math.round(d.temperature_2m_max[day])}°</span>
      <span class="t2">${lk ? `<b>${lk.text}</b> – ${esc(lk.lyDo)}` : "Thời tiết dễ chịu – món nào cũng hợp"}</span></summary>
    <div class="tip-more">🌧️ Mưa ${d.precipitation_sum[day]} mm (khả năng ${d.precipitation_probability_max[day]}%) · 💨 Gió ${Math.round(d.wind_speed_10m_max[day])} km/h
      · 🔆 UV ${Math.round(d.uv_index_max[day])}${c ? ` · Lúc này ${Math.round(c.temperature_2m)}°, ẩm ${c.relative_humidity_2m}%` : ""}</div>
  </details>`;
}

const ICON_DAM = { ca: "🐟", hai_san: "🦐", heo: "🥩", ga: "🍗", bo: "🥩", trung_dau: "🥚" };
const ICON_VAI = { rau: "🥬", canh: "🍲", lau: "🫕", nuong: "🔥", trang_mieng: "🍮", mot_to: "🍜", do_uong: "🥤", an_vat: "🥨", dua_kem: "🥒" };
// Biểu tượng theo nguyên liệu trong tên món (đúng hơn nhóm đạm), rồi mới theo nhóm đạm / vai trong mâm.
const ICON_TEN = [[/ếch/, "🐸"], [/cua|ghẹ|riêu/, "🦀"], [/mực/, "🦑"], [/tôm/, "🦐"], [/ốc|nghêu|ngao|sò|hến|hàu/, "🐚"],
  [/vịt/, "🦆"], [/gà/, "🍗"], [/(^|\s)(cá|lươn)(\s|$)/, "🐟"], [/(^|\s)(bò|dê|cừu)(\s|$)/, "🥩"], [/trứng/, "🥚"],
  [/đậu (phụ|hũ)|tàu hũ/, "🧈"], [/nấm/, "🍄"]];
function iconOf(d) {
  const v = vaiOf(d);
  if (v === "man" || v === "rau") {
    const t = d.ten_mon.toLowerCase(), hit = ICON_TEN.find(([re]) => re.test(t));
    if (hit && (v === "man" || (hit[1] === "🍄" && t.startsWith("nấm")))) return hit[1];
  }
  return v === "man" ? ICON_DAM[damOf(d)] || "🍽️" : ICON_VAI[v] || "🍽️";
}
const VAI_NGAN = { man: "Mặn", rau: "Rau", canh: "Canh", lau: "Lẩu", nuong: "Nướng", mot_to: "Một tô", trang_mieng: "Tráng miệng", do_uong: "Đồ uống", an_vat: "Ăn vặt", dua_kem: "Ăn kèm" };

// Ảnh món: mã ảnh trên CDN Cookpad, ghép URL theo cỡ (CDN tự cắt, ảnh nhỏ chỉ vài KB).
const anhUrl = (ma, w, h) => S.anh[ma] && `https://img-global.cpcdn.com/recipes/${S.anh[ma].anh_id}/${w}x${h}cq70/photo.webp`;
// Ô vuông nhỏ: ảnh nếu có, biểu tượng nằm dưới để hiện khi ảnh lỗi/chưa tải.
const thumb = (d, cls = "") => `<span class="ic ${cls}">${iconOf(d)}${S.anh[d.ma_mon]
  ? `<img src="${anhUrl(d.ma_mon, 112, 112)}" alt="" loading="lazy" onerror="this.remove()">` : ""}</span>`;

// Dòng phụ dưới tên món: chỉ những gì giúp quyết định nhanh.
function metaMon(d, du) {
  const p = [], dg = dgMon(d.ma_mon);
  if (vaiOf(d) === "dua_kem") return `ăn kèm${d.thoi_gian_phut ? ` · làm trước ~${String(Math.round(d.thoi_gian_phut / 30) / 2).replace(".", ",")} tiếng` : ""}`;
  if (dg.y === 1 || dg.tim) p.push(`<span class="peak">${dg.tim ? "♥" : ""}${dg.y === 1 ? "👍" : ""}</span>`);
  if (d.season === 2) p.push(`<span class="peak">Đang rộ</span>`);
  else if (d.nhiet === "nong") p.push(`<span class="hot">Nóng</span>`);
  else if (d.nhiet === "mat") p.push(`<span class="cool">Mát</span>`);
  if (chinhCua(d).some(trongTu)) p.push(`<span class="tl-co">🧊 có trong tủ</span>`);
  if (d.thoi_gian_phut) p.push(`${d.thoi_gian_phut}′`);
  if (du) p.push("nấu thêm phần cho tối");
  if (coNuoc(d)) p.push("có nước, thay canh");
  else if (d.do_kho && !du) p.push((LABEL.do_kho[d.do_kho] || d.do_kho).toLowerCase());
  if (!hopTre(d)) p.push("cân nhắc cho bé");
  return p.join(" · ");
}

function mealBlock(meals, k, chon) {
  const anLai = (d) => k === "toi" && d.ma_mon === meals.du;
  const nau = meals[k].filter((d) => !anLai(d) && vaiOf(d) !== "dua_kem"); // đồ ăn kèm làm trước, không tính vào giờ nấu
  const phut = Math.max(0, ...nau.map((d) => Number(d.thoi_gian_phut) || 0));
  const conDoi = meals[k].some((d) => !anLai(d) && !chon[k].has(d.ma_mon));
  const sub = k === "trua"
    ? [`${nau.length} món`, phut && `~${phut}′`, meals.lau && `dễ nấu, tối ăn ${tenMotNoi(meals)}`, meals.du && "nấu thêm phần cho tối"]
    : meals.lau ? [`${tenMotNoi(meals)} + tráng miệng`, phut && `~${phut}′`]
    : meals.du ? ["dùng tiếp món trưa", `nấu thêm ${nau.length} món`, phut && `~${phut}′`] : [`${nau.length} món`, phut && `~${phut}′`];
  return `<section class="meal">
    <div class="mh"><h3>${k === "trua" ? "🍚 Trưa" : "🌙 Tối"}<span class="sub">${[...sub, !(meals.lau && k === "toi") && meals[k].some(coNuoc) && "không cần canh"].filter(Boolean).join(" · ")}</span></h3>
      ${conDoi ? `<button class="swap" data-swap="${k}">🔄 ${chon[k].size ? "Đổi món còn lại" : "Đổi"}</button>` : `<span class="chot">✓ Đã chốt bữa</span>`}</div>
    ${meals[k].map((d) => {
      const on = chon[k].has(d.ma_mon), lai = anLai(d);
      return `<div class="row ${lai ? "ghost" : ""} ${on ? "picked" : ""}">
        <a class="row-link" href="#/mon/${d.ma_mon}">${thumb(d)}
          <span class="tx"><b>${esc(d.ten_mon)}</b><span class="meta">${lai ? "Phần để dành từ bữa trưa" : metaMon(d, d.ma_mon === meals.du)}</span></span></a>
        ${lai ? "" : `<button class="ck ${on ? "on" : ""}" data-chon="${k}" data-ma="${d.ma_mon}" aria-pressed="${on}"
          aria-label="${on ? "Bỏ chọn" : "Chọn"} ${esc(d.ten_mon)}" title="${on ? "Bỏ chọn" : "Chọn – giữ món này khi đổi các món còn lại"}">✓</button>`}
      </div>`;
    }).join("")}
  </section>`;
}

// Rã đông cho ngày mai: một dòng, chạm để mở danh sách ngay tại chỗ, chạm lần nữa để thu lại.
function thawBox(moSan = false) {
  if (!S.meals[1]) return "";
  const thang = [], list = thawList(S.meals[1], thang);
  const nhacThang = thang.length ? `${thang.join(", ")}: lấy từ ngăn đá nấu thẳng, không cần rã đông` : "";
  if (!list.length) return `<div class="nhac"><span class="ic">🧊</span><span class="tx"><b>Rã đông</b>
    <span class="meta">${esc(nhacThang || "Món ngày mai không cần rã đông thịt, cá")}</span></span></div>`;
  const tom = list.slice(0, 3).map((x) => `${x.ten} ${x.qty}`).join(" · ") + (list.length > 3 ? ` · +${list.length - 3}` : "");
  return `<details class="nhac-d" ${moSan ? "open" : ""}>
    <summary class="nhac"><span class="ic">🧊</span>
      <span class="tx"><b>Rã đông tối nay cho mai (${list.length})</b><span class="meta">${esc(tom)}</span></span><span class="chev">›</span></summary>
    <div class="nhac-body">
      <p class="note">Tối nay chuyển từ ngăn đá xuống ngăn mát:</p>
      <ul class="thaw">${list.map((x) => `<li><span><b>${esc(x.ten)}</b><small>${esc(x.mon)}</small></span><span>${esc(x.qty)}</span></li>`).join("")}</ul>
      ${nhacThang ? `<p class="note">🦐 ${esc(nhacThang)}.</p>` : ""}
      <p class="note">Ngăn mát mất 12–24 giờ. Quên thì ngâm cả túi kín trong nước lạnh, 30 phút thay nước. Không rã đông ở nhiệt độ phòng.</p>
    </div>
  </details>`;
}

// Nhắc đồ trong tủ cần dùng sớm và bữa hôm nay đã dùng tới chưa.
function tlBox(meals) {
  const som = Object.keys(tuLanh()).filter((c) => S.ing[c] && canDungSom(c));
  if (!som.length) return "";
  const trongBuaNay = new Set(mealDishes(meals).flatMap(chinhCua).map(trongTu));
  const chua = som.filter((c) => !trongBuaNay.has(c)), ten = (l) => l.map((c) => S.ing[c].ten).join(", ");
  return `<a class="nhac tl-nhac" href="#/tu-lanh"><span class="ic">🧊</span>
    <span class="tx"><b>Tủ lạnh: ${som.length} thứ cần dùng sớm</b><span class="meta">${chua.length
      ? `Chưa có trong bữa: ${esc(ten(chua))} – chạm để chọn món`
      : `Bữa hôm nay đã dùng: ${esc(ten(som))}`}</span></span><span class="chev">›</span></a>`;
}

// ---------- Trang Nấu gì (hôm nay / ngày mai) ----------
function pageHome(day = 0) {
  const ranked = day ? S.rankedTomorrow : S.ranked;
  const meals = S.meals[day];
  const chon = chonOf(day);
  const m = month(day);
  const inSeason = S.data.nguyen_lieu.filter((n) => n.thang[m - 1] === 2);
  const shown = new Set(mealDishes(meals).map((p) => p.ma_mon));
  const others = ranked.filter((d) => !shown.has(d.ma_mon) && ["man", "rau", "canh", "lau", "nuong", "mot_to"].includes(vaiOf(d))).slice(0, 10);
  $app.innerHTML = `
    <div class="seg"><a href="#/" class="${day ? "" : "on"}">Hôm nay</a><a href="#/ngay-mai" class="${day ? "on" : ""}">Ngày mai</a></div>
    ${weatherTip(day)}
    ${mealBlock(meals, "trua", chon)}
    ${mealBlock(meals, "toi", chon)}
    ${day ? "" : tlBox(meals)}
    ${thawBox(day === 1)}
    <h4>Đang vào mùa tháng ${m}</h4>
    <div class="hs">${inSeason.map((n) => `<a class="chip peak" href="#/lich/${n.ma}">${esc(n.ten)}</a>`).join("") || '<span class="muted">Chưa có dữ liệu</span>'}</div>
    <h4>Món khác cũng hợp</h4>
    <div class="hs">${others.map((d) => `<a class="card2" href="#/mon/${d.ma_mon}">${S.anh[d.ma_mon]
      ? `<span class="c2img"><img src="${anhUrl(d.ma_mon, 320, 200)}" alt="" loading="lazy" onerror="this.parentNode.remove()"></span>` : thumb(d)}
      <b>${esc(d.ten_mon)}</b><small>${VAI_NGAN[vaiOf(d)] || ""} · ${d.score > 0 ? "+" : ""}${d.score} điểm</small></a>`).join("")}</div>`;
  $app.querySelectorAll("[data-chon]").forEach((btn) => (btn.onclick = () => {
    const k = btn.dataset.chon, ma = btn.dataset.ma;
    if (chon[k].has(ma)) chon[k].delete(ma); else chon[k].add(ma);
    saveChon(day, chon);
    pageHome(day);
  }));
  $app.querySelectorAll("[data-swap]").forEach((btn) => (btn.onclick = () => {
    const k = btn.dataset.swap;
    const giu = (b) => meals[b].filter((d) => chon[b].has(d.ma_mon));
    // Đưa món vừa hiện về cuối danh sách đã xem (kể cả món đã xem từ trước) để lần đổi này không ra lại.
    meals[k].filter((d) => !chon[k].has(d.ma_mon) && (k === "trua" || d.ma_mon !== meals.du))
      .forEach((d) => { S.shown[day][k].delete(d.ma_mon); S.shown[day][k].add(d.ma_mon); });
    // Đổi trưa: giữ món đã chọn của trưa; tối giữ lẩu (nếu có) hoặc món đã chọn, phần còn lại tính lại theo trưa mới.
    // Đổi tối: giữ nguyên trưa và món đã chọn của tối.
    const keep = k === "trua" ? { trua: giu("trua"), toi: meals.lau ? meals.toi : giu("toi") } : { trua: meals.trua, toi: giu("toi") };
    let next = pickMeals(ranked, day, keep);
    const moi = (b) => next[b].filter((d) => !chon[b].has(d.ma_mon)).length;
    if (!moi(k)) { S.shown[day][k].clear(); next = pickMeals(ranked, day, keep); } // hết món thì quay vòng
    datBua(day, next);
    pageHome(day);
  }));
}

// Lưu bữa mới của một ngày; hôm nay đổi sang món đang có trong bữa ngày mai thì gợi ý lại ngày mai (giữ món đã chọn).
function datBua(day, next) {
  S.meals[day] = next;
  saveBua(day);
  if (day !== 0) return;
  recordHistory(mealDishes(next).map((d) => d.ma_mon));
  const homNay = new Set(mealDishes(next).map((d) => d.ma_mon));
  if (S.meals[1] && mealDishes(S.meals[1]).some((d) => homNay.has(d.ma_mon) && !chonOf(1).trua.has(d.ma_mon) && !chonOf(1).toi.has(d.ma_mon))) {
    S.rankedTomorrow = rankDishes(1);
    S.meals[1] = pickMeals(S.rankedTomorrow, 1, monDaChon(S.rankedTomorrow, 1));
    saveBua(1);
  }
}

// Đưa một món vào bữa (từ tab Tủ lạnh): món thành "đã chọn", thay món đã chọn cùng vai; các món chưa chọn ghép lại theo quy tắc.
// Lẩu chỉ vào bữa tối và thay cả bữa tối (giữ tráng miệng).
function duaVaoBua(ma, k, day = 0) {
  const ranked = day ? S.rankedTomorrow : S.ranked, chon = chonOf(day);
  const d = ranked.find((x) => x.ma_mon === ma), v = vaiOf(d);
  for (const x of [...chon[k]]) {
    const vx = vaiOf(ranked.find((y) => y.ma_mon === x) || {});
    if (vx === v || MOT_NOI.includes(vx) || (MOT_NOI.includes(v) && vx !== "trang_mieng")) chon[k].delete(x);
  }
  chon[k === "trua" ? "toi" : "trua"].delete(ma);
  chon[k].add(ma);
  saveChon(day, chon);
  datBua(day, pickMeals(ranked, day, monDaChon(ranked, day)));
}

// ---------- Trang món ----------
// Thanh mùa vụ cho các nguyên liệu của món có mùa rõ rệt (bỏ qua loại có quanh năm như bột gạo, thịt heo).
function seasonBlock(ma) {
  const m = month();
  const seen = new Set();
  const rows = (S.ingByDish[ma] || [])
    .filter((r) => r.ma_nguyen_lieu && r.vai_tro !== "gia_vi" && !seen.has(r.ma_nguyen_lieu) && seen.add(r.ma_nguyen_lieu))
    .map((r) => ({ ten: r.ten_hien_thi, chinh: r.vai_tro === "chinh",
      thang: Array.from({ length: 12 }, (_, i) => seasonOf(r.ma_nguyen_lieu, i + 1)) }))
    .filter((r) => r.thang.some((v) => v !== 1))
    .sort((a, b) => b.chinh - a.chinh)
    .slice(0, 5);
  if (!rows.length) return `<p class="note">Nguyên liệu của món này có quanh năm.</p>`;
  return `<div class="box">${rows.map((r) => `<div class="srow"><span>${esc(r.ten)}</span>${thangBar(r.thang, m)}</div>`).join("")}
    <div class="srow lbl"><span></span>${thangBar(null, m)}</div></div>
    <p class="note">Đậm: đang rộ · nhạt: có hàng · xám: trái mùa · khung: tháng ${m}.</p>`;
}
// Dải 12 ô theo tháng (thang = null: dòng số tháng).
const thangBar = (thang, m) => `<span class="bar">${Array.from({ length: 12 }, (_, i) =>
  thang ? `<i class="v${thang[i]} ${i + 1 === m ? "cur" : ""}"></i>` : `<i class="n ${i + 1 === m ? "cur" : ""}">${i + 1}</i>`).join("")}</span>`;

// Thanh phản hồi: đã nấu, ngon / không hợp, yêu thích. moiXong: vừa bấm "Xong" ở chế độ nấu.
function thanhDanhGia(d, moiXong) {
  const dg = dgMon(d.ma_mon), nau = dg.nau || [], hom = nau.includes(dayStr(0)), tlDung = [...new Set(chinhCua(d).map(trongTu).filter(Boolean))];
  const lan = nau.length ? `Nhà đã nấu ${nau.length} lần, gần nhất ${nau.at(-1).slice(8, 10)}/${Number(nau.at(-1).slice(5, 7))}` : "Nhà chưa nấu món này";
  return `<div class="dg ${moiXong && !dg.y ? "hoi" : ""}">
    ${moiXong && !dg.y ? `<p class="dg-hoi">Đã ghi là nấu hôm nay. Món này cả nhà thấy thế nào?</p>` : ""}
    <div class="dg-nut">
      <button data-dg="nau" class="${hom ? "on" : ""}">✓ Đã nấu</button>
      <button data-dg="ngon" class="${dg.y === 1 ? "on" : ""}" aria-pressed="${dg.y === 1}">👍 Ngon</button>
      <button data-dg="khong" class="${dg.y === -1 ? "on xau" : ""}" aria-pressed="${dg.y === -1}">👎 Không hợp</button>
      <button data-dg="tim" class="${dg.tim ? "on" : ""}" aria-pressed="${!!dg.tim}" aria-label="Yêu thích">${dg.tim ? "♥" : "♡"}</button>
    </div>
    ${hom && tlDung.length ? `<p class="dg-tl">🧊 Trong tủ còn ghi: ${esc(tlDung.map((c) => S.ing[c].ten).join(", "))}
      <button class="link" data-dung="1">Đã dùng hết – bỏ khỏi tủ</button></p>` : ""}
    <p class="src">${lan}${dg.y === -1 ? " · sẽ hầu như không được gợi ý nữa" : dg.y === 1 ? " · được ưu tiên gợi ý" : ""}</p>
  </div>`;
}

// Món này có trong bữa nào hôm nay / ngày mai.
function trongBua(ma) {
  for (const [day, ten] of [[0, "nay"], [1, "mai"]]) {
    const m = S.meals[day];
    if (!m) continue;
    if (m.trua.some((d) => d.ma_mon === ma)) return `Trưa ${ten}`;
    if (m.toi.some((d) => d.ma_mon === ma)) return `Tối ${ten}`;
  }
  return "";
}

const steps = (d) => String(d.cach_lam || "").split("\n").map((s) => s.replace(/^\d+\.\s*/, "").trim()).filter(Boolean);
const MUA_CHU = { 2: ["Rộ", "peak"], 1: ["Có hàng", ""], 0: ["Trái mùa", "muted"] };

function pageRecipe(ma, moiXong = false) {
  const d = S.ranked.find((x) => x.ma_mon === ma);
  if (!d) { $app.innerHTML = `<p>Không tìm thấy món.</p><a href="#/">‹ Về trang chính</a>`; return; }
  const base = Number(d.khau_phan_goc) || 4;
  const n = S.servings[ma] ?? base;
  const factor = n / base;
  const rows = S.ingByDish[ma] || [];
  const unitName = d.loai === "do_uong" || d.loai === "trang_mieng" ? "phần" : "người";
  const tab = S.tabMon || "nl";
  const bua = trongBua(ma);
  const [mua, muaCls] = MUA_CHU[d.season] || MUA_CHU[1];
  const bqMon = [...new Set(rows.filter((r) => r.vai_tro === "chinh").flatMap((r) => String(r.ma_nguyen_lieu || "").split("|")))]
    .filter((c) => S.bq[c] && !NL_CHUNG.has(c));
  const nhom = [["chinh", "Chính"], ["phu", "Thêm"], ["gia_vi", "Gia vị"]]
    .map(([v, t]) => [t, rows.filter((r) => (r.vai_tro || "phu") === v)]).filter(([, l]) => l.length);
  const body = {
    nl: rows.length ? `
      <div class="ppl"><span>Khẩu phần</span><span class="st"><button id="minus" aria-label="Bớt">−</button><b>${n} ${unitName}</b><button id="plus" aria-label="Thêm">+</button></span></div>
      <div class="ing">${nhom.map(([t, l]) => `<div class="grp">${t}</div>${l.map((r) => {
        const c0 = String(r.ma_nguyen_lieu).split("|")[0], price = S.prices[c0] || S.prices[S.ing[c0]?.cha];
        return `<div class="ir"><span class="${r.vai_tro === "chinh" ? "k" : ""}">${esc(r.ten_hien_thi)}
          ${price ? `<a class="go" href="${esc(price.url)}" target="_blank" rel="noopener">GO! ${Number(price.gia_vnd).toLocaleString("vi-VN")}đ</a>` : ""}</span>
          <span class="q">${esc(scaleQty(r, factor))}</span></div>`;
      }).join("")}`).join("")}</div>
      <p class="note">Gia vị và nước dùng tăng chậm hơn số người – nêm lại cho vừa.</p>
      ${bqMon.length ? `<h4 class="bq-h">💡 Bí quyết chọn nguyên liệu</h4><div class="bq">${bqMon.map((c, i) => bqBox(c, i === 0 && bqMon.length === 1)).join("")}</div>` : ""}`
      : `<p class="note">Chưa có bảng nguyên liệu.</p>`,
    cl: hasRecipe(d) ? `<ol class="steps">${steps(d).map((s) => `<li>${esc(s)}</li>`).join("")}</ol>`
      : `<div class="box">Cá Chef chưa có cách làm chi tiết cho món này.<br><a class="btn" href="${esc(d.nguon)}" target="_blank" rel="noopener">Xem trên Cookpad ↗</a></div>`,
    mv: `${seasonBlock(d.ma_mon)}
      <div class="box"><b>Điểm hôm nay: ${d.score}</b>
        ${d.reasons.length ? `<ul class="why">${d.reasons.map((r) => `<li>${esc(r.text)} <span class="${r.diem > 0 ? "plus" : "minus"}">${r.diem > 0 ? "+" : ""}${r.diem}</span></li>`).join("")}</ul>` : ""}</div>`,
  }[tab];
  $app.innerHTML = `
    <div class="rhead"><a class="back" href="#/" id="back">‹ Quay lại</a>${bua ? `<span class="pill">${bua}</span>` : ""}</div>
    ${S.anh[ma] ? `<figure class="anh"><img src="${anhUrl(ma, 800, 520)}" alt="${esc(d.ten_mon)}" onerror="this.parentNode.remove()">
      <figcaption>Ảnh: <a href="${esc(S.anh[ma].nguon_anh)}" target="_blank" rel="noopener">${esc(S.anh[ma].tac_gia || "Cookpad")} · Cookpad</a></figcaption></figure>` : ""}
    <div class="hero"><h1>${esc(d.ten_mon)}</h1>${d.mo_ta_ngan ? `<p>${esc(d.mo_ta_ngan)}</p>` : ""}</div>
    <div class="facts">
      <div><b>${d.thoi_gian_phut ? d.thoi_gian_phut + "′" : "–"}</b>thời gian</div>
      <div><b>${LABEL.do_kho[d.do_kho] || "–"}</b>độ khó</div>
      <div><b>${LABEL.nhiet[d.nhiet] || "–"}</b>${LABEL.dau_mo[d.dau_mo]?.toLowerCase() || "món"}</div>
      <div><b class="${muaCls}">${mua}</b>tháng ${month()}</div>
    </div>
    ${thanhDanhGia(d, moiXong)}
    <div class="tabs2">${[["nl", "Nguyên liệu"], ["cl", "Cách làm"], ["mv", "Mùa vụ"]].map(([k, t]) =>
      `<button data-tab="${k}" class="${k === tab ? "on" : ""}">${t}</button>`).join("")}</div>
    ${body}
    <p class="src">Tham khảo: <a href="${esc(d.nguon)}" target="_blank" rel="noopener">Cookpad</a> · ${d.trang_thai === "da_nau_thu" || dgMon(d.ma_mon).nau?.length ? "đã nấu thử" : "chưa nấu thử"}</p>
    ${hasRecipe(d) ? `<a class="cta" href="#/nau/${d.ma_mon}">👩‍🍳 Bắt đầu nấu – từng bước</a>` : ""}`;
  document.getElementById("back").onclick = (e) => { if (history.length > 1) { e.preventDefault(); history.back(); } };
  $app.querySelectorAll("[data-dg]").forEach((b) => (b.onclick = () => {
    const dg = dgMon(ma), hom = dayStr(0), k = b.dataset.dg;
    if (k === "nau") saveDanhGia(ma, { nau: dg.nau?.includes(hom) ? dg.nau.filter((x) => x !== hom) : [...(dg.nau || []), hom] });
    if (k === "ngon") saveDanhGia(ma, { y: dg.y === 1 ? 0 : 1 });
    if (k === "khong") saveDanhGia(ma, { y: dg.y === -1 ? 0 : -1 });
    if (k === "tim") saveDanhGia(ma, { tim: !dg.tim });
    pageRecipe(ma);
  }));
  const dungHet = $app.querySelector("[data-dung]");
  if (dungHet) dungHet.onclick = () => { for (const c of chinhCua(d).map(trongTu)) if (c) delete tuLanh()[c]; saveTuLanh(); pageRecipe(ma); };
  $app.querySelectorAll("[data-tab]").forEach((b) => (b.onclick = () => { S.tabMon = b.dataset.tab; pageRecipe(ma); }));
  if (tab !== "nl" || !rows.length) return;
  const set = (v) => { S.servings[ma] = Math.min(20, Math.max(1, v)); pageRecipe(ma); };
  document.getElementById("minus").onclick = () => set(n - 1);
  document.getElementById("plus").onclick = () => set(n + 1);
}

// ---------- Chế độ nấu: từng bước, chữ to, giữ màn hình sáng ----------
let wakeLock = null;
async function giuManHinh(bat) {
  try {
    if (bat && !wakeLock && navigator.wakeLock) wakeLock = await navigator.wakeLock.request("screen");
    if (!bat && wakeLock) { await wakeLock.release(); wakeLock = null; }
  } catch { wakeLock = null; /* trình duyệt không hỗ trợ: bỏ qua */ }
}

function pageCook(ma, i) {
  const d = S.ranked.find((x) => x.ma_mon === ma);
  const list = d ? steps(d) : [];
  if (!list.length) { location.hash = `#/mon/${ma}`; return; }
  i = Math.min(list.length - 1, Math.max(0, i || 0));
  const cuoi = i === list.length - 1;
  document.body.classList.add("cook");
  giuManHinh(true);
  $app.innerHTML = `
    <div class="cook-top"><a href="#/mon/${ma}">✕ Thoát</a><span>${esc(d.ten_mon)}</span></div>
    <div class="prog">${list.map((_, j) => `<i class="${j <= i ? "on" : ""}"></i>`).join("")}</div>
    <p class="cook-n">Bước ${i + 1}/${list.length}</p>
    <p class="cook-step">${esc(list[i])}</p>
    <div class="cook-nav">
      ${i ? `<a class="btn" href="#/nau/${ma}/${i}">‹ Trước</a>` : "<span></span>"}
      <a class="btn on" href="${cuoi ? `#/mon/${ma}/xong` : `#/nau/${ma}/${i + 2}`}">${cuoi ? "Xong 🎉" : "Tiếp ›"}</a>
    </div>`;
}

// ---------- Mùa vụ theo tháng ----------
const NHOM_LOC = { all: "Tất cả", hs: "Hải sản", rau: "Rau củ", trai: "Trái cây", thit: "Thịt, trứng", khac: "Khác" };
const nhomLoc = (n) => /hải sản|thủy sản/.test(n.nhom) ? "hs" : n.nhom === "rau củ" ? "rau" : n.nhom === "trái cây" ? "trai"
  : /thịt|trứng|đậu/.test(n.nhom) ? "thit" : "khac";
// Món dùng nguyên liệu này làm nguyên liệu chính.
const monDung = (ma) => S.ranked.filter((d) => String(d.nguyen_lieu_chinh || "").split("|").some((c) => c === ma || S.ing[c]?.cha === ma));

function pageCalendar(mo) {
  if (mo) { S.calOpen = mo; S.calMonth = month(); S.calNhom = "all"; }
  const m = S.calMonth || month(), loc = S.calNhom || "all";
  const sau = [m % 12, (m + 1) % 12]; // chỉ số 2 tháng tới
  const ds = S.data.nguyen_lieu.filter((n) => !n.cha && (loc === "all" || nhomLoc(n) === loc)); // nhánh (ba chỉ, sườn...) cùng lịch với cha
  const ro = ds.filter((n) => n.thang[m - 1] === 2);
  const sap = ds.filter((n) => n.thang[m - 1] < 2 && sau.some((j) => n.thang[j] === 2));
  const traiMua = ds.filter((n) => n.thang[m - 1] === 0 && !sap.includes(n));
  const coHang = ds.filter((n) => n.thang[m - 1] === 1 && !sap.includes(n));
  const item = (n) => {
    const mon = monDung(n.ma).slice(0, 6);
    return `<details class="ni" id="nl-${n.ma}" ${S.calOpen === n.ma ? "open" : ""}>
      <summary><span class="nn">${esc(n.ten)}${n.vung && n.vung !== "chung" ? `<small>${esc(n.vung)}</small>` : ""}</span>${thangBar(n.thang, m)}</summary>
      <div class="nd">${n.ghi_chu ? `<p>${esc(n.ghi_chu)}</p>` : ""}${bqDl(n.ma)}
        <p class="src">Mua ở: ${esc(n.noi_mua || "chợ")} · tin cậy ${esc(n.tin_cay || "–")}${n.nguon ? ` · nguồn: ${String(n.nguon).split("|")
          .map((u, i) => `<a href="${esc(u.trim())}" target="_blank" rel="noopener">${i + 1}</a>`).join(", ")}` : ""}</p>
        ${mon.length ? `<div class="hs wrap">${mon.map((d) => `<a class="chip" href="#/mon/${d.ma_mon}">${esc(d.ten_mon)}</a>`).join("")}</div>` : ""}</div>
    </details>`;
  };
  const nhomBox = (title, list, note, mo2) => list.length ? `<details class="ss" ${mo2 ? "open" : ""}>
    <summary><b>${title}</b><span class="src">${note || list.length + " loại"}</span></summary>${list.map(item).join("")}</details>` : "";
  $app.innerHTML = `
    <h1 class="ptitle">Mùa vụ<small>Phan Rang & vùng lân cận</small></h1>
    <div class="months">${Array.from({ length: 12 }, (_, i) => `<button data-m="${i + 1}" class="${i + 1 === m ? "on" : ""}">T${i + 1}</button>`).join("")}</div>
    <div class="filt">${Object.entries(NHOM_LOC).map(([k, t]) => `<button data-n="${k}" class="${k === loc ? "on" : ""}">${t}</button>`).join("")}</div>
    ${nhomBox("🔥 Đang rộ", ro, "", true) || `<div class="box muted">Tháng ${m} chưa có loại nào rộ trong nhóm này.</div>`}
    ${nhomBox("⏳ Sắp vào mùa", sap, `tháng ${sau[0] + 1}–${sau[1] + 1}`, true)}
    ${nhomBox("✓ Có hàng", coHang, "", coHang.some((n) => n.ma === S.calOpen))}
    ${nhomBox("✕ Trái mùa – nên tránh", traiMua, "", traiMua.some((n) => n.ma === S.calOpen))}
    <p class="note">Chạm vào nguyên liệu để xem cách chọn, cách cất, nguồn và món nấu được.</p>`;
  $app.querySelectorAll("[data-m]").forEach((b) => (b.onclick = () => { S.calMonth = Number(b.dataset.m); pageCalendar(); }));
  $app.querySelectorAll("[data-n]").forEach((b) => (b.onclick = () => { S.calNhom = b.dataset.n; pageCalendar(); }));
  $app.querySelector(".months .on")?.scrollIntoView({ inline: "center", block: "nearest" });
  if (mo) document.getElementById("nl-" + mo)?.scrollIntoView({ block: "center" });
}

// ---------- Tất cả món ----------
const VAI_LOC = ["all", "yt", "da_nau", "man", "rau", "canh", "lau", "nuong", "mot_to", "trang_mieng", "do_uong"];
const TEN_LOC = { all: "Tất cả", yt: "♥ Yêu thích", da_nau: "✓ Đã nấu" };
const hopLoc = (d, v) => v === "all" || (v === "yt" ? dgMon(d.ma_mon).tim || dgMon(d.ma_mon).y === 1
  : v === "da_nau" ? (dgMon(d.ma_mon).nau || []).length > 0 : vaiOf(d) === v);
function pageAll() {
  $app.innerHTML = `<h1 class="ptitle">Món ăn<small>${S.ranked.length} món · sắp theo điểm hôm nay</small></h1>
    <input id="q" class="search" type="search" placeholder="Tìm món – gõ không dấu được (ca thu, canh chua)" value="${esc(S.query)}">
    <div class="filt">${VAI_LOC.map((v) => `<button data-v="${v}" class="${v === (S.vaiLoc || "all") ? "on" : ""}">${TEN_LOC[v] || VAI_NGAN[v]}</button>`).join("")}</div>
    <div id="all-list"></div>`;
  const q = document.getElementById("q");
  q.oninput = () => { S.query = q.value; renderAll(); };
  $app.querySelectorAll("[data-v]").forEach((b) => (b.onclick = () => { S.vaiLoc = b.dataset.v; pageAll(); }));
  renderAll();
}

function renderAll() {
  const words = plain(S.query).split(/\s+/).filter(Boolean), v = S.vaiLoc || "all";
  const list = S.ranked.filter((d) => hopLoc(d, v) && words.every((w) => plain(d.ten_mon).includes(w)));
  document.getElementById("all-list").innerHTML = list.length ? `<div class="list">${list.map((d) => `
    <a class="row-link li" href="#/mon/${d.ma_mon}">${thumb(d)}
      <span class="tx"><b>${esc(d.ten_mon)}</b><span class="meta">${VAI_NGAN[vaiOf(d)] || ""}${d.thoi_gian_phut ? ` · ${d.thoi_gian_phut}′` : ""}${d.season === 2 ? ' · <span class="peak">Đang rộ</span>' : d.season === 0 ? " · trái mùa" : ""}</span></span>
      <span class="score ${d.score < 0 ? "neg" : ""}">${d.score > 0 ? "+" : ""}${d.score}</span></a>`).join("")}</div>` : `<p class="muted">${v === "yt" ? "Chưa có món yêu thích – bấm ♡ hoặc 👍 trên trang món." : v === "da_nau" ? "Chưa ghi món nào đã nấu." : "Không thấy món nào."}</p>`;
}

// ---------- Tủ lạnh: có gì trong tủ -> nấu được món gì ----------
const TL_KEY = "cachef.tulanh";
const TL_BO = new Set([...NL_CHUNG, "gao_nep", "dau_hat"]); // gia vị, đồ khô dùng chung: coi như luôn có
// Tủ lạnh: { mã nguyên liệu: { n: ngày cho vào, da: 1 nếu để ngăn đá } }. Bản cũ lưu mảng mã – đổi sang dạng mới, coi như cho vào hôm nay.
function tuLanh() {
  if (!S.tuLanh) {
    let v;
    try { v = JSON.parse(localStorage.getItem(TL_KEY) || "{}"); } catch { v = {}; }
    if (Array.isArray(v)) v = Object.fromEntries(v.map((ma) => [ma, { n: dayStr(0) }]));
    S.tuLanh = v && typeof v === "object" ? v : {};
  }
  return S.tuLanh;
}
function saveTuLanh() {
  try { localStorage.setItem(TL_KEY, JSON.stringify(S.tuLanh)); } catch { /* chặn lưu: chỉ giữ trong phiên */ }
  S.ranked = rankDishes(0); S.rankedTomorrow = rankDishes(1);
}
// Hạn dùng theo bí quyết bảo quản: de = số ngày đã để, con = số ngày còn ngon (âm là quá hạn).
function hanTL(ma) {
  const x = tuLanh()[ma];
  if (!x) return null;
  const bq = S.bq[ma] || {}, han = x.da ? Number(bq.da) || 30 : Number(bq.mat) || 3;
  const de = Math.max(0, Math.round((Date.parse(dayStr(0)) - Date.parse(x.n)) / 864e5)) || 0;
  return { de, con: han - de, da: !!x.da, hopDa: Number(bq.da) > 0 };
}
// Tủ có nguyên liệu c chưa – trả về mã đang ghi trong tủ: đúng mã; mã cha ghi chung (tủ ghi "Thịt heo" thì món cần
// ba chỉ cũng tính là có); hoặc c là mã cha (món ghi chung "thịt heo") và tủ có một nhánh của nó.
function trongTu(c) {
  const tl = tuLanh();
  if (tl[c]) return c;
  const cha = S.ing[c]?.cha;
  if (cha && tl[cha]) return cha;
  return Object.keys(tl).find((k) => S.ing[k]?.cha === c) || "";
}
const canDungSom = (ma) => { const h = hanTL(ma); return !!h && !h.da && h.con <= 1; };
// Mã nguyên liệu chính của món (bỏ gia vị, đồ dùng chung).
const chinhCua = (d) => [...new Set(String(d.nguyen_lieu_chinh || "").split("|").filter((c) => c && S.ing[c] && !TL_BO.has(c)))];

// Bí quyết chọn và bảo quản một nguyên liệu, dạng mở/thu.
function bqBox(ma, mo = false) {
  const bq = S.bq[ma], n = S.ing[ma];
  if (!bq || !n) return "";
  return `<details class="bq-d" ${mo ? "open" : ""}><summary>${esc(n.ten)}</summary>${bqDl(ma)}</details>`;
}
function bqDl(ma) {
  const bq = S.bq[ma];
  return bq ? `<dl class="bq-dl"><dt>Chọn</dt><dd>${esc(bq.chon)}</dd>${bq.tranh ? `<dt>Tránh</dt><dd>${esc(bq.tranh)}</dd>` : ""}
    <dt>Cất</dt><dd>${esc(bq.bao_quan)}</dd></dl>` : "";
}
const hanChu = (h) => h.con < 0 ? `<span class="minus">quá ${-h.con} ngày – xem lại trước khi dùng</span>`
  : h.con === 0 ? `<span class="minus">nên dùng hôm nay</span>` : h.con === 1 ? `<span class="hot">nên dùng trước mai</span>`
  : h.con > 60 ? "còn để lâu" : `còn ~${h.con} ngày`;

function pageFridge() {
  const tl = tuLanh(), loc = S.tlNhom || "all", q = plain(S.tlQuery || "");
  const co = Object.keys(tl).filter((c) => S.ing[c]).sort((a, b) => hanTL(a).con - hanTL(b).con);
  const dung = new Set(S.ranked.flatMap(chinhCua));
  const nl = S.data.nguyen_lieu.filter((n) => !tl[n.ma] && dung.has(n.ma) && (loc === "all" || nhomLoc(n) === loc) && (!q || plain(n.ten).includes(q)))
    .sort((a, b) => a.ten.localeCompare(b.ten, "vi"));
  // Món dùng đồ trong tủ, đã sắp theo điểm hôm nay (đồ sắp quá hạn được cộng điểm nên lên trước).
  const mon = S.ranked.filter((d) => ["man", "rau", "canh", "lau", "nuong", "mot_to"].includes(vaiOf(d)))
    .map((d) => ({ d, c: chinhCua(d) })).filter((x) => x.c.length && x.c.some(trongTu))
    .map((x) => ({ ...x, thieu: x.c.filter((c) => !trongTu(c)) }));
  const du = mon.filter((x) => !x.thieu.length).slice(0, 12), gan = mon.filter((x) => x.thieu.length === 1).slice(0, 8);
  const nutBua = (d) => {
    const o = trongBua(d.ma_mon);
    if (/nay/.test(o)) return `<span class="pill">${o}</span>`;
    const v = vaiOf(d);
    if (!["man", "rau", "canh", "lau", "nuong"].includes(v)) return "";
    return `<span class="add">${MOT_NOI.includes(v) ? "" : `<button data-add="trua" data-ma="${d.ma_mon}" aria-label="Đưa ${esc(d.ten_mon)} vào bữa trưa nay">＋Trưa</button>`}<button data-add="toi" data-ma="${d.ma_mon}" aria-label="Đưa ${esc(d.ten_mon)} vào bữa tối nay">＋Tối</button></span>`;
  };
  const monRow = (x) => `<div class="li tl-mon"><a class="row-link" href="#/mon/${x.d.ma_mon}">${thumb(x.d)}
    <span class="tx"><b>${esc(x.d.ten_mon)}</b><span class="meta">${x.thieu.length ? `thiếu ${esc(x.thieu.map((c) => S.ing[c].ten).join(", "))}`
      : `${VAI_NGAN[vaiOf(x.d)]}${x.d.thoi_gian_phut ? ` · ${x.d.thoi_gian_phut}′` : ""}${x.c.some((c) => canDungSom(trongTu(c))) ? ' · <span class="hot">dùng đồ sắp hết hạn</span>' : ""}`}</span></span></a>
    ${x.thieu.length ? "" : nutBua(x.d)}</div>`;
  const itemRow = (c) => {
    const h = hanTL(c), n = S.ing[c];
    return `<div class="tli ${h.con <= 1 && !h.da ? "gap" : ""}">
      <details><summary><b>${esc(n.ten)}</b><span class="meta">${h.da ? "❄ ngăn đá" : "ngăn mát"} · ${h.de ? `để ${h.de} ngày` : "mới cho vào"} · ${hanChu(h)}</span></summary>
        ${S.bq[c] ? `<p class="bq-t">${esc(S.bq[c].bao_quan)}${h.da && !h.hopDa ? " <b>Loại này không hợp để ngăn đá.</b>" : ""}</p>` : ""}</details>
      <button class="ngan ${h.da ? "on" : ""}" data-da="${c}" aria-pressed="${h.da}" title="${h.da ? "Chuyển xuống ngăn mát" : "Chuyển lên ngăn đá"}">❄</button>
      <button class="bo" data-bo="${c}" aria-label="Bỏ ${esc(n.ten)} khỏi tủ">✕</button></div>`;
  };
  const chip = (n) => `<button class="chip" data-nl="${n.ma}">＋ ${esc(n.ten)}</button>`;
  $app.innerHTML = `
    <h1 class="ptitle">Tủ lạnh<small>Ghi thứ đang có – Cá Chef ưu tiên món dùng đồ trong tủ, nhắc thứ cần dùng sớm</small></h1>
    ${thawBox()}
    ${co.length ? `<div class="tl-head"><b>Trong tủ có (${co.length})</b><button class="link" id="xoa">Xóa hết</button></div>
      <div class="tl-list">${co.map(itemRow).join("")}</div>
      <h4>Nấu được ngay (${du.length})</h4>${du.length ? `<div class="list">${du.map(monRow).join("")}</div>` : '<p class="muted">Chưa đủ nguyên liệu chính cho món nào.</p>'}
      ${gan.length ? `<h4>Thiếu 1 thứ</h4><div class="list">${gan.map(monRow).join("")}</div>` : ""}`
      : '<p class="note">Chạm vào nguyên liệu bên dưới để ghi là đang có trong tủ. Cá Chef sẽ gợi ý món nấu được, ưu tiên đồ trong tủ khi ghép bữa và nhắc thứ cần dùng sớm.</p>'}
    <h4>${co.length ? "Thêm nguyên liệu" : "Trong tủ có gì?"}</h4>
    <input id="tlq" class="search" type="search" placeholder="Tìm nguyên liệu (ca, tom, bi…)" value="${esc(S.tlQuery || "")}">
    <div class="filt">${Object.entries(NHOM_LOC).map(([k, t]) => `<button data-n="${k}" class="${k === loc ? "on" : ""}">${t}</button>`).join("")}</div>
    <div class="hs wrap tl">${nl.map(chip).join("") || '<span class="muted">Không thấy nguyên liệu.</span>'}</div>`;
  $app.querySelectorAll("[data-nl]").forEach((b) => (b.onclick = () => { tl[b.dataset.nl] = { n: dayStr(0) }; saveTuLanh(); pageFridge(); }));
  $app.querySelectorAll("[data-bo]").forEach((b) => (b.onclick = () => { delete tl[b.dataset.bo]; saveTuLanh(); pageFridge(); }));
  $app.querySelectorAll("[data-da]").forEach((b) => (b.onclick = () => {
    const x = tl[b.dataset.da];
    if (x.da) delete x.da; else x.da = 1;
    saveTuLanh(); pageFridge();
  }));
  $app.querySelectorAll("[data-add]").forEach((b) => (b.onclick = () => { duaVaoBua(b.dataset.ma, b.dataset.add); location.hash = "#/"; }));
  $app.querySelectorAll("[data-n]").forEach((b) => (b.onclick = () => { S.tlNhom = b.dataset.n; pageFridge(); }));
  const ip = document.getElementById("tlq");
  ip.oninput = () => { S.tlQuery = ip.value; pageFridge(); const e = document.getElementById("tlq"); e.focus(); e.setSelectionRange(e.value.length, e.value.length); };
  const x = document.getElementById("xoa"); if (x) x.onclick = () => { if (!confirm("Xóa hết đồ trong tủ?")) return; for (const k of Object.keys(tl)) delete tl[k]; saveTuLanh(); pageFridge(); };
}

// ---------- Điều hướng ----------
function route() {
  const h = location.hash.slice(1) || "/";
  const [, page, arg, arg2] = h.split("/");
  const tab = page === "lich" ? "lich" : page === "mon" || page === "yeu-thich" ? "mon" : page === "tu-lanh" ? "tu-lanh" : page === "nau" ? "" : "home";
  document.querySelectorAll("[data-nav]").forEach((a) => a.classList.toggle("on", a.dataset.nav === tab));
  if (page !== "nau") { document.body.classList.remove("cook"); giuManHinh(false); }
  if (page === "lich") pageCalendar(arg && decodeURIComponent(arg));
  else if (page === "ngay-mai") pageHome(1);
  else if (page === "mon" && arg) {
    if (S.lastMon !== arg) S.tabMon = "nl";
    S.lastMon = arg;
    const ma = decodeURIComponent(arg), xong = arg2 === "xong";
    if (xong && !(dgMon(ma).nau || []).includes(dayStr(0))) saveDanhGia(ma, { nau: [...(dgMon(ma).nau || []), dayStr(0)] });
    pageRecipe(ma, xong);
  }
  else if (page === "yeu-thich") { S.vaiLoc = "yt"; pageAll(); }
  else if (page === "mon") pageAll();
  else if (page === "tu-lanh") pageFridge();
  else if (page === "nau" && arg) pageCook(decodeURIComponent(arg), Number(arg2 || 1) - 1);
  else pageHome();
  if (!(page === "lich" && arg)) window.scrollTo(0, 0);
}

load().then(() => { headerBar(); window.addEventListener("hashchange", route); route(); })
  .catch((e) => { $app.innerHTML = `<div class="box">Lỗi tải dữ liệu: ${esc(e.message)}</div>`; });
