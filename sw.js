/* Kupati Service Worker — caches the app shell for offline/fast load */
const CACHE = "kupati-v1";
const SHELL = ["/", "/index.html", "/manifest.json"];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);

  // Never intercept Firebase / Google API calls
  if (
    url.hostname.includes("firebaseio.com") ||
    url.hostname.includes("googleapis.com") ||
    url.hostname.includes("firebaseapp.com") ||
    url.hostname.includes("gstatic.com") ||
    url.hostname.includes("fonts.gstatic.com") ||
    url.protocol === "chrome-extension:"
  ) return;

  // Network-first for navigation; cache-first for static assets
  if (e.request.mode === "navigate") {
    e.respondWith(
      fetch(e.request)
        .then(res => { caches.open(CACHE).then(c => c.put(e.request, res.clone())); return res; })
        .catch(() => caches.match("/index.html"))
    );
  } else {
    e.respondWith(
      caches.match(e.request).then(cached => cached || fetch(e.request))
    );
  }
});
