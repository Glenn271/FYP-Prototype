importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');
console.log('Hello from serviceworker.js');

self.addEventListener('message', (event) => {
    if(event.data && event.data.type === 'SKIP_WAITING'){
        console.log("Invoked skipWaiting");
        self.skipWaiting();
    }
})

if(workbox){
    console.log("Workbox loaded");
} else{
    console.log("Workbox didn't load");
}

//workbox
const{strategies} = workbox;
const{routing} = workbox;
const{precaching} = workbox;
const{core} = workbox;
const cacheable_response = workbox.cacheableResponse;
const expiration = workbox.expiration;

//default
core.setCacheNameDetails({
    prefix: 'awm2021',
    suffix: 'v1',
    precache: 'precache',
    runtime: 'runtime',
    googleAnalytics: 'analytics'
});

routing.registerRoute(
    ({url}) => url.origin === 'https://fonts.googleapis.com',
    new strategies.StaleWhileRevalidate({
        cacheName: 'google-fonts',
    })
);


// Cache CSS and javaScript assets with a stale-while-revalidate strategy.
routing.registerRoute(
    ({request}) => request.destination === 'script' ||
        request.destination === 'style',
    new strategies.StaleWhileRevalidate({
        cacheName: 'static-resources',
    })
);

// Cache image files with a cache-first strategy for 30 days.
routing.registerRoute(
    ({request}) => request.destination === 'image',
    new strategies.CacheFirst({
        cacheName: 'images',
        plugins: [
            new expiration.ExpirationPlugin({
                maxEntries: 60,
                maxAgeSeconds: 30 * 24 * 60 * 60,
            }),
        ],
    })
);



