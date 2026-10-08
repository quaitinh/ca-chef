// Cá Chef – demo: thời tiết Phan Rang + mùa vụ -> 3 món gợi ý (hôm nay và ngày mai).
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
  vai_mam: { man: "Món mặn", rau: "Món rau", canh: "Canh", mot_to: "Món một tô (sáng)", lau: "Lẩu",
    trang_mieng: "Tráng miệng, chè", do_uong: "Đồ uống", an_vat: "Ăn vặt", dua_kem: "Dưa, đồ ăn kèm" },
};

const S = { data: null, weather: null, ing: {}, prices: {}, ingByDish: {}, nhan: {}, query: "", ranked: [], rankedTomorrow: [], meals: [null, null], shown: [{ trua: new Set(), toi: new Set() }, { trua: new Set(), toi: new Set() }], servings: {}, chon: {} };

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
  S.ranked = rankDishes(0);
  S.meals[0] = pickMeals(S.ranked, 0, monDaChon(S.ranked, 0));
  recordHistory(mealDishes(S.meals[0]).map((d) => d.ma_mon));
  S.rankedTomorrow = rankDishes(1); // sau recordHistory để không gợi ý lại món của hôm nay
  S.meals[1] = pickMeals(S.rankedTomorrow, 1, monDaChon(S.rankedTomorrow, 1));
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
  return { ...dish, score, reasons, season };
}

// Xáo nhẹ theo ngày để các món bằng điểm không lần nào cũng xếp như nhau.
function dayHash(s, day = 0) {
  let h = 0;
  for (const c of dayStr(day) + s) h = (h * 31 + c.charCodeAt(0)) | 0;
  return h;
}

function rankDishes(day = 0) {
  const hits = weatherRulesHit(day);
  return S.data.mon_an
    .map((d) => scoreDish(d, hits, day))
    .sort((a, b) => b.score - a.score || dayHash(a.ma_mon, day) - dayHash(b.ma_mon, day));
}

// Lẩu là bữa lớn: chỉ gợi ý khi 6 ngày trước chưa gợi ý lẩu nào.
const LAU_CACH_NGAY = 7;
function lauGanDay(day) {
  const ref = dayStr(day), loai = Object.fromEntries(S.data.mon_an.map((m) => [m.ma_mon, m.loai]));
  return Object.entries(readHistory()).some(([date, list]) =>
    date < ref && (new Date(ref) - new Date(date)) / 86400000 < LAU_CACH_NGAY && list.some((ma) => loai[ma] === "lau"));
}

