// Cá Chef – đồng bộ dữ liệu dùng chung trong nhà (tủ lạnh, đánh giá, bữa đã chọn, lịch sử, đi chợ) giữa các máy,
// qua Apps Script gắn với Google Sheet (scripts/apps_script/dong_bo.gs). Chưa cài thì app chạy như cũ, chỉ lưu trên máy.
//
// Mỗi khóa localStorage là một object; đồng bộ theo từng mục cấp 1 ("tulanh/rau_muong", "bua/2026-10-08"...):
// mục nào sửa sau cùng (theo giờ máy sửa) thì thắng; xóa mục ghi null. Lịch sử gợi ý thì gộp (hợp các món), không đè.
const DB_KEY = "cachef.dong_bo"; // { url, nha, since, t: { "tên/mục": giờ sửa }, cho: { "tên/mục": 1 chờ gửi } }
const DB_TEN = { "cachef.tulanh": "tulanh", "cachef.danh_gia": "danh_gia", "cachef.chon": "chon", "cachef.bua": "bua",
  "cachef.history": "lich_su", "cachef.di_cho": "di_cho" };
const DB_LS = Object.fromEntries(Object.entries(DB_TEN).map(([k, v]) => [v, k]));
const DB = { cfg: null, hen: null, dang: false, loi: "", luc: 0, onDoi: null };

function dbCfg() {
  if (!DB.cfg) {
    let v = null;
    try { v = JSON.parse(localStorage.getItem(DB_KEY) || "null"); } catch { /* chặn lưu */ }
    DB.cfg = { url: "", nha: "", since: 0, t: {}, cho: {}, ...(v || {}) };
  }
  return DB.cfg;
}
function dbLuu() { try { localStorage.setItem(DB_KEY, JSON.stringify(dbCfg())); } catch { /* chặn lưu */ } }
const dbBat = () => !!(dbCfg().url && dbCfg().nha);
function docLS(k) { try { const v = JSON.parse(localStorage.getItem(k) || "{}"); return v && typeof v === "object" && !Array.isArray(v) ? v : {}; } catch { return {}; } }

// Ghi một khóa dùng chung: lưu máy, đánh dấu các mục đổi để gửi đi. Trình duyệt chặn lưu thì ném lỗi như setItem.
function ghiLS(k, obj) {
  const ten = DB_TEN[k], cu = ten && dbBat() ? docLS(k) : null;
  localStorage.setItem(k, JSON.stringify(obj));
  if (!cu) return;
  const cfg = dbCfg(), now = Date.now();
  for (const muc of new Set([...Object.keys(cu), ...Object.keys(obj)])) {
    if (JSON.stringify(cu[muc]) === JSON.stringify(obj[muc])) continue;
    cfg.t[`${ten}/${muc}`] = now;
    cfg.cho[`${ten}/${muc}`] = 1;
  }
  dbLuu();
  clearTimeout(DB.hen);
  DB.hen = setTimeout(dbGui, 1200);
}

async function dbGui() {
  const cfg = dbCfg(), ds = Object.keys(cfg.cho);
  if (!dbBat() || !ds.length) return true;
  const entries = ds.map((p) => {
    const [ten, ...r] = p.split("/"), v = docLS(DB_LS[ten])[r.join("/")];
    return { k: p, v: v === undefined ? null : v, t: cfg.t[p] || 1 };
  });
  try {
    // text/plain để không bị chặn CORS (Apps Script không trả lời preflight).
    const body = JSON.stringify({ nha: cfg.nha, entries });
    const res = await fetch(cfg.url, { method: "POST", body, keepalive: body.length < 60000 }).then((r) => r.json()); // keepalive tối đa 64 KB
    if (res.loi) throw new Error(res.loi);
    for (const e of entries) if (cfg.t[e.k] === e.t) delete cfg.cho[e.k];
    dbLuu(); DB.loi = ""; DB.luc = Date.now();
    return true;
  } catch (e) { DB.loi = "Chưa gửi được: " + e.message; return false; }
}

// Lấy các mục máy khác đã sửa; trả về true nếu dữ liệu trên máy có thay đổi.
async function dbKeo() {
  const cfg = dbCfg();
  if (!dbBat()) return false;
  try {
    const u = `${cfg.url}${cfg.url.includes("?") ? "&" : "?"}nha=${encodeURIComponent(cfg.nha)}&since=${cfg.since || 0}`;
    const res = await fetch(u).then((r) => r.json());
    if (res.loi) throw new Error(res.loi);
    const doi = new Map(); // khóa localStorage -> object đã sửa
    for (const e of res.entries || []) {
      const [ten, ...r] = String(e.k).split("/"), ls = DB_LS[ten], muc = r.join("/");
      if (!ls || !muc) continue;
      const obj = doi.get(ls) || docLS(ls);
      if (ten === "lich_su" && e.v !== null) {
        // Lịch sử gợi ý: gộp món của cả hai máy trong ngày.
        const hop = [...new Set([...(obj[muc] || []), ...(e.v || [])])];
        if (hop.length !== (obj[muc] || []).length) { obj[muc] = hop; doi.set(ls, obj); }
        if (hop.length !== (e.v || []).length) { cfg.t[e.k] = Math.max(Date.now(), e.t + 1); cfg.cho[e.k] = 1; }
        continue;
      }
      if (!(e.t > (cfg.t[e.k] || 0))) continue;
      if (e.v === null) delete obj[muc]; else obj[muc] = e.v;
      cfg.t[e.k] = e.t; delete cfg.cho[e.k];
      doi.set(ls, obj);
    }
    for (const [ls, obj] of doi) localStorage.setItem(ls, JSON.stringify(obj));
    cfg.since = Math.max(0, (res.now || 0) - 5000); // lùi 5 giây phòng lệch lúc ghi
    dbLuu(); DB.loi = ""; DB.luc = Date.now();
    if (Object.keys(cfg.cho).length) dbGui();
    return doi.size > 0;
  } catch (e) { DB.loi = "Chưa lấy được: " + e.message; return false; }
}

// Bật đồng bộ: dữ liệu đang có trên máy coi như cũ (giờ sửa = 1) – trên Sheet có bản mới hơn thì lấy bản trên Sheet,
// mục Sheet chưa có thì gửi lên.
async function dbBatDau(url, nha) {
  const cfg = dbCfg();
  Object.assign(cfg, { url: url.trim(), nha: nha.trim(), since: 0 });
  for (const [ls, ten] of Object.entries(DB_TEN))
    for (const muc of Object.keys(docLS(ls))) { const p = `${ten}/${muc}`; cfg.t[p] = cfg.t[p] || 1; cfg.cho[p] = 1; }
  dbLuu();
  const doi = await dbKeo();
  const ok = await dbGui();
  return { doi, ok: ok && !DB.loi };
}
function dbTat() { Object.assign(dbCfg(), { url: "", nha: "", since: 0, t: {}, cho: {} }); dbLuu(); }

// Tự lấy dữ liệu mới: khi mở lại app và mỗi 45 giây lúc đang xem.
function dbTuDong() {
  const keo = async () => { if (dbBat() && !DB.dang && document.visibilityState === "visible") { DB.dang = true; const d = await dbKeo(); DB.dang = false; if (d && DB.onDoi) DB.onDoi(); } };
  setInterval(keo, 45000);
  document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible") keo(); else dbGui(); });
}
