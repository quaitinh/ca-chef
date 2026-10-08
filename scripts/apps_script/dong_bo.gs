// Cá Chef – đồng bộ dữ liệu giữa các máy trong nhà (tủ lạnh, đánh giá món, bữa đã chọn, lịch sử, đi chợ).
// Cài: mở Google Sheet "Cá Chef" > Tiện ích mở rộng > Apps Script, dán file này, Triển khai > Tùy chọn triển khai mới >
// Ứng dụng web, "Thực thi với tư cách: Tôi", "Người có quyền truy cập: Bất kỳ ai". Chép URL ứng dụng web vào app (Đồng bộ).
// Dữ liệu nằm ở tab "dong_bo": mỗi dòng một mục (nha, k, v JSON, t giờ máy sửa, s giờ Sheet nhận).
// Ai có cả URL lẫn mã nhà mới đọc/ghi được dữ liệu của nhà đó.
var TAB = "dong_bo";

function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet(), sh = ss.getSheetByName(TAB);
  if (!sh) { sh = ss.insertSheet(TAB); sh.appendRow(["nha", "k", "v", "t", "s"]); }
  return sh;
}
function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function nha_(x) { x = String(x || ""); if (!/^[A-Za-z0-9_-]{8,64}$/.test(x)) throw new Error("Mã nhà không hợp lệ"); return x; }

// GET ?nha=...&since=...: các mục Sheet nhận sau mốc since.
function doGet(e) {
  try {
    var nha = nha_(e.parameter.nha), since = Number(e.parameter.since || 0), now = Date.now();
    var rows = sheet_().getDataRange().getValues().slice(1), entries = [];
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i];
      if (String(r[0]) === nha && Number(r[4]) > since) entries.push({ k: String(r[1]), v: r[2] === "" ? null : JSON.parse(r[2]), t: Number(r[3]) });
    }
    return out_({ now: now, entries: entries });
  } catch (err) { return out_({ loi: String(err.message || err) }); }
}

// POST {nha, entries: [{k, v, t}]}: ghi mục mới hơn bản đang có (t lớn hơn); v null là đã xóa.
function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
    var body = JSON.parse(e.postData.contents), nha = nha_(body.nha), sh = sheet_(), now = Date.now();
    var rows = sh.getDataRange().getValues(), dong = {}, them = [], n = 0;
    for (var i = 1; i < rows.length; i++) if (String(rows[i][0]) === nha) dong[String(rows[i][1])] = i;
    (body.entries || []).slice(0, 2000).forEach(function (x) {
      var k = String(x.k || ""), t = Number(x.t) || 0, v = x.v === null || x.v === undefined ? "" : JSON.stringify(x.v);
      if (!k || v.length > 45000) return;
      var i = dong[k];
      if (i === undefined) { them.push([nha, k, v, t, now]); dong[k] = -1; n++; return; }
      if (i < 0 || t <= Number(rows[i][3])) return;
      sh.getRange(i + 1, 3, 1, 3).setValues([[v, t, now]]); n++;
    });
    if (them.length) sh.getRange(sh.getLastRow() + 1, 1, them.length, 5).setValues(them);
    return out_({ now: now, ok: n });
  } catch (err) { return out_({ loi: String(err.message || err) }); }
  finally { try { lock.releaseLock(); } catch (e2) {} }
}