// ---------- Ghép bữa ----------
// Quy tắc:
//  - Lẩu chỉ ăn buổi tối (tối đa 1 lần/7 ngày). Hôm tối ăn lẩu thì trưa gợi ý món dễ nấu.
//  - Trưa: mặn + rau + canh. Món mặn kho/hầm/om/rim thì nấu dư, tối ăn lại -> tối chỉ nấu thêm rau + canh.
//  - Không lặp nguyên liệu chính trong ngày (rau thơm, gia vị dùng chung được); đạm tối khác đạm trưa.
//  - Trong một bữa: tối đa 1 món nấu lâu (kho/om/hầm/rim...) và 1 món cầu kì (nướng, nhồi, cuốn, chả...);
//    không 2 món cùng chiên/xào/nướng; canh có đạm thì khác nhóm đạm của món mặn.
//  - Món mặn có nhiều nước (om, bung, nấu, cà ri...) thì bữa đó bỏ canh: chỉ mặn + rau.
//  - Cả ngày tối đa 1 món nhiều dầu mỡ.
//  - Ưu tiên (bỏ được khi hết món): bữa có rau xanh; món mặn khó ăn với trẻ (cay, nhiều xương) thì canh có đạm dễ ăn.
const VAI_TU_LOAI = { canh: "canh", lau: "lau", goi: "rau", trang_mieng: "trang_mieng", do_uong: "do_uong", an_vat: "an_vat", mon_chinh: "man" };
const vaiOf = (d) => S.nhan[d.ma_mon]?.vai_mam || VAI_TU_LOAI[d.loai] || "man";
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
const coNuoc = (d) => vaiOf(d) === "man" && /(^|\s)(om|bung|nấu|hầm|sốt vang|cà ri)(\s|$)|bò kho|riêu/i.test(d.ten_mon);
const CACH_KHONG_LAP = new Set(["chien", "xao", "nuong"]);
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
const NL_MA = { thit_heo: "heo", long_heo: "heo", tom_the: "tom", tom_hum: "tom", muc_tuoi: "muc", muc_mot_nang: "muc",
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
    if (vaiOf(d) === "lau" && r.vai_tro !== "chinh") continue; // lẩu: rau nhúng, bún đi kèm không tính là nguyên liệu chính
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
const THU_TU_VAI = ["lau", "man", "rau", "canh", "trang_mieng"];
const theoVai = (list) => [...list].sort((a, b) => THU_TU_VAI.indexOf(vaiOf(a)) - THU_TU_VAI.indexOf(vaiOf(b)));

function pickTrua(ranked, daXem, cam, used, ctx, deThoi, giu = []) {
  const de = deThoi ? { man: deNau, rau: deNau, canh: deNau } : {};
  const ex = { da_xem: daXem, cam: [...cam, ...giu.map((d) => d.ma_mon), ...vuaHien(daXem)] };
  return theoVai([...giu, ...pickBua(ranked, conThieu(giu), ex, used, ctx, [...giu], de)]);
}

function pickToi(ranked, daXem, used, ctx, trua, du, giu = []) {
  const coSan = du ? [du, ...giu] : giu;
  const ex = { da_xem: daXem, cam: [...trua.map((d) => d.ma_mon), ...giu.map((d) => d.ma_mon), ...vuaHien(daXem)] };
  const damTrua = damOf(trua.find((d) => vaiOf(d) === "man") || {});
  return theoVai([...coSan, ...pickBua(ranked, conThieu(coSan), ex, used, ctx, [...coSan],
    { man: (x) => !damTrua || damOf(x) !== damTrua })]);
}

// keep.trua / keep.toi: các món giữ nguyên (món đã chọn, hoặc cả bữa còn lại khi bấm Đổi một bữa).
function pickMeals(ranked, day, keep = {}) {
  const sh = S.shown[day], used = new Set();
  const kTrua = keep.trua || [], kToi = keep.toi || [];
  const ctx = { mo: [...kTrua, ...kToi].filter((d) => d.dau_mo === "nhieu").length };
  [...kTrua, ...kToi].forEach((d) => dungNL(d, used));
  // Lẩu tối: giữ nếu đã chọn; nếu tối chưa có món nào giữ thì xét gợi ý lẩu (không trùng nguyên liệu bữa trưa).
  let toi = kToi.some((d) => vaiOf(d) === "lau") ? [...kToi] : null;
  if (!toi && !kToi.length && !lauGanDay(day)) {
    const bestMan = ranked.find((d) => d.score > -3 && vaiOf(d) === "man");
    const l = pickRole(ranked, "lau", new Set([...sh.toi, ...kTrua.map((d) => d.ma_mon)]), (x) => khongTrung(x, used));
    if (l && khongTrung(l, used) && l.score >= (bestMan?.score ?? -99)) { toi = [l]; dungNL(l, used); }
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
  const du = manTrua && khoHam(manTrua) && !kToi.some((d) => vaiOf(d) === "man") ? manTrua : null;
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

function weatherCard(day = 0) {
  const d = S.weather?.daily;
  if (!d || d.time.length <= day) return `<div class="card">Không lấy được thời tiết${day ? " ngày mai" : ""} (kiểm tra mạng). Gợi ý chỉ dựa trên mùa vụ.</div>`;
  const c = S.weather.current;
  const [icon, desc] = wmo(day === 0 && c ? c.weather_code : d.weather_code[day]);
  const hits = weatherRulesHit(day);
  const names = [...new Set(hits.map((r) => r.ten))];
  const rainy = hits.some((r) => r.ap_dung_cho === "nhiet=nong" && r.diem > 0);
  const hot = hits.some((r) => r.ap_dung_cho === "nhiet=mat" && r.diem > 0);
  const verdict = rainy ? ["rain", "Ưu tiên món nóng, ấm bụng"] : hot ? ["hot", "Ưu tiên món mát, thanh nhiệt, ít dầu"] : null;
  const [, mm, dd] = d.time[day].split("-");
  const big = day === 0 && c ? `${Math.round(c.temperature_2m)}°C` : `${Number(dd)}/${Number(mm)}`;
  const where = day === 0 && c ? "Phan Rang" : "Ngày mai · Phan Rang";
  return `<div class="card">
    <div class="weather">
      <div class="icon">${icon}</div>
      <div class="now">${big} <span class="muted" style="font-size:16px;font-weight:400">${where}</span></div>
      <div class="desc">${desc} · cao ${Math.round(d.temperature_2m_max[day])}° / thấp ${Math.round(d.temperature_2m_min[day])}°</div>
    </div>
    <div class="stats">
      <span class="stat">🌧️ Mưa <b>${d.precipitation_sum[day]} mm</b> (${d.precipitation_probability_max[day]}%)</span>
      <span class="stat">💨 Gió <b>${Math.round(d.wind_speed_10m_max[day])} km/h</b></span>
      <span class="stat">🔆 UV <b>${Math.round(d.uv_index_max[day])}</b></span>
      ${day === 0 && c ? `<span class="stat">💧 Ẩm <b>${c.relative_humidity_2m}%</b></span>` : ""}
    </div>
    ${verdict ? `<div class="verdict ${verdict[0]}">${verdict[1]}${names.length ? ` – ${esc(names.join(", ").toLowerCase())}` : ""}</div>` : ""}
  </div>`;
}

// Tóm tắt thời tiết ngày mai một dòng, hiện ở trang Hôm nay.
function tomorrowTeaser() {
  const d = S.weather?.daily;
  if (!d || d.time.length < 2) return "";
  const [icon, desc] = wmo(d.weather_code[1]);
  const m = S.meals[1];
  const top = `trưa ${m.trua.map((x) => x.ten_mon).join(", ")}; tối ${m.toi.filter((x) => x.ma_mon !== m.du).map((x) => x.ten_mon).join(", ")}${m.du ? " (+ món mặn ăn lại từ trưa)" : ""}`;
  return `<a class="card teaser" href="#/ngay-mai">
    <span class="t-icon">${icon}</span>
    <span><b>Ngày mai:</b> ${desc.toLowerCase()}, ${Math.round(d.temperature_2m_min[1])}–${Math.round(d.temperature_2m_max[1])}°, mưa ${d.precipitation_sum[1]} mm
      <span class="muted">· Gợi ý: ${esc(top)}</span></span>
    <span class="t-go">Xem & rã đông →</span>
  </a>`;
}

// Đồ tươi sống (thịt, hải sản) của các món ngày mai – thường để ngăn đá, cần rã đông từ tối nay.
const FROZEN_GROUPS = ["thịt", "hải sản"];
const NOT_FROZEN = ["rong_sun", "sua", "muc_mot_nang"]; // rong khô, sứa ngâm, mực phơi: không cần rã đông lâu
const FROZEN_WORDS = /chả cá|xương|mỡ heo|sườn|giò heo/i;
function thawList(meals) {
  const out = [];
  for (const d of mealDishes(meals)) {
    const f = d.ma_mon === meals.du ? 2 : 1; // nấu dư cho bữa tối
    for (const r of S.ingByDish[d.ma_mon] || []) {
      if (r.vai_tro === "gia_vi") continue;
    if (vaiOf(d) === "lau" && r.vai_tro !== "chinh") continue; // lẩu: rau nhúng, bún đi kèm không tính là nguyên liệu chính
      const codes = String(r.ma_nguyen_lieu || "").split("|").filter(Boolean);
      const frozen = codes.length
        ? codes.some((c) => FROZEN_GROUPS.includes(S.ing[c]?.nhom) && !NOT_FROZEN.includes(c))
        : FROZEN_WORDS.test(r.ten_hien_thi);
      if (frozen) out.push({ ten: r.ten_hien_thi, mon: d.ten_mon + (f > 1 ? " (nấu dư cho tối)" : ""), qty: scaleQty(r, f) });
    }
  }
  return out;
}

function thawCard(meals) {
  const list = thawList(meals);
  if (!list.length) return `<div class="card thaw"><b>🧊 Rã đông:</b> các món gợi ý ngày mai không cần rã đông thịt/cá.</div>`;
  return `<div class="card thaw">
    <b>🧊 Tối nay chuyển từ ngăn đá xuống ngăn mát:</b>
    <ul>${list.map((x) => `<li><b>${esc(x.ten)}</b> <span class="muted">– ${esc(x.qty)} · cho ${esc(x.mon)}</span></li>`).join("")}</ul>
    <p class="note">Rã đông trong ngăn mát mất khoảng 12–24 giờ (miếng to lâu hơn). Quên thì ngâm cả túi kín trong nước lạnh, 30 phút thay nước một lần.
      Không rã đông ở nhiệt độ phòng.</p>
  </div>`;
}

// ---------- Trang ----------
function chips(d) {
  const peak = d.season === 2 ? `<span class="chip peak">Đang rộ</span>` : "";
  return `<div class="chips">${peak}
    <span class="chip ${d.nhiet}">${LABEL.nhiet[d.nhiet] ?? d.nhiet}</span>
    <span class="chip">${LABEL.loai[d.loai] ?? d.loai}</span>
    ${LABEL.do_nang[d.do_nang] ? `<span class="chip">${LABEL.do_nang[d.do_nang]}</span>` : ""}
    ${LABEL.dau_mo[d.dau_mo] ? `<span class="chip">${LABEL.dau_mo[d.dau_mo]}</span>` : ""}
    ${d.thoi_gian_phut ? `<span class="chip">⏱ ${d.thoi_gian_phut}′</span>` : ""}
    ${hasRecipe(d) ? "" : `<span class="chip">↗ Cookpad</span>`}</div>`;
}

function mealCards(list, meals, bua, chon) {
  return `<div class="picks">${list.map((d) => {
    const du = d.ma_mon === meals.du, anLai = du && bua === "toi";
    const ghi = (du ? (bua === "trua" ? " · nấu gấp đôi, tối ăn tiếp" : " · ăn lại từ trưa") : "") +
      (coNuoc(d) ? " · có nước, thay canh" : "");
    const daChon = chon?.[bua].has(d.ma_mon);
    return `
      <div class="pick-wrap">
        <a class="card pick ${anLai ? "leftover" : ""} ${daChon ? "da-chon" : ""}" href="#/mon/${d.ma_mon}">
          <span class="rank">${esc(LABEL.vai_mam[vaiOf(d)] ?? "")}${ghi}</span>
          <h3>${esc(d.ten_mon)}</h3>
          ${d.mo_ta_ngan && !anLai ? `<p>${esc(d.mo_ta_ngan)}</p>` : ""}
          ${anLai ? "" : chips(d)}
          ${anLai ? "" : `<span class="why">✓ ${esc(d.reasons.filter((r) => r.diem > 0).map((r) => r.text).join(" · ") || "Hợp mùa")}</span>`}
        </a>
        ${chon && !anLai ? `<button class="chon ${daChon ? "on" : ""}" data-chon="${bua}" data-ma="${d.ma_mon}" aria-pressed="${daChon}"
          title="${daChon ? "Bỏ chọn – món này sẽ được đổi cùng các món khác" : "Chọn món này – giữ lại khi đổi các món còn lại"}">${daChon ? "✓ Đã chọn" : "Chọn"}</button>` : ""}
      </div>`;
  }).join("")}</div>`;
}

function buaTitle(meals, bua) {
  if (bua === "trua") return "🍚 Bữa trưa" + (meals.lau ? " – món dễ nấu (tối ăn lẩu)" : "");
  const them = meals.toi.some(coNuoc) ? "rau" : "rau + canh";
  return "🌙 Bữa tối" + (meals.lau ? " – lẩu" : meals.du ? ` – nấu thêm ${them}` : "");
}

function pageHome(day = 0) {
  const ranked = day ? S.rankedTomorrow : S.ranked;
  const meals = S.meals[day];
  const chon = chonOf(day);
  // Đổi một bữa: chỉ đổi các món chưa chọn; chọn đủ cả bữa thì coi như đã chốt bữa.
  const conDoi = (k) => meals[k].some((d) => !chon[k].has(d.ma_mon) && !(k === "toi" && d.ma_mon === meals.du));
  const m = month(day);
  const inSeason = S.data.nguyen_lieu.filter((n) => n.thang[m - 1] === 2);
  const shown = new Set(mealDishes(meals).map((p) => p.ma_mon));
  const others = ranked.filter((d) => !shown.has(d.ma_mon) && vaiOf(d) !== "dua_kem").slice(0, 8);
  $app.innerHTML = `
    ${weatherCard(day)}
    ${day ? "" : tomorrowTeaser()}
    <h2>${day ? "Ngày mai nấu gì?" : "Hôm nay nấu gì?"}</h2>
    ${["trua", "toi"].map((k) => `
      <div class="row meal-head"><h3>${buaTitle(meals, k)}</h3>
        ${conDoi(k) ? `<button class="btn" data-swap="${k}">🔄 ${chon[k].size ? "Đổi món còn lại" : "Đổi"}</button>`
          : '<span class="chot">✓ Đã chốt bữa</span>'}</div>
      ${mealCards(meals[k], meals, k, chon)}`).join("")}
    ${day ? thawCard(meals) : ""}
    <h2>Đang vào mùa tháng ${m}</h2>
    <div class="chips">${inSeason.map((n) => `<span class="chip peak">${esc(n.ten)}</span>`).join("") || '<span class="muted">Chưa có dữ liệu</span>'}</div>
    <h2>Món khác cũng hợp</h2>
    <div class="card list">${others.map((d) => `
      <a href="#/mon/${d.ma_mon}"><span>${esc(d.ten_mon)} <span class="muted">· ${LABEL.vai_mam[vaiOf(d)] ?? ""}</span></span>
      <span class="score ${d.score < 0 ? "neg" : ""}">${d.score > 0 ? "+" : ""}${d.score} điểm</span></a>`).join("")}</div>`;
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
    S.meals[day] = next;
    if (day === 0) recordHistory(mealDishes(next).map((d) => d.ma_mon));
    pageHome(day);
  }));
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
    .slice(0, 4);
  if (!rows.length) return `<p class="note">Nguyên liệu của món này có quanh năm.</p>`;
  const bar = (r) => `<div class="mini-row"><span class="mini-name">${esc(r.ten)}</span>
    <div class="mini">${r.thang.map((v, i) => `<span class="v${v} ${i + 1 === m ? "cur" : ""}" title="Tháng ${i + 1}"></span>`).join("")}</div></div>`;
  return `<p class="note">Mùa vụ nguyên liệu (khung đậm = tháng ${m}):</p>
    ${rows.map(bar).join("")}
    <div class="mini-row"><span class="mini-name"></span><div class="mini-lbl">${rows[0].thang.map((_, i) =>
      `<span class="${i + 1 === m ? "cur-lbl" : ""}">${i + 1}</span>`).join("")}</div></div>`;
}


