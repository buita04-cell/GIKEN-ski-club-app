
const CACHE_NAME = "giken-pwa-v2";

const APP_FILES = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(APP_FILES);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) =>
            key.startsWith("giken-pwa-") &&
            key !== CACHE_NAME
          )
          .map((key) => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  const url = new URL(event.request.url);

  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(event.request).then(async (cached) => {
      if (cached) return cached;

      try {
        return await fetch(event.request);
      } catch (error) {
        console.warn("Network request failed:", url.pathname);

        if (event.request.mode === "navigate") {
          const fallback = await caches.match("./index.html");
          if (fallback) return fallback;
        }

        return new Response("Resource unavailable", {
          status: 503,
          statusText: "Service Unavailable",
          headers: {
            "Content-Type": "text/plain; charset=utf-8"
          }
        });
      }
    })
  );
});
