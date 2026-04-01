# Random of Exile — Design Spec

## Overview

A dead-simple webapp that randomly generates a Path of Exile skill gem + ascendancy combo. Supports both PoE 1 and PoE 2. Includes a slot machine animation and helpful links.

## Tech Stack

- Pure HTML/CSS/JS — single `index.html`, no frameworks
- Game data in separate JSON files loaded via `fetch()`
- Python script to update JSON data from community sources

## File Structure

```
randomofexile/
├── index.html
├── update-data.py
├── data/
│   ├── poe1-gems.json
│   ├── poe1-ascendancies.json
│   ├── poe2-gems.json
│   └── poe2-ascendancies.json
└── docs/
    └── superpowers/
        └── specs/
            └── (this file)
```

## Data Format

### Gems JSON

```json
[
  { "name": "Arc", "tags": ["Spell", "Lightning"] },
  { "name": "Cyclone", "tags": ["Attack", "Melee"] }
]
```

Tags are for display/flavor only — no filtering logic.

### Ascendancies JSON

```json
[
  { "name": "Juggernaut", "class": "Marauder" },
  { "name": "Elementalist", "class": "Witch" }
]
```

## UI Design

### Theme
Dark themed (PoE aesthetic), centered layout.

### Layout (top to bottom)

1. **Game Toggle** — PoE 1 / PoE 2 buttons at the top. Active state highlighted. Disabled while a spin is in progress.

2. **Slot Machine** — Two vertical columns side by side:
   - Left: **Skill Gem**
   - Right: **Ascendancy**
   - Each column shows a vertical window with one name visible at a time
   - Names scroll vertically and decelerate to a stop

3. **Randomize Button** — Large button below the slots. Disabled while spinning.

4. **Results Panel** — Appears after both slots land. Shows:
   - Selected gem name + tags
   - Selected ascendancy name + base class
   - Link to gem's wiki page
   - Link to ascendancy's wiki page
   - Link to poe.ninja builds search for the combo

### Slot Machine Animation

- CSS-driven using `transform: translateY()` on a tall strip of names
- Eases from fast to slow over ~2-3 seconds
- Gem slot stops first
- Ascendancy slot stops ~0.5s later

### Link Formats

- **Wiki (PoE 1):** `https://www.poewiki.net/wiki/{Name}` (spaces → underscores)
- **Wiki (PoE 2):** `https://www.poe2wiki.net/wiki/{Name}` (spaces → underscores)
- **poe.ninja (PoE 1):** `https://poe.ninja/challenge/builds?skill={Name}&class={Ascendancy}` (spaces → URL-encoded)
- **poe.ninja (PoE 2):** `https://poe.ninja/poe2/builds?skill={Name}&class={Ascendancy}` (spaces → URL-encoded)

## Error Handling

- **Failed JSON fetch:** Show friendly error in the slot area ("Couldn't load data — are you running a local server?")
- **Toggle during spin:** Ignored until spin finishes
- **Rapid Randomize clicks:** Ignored while spin is in progress

## Data Update Script (`update-data.py`)

### Purpose
Fetches current game data from [RePoE](https://github.com/brather1ng/RePoE) (community-maintained extracted PoE data) and writes the JSON files.

### Behavior

1. Fetch gem and character data from RePoE's GitHub raw JSON URLs
2. Filter gems to active skills only (exclude support gems)
3. Extract ascendancy classes with their base class
4. Write to `data/*.json`
5. Print summary (e.g., "Updated: 203 gems, 19 ascendancies for PoE 1")

### Dependencies
- Python 3
- `requests` library (or stdlib `urllib` to keep it zero-dep)

### PoE 2 Data
RePoE may not cover PoE 2 yet. If not available, the script hardcodes PoE 2 data with a TODO comment, and we update the source when one becomes available.

## Out of Scope

- User accounts / persistence
- Filtering gems by category
- Build guides or detailed gem info
- Mobile-specific responsive design (basic centering should work fine on mobile though)
