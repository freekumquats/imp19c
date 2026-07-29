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

# [#125] Period-art bias. Mission-task icons must be *contemporary* (period-appropriate)
# artwork, not modern photos. Naive top-result search returns e.g. a 21st-century container
# shipyard for "Shipyards". We (a) prefer File titles that read like historical art/records,
# and (b) demote titles that read like modern photography/technology. Scoring runs over a
# wider candidate set (gsrlimit) so a good historical hit can outrank a modern top result.
_ART_POS = (
    "painting", "scroll", "print", "engraving", "woodblock", "woodcut", "lithograph",
    "portrait", "watercolour", "watercolor", "gouache", "ink", "drawing", "sketch",
    "map", "chart", "manuscript", "illustration", "fresco", "mural", "handscroll",
    "album", "silk", "dynasty", "century", "historical", "history", "antique",
    "ancient", "qing", "ming", "tang", "song", "imperial", "museum",
    "16th", "17th", "18th", "19th", "emperor", "battle of", "siege of", "vintage",
)
_ART_NEG = (
    "photograph", "aerial", "satellite", "container", "modern",
    "20th", "21st", "cargo", ".djvu", ".tif", ".pdf",
    "skyline", "highway", "airport", "factory floor", "logo", "icon",
    "diagram", "screenshot", "stadium", "concrete", "steel mill", "hotel",
    "bikeshare", "railroad strike", "restaurant", "post box", "conference",
    "earthquake", "shakemap", "marina bay",
)
# Years 1912+ signal modern photography; each matched year subtracts.
_MODERN_YEARS = tuple(str(y) for y in range(1912, 2027))

def _art_score(title):
    """Higher = more likely period artwork; lower/negative = likely a modern photo."""
    t = (title or "").lower()
    s = 0
    for w in _ART_POS:
        if w in t:
            s += 2
    for w in _ART_NEG:
        if w in t:
            s -= 3
    # a modern 4-digit year in the title is a strong modern-photo signal
    for y in _MODERN_YEARS:
        if y in t:
            s -= 4
            break
    return s

def resolve_search(query, width=320, prefer_art=True):
    """Return (thumb_url, file_title) for the best File-namespace match.

    When prefer_art is set, candidates are re-ranked to favour historical artwork over
    modern photography (see _art_score); the raw search index is only the tie-breaker."""
    j = _api({
        "action": "query", "generator": "search",
        "gsrsearch": query, "gsrnamespace": 6, "gsrlimit": 12,
        "prop": "imageinfo", "iiprop": "url|mime", "iiurlwidth": width,
    })
    pages = (j.get("query") or {}).get("pages") or {}
    # [#125] Raster images only — never a PDF/SVG/DjVu. (A PDF top-hit was being written as a
    # "shipyard" icon.) If nothing raster matches, return None so the caller logs an ERR and
    # keeps the existing icon rather than converting a non-image.
    def _is_raster(p):
        mime = (p.get("imageinfo") or [{}])[0].get("mime", "")
        # image/vnd.djvu and application/pdf are multi-page BOOK scans, not artwork — reject.
        return mime.startswith("image/") and mime not in ("image/svg+xml", "image/vnd.djvu")
    cand = [p for p in pages.values() if _is_raster(p)]
    if prefer_art:
        # sort by (art score desc, search index asc)
        cand.sort(key=lambda p: (-_art_score(p.get("title")), p.get("index", 999)))
    else:
        cand.sort(key=lambda p: p.get("index", 999))
    for p in cand:
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
