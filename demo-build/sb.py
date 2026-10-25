"""Shared Storyblok Management API helpers (no secrets in this file).
Token is read from env STORYBLOK_MANAGEMENT_TOKEN or darwin/storyblok.env."""
import json, os, time, urllib.request, urllib.error

SPACE_ID = 296113342540964
BASE = f"https://mapi.storyblok.com/v1/spaces/{SPACE_ID}"


def _token():
    t = os.environ.get("STORYBLOK_MANAGEMENT_TOKEN")
    if not t:
        p = os.environ.get("DARWIN_ENV", "/Users/walid.elmselmi/dev/darwin/storyblok.env")
        for l in open(p):
            if l.startswith("STORYBLOK_MANAGEMENT_TOKEN="):
                t = l.split("=", 1)[1].strip().strip("\"'")
    return t


TOKEN = _token()
_last = [0.0]


def api(method, path, body=None, full=False, retries=5):
    url = path if path.startswith("http") else f"{BASE}/{path}"
    data = json.dumps(body).encode() if body is not None else None
    for i in range(retries):
        # stay under 3 req/s
        wait = 0.36 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        req = urllib.request.Request(url, data=data, method=method,
                                     headers={"Authorization": TOKEN, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as r:
                raw = r.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            msg = e.read().decode()
            if e.code == 429:
                time.sleep(1.5 * (i + 1))
                continue
            raise RuntimeError(f"{method} {path} -> {e.code}: {msg[:600]}")
    raise RuntimeError(f"{method} {path}: too many retries")


def list_all(path, key, per_page=100, extra=""):
    out, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        d = api("GET", f"{path}{sep}per_page={per_page}&page={page}{extra}")
        items = d.get(key, [])
        out += items
        if len(items) < per_page:
            return out
        page += 1
