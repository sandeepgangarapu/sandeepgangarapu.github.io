# Garden Ornamentals & Shrubs — Design Spec

**Date:** 2026-06-14
**Page:** `static/garden/index.html` (Gangarapu Garden, Zone 8b Sammamish)
**Goal:** Add the homeowner's ornamental plants — shrubs, perennials, and bulbs — to the existing garden planner as a self-contained section, with the best grouping (placement) and full care guidance for each. Kept separate from the existing edible/veggie content.

## Plants to add (13)

Rhododendron, Camellia, Azalea, Hydrangea, Roses, Tulips, Blueberry, Shasta daisy, Hollyhock, Japanese barberry, Peony, Hyacinth, Hosta.

## Decisions

- **Integration:** New "Ornamentals & Shrubs" section on the **existing** `/garden` page (not a separate page, not a minimal version). Reuses the existing CSS/card styling.
- **Data model:** A **parallel `DATA.ornamentals` dataset** + parallel render code. The existing `DATA.plants` (veggies) and all veggie logic stay untouched. Ornamentals use ornamental-appropriate fields (bloom time, prune timing, bulb-planting timing) instead of the veggie sow→transplant→harvest model.
- **Grouping:** Recommend placement via a 4-zone map (analogous to the veggie Bed Map). User has no fixed beds yet, so zones are defined by plant needs (sun + soil), and the user places each group where it fits.
- **Seasonal detail:** Full 12-month bloom & care calendar (color-coded) + a season-by-season care task list.
- **Placement on page:** New section sits **below** the veggie content, with its own entry in the top nav. Visually distinct but consistent styling.

## Section structure (mirrors veggie sections)

1. **Zone Map** — the 4 recommended groupings, each with sun/soil tag + member plants.
2. **Ornamental Plant cards** — one card per plant, tap to expand full care.
3. **Bloom & Care Calendar** — 12-month color-coded timeline (bloom vs. care-action) + legend.
4. **Seasonal Care Tasks** — what to do each season.

The new section gets its own nav link and its own anchor (`#ornamentals`).

## The 4 zones (best grouping)

Grouping is driven by the two hard dividing lines: **sun vs. shade** and **acidic vs. neutral soil**. This way each zone shares one watering/feeding/mulching regime, evergreens anchor year-round structure, and bloom times stagger so something is always in flower.

### Zone O1 — 🌳 Woodland Shade Bed (acid-loving)
**Plants:** Rhododendron, Azalea, Camellia, Hydrangea, Hosta
**Site:** Part shade (morning sun / afternoon shade), acidic organic soil, even moisture, mulched. North/east side of house or under tree canopy. Camellia + rhododendron as evergreen backbone, hydrangea mid, hosta at the shady edge.

### Zone O2 — 🌸 Sunny Cottage Border (perennials)
**Plants:** Roses, Peony, Shasta Daisy, Hollyhock
**Site:** Full sun 6+ hrs, rich well-drained soil, good airflow (PNW disease pressure). Hollyhock at the back (tall), roses + peony mid, shasta daisy front. Stake peony & hollyhock.

### Zone O3 — 🌷 Spring Bulbs
**Plants:** Tulips, Hyacinth
**Site:** Full sun, sharp drainage. Plant in fall (Oct–Nov), bloom Mar–May. Tuck into the cottage border or pots. Hyacinth perennializes here; tulips are often short-lived in wet PNW summers.

### Zone O4 — 🫐 Edible & Foliage Accents (full sun)
**Plants:** Blueberry, Japanese Barberry
**Site:** Full sun. Blueberry needs the same acidic soil as the rhodies but wants sun — plant 2+ varieties for cross-pollination; makes an edible hedge. Barberry is a tough, thorny, colorful low-care hedge/accent (invasive-in-some-states caveat noted).

## Per-plant care data

Each ornamental card carries: `name`, `type`, `zone`, `sun`, `soilPH`, `water`, `matureSize`, `bloomTime`, `prune`, `feed`, `ease` (1–3), `careFlags[]`, `note` (the PNW-specific gotcha), and `timeline[12]`.

