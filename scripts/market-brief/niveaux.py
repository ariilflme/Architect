#!/usr/bin/env python3
"""Niveaux quotidiens pour le rapport NQ / ES : cours, RSI 14, MM20/MM50, plus haut/bas/clôture de la veille.

Bibliothèque standard uniquement. Source : Yahoo Finance (gratuit, non officiel, peut être en retard).
Usage : python3 -I niveaux.py NQ=F ES=F > marche.json
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone

NOMS = {"NQ=F": "Nasdaq-100 (E-mini)", "ES=F": "S&P 500 (E-mini)"}
URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}?range=6mo&interval=1d"


def rsi(closes, n=14):
    """RSI de Wilder (lissage exponentiel), la méthode standard."""
    if len(closes) <= n:
        return None
    d = [b - a for a, b in zip(closes, closes[1:])]
    gain = sum(max(x, 0) for x in d[:n]) / n
    perte = sum(max(-x, 0) for x in d[:n]) / n
    for x in d[n:]:
        gain = (gain * (n - 1) + max(x, 0)) / n
        perte = (perte * (n - 1) + max(-x, 0)) / n
    if perte == 0:
        return 100.0
    return round(100 - 100 / (1 + gain / perte), 1)


def mm(closes, n):
    return round(sum(closes[-n:]) / n, 2) if len(closes) >= n else None


def instrument(sym):
    req = urllib.request.Request(URL.format(sym), headers={"User-Agent": "Mozilla/5.0 (market-brief)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)["chart"]["result"][0]
    meta, q = res["meta"], res["indicators"]["quote"][0]
    rows = [(t, h, l, c) for t, h, l, c in zip(res["timestamp"], q["high"], q["low"], q["close"]) if c is not None]
    closes = [c for _, _, _, c in rows]
    dernier = meta.get("regularMarketPrice") or closes[-1]
    # La dernière barre est la séance en cours ; la veille est l'avant-dernière.
    _, hv, bv, cv = rows[-2]
    m20, m50 = mm(closes, 20), mm(closes, 50)
    return {
        "symbole": sym,
        "nom": NOMS.get(sym, sym),
        "dernier": round(dernier, 2),
        "heure": datetime.fromtimestamp(meta["regularMarketTime"], timezone.utc).isoformat(),
        "variation_pct": round((dernier / cv - 1) * 100, 2),
        "rsi14": rsi(closes),
        "mm20": m20,
        "mm50": m50,
        "vs_mm20": None if m20 is None else ("au-dessus" if dernier > m20 else "en dessous"),
        "vs_mm50": None if m50 is None else ("au-dessus" if dernier > m50 else "en dessous"),
        "haut_veille": round(hv, 2),
        "bas_veille": round(bv, 2),
        "cloture_veille": round(cv, 2),
    }


def main(syms):
    out = {"source": "Yahoo Finance", "genere_le": datetime.now(timezone.utc).isoformat(), "instruments": [], "erreurs": []}
    for s in syms:
        try:
            out["instruments"].append(instrument(s))
        except Exception as exc:  # une source en panne ne doit pas bloquer le rapport
            out["erreurs"].append("%s : %s" % (s, exc))
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main(sys.argv[1:] or ["NQ=F", "ES=F"])
