#!/usr/bin/env python3
"""
fetch_wm.py — resolve a Wikimedia Commons image to a local raster for icon conversion.

Two modes:
  - direct : a full upload.wikimedia.org/... URL (used as-is)
  - search : a free-text query; queries the Commons API in the File namespace,
             takes the top image result, and downloads a scaled thumbnail.

Thumbnails (iiurlwidth) keep downloads small and are plenty for a 50px icon.
"""
import sys, json, urllib.parse, urllib.request, urllib.error, os, hashlib, time

UA = "imp19c-icon-tool/1.0 (non-commercial mod placeholder art)"
API = "https://commons.wikimedia.org/w/api.php"

# Commons asks anonymous clients to stay gentle. Serialize + throttle every request,
# and back off on HTTP 429 rather than hammering.
_MIN_INTERVAL = 1.1   # seconds between requests
_last = [0.0]

def _throttle():
    import time as _t
    dt = _t.monotonic() - _last[0]
    if dt < _MIN_INTERVAL:
        _t.sleep(_MIN_INTERVAL - dt)
    _last[0] = _t.monotonic()

def _get(url, retries=5):
    import time as _t
    delay = 3.0
    for attempt in range(retries):
        _throttle()
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                ra = e.headers.get("Retry-After")
                wait = float(ra) if (ra and ra.isdigit()) else delay
                _t.sleep(wait)
                delay = min(delay * 2, 60)
                continue
            raise
    raise RuntimeError("unreachable")

def _api(params):
    params = dict(params); params["format"] = "json"
    url = API + "?" + urllib.parse.urlencode(params)
    return json.loads(_get(url).decode("utf-8"))

def resolve_search(query, width=320):
    """Return (thumb_url, file_title) for the best File-namespace match."""
    j = _api({
        "action": "query", "generator": "search",
        "gsrsearch": query, "gsrnamespace": 6, "gsrlimit": 5,
        "prop": "imageinfo", "iiprop": "url|mime", "iiurlwidth": width,
    })
    pages = (j.get("query") or {}).get("pages") or {}
    # rank by search index order
    best = sorted(pages.values(), key=lambda p: p.get("index", 999))
    for p in best:
        ii = (p.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        if mime.startswith("image/") and mime not in ("image/svg+xml",):
            return ii.get("thumburl") or ii.get("url"), p.get("title")
    # fall back to first with any url
    for p in best:
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("thumburl") or ii.get("url"):
            return ii.get("thumburl") or ii.get("url"), p.get("title")
    return None, None

def download(url, dest):
    data = _get(url)
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)

def fetch(spec, dest, width=320):
    """spec = ('direct', url) or ('search', query). Returns (path, source_desc)."""
    kind, val = spec
    if kind == "direct":
        n = download(val, dest)
        return dest, f"direct:{val} ({n}B)"
    elif kind == "search":
        url, title = resolve_search(val, width=width)
        if not url:
            raise RuntimeError(f"no image found for query: {val}")
        n = download(url, dest)
        return dest, f"search:'{val}' -> {title} ({n}B)"
    raise ValueError(kind)

if __name__ == "__main__":
    # smoke test
    kind = sys.argv[1]; val = sys.argv[2]; dest = sys.argv[3]
    p, desc = fetch((kind, val), dest)
    print(desc)
