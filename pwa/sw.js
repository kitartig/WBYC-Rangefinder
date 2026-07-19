/* WBYC Rangefinder service worker — offline-first app shell */
const VERSION = 'wbyc-v129';
const SHELL = ['./', './index.html', './manifest.webmanifest',
               './icon-192.png', './icon-512.png', './course_data_v2.json'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  // course data: stale-while-revalidate (instant offline, refreshes in background)
  if (url.pathname.endsWith('course_data_v2.json')) {
    e.respondWith(caches.open(VERSION).then(async c => {
      const cached = await c.match(e.request);
      const net = fetch(e.request).then(r => { if (r.ok) c.put(e.request, r.clone()); return r; })
                                  .catch(() => cached);
      return cached || net;
    }));
    return;
  }
  // everything else: cache-first, network fallback; navigations fall back to shell
  e.respondWith(caches.match(e.request).then(r =>
    r || fetch(e.request).then(resp => {
      if (resp.ok && e.request.method === 'GET') {
        const copy = resp.clone();
        caches.open(VERSION).then(c => c.put(e.request, copy));
      }
      return resp;
    }).catch(() =>
      e.request.mode === 'navigate' ? caches.match('./index.html') : Response.error())));
});
