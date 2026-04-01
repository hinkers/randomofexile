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

        if display_name.startswith("["):
            continue

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


POE1_ASCENDANCIES = [
    {"name": "Juggernaut", "class": "Marauder"},
    {"name": "Berserker", "class": "Marauder"},
    {"name": "Chieftain", "class": "Marauder"},
    {"name": "Warden", "class": "Ranger"},
    {"name": "Deadeye", "class": "Ranger"},
    {"name": "Pathfinder", "class": "Ranger"},
    {"name": "Occultist", "class": "Witch"},
    {"name": "Elementalist", "class": "Witch"},
    {"name": "Necromancer", "class": "Witch"},
    {"name": "Slayer", "class": "Duelist"},
    {"name": "Gladiator", "class": "Duelist"},
    {"name": "Champion", "class": "Duelist"},
    {"name": "Inquisitor", "class": "Templar"},
    {"name": "Hierophant", "class": "Templar"},
    {"name": "Guardian", "class": "Templar"},
    {"name": "Assassin", "class": "Shadow"},
    {"name": "Saboteur", "class": "Shadow"},
    {"name": "Trickster", "class": "Shadow"},
    {"name": "Ascendant", "class": "Scion"},
]

POE2_ASCENDANCIES = [
    {"name": "Titan", "class": "Warrior"},
    {"name": "Warbringer", "class": "Warrior"},
    {"name": "Gemling Legionnaire", "class": "Mercenary"},
    {"name": "Witchhunter", "class": "Mercenary"},
    {"name": "Invoker", "class": "Monk"},
    {"name": "Acolyte of Chayula", "class": "Monk"},
    {"name": "Stormweaver", "class": "Sorceress"},
    {"name": "Chronomancer", "class": "Sorceress"},
    {"name": "Deadeye", "class": "Ranger"},
    {"name": "Pathfinder", "class": "Ranger"},
    {"name": "Blood Mage", "class": "Witch"},
    {"name": "Infernalist", "class": "Witch"},
]

POE2_GEMS = [
    {"name": "Lightning Arrow", "tags": ["Attack", "Projectile", "Lightning"]},
    {"name": "Ice Shot", "tags": ["Attack", "Projectile", "Cold"]},
    {"name": "Tornado Shot", "tags": ["Attack", "Projectile"]},
    {"name": "Rain of Arrows", "tags": ["Attack", "Projectile", "AoE"]},
    {"name": "Power Siphon", "tags": ["Attack", "Projectile"]},
    {"name": "Splitting Steel", "tags": ["Attack", "Projectile"]},
    {"name": "Lancing Steel", "tags": ["Attack", "Projectile"]},
    {"name": "Shattering Steel", "tags": ["Attack", "Projectile"]},
    {"name": "Poisonous Concoction", "tags": ["Attack", "AoE", "Chaos"]},
    {"name": "Explosive Concoction", "tags": ["Attack", "AoE", "Fire"]},
    {"name": "Rolling Slam", "tags": ["Attack", "Melee", "AoE"]},
    {"name": "Boneshatter", "tags": ["Attack", "Melee"]},
    {"name": "Hammer of the Gods", "tags": ["Attack", "Melee", "AoE"]},
    {"name": "Earthquake", "tags": ["Attack", "Melee", "AoE"]},
    {"name": "Shield Wall", "tags": ["Attack", "Melee"]},
    {"name": "Leap Slam", "tags": ["Attack", "Melee", "AoE", "Movement"]},
    {"name": "Reap", "tags": ["Spell", "Physical"]},
    {"name": "Exsanguinate", "tags": ["Spell", "Physical"]},
    {"name": "Bone Storm", "tags": ["Spell", "Physical", "AoE"]},
    {"name": "Unearth", "tags": ["Spell", "Physical", "Projectile"]},
    {"name": "Raise Zombie", "tags": ["Spell", "Minion"]},
    {"name": "Summon Skeletal Warriors", "tags": ["Spell", "Minion"]},
    {"name": "Raise Spectre", "tags": ["Spell", "Minion"]},
    {"name": "Spirit Offering", "tags": ["Spell", "Minion"]},
    {"name": "Fireball", "tags": ["Spell", "Projectile", "Fire"]},
    {"name": "Firestorm", "tags": ["Spell", "AoE", "Fire"]},
    {"name": "Flame Wall", "tags": ["Spell", "Fire"]},
    {"name": "Incinerate", "tags": ["Spell", "Fire"]},
    {"name": "Ice Nova", "tags": ["Spell", "AoE", "Cold"]},
    {"name": "Freezing Pulse", "tags": ["Spell", "Projectile", "Cold"]},
    {"name": "Frost Bomb", "tags": ["Spell", "AoE", "Cold"]},
    {"name": "Frozen Sweep", "tags": ["Attack", "Melee", "Cold"]},
    {"name": "Arc", "tags": ["Spell", "Chaining", "Lightning"]},
    {"name": "Spark", "tags": ["Spell", "Projectile", "Lightning"]},
    {"name": "Storm Call", "tags": ["Spell", "AoE", "Lightning"]},
    {"name": "Tempest Flurry", "tags": ["Attack", "Melee", "Lightning"]},
    {"name": "Whirling Assault", "tags": ["Attack", "Melee", "Movement"]},
    {"name": "Rapid Assault", "tags": ["Attack", "Melee"]},
    {"name": "Stormblast Mine", "tags": ["Spell", "Mine", "Lightning"]},
    {"name": "Voltaxic Burst", "tags": ["Spell", "AoE", "Lightning", "Chaos"]},
    {"name": "Chaos Bolt", "tags": ["Spell", "Projectile", "Chaos"]},
    {"name": "Essence Drain", "tags": ["Spell", "Projectile", "Chaos"]},
    {"name": "Contagion", "tags": ["Spell", "AoE", "Chaos"]},
]


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)

    poe1_gems = build_poe1_gems()
    for filename, data in [
        ("poe1-gems.json", poe1_gems),
        ("poe1-ascendancies.json", POE1_ASCENDANCIES),
        ("poe2-gems.json", POE2_GEMS),
        ("poe2-ascendancies.json", POE2_ASCENDANCIES),
    ]:
        with open(os.path.join(DATA_DIR, filename), "w") as f:
            json.dump(data, f, indent=2)
        print(f"  {filename}: {len(data)} entries")

    print("Done!")