**Calendar codes** (one per month cell, priority bloom > prune > plant > feed): `bloom` (in flower / fruit), `prune`, `plant` (plant bulb / best planting window), `feed`, `''` (none). Nuance that doesn't fit one cell lives in the card text.

| # | Plant | Zone | Sun | Soil/pH | Bloom | Prune | Key PNW note |
|---|-------|------|-----|---------|-------|-------|--------------|
| 1 | Rhododendron | O1 | Part shade | Acidic 4.5–6.0, organic, well-drained | Apr–May | Right after bloom; deadhead trusses | Don't plant deep — keep root ball at/above grade; shallow roots hate drying & clay |
| 2 | Azalea | O1 | Part shade | Acidic, organic, well-drained | Apr–May | Lightly after bloom | A small rhododendron; deciduous types add fall color; watch lacebug/petal blight |
| 3 | Camellia | O1 | Part shade (sasanqua takes more sun) | Acidic, rich, well-drained | Japonica Feb–Apr; Sasanqua Oct–Dec | After bloom | Two types extend the season; rake fallen blooms to prevent petal blight; bud drop if dry |
| 4 | Hydrangea | O1 | Morning sun / afternoon shade | Rich, moist; bigleaf color shifts w/ pH | Jun–Sep | **Bigleaf/oakleaf = right after bloom (old wood); panicle/smooth = late winter (new wood)** | #1 mistake is spring-pruning bigleaf and cutting off the flowers — know your type |
| 5 | Hosta | O1 | Shade / part shade | Rich, moist | Jul–Aug (grown for foliage) | Cut back dead foliage late fall; divide spring/fall | **Slug magnet** — Sluggo at first spring shoots (ties to existing slug strategy); dies back in winter |
| 6 | Roses | O2 | Full sun 6+ | Rich, well-drained | Jun–Oct (repeat) | Main prune late winter (Feb–Mar); deadhead | PNW damp = blackspot/mildew — full sun, airflow, base-water, clean fallen leaves |
| 7 | Peony | O2 | Full sun 6+ | Rich, well-drained | May–Jun | Cut to ground in fall | **Plant eyes only 1–2" deep** or it won't bloom; support heavy blooms; ants harmless; resents moving |
| 8 | Shasta daisy | O2 | Full sun | Average, well-drained | Jun–Aug | Deadhead; cut back fall; divide every 2–3 yrs | Deadhead for rebloom; tall types flop (support); divide to keep vigorous |
| 9 | Hollyhock | O2 (back row) | Full sun | Rich, well-drained | Jul–Aug | Cut spent spikes; let some self-seed | **Rust-prone in damp PNW** — airflow, base-water, strip infected lower leaves; stake; biennial |
| 10 | Tulips | O3 | Full sun | Sharp drainage | Apr–May | Deadhead; let foliage die back | Plant fall (Oct–Nov) 6–8" deep; short-lived in wet PNW — treat as annual or sharpest-draining spot |
| 11 | Hyacinth | O3 | Full / part sun | Well-drained | Mar–Apr (fragrant) | Deadhead; foliage die back | Plant fall (Oct–Nov) 4–6" deep; perennializes better than tulips; wear gloves (skin irritant) |
| 12 | Blueberry | O4 | Full sun 6+ | **Very acidic 4.5–5.5** | Apr–May bloom, Jun–Aug fruit | Late winter from year 3 | PNW is prime — needs **2+ varieties** for cross-pollination; net from birds; mulch shallow roots |
| 13 | Japanese barberry | O4 | Full sun (best color) to part shade | Adaptable, well-drained; drought-tolerant | Minor Apr; grown for foliage | Anytime; shears as hedge | Very low-care, thorny barrier; **invasive in some states (not WA)** — consider sterile/dwarf cultivar |

### Timelines (month index 0=Jan … 11=Dec)

