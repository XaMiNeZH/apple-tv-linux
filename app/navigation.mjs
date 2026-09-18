const ALLOWED_HOSTS = new Set([
  "tv.apple.com",
  "www.apple.com",
  "apple.com",
  "account.apple.com",
  "idmsa.apple.com",
  "gsa.apple.com",
  "secure.store.apple.com",
  "buy.tv.apple.com",
  "play-edge.itunes.apple.com",
  "uts-api.itunes.apple.com",
  "amp-api.music.apple.com",
]);

const ALLOWED_SUFFIXES = [
  ".apple.com",
  ".cdn-apple.com",
  ".mzstatic.com",
  ".icloud.com",
];

export function isAppleUrl(urlString) {
  try {
    const url = new URL(urlString);
    if (url.protocol !== "https:") {
      return false;
    }
    return (
      ALLOWED_HOSTS.has(url.hostname) ||
      ALLOWED_SUFFIXES.some((suffix) => url.hostname.endsWith(suffix))
    );
  } catch {
    return false;
  }
}

export function isExternalWebUrl(urlString) {
  try {
    const { protocol } = new URL(urlString);
    return protocol === "https:" || protocol === "http:";
  } catch {
    return false;
  }
}
