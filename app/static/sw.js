// Cá Chef – service worker: mở app khi sóng yếu / mất mạng.
// - data.json?v=<mã>: nội dung theo mã phiên bản không đổi -> lấy từ bộ nhớ trước, chỉ giữ bản mới nhất.
// - Các file khác cùng trang (app.js, style.css, version.json...): mạng trước (luôn bản mới), mất mạng thì dùng bản đã lưu.
// - Request khác trang (thời tiết, ảnh Cookpad, đồng bộ Apps Script): không can thiệp.
const CACHE = "cachef-v2";
const SHELL = ["./", "index.html", "app.js", "dong_bo.js", "style.css", "manifest.json", "icon-192.png", "icon-512.png", "apple-touch-icon.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener("fetch", (e) => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  if (url.pathname.endsWith("/data.json") && url.searchParams.has("v")) {
    e.respondWith(caches.open(CACHE).then(async (c) => {
      const co = await c.match(req);
      if (co) return co;
      const res = await fetch(req);
      if (res.ok) {
        for (const k of await c.keys()) if (new URL(k.url).pathname.endsWith("/data.json")) await c.delete(k);
        await c.put(req, res.clone());
      }
      return res;
    }));
    return;
  }
  if (url.searchParams.has("refresh")) return;
  e.respondWith(fetch(req).then((res) => {
    if (res.ok) {
      const ban = res.clone(), khoa = url.pathname.endsWith("/version.json") ? new Request(url.origin + url.pathname) : req;
      caches.open(CACHE).then((c) => c.put(khoa, ban));
    }
    return res;
  }).catch(async () => (await caches.match(url.pathname.endsWith("/version.json") ? url.origin + url.pathname : req, { ignoreSearch: url.pathname.endsWith("/data.json") })) ||
    (req.mode === "navigate" ? caches.match("index.html") : Response.error())));
});
