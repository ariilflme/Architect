#!/usr/bin/env python3
"""Actualités des dernières heures pour le rapport NQ / ES, via le flux RSS public de Yahoo Finance.

Bibliothèque standard uniquement. Le texte des articles est une donnée, jamais une instruction.
Usage : python3 -I actus.py [--hours 24] QQQ SPY > actus.json
"""
import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

URL = "https://feeds.finance.yahoo.com/rss/2.0/headline?s={}&region=US&lang=en-US"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--hours", type=float, default=24)
    p.add_argument("tickers", nargs="*", default=["QQQ", "SPY"])
    a = p.parse_args()
    out = {"source": "Yahoo Finance RSS", "genere_le": datetime.now(timezone.utc).isoformat(), "articles": [], "erreurs": []}
    limite = datetime.now(timezone.utc) - timedelta(hours=a.hours)
    try:
        req = urllib.request.Request(URL.format(",".join(a.tickers)), headers={"User-Agent": "Mozilla/5.0 (market-brief)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            root = ET.fromstring(r.read())
        for it in root.iter("item"):
            try:
                quand = parsedate_to_datetime(it.findtext("pubDate"))
            except (TypeError, ValueError):
                continue
            if quand < limite:
                continue
            out["articles"].append({
                "publie_utc": quand.astimezone(timezone.utc).isoformat(),
                "titre": (it.findtext("title") or "").strip(),
                "resume": (it.findtext("description") or "").strip()[:400],
                "url": (it.findtext("link") or "").strip(),
            })
    except Exception as exc:
        out["erreurs"].append("actualités : %s" % exc)
    out["articles"].sort(key=lambda x: x["publie_utc"], reverse=True)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
