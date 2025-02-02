
var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
'/offline',
'/css/django-pwa-app.css',
'/static/images/nk-72x72.png',
'/static/images/nk-96x96.png',
'/static/images/nk-128x128.png',
'/static/images/nk-144x144.png',
'/static/images/nk-152x152.png',
'/static/images/nk-192x192.png',
'/static/images/nk-384x384.png',
'/static/images/nk-512x512.png',
'/static/images/nk-640x1136.png',
'/static/images/nk-750x1334.png',
'/static/images/nk-1242x2208.png',
'/static/images/nk-1125x2436.png',
'/static/images/nk-828x1792.png',
'/static/images/nk-1242x2688.png',
'/static/images/nk-1536x2048.png',
'/static/images/nk-1668x2224.png',
'/static/images/nk-1668x2388.png',
'/static/images/nk-2048x2732.png'
];

// Cache on install
self.addEventListener("install", event => {
this.skipWaiting();
event.waitUntil(
    caches.open(staticCacheName)
        .then(cache => {
            return cache.addAll(filesToCache);
        })
)
});

// Clear cache on activate
self.addEventListener('activate', event => {
event.waitUntil(
    caches.keys().then(cacheNames => {
        return Promise.all(
            cacheNames
                .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                .filter(cacheName => (cacheName !== staticCacheName))
                .map(cacheName => caches.delete(cacheName))
        );
    })
);
});

// Serve from Cache
self.addEventListener("fetch", event => {
event.respondWith(
    caches.match(event.request)
        .then(response => {
            return response || fetch(event.request);
        })
        .catch(() => {
            return caches.match('offline');
        })
)
});
