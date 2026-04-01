#!/usr/bin/env python3
"""Fetches PoE game data from community sources and writes JSON files."""

import json
import os
import urllib.request

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

REPOE_GEMS_URL = "https://raw.githubusercontent.com/brather1ng/RePoE/master/RePoE/data/gems.json"
REPOE_GEM_TAGS_URL = "https://raw.githubusercontent.com/brather1ng/RePoE/master/RePoE/data/gem_tags.json"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "RandomOfExile/1.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def build_poe1_gems():
    print("Fetching PoE 1 gem data from RePoE...")
    raw_gems = fetch_json(REPOE_GEMS_URL)
    tag_names = fetch_json(REPOE_GEM_TAGS_URL)

    gems = []
    for key, gem in raw_gems.items():
        if gem.get("is_support", True):
            continue
        base_item = gem.get("base_item")
        if not base_item or base_item.get("release_state") != "released":
            continue

        display_name = gem.get("active_skill", {}).get("display_name")
        if not display_name:
            display_name = gem.get("base_item", {}).get("display_name", key)

        raw_tags = gem.get("tags", [])
        display_tags = []
        for t in raw_tags:
            mapped = tag_names.get(t)
            if mapped:
                display_tags.append(mapped)

        gems.append({"name": display_name, "tags": display_tags})

    # Deduplicate by name (some gems have multiple internal entries)
    seen = set()
    unique_gems = []
    for g in gems:
        if g["name"] not in seen:
            seen.add(g["name"])
            unique_gems.append(g)

    unique_gems.sort(key=lambda g: g["name"])
    return unique_gems


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)

    poe1_gems = build_poe1_gems()
    with open(os.path.join(DATA_DIR, "poe1-gems.json"), "w") as f:
        json.dump(poe1_gems, f, indent=2)
    print(f"  PoE 1 gems: {len(poe1_gems)}")
