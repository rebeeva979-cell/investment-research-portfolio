"""Small cached HTTP helper for the ETHFI on-chain verification.

No third-party deps: urllib + json. Retries with backoff, caches raw bodies
under raw/ so the analysis is reproducible without re-hitting public APIs.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
os.makedirs(RAW, exist_ok=True)

UA = "investment-research-portfolio/1.0 (+local analysis; contact rebeeva979@gmail.com)"


def _cache_path(url: str) -> str:
    h = hashlib.sha256(url.encode()).hexdigest()[:16]
    safe = url.split("://", 1)[-1][:80].replace("/", "_").replace("?", "_")
    return os.path.join(RAW, f"{safe}_{h}.json")


def get_json(url: str, *, timeout: int = 25, retries: int = 3, refresh: bool = False):
    path = _cache_path(url)
    if os.path.exists(path) and not refresh:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.load(resp)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=1)
            return data
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed after {retries}: {url}: {last}")


def save_json(name: str, data) -> str:
    path = os.path.join(RAW, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    return path


def get_text(url: str, *, timeout: int = 25, retries: int = 2) -> str:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
            time.sleep(1.0 * (attempt + 1))
    raise RuntimeError(f"GET text failed: {url}: {last}")


def blockscout(path: str, **kw):
    return get_json("https://eth.blockscout.com/api/v2" + path, **kw)