- **Rhododendron:** Apr,May=bloom; Jun=prune; Jun=feed → `['','','','bloom','bloom','prune','','','','','','']`
- **Azalea:** same as rhododendron.
- **Camellia:** Feb,Mar,Apr=bloom; May=prune; Oct,Nov,Dec=bloom → `['','bloom','bloom','bloom','prune','','','','','bloom','bloom','bloom']`
- **Hydrangea:** Feb=prune (new-wood); Jun,Jul,Aug,Sep=bloom (old-wood prune noted in card) → `['','prune','','','','bloom','bloom','bloom','bloom','','','']`
- **Hosta:** Apr=feed; Jul,Aug=bloom; Nov=prune → `['','','','feed','','','bloom','bloom','','','prune','']`
- **Roses:** Feb=prune; Apr=feed; Jun–Oct=bloom → `['','prune','','feed','','bloom','bloom','bloom','bloom','bloom','','']`
- **Peony:** Apr=feed; May,Jun=bloom; Oct=prune → `['','','','feed','bloom','bloom','','','','prune','','']`
- **Shasta daisy:** Apr=feed; Jun,Jul,Aug=bloom; Oct=prune → `['','','','feed','','bloom','bloom','bloom','','prune','','']`
- **Hollyhock:** Apr=feed; Jul,Aug=bloom; Sep=prune → `['','','','feed','','','bloom','bloom','prune','','','']`
- **Tulips:** Apr,May=bloom; Oct,Nov=plant → `['','','','bloom','bloom','','','','','plant','plant','']`
- **Hyacinth:** Mar,Apr=bloom; Oct,Nov=plant → `['','','bloom','bloom','','','','','','plant','plant','']`
- **Blueberry:** Feb=prune; Mar=feed; Apr,May=bloom; Jun,Jul,Aug=bloom(fruit) → `['','prune','feed','bloom','bloom','bloom','bloom','bloom','','','','']`
- **Japanese barberry:** Apr=bloom (minor); Jul=prune → `['','','','bloom','','','prune','','','','','']`

## Seasonal Care Tasks (PNW Zone 8b)

- **Late winter (Feb–Mar):** Prune roses; prune panicle/smooth hydrangeas & blueberries; cut remaining dead perennial foliage; feed acid-lovers (rhododendron, azalea, camellia, blueberry) as growth resumes. Camellia japonica blooming.
- **Early spring (Mar–Apr):** Hyacinth & camellia japonica bloom; Sluggo at hosta & peony emergence; mulch all beds; install peony rings & hollyhock stakes.
- **Spring (Apr–May):** Rhododendron, azalea, tulips, peony bloom; deadhead spent bulbs (leave foliage); feed roses.
- **After bloom (May–Jun):** Prune rhododendron, azalea, camellia, and bigleaf hydrangea right after flowering; deadhead spent rhody trusses & roses.
- **Summer (Jun–Aug):** Roses, hydrangea, shasta, hollyhock bloom; blueberries fruit (net from birds); deep-water hydrangea & blueberry; deadhead roses & shasta; watch blackspot/rust/mildew & keep airflow. Stop feeding roses by late Aug.
- **Fall (Sep–Nov):** **Plant tulip & hyacinth bulbs**; cut peony & shasta foliage to the ground; divide hosta & shasta; **best time to plant or move shrubs** in PNW; mulch; camellia sasanqua blooms.
- **Winter (Dec–Jan):** Mostly dormant; camellia buds; plan & order; protect containers in hard freezes.

## Filtering / nav

- New nav link "Ornamentals" added to the hero nav, scrolls to `#ornamentals`.
- The ornamental section may include its own lightweight chip filter (by zone / sun) reusing existing chip CSS, OR rely on the cards + zone map only. Default: zone-map + cards + calendar + tasks, no separate filter UI (keeps it simple and distinct from the veggie filter bar, which stays scoped to veggies).

## Non-goals (YAGNI)

- Not merging ornamentals into the veggie search/filter bar or the veggie planting calendar.
- Not adding a separate page or new Hugo content file — this is a single static HTML edit.
- No images/photos in this pass (cards are text + color-coded, like the veggie cards).

## Testing / verification

- Build with `hugo --gc --minify` (or `hugo server`) and confirm the page renders with the new section.
- Manually verify: nav link scrolls to the section; all 13 cards render & expand; calendar shows 12 months with correct color coding & legend; zone map lists all plants; no JS console errors; existing veggie sections unchanged.