function pageRecipe(ma) {
  const d = S.ranked.find((x) => x.ma_mon === ma);
  if (!d) { $app.innerHTML = `<p>Không tìm thấy món.</p><a href="#/">← Về trang chính</a>`; return; }
  const base = Number(d.khau_phan_goc) || 4;
  const n = S.servings[ma] ?? base;
  const factor = n / base;
  const rows = S.ingByDish[ma] || [];
  const unitName = d.loai === "do_uong" || d.loai === "trang_mieng" ? "phần" : "người";
  $app.innerHTML = `
    <a class="back" href="#/">← Hôm nay</a>
    <div class="card">
      <h1>${esc(d.ten_mon)}</h1>
      ${d.mo_ta_ngan ? `<p>${esc(d.mo_ta_ngan)}</p>` : ""}
      ${chips(d)}
      <p class="note">${d.do_kho ? `Độ khó: ${LABEL.do_kho[d.do_kho] ?? d.do_kho} · ` : ""}Điểm hôm nay: ${d.score}
        ${d.reasons.length ? `(${d.reasons.map((r) => `${esc(r.text)} ${r.diem > 0 ? "+" : ""}${r.diem}`).join(", ")})` : ""}</p>
      ${seasonBlock(d.ma_mon)}
    </div>
    ${hasRecipe(d) ? "" : `<div class="card cookpad">
      <p>Cá Chef chưa có công thức chi tiết cho món này. Xem cách làm trên Cookpad:</p>
      <a class="btn on" href="${esc(d.nguon)}" target="_blank" rel="noopener">Mở công thức trên Cookpad ↗</a></div>`}
    ${rows.length ? `<h2>Nguyên liệu</h2>
    <div class="servings">
      <button id="minus" aria-label="Bớt">−</button><b>${n}</b><span>${unitName}</span><button id="plus" aria-label="Thêm">+</button>
    </div>
    <ul class="card ing">${rows.map((r) => {
      const price = S.prices[String(r.ma_nguyen_lieu).split("|")[0]];
      return `<li><span class="${r.vai_tro === "chinh" ? "main" : ""}">${esc(r.ten_hien_thi)}
        ${price ? `<a class="go" href="${esc(price.url)}" target="_blank" rel="noopener">GO!: ${esc(price.san_pham_go)} – ${Number(price.gia_vnd).toLocaleString("vi-VN")}đ</a>` : ""}</span>
        <span class="qty">${esc(scaleQty(r, factor))}</span></li>`;
    }).join("")}</ul>
    <p class="note">Gia vị và nước dùng tăng chậm hơn số người – nêm lại cho vừa.</p>` : ""}
    ${hasRecipe(d) ? `<h2>Cách làm</h2>
    <ol class="card steps">${String(d.cach_lam).split("\n").map((s) => `<li>${esc(s.replace(/^\d+\.\s*/, ""))}</li>`).join("")}</ol>` : ""}
    <p class="note">Tham khảo: <a href="${esc(d.nguon)}" target="_blank" rel="noopener">Cookpad</a> ·
      Trạng thái: ${d.trang_thai === "da_nau_thu" ? "đã nấu thử" : "chưa nấu thử"}</p>`;
  if (!rows.length) return;
  const set = (v) => { S.servings[ma] = Math.min(20, Math.max(1, v)); pageRecipe(ma); };
  document.getElementById("minus").onclick = () => set(n - 1);
  document.getElementById("plus").onclick = () => set(n + 1);
}

