// Cá Chef – demo: thời tiết Phan Rang + mùa vụ -> 3 món gợi ý (hôm nay và ngày mai).
const LAT = 11.56, LON = 108.99;
const WEATHER_URL = `https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}` +
  "&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m" +
  "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum," +
  "precipitation_probability_max,wind_speed_10m_max,uv_index_max" +
  "&timezone=Asia%2FHo_Chi_Minh&forecast_days=2";
const HISTORY_KEY = "cachef.history";

const LABEL = {
  loai: { mon_chinh: "Món chính", canh: "Canh", goi: "Gỏi", lau: "Lẩu", an_vat: "Ăn vặt", trang_mieng: "Tráng miệng", do_uong: "Đồ uống" },
  nhiet: { mat: "Mát", am: "Ấm", nong: "Nóng" },
  do_nang: { nhe: "Nhẹ bụng", nang: "No lâu" },
  dau_mo: { it: "Ít dầu", vua: "Dầu vừa", nhieu: "Nhiều dầu" },
  do_kho: { de: "Dễ", vua: "Vừa", kho: "Khó" },
};

const S = { data: null, weather: null, ing: {}, prices: {}, ingByDish: {}, ranked: [], rankedTomorrow: [], offset: [0, 0], servings: {} };
const $app = document.getElementById("app");
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
  S.ranked = rankDishes(0);
  recordHistory(S.ranked.slice(0, 3).map((d) => d.ma_mon));
  S.rankedTomorrow = rankDishes(1); // sau recordHistory để không gợi ý lại món của hôm nay
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
function daysSinceSuggested(ma, ref = today()) {
  let hist = {};
  try { hist = JSON.parse(localStorage.getItem(HISTORY_KEY) || "{}"); } catch {}
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
    hist[today()] = list;
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

// 3 món điểm cao nhất, không trùng loại (bắt đầu từ vị trí offset khi bấm "Đổi món").
function pickThree(ranked, offset) {
  const pool = ranked.slice(offset).concat(ranked.slice(0, offset)).filter((d) => d.score > -3);
  const out = [], used = new Set();
  for (const d of pool) {
    if (used.has(d.loai)) continue;
    out.push(d);
    used.add(d.loai);
    if (out.length === 3) break;
  }
  return out;
}

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
  const top = pickThree(S.rankedTomorrow, 0).map((x) => x.ten_mon).join(", ");
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
function thawList(picks) {
  const out = [];
  for (const d of picks) {
    for (const r of S.ingByDish[d.ma_mon] || []) {
      if (r.vai_tro === "gia_vi") continue;
      const codes = String(r.ma_nguyen_lieu || "").split("|").filter(Boolean);
      const frozen = codes.length
        ? codes.some((c) => FROZEN_GROUPS.includes(S.ing[c]?.nhom) && !NOT_FROZEN.includes(c))
        : FROZEN_WORDS.test(r.ten_hien_thi);
      if (frozen) out.push({ ten: r.ten_hien_thi, mon: d.ten_mon, qty: scaleQty(r, 1) });
    }
  }
  return out;
}

function thawCard(picks) {
  const list = thawList(picks);
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
    <span class="chip">${LABEL.do_nang[d.do_nang] ?? ""}</span>
    <span class="chip">${LABEL.dau_mo[d.dau_mo] ?? ""}</span>
    <span class="chip">⏱ ${d.thoi_gian_phut}′</span></div>`;
}

function pageHome(day = 0) {
  const ranked = day ? S.rankedTomorrow : S.ranked;
  const picks = pickThree(ranked, S.offset[day]);
  const m = month(day);
  const inSeason = S.data.nguyen_lieu.filter((n) => n.thang[m - 1] === 2);
  const shown = new Set(picks.map((p) => p.ma_mon));
  const others = ranked.filter((d) => !shown.has(d.ma_mon)).slice(0, 8);
  $app.innerHTML = `
    ${weatherCard(day)}
    ${day ? "" : tomorrowTeaser()}
    <div class="row"><h2>${day ? "Ngày mai nấu gì?" : "Hôm nay nấu gì?"}</h2><button class="btn" id="swap">🔄 Đổi món khác</button></div>
    <div class="picks">${picks.map((d, i) => `
      <a class="card pick" href="#/mon/${d.ma_mon}">
        <span class="rank">Gợi ý ${i + 1}</span>
        <h3>${esc(d.ten_mon)}</h3>
        <p>${esc(d.mo_ta_ngan)}</p>
        ${chips(d)}
        <span class="why">✓ ${esc(d.reasons.filter((r) => r.diem > 0).map((r) => r.text).join(" · ") || "Hợp mùa")}</span>
      </a>`).join("")}</div>
    ${day ? thawCard(picks) : ""}
    <h2>Đang vào mùa tháng ${m}</h2>
    <div class="chips">${inSeason.map((n) => `<span class="chip peak">${esc(n.ten)}</span>`).join("") || '<span class="muted">Chưa có dữ liệu</span>'}</div>
    <h2>Món khác cũng hợp</h2>
    <div class="card list">${others.map((d) => `
      <a href="#/mon/${d.ma_mon}"><span>${esc(d.ten_mon)} <span class="muted">· ${LABEL.loai[d.loai] ?? ""}</span></span>
      <span class="score ${d.score < 0 ? "neg" : ""}">${d.score > 0 ? "+" : ""}${d.score} điểm</span></a>`).join("")}</div>`;
  document.getElementById("swap").onclick = () => {
    S.offset[day] = (S.offset[day] + 3) % Math.max(ranked.length, 1);
    if (S.offset[day] >= 12) S.offset[day] = 0; // chỉ xoay trong nhóm điểm cao
    pageHome(day);
  };
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
    .filter((r) => r.ma_nguyen_lieu && !seen.has(r.ma_nguyen_lieu) && seen.add(r.ma_nguyen_lieu))
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
      <p>${esc(d.mo_ta_ngan)}</p>
      ${chips(d)}
      <p class="note">Độ khó: ${LABEL.do_kho[d.do_kho] ?? d.do_kho} · Điểm hôm nay: ${d.score}
        ${d.reasons.length ? `(${d.reasons.map((r) => `${esc(r.text)} ${r.diem > 0 ? "+" : ""}${r.diem}`).join(", ")})` : ""}</p>
      ${seasonBlock(d.ma_mon)}
    </div>
    <h2>Nguyên liệu</h2>
    <div class="servings">
      <button id="minus" aria-label="Bớt">−</button><b>${n}</b><span>${unitName}</span><button id="plus" aria-label="Thêm">+</button>
    </div>
    <ul class="card ing">${rows.map((r) => {
      const price = S.prices[String(r.ma_nguyen_lieu).split("|")[0]];
      return `<li><span class="${r.vai_tro === "chinh" ? "main" : ""}">${esc(r.ten_hien_thi)}
        ${price ? `<a class="go" href="${esc(price.url)}" target="_blank" rel="noopener">GO!: ${esc(price.san_pham_go)} – ${Number(price.gia_vnd).toLocaleString("vi-VN")}đ</a>` : ""}</span>
        <span class="qty">${esc(scaleQty(r, factor))}</span></li>`;
    }).join("")}</ul>
    <p class="note">Gia vị và nước dùng tăng chậm hơn số người – nêm lại cho vừa.</p>
    <h2>Cách làm</h2>
    <ol class="card steps">${String(d.cach_lam).split("\n").map((s) => `<li>${esc(s.replace(/^\d+\.\s*/, ""))}</li>`).join("")}</ol>
    <p class="note">Tham khảo: <a href="${esc(d.nguon)}" target="_blank" rel="noopener">Cookpad</a> ·
      Trạng thái: ${d.trang_thai === "da_nau_thu" ? "đã nấu thử" : "chưa nấu thử"}</p>`;
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

function pageAll() {
  const groups = {};
  for (const d of S.ranked) (groups[d.loai] ??= []).push(d);
  $app.innerHTML = `<h1>Tất cả món (${S.ranked.length})</h1>` +
    Object.entries(groups).map(([loai, list]) => `
      <h2>${LABEL.loai[loai] ?? loai}</h2>
      <div class="card list">${list.map((d) => `
        <a href="#/mon/${d.ma_mon}"><span>${esc(d.ten_mon)} ${d.season === 2 ? '<span class="chip peak">Đang rộ</span>' : d.season === 0 ? '<span class="chip">Trái mùa</span>' : ""}</span>
        <span class="score ${d.score < 0 ? "neg" : ""}">${d.score > 0 ? "+" : ""}${d.score}</span></a>`).join("")}</div>`).join("");
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
