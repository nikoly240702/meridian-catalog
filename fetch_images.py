#!/usr/bin/env python3
"""Скачивает реальные фото оборудования с Wikimedia Commons по КАТЕГОРИЯМ.

Категории курируются вручную, поэтому релевантность выше, чем у полнотекстового
поиска. На каждый слот качаем несколько кандидатов (name-1.jpg, name-2.jpg, ...),
чтобы потом визуально выбрать лучший и переименовать в name.jpg.
"""
import json, os, subprocess, urllib.parse, sys

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
OUT = "assets/img"
CAND = "assets/img/_cand"
os.makedirs(CAND, exist_ok=True)

# слот -> список категорий Commons (пробуем по очереди, собираем кандидатов)
TARGETS = {
    "cat-equipment": ["Industrial machinery", "Machine tools"],
    "cat-electro":   ["Switchgear", "Electrical control panels"],
    "cat-tools":     ["Hand tools", "Power tools"],
    "cat-metal":     ["Steel pipes", "Rolled metal"],
    "cat-build":     ["Building materials", "Construction materials"],
    "cat-ppe":       ["Hard hats", "Personal protective equipment"],
    "cat-vent":      ["HVAC", "Ventilation ducts"],
    "cat-supply":    ["Warehouses", "Cardboard boxes"],
    "factory":       ["Factory interiors", "Industrial buildings interiors"],
    "warehouse":     ["Warehouse interiors", "Logistics centres"],
    "pump":          ["Centrifugal pumps", "Water pumps"],
    "compressor":    ["Air compressors", "Screw compressors"],
    "lathe":         ["Metalworking lathes", "Lathes"],
    "motor":         ["Electric motors", "Induction motors"],
    "gearbox":       ["Gearboxes", "Worm drives"],
    "fan":           ["Centrifugal fans", "Industrial fans"],
    "drill":         ["Drill presses", "Drilling machines"],
    "mill":          ["Milling machines", "Vertical milling machines"],
}

BAD = ("schematic", "diagram", "icon", "logo", "_map", ".svg", "drawing",
       "graph", "chart", "symbol", "sketch", "patent", "plan_", "seal",
       "animation", "cutaway", "cross_section", "cross-section", "label")

def curl(url, binary=False):
    r = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", UA, url],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", "replace")[:200])
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")

def category_files(cat, limit=20):
    q = urllib.parse.urlencode({
        "action": "query", "generator": "categorymembers",
        "gcmtitle": f"Category:{cat}", "gcmtype": "file", "gcmlimit": str(limit),
        "prop": "imageinfo", "iiprop": "url|mime|size", "iiurlwidth": "800",
        "format": "json",
    })
    data = json.loads(curl("https://commons.wikimedia.org/w/api.php?" + q))
    pages = data.get("query", {}).get("pages", {})
    out = []
    for p in pages.values():
        ii = p.get("imageinfo", [{}])[0]
        thumb, mime = ii.get("thumburl"), ii.get("mime", "")
        w, h = ii.get("width", 0), ii.get("height", 0)
        title = p.get("title", "").lower()
        if not thumb or mime != "image/jpeg":
            continue
        if any(b in title or b in thumb.lower() for b in BAD):
            continue
        if w and h and w < h:        # пропускаем портретные — нужны горизонтальные
            continue
        out.append(thumb)
    return out

def download(thumburl, dest):
    data = curl(thumburl, binary=True)
    if len(data) < 8000:
        return False
    with open(dest, "wb") as f:
        f.write(data)
    return True

def main():
    per_slot = 4
    for name, cats in TARGETS.items():
        got = 0
        seen = set()
        for cat in cats:
            try:
                hits = category_files(cat)
            except Exception as e:
                print(f"ERR {name}/{cat}: {e}", file=sys.stderr); continue
            for thumb in hits:
                if thumb in seen:
                    continue
                seen.add(thumb)
                dest = f"{CAND}/{name}-{got+1}.jpg"
                try:
                    if download(thumb, dest):
                        got += 1
                        print(f"OK {name}-{got}  <- {thumb.split('/')[-1][:60]}")
                except Exception as e:
                    print(f"err {name}: {e}", file=sys.stderr)
                if got >= per_slot:
                    break
            if got >= per_slot:
                break
        if got == 0:
            print(f"FAIL {name}")

if __name__ == "__main__":
    main()