const REGIONS = {
  nt: { label: "Ninh Thuận", test: (n) => n.vung.includes("Ninh Thuận") },
  lc: { label: "Tỉnh lân cận", test: (n) => !n.vung.includes("Ninh Thuận") && n.vung !== "Đà Lạt" && n.vung !== "chung" },
  dl: { label: "Đà Lạt", test: (n) => n.vung === "Đà Lạt" },
  all: { label: "Tất cả", test: (n) => n.vung !== "chung" },
};
let calRegion = "all";

function pageCalendar() {
  const m = month();
  const rows = S.data.nguyen_lieu.filter(REGIONS[calRegion].test);
  $app.innerHTML = `
    <h1>Lịch mùa vụ</h1>
    <div class="filters">${Object.entries(REGIONS).map(([k, r]) =>
      `<button class="btn ${k === calRegion ? "on" : ""}" data-r="${k}">${r.label}</button>`).join("")}</div>
    <div class="legend"><span><i class="v2"></i>Đang rộ / ngon nhất</span><span><i class="v1"></i>Có hàng</span><span><i class="v0"></i>Trái mùa</span><span>Khung đậm = tháng này</span></div>
    <div class="cal-wrap"><table class="cal">
      <thead><tr><th>Nguyên liệu</th>${Array.from({ length: 12 }, (_, i) => `<th>T${i + 1}</th>`).join("")}</tr></thead>
      <tbody>${rows.map((n) => `<tr title="${esc(n.ghi_chu)}">
        <td>${esc(n.ten)}<span class="region">${esc(n.vung)} · ${esc(n.noi_mua)} · tin cậy ${esc(n.tin_cay)}</span></td>
        ${n.thang.map((v, i) => `<td class="m"><span class="v${v} ${i + 1 === m ? "cur" : ""}"></span></td>`).join("")}
      </tr>`).join("")}</tbody>
    </table></div>`;
  $app.querySelectorAll("[data-r]").forEach((b) => (b.onclick = () => { calRegion = b.dataset.r; pageCalendar(); }));
}

// Nhóm theo vai trong mâm (tab mon_nhan); món chưa có nhãn thì theo loại.
function groupOf(d) {
  const v = S.nhan[d.ma_mon]?.vai_mam;
  return v ? LABEL.vai_mam[v] ?? v : LABEL.loai[d.loai] ?? d.loai;
}

function pageAll() {
  $app.innerHTML = `<h1>Tất cả món (${S.ranked.length})</h1>
    <input id="q" class="search" type="search" placeholder="Tìm món (gõ không dấu được, vd: ca thu, canh chua)" value="${esc(S.query)}">
    <div id="all-list"></div>`;
  const q = document.getElementById("q");
  q.oninput = () => { S.query = q.value; renderAll(); };
  renderAll();
}

function renderAll() {
  const words = plain(S.query).split(/\s+/).filter(Boolean);
  const list = S.ranked.filter((d) => words.every((w) => plain(d.ten_mon).includes(w)));
  const order = Object.values(LABEL.vai_mam);
  const groups = {};
  for (const d of list) (groups[groupOf(d)] ??= []).push(d);
  const keys = Object.keys(groups).sort((a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99));
  document.getElementById("all-list").innerHTML = (words.length ? `<p class="note">${list.length} món khớp</p>` : "") +
    (keys.map((g) => `
      <h2>${esc(g)} <span class="muted" style="font-size:14px;font-weight:400">(${groups[g].length})</span></h2>
      <div class="card list">${groups[g].map((d) => `
        <a href="#/mon/${d.ma_mon}"><span>${esc(d.ten_mon)} ${d.season === 2 ? '<span class="chip peak">Đang rộ</span>' : d.season === 0 ? '<span class="chip">Trái mùa</span>' : ""}${hasRecipe(d) ? "" : ' <span class="muted" title="Công thức trên Cookpad">↗</span>'}</span>
        <span class="score ${d.score < 0 ? "neg" : ""}">${d.score > 0 ? "+" : ""}${d.score}</span></a>`).join("")}</div>`).join("") ||
      `<p class="muted">Không thấy món nào.</p>`);
}

// ---------- Điều hướng ----------
function route() {
  const h = location.hash.slice(1) || "/";
  const [, page, arg] = h.split("/");
  document.querySelectorAll("[data-nav]").forEach((a) =>
    a.classList.toggle("on", a.dataset.nav === (page === "lich" ? "lich" : page === "ngay-mai" ? "ngay-mai" : page === "mon" && !arg ? "mon" : !page ? "home" : "")));
  if (page === "lich") pageCalendar();
  else if (page === "ngay-mai") pageHome(1);
  else if (page === "mon" && arg) pageRecipe(decodeURIComponent(arg));
  else if (page === "mon") pageAll();
  else pageHome();
  window.scrollTo(0, 0);
}

load().then(() => { window.addEventListener("hashchange", route); route(); })
  .catch((e) => { $app.innerHTML = `<div class="card">Lỗi tải dữ liệu: ${esc(e.message)}</div>`; });
