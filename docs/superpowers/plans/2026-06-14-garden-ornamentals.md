# Garden Ornamentals & Shrubs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a self-contained "Ornamentals & Shrubs" section to `static/garden/index.html` with a 4-zone grouping map, per-plant care cards, a 12-month bloom & care calendar, and seasonal care tasks — without touching the existing veggie content.

**Architecture:** The page is a single self-contained HTML file with one `<script>` block. The veggie data lives in `const DATA = {...}` (line 221) and is rendered by functions wired up on a single init line (line 376). We add a parallel `const ODATA = {...}` data object, an `OCODE` color map, four new render functions (`ornZones`, `ornCards`, `ornCalendar`, `ornTasks`), a new `<section id="ornamentals">` placed below the veggie content, and a new nav link. All new UI reuses existing CSS classes (`.beds/.bedzone`, `.gallery/.pc`, `.cal/.calwrap/.legend`, `.guides/.guide`) plus one new `.osub` subheading class. The existing veggie `DATA`, filter bar, calendar, chores, and guides are left untouched.

**Tech Stack:** Static HTML/CSS/vanilla JS. Hugo (site build) for sanity only — `static/` files are copied verbatim, so real verification is opening the self-contained file in a browser. Node is used for a JS syntax check.

**Reference:** Design spec at `docs/superpowers/specs/2026-06-14-garden-ornamentals-design.md`.

**Note on verification:** This is a browser page with no JS test harness. "Verify" steps mean: (a) a JS syntax check with `node --check`, (b) `hugo --gc --minify` still builds, and (c) opening `static/garden/index.html` in a browser and visually confirming. The file is offline-ready, so opening it directly (file://) works.

---

### Task 1: Add the Ornamentals section markup, subheading CSS, and nav link

**Files:**
- Modify: `static/garden/index.html` (CSS block ~line 141, nav ~line 174, section insert ~line 216)

- [ ] **Step 1: Add the `.osub` subheading CSS**

Find this line in the `<style>` block (the `.foot` rule, ~line 141):

```css
.foot{text-align:center;color:var(--muted);font-size:12px;margin-top:40px;border-top:1px solid var(--line);padding-top:16px}
```

Add this line immediately **before** it:

```css
.osub{font-family:ui-serif,Georgia,serif;font-size:18px;color:var(--green-d);margin:24px 0 10px}
```

- [ ] **Step 2: Add the "Ornamentals" nav link**

Find the hero nav (~line 174):

```html
    <a data-go="beds" tabindex="0" role="button">Bed Map</a><a data-go="plants" tabindex="0" role="button">Plants</a><a data-go="calendar" tabindex="0" role="button">Calendar</a><a data-go="chores" tabindex="0" role="button">Monthly Chores</a><a data-go="guides" tabindex="0" role="button">Care Guides</a>
```

Replace it with (adds one link at the end):

```html
    <a data-go="beds" tabindex="0" role="button">Bed Map</a><a data-go="plants" tabindex="0" role="button">Plants</a><a data-go="calendar" tabindex="0" role="button">Calendar</a><a data-go="chores" tabindex="0" role="button">Monthly Chores</a><a data-go="guides" tabindex="0" role="button">Care Guides</a><a data-go="ornamentals" tabindex="0" role="button">Ornamentals</a>
```

(The existing `data-go` scroll wiring at the bottom of the script already handles any `.nav a[data-go]`, so no JS change is needed for scrolling.)

- [ ] **Step 3: Insert the Ornamentals section markup**

Find the footer div inside `.wrap` (~line 217):

```html
  <div class="foot">&#127793; Built for the Gangarapu garden, Sammamish &middot; 2026 &middot; offline-ready, mobile-friendly</div>
```

Insert this **before** that footer div:

```html
  <section id="ornamentals"><h2 class="sec">Ornamentals &amp; Shrubs</h2>
    <div class="sub">Your shrubs, perennials &amp; bulbs &mdash; kept separate from the veggie beds and grouped by what each plant needs. Tap any card for full care.</div>
    <h3 class="osub">Best Grouping &mdash; 4 Zones</h3>
    <div class="beds" id="ornzonemap"></div>
    <h3 class="osub">Plants</h3>
    <div class="gallery" id="orngallery"></div>
    <h3 class="osub">Bloom &amp; Care Calendar</h3>
    <div class="legend" id="ornlegend"></div>
    <div class="calwrap"><table class="cal" id="orncaltable"></table></div>
    <h3 class="osub">Seasonal Care Tasks</h3>
    <div class="guides" id="orntasks"></div>
  </section>

```

- [ ] **Step 4: Verify the markup is present and the build still works**

Run:
```bash
cd "/Users/sandeepgangarapu/Library/Mobile Documents/com~apple~CloudDocs/projects/2026-HugoWebsite"
grep -c 'id="ornamentals"\|id="ornzonemap"\|id="orngallery"\|id="orncaltable"\|id="orntasks"\|data-go="ornamentals"' static/garden/index.html
hugo --gc --minify
```
Expected: grep prints `6`; hugo build completes with no error.

- [ ] **Step 5: Commit**

```bash
git add static/garden/index.html
git commit -m "Add ornamentals section markup, nav link, and subheading style"
```

---

### Task 2: Add the ornamentals data (`ODATA`) and color code map (`OCODE`)

**Files:**
- Modify: `static/garden/index.html` (after the `const DATA = {...}` line, ~line 221)

- [ ] **Step 1: Add the `OCODE` map and `ODATA` object**

Find the line that defines `const P=DATA.plants;` (~line 224):

```javascript
const P=DATA.plants;
```

Insert the following immediately **after** that line:

```javascript
// ---- ornamentals data ----
const OCODE={bloom:["#d56aa0","In bloom / fruit"],prune:["#9c6b3f","Prune"],plant:["#4a9d4a","Plant bulb"],feed:["#3b82f6","Feed"]};
const ODATA={
 zones:[
  {id:"O1",icon:"&#127795;",name:"Woodland Shade Bed",sunClass:"shade",tag:"Part shade &middot; acidic soil",site:"Morning sun / afternoon shade, acidic organic soil, even moisture, mulched. North or east side of the house, or under tree canopy. Evergreen camellia &amp; rhododendron anchor it; hydrangea in the middle; hosta at the shady edge."},
  {id:"O2",icon:"&#127800;",name:"Sunny Cottage Border",sunClass:"sun",tag:"Full sun &middot; rich, well-drained",site:"Full sun 6+ hrs with good airflow (PNW disease pressure). Hollyhock at the back (tall), roses + peony in the middle, shasta daisy at the front. Stake peony &amp; hollyhock."},
  {id:"O3",icon:"&#127799;",name:"Spring Bulbs",sunClass:"sun",tag:"Full sun &middot; sharp drainage",site:"Plant in fall (Oct&ndash;Nov), bloom Mar&ndash;May. Tuck into the cottage border or pots. Hyacinth perennializes here; tulips are often short-lived in our wet summers."},
  {id:"O4",icon:"&#129744;",name:"Edible &amp; Foliage Accents",sunClass:"sun",tag:"Full sun",site:"Blueberry wants the same acidic soil as the rhodies but needs sun &mdash; plant 2+ varieties for cross-pollination. Barberry is a tough, thorny, colorful, low-care hedge/accent."}
 ],
 ornamentals:[
  {name:"Rhododendron",type:"Broadleaf evergreen shrub",zone:"O1",zoneName:"Woodland Shade",sun:"Part shade",soilPH:"Acidic 4.5–6.0, organic, well-drained",water:"Even moisture; deep-water in summer dry spells (shallow roots); mulch 2–3 in",size:"3–8 ft",bloomTime:"Apr–May",prune:"Right after bloom (May–Jun); deadhead spent trusses",feed:"Light, after bloom, with acid (rhododendron) fertilizer",ease:"Easy in PNW",careFlags:["acid-loving","shallow roots — don't plant deep","even moisture","watch root weevil"],note:"Don't plant too deep — keep the root ball at or slightly above grade. Shallow roots hate drying out and heavy clay, so mulch and water deeply in summer. Deadhead spent flower trusses by snapping them off above the new buds.",timeline:["","","","bloom","bloom","prune","","","","","",""]},
  {name:"Azalea",type:"Shrub (a small Rhododendron)",zone:"O1",zoneName:"Woodland Shade",sun:"Part shade",soilPH:"Acidic, organic, well-drained",water:"Even moisture; mulch",size:"2–4 ft",bloomTime:"Apr–May",prune:"Lightly right after bloom",feed:"After bloom, acid fertilizer",ease:"Easy",careFlags:["acid-loving","shallow roots","watch lacebug & petal blight"],note:"Care is the same as rhododendron, just smaller. Deciduous types add fall color. Prune lightly right after flowering, before it sets next year's buds.",timeline:["","","","bloom","bloom","prune","","","","","",""]},
  {name:"Camellia",type:"Broadleaf evergreen shrub",zone:"O1",zoneName:"Woodland Shade",sun:"Part shade (sasanqua takes more sun)",soilPH:"Acidic, rich, well-drained",water:"Even moisture; mulch; don't let it dry while budding",size:"6–12 ft (can be hedged)",bloomTime:"Japonica Feb–Apr; Sasanqua Oct–Dec",prune:"After bloom",feed:"After bloom, acid fertilizer",ease:"Easy",careFlags:["acid-loving","rake fallen blooms (petal blight)","bud drop if dry"],note:"Two types extend the season — japonica blooms late winter to spring, sasanqua blooms in fall. Rake up fallen flowers to prevent petal blight. Keep it watered while budding or the buds drop.",timeline:["","bloom","bloom","bloom","prune","","","","","bloom","bloom","bloom"]},
  {name:"Hydrangea",type:"Deciduous shrub",zone:"O1",zoneName:"Woodland Shade",sun:"Morning sun / afternoon shade",soilPH:"Rich, moist; bigleaf color shifts with pH (acidic = blue)",water:"Thirsty — deep-water in summer; wilts midday in heat",size:"3–6 ft",bloomTime:"Jun–Sep",prune:"Bigleaf/oakleaf: right after bloom (old wood). Panicle/smooth: late winter (new wood)",feed:"Spring",ease:"Easy",careFlags:["thirsty","prune-timing is critical","blooms on old vs new wood"],note:"The #1 mistake is spring-pruning a bigleaf (mophead/lacecap) and cutting off all the flower buds. Know your type: mophead/lacecap = prune just after summer bloom; panicle/Annabelle = prune in late winter. Soil pH tints bigleaf flowers — acidic soil = blue.",timeline:["","prune","","","","bloom","bloom","bloom","bloom","","",""]},
  {name:"Hosta",type:"Herbaceous perennial (foliage)",zone:"O1",zoneName:"Woodland Shade",sun:"Shade / part shade",soilPH:"Rich, moist",water:"Consistent moisture",size:"1–3 ft mounds",bloomTime:"Jul–Aug (grown mainly for foliage)",prune:"Cut back dead foliage in late fall; divide spring or fall",feed:"Spring",ease:"Easy (if slugs controlled)",careFlags:["SLUG MAGNET — use the slug strategy","dies back in winter","divide to propagate"],note:"Slugs love hosta — start Sluggo at the very first spring shoots (the same slug strategy you use on the veggie beds). It dies back fully in winter and returns in spring. Divide clumps in spring or fall to make more.",timeline:["","","","feed","","","bloom","bloom","","","prune",""]},
  {name:"Roses",type:"Shrub (repeat-blooming)",zone:"O2",zoneName:"Cottage Border",sun:"Full sun 6+ hrs",soilPH:"Rich, well-drained",water:"Deep, at the base — not overhead",size:"3–6 ft",bloomTime:"Jun–Oct (repeat)",prune:"Main prune late winter (Feb–Mar); deadhead through the season",feed:"Spring + early summer (stop by late Aug)",ease:"Moderate (disease management)",careFlags:["blackspot & powdery mildew in damp PNW","prune late winter","deadhead","water at the base"],note:"Our damp climate brings blackspot and powdery mildew pressure. Give full sun and air circulation, water at the base (not the leaves), clean up fallen leaves, and deadhead spent blooms to keep flowers coming. Main prune in late winter.",timeline:["","prune","","feed","","bloom","bloom","bloom","bloom","bloom","",""]},
  {name:"Peony",type:"Herbaceous perennial (long-lived)",zone:"O2",zoneName:"Cottage Border",sun:"Full sun 6+ hrs",soilPH:"Rich, well-drained",water:"Moderate, even",size:"2–3 ft",bloomTime:"May–Jun",prune:"Cut stems to the ground in fall",feed:"Spring (low-nitrogen)",ease:"Easy once established; resents being moved",careFlags:["don't plant eyes too deep (1–2 in max)","support heavy blooms","cut back in fall","ants are harmless"],note:"Plant the buds (\"eyes\") only 1–2 inches deep — planting too deep is the classic reason peonies never bloom. Support the heavy flowers with a peony ring. Cut the foliage to the ground in fall to prevent botrytis. Ants on the buds are harmless. Don't move it once it's settled.",timeline:["","","","feed","bloom","bloom","","","","prune","",""]},
  {name:"Shasta daisy",type:"Perennial",zone:"O2",zoneName:"Cottage Border",sun:"Full sun",soilPH:"Average, well-drained",water:"Moderate",size:"2–3 ft",bloomTime:"Jun–Aug",prune:"Deadhead; cut back in fall; divide every 2–3 yrs",feed:"Light, spring",ease:"Easy",careFlags:["deadhead for rebloom","tall types flop — support","divide to keep vigorous"],note:"Deadhead spent flowers for more blooms. Tall types flop, so give support or grow compact varieties. Divide every 2–3 years to keep the clump vigorous.",timeline:["","","","feed","","bloom","bloom","bloom","","prune","",""]},
  {name:"Hollyhock",type:"Biennial / short-lived perennial",zone:"O2",zoneName:"Cottage Border (back row)",sun:"Full sun",soilPH:"Rich, well-drained",water:"Moderate; water at the base",size:"5–8 ft (back of border)",bloomTime:"Jul–Aug (often year 2 from seed)",prune:"Cut spent spikes; let some self-seed",feed:"Spring",ease:"Easy but rust-prone",careFlags:["rust-prone in damp PNW","stake tall stalks","self-seeds","biennial"],note:"Hollyhock rust is common in our damp climate — space plants for airflow, water at the base, and strip infected lower leaves. Stake the tall stalks. It self-seeds, so expect volunteers. Often blooms in its second year from seed.",timeline:["","","","feed","","","bloom","bloom","prune","","",""]},
  {name:"Tulips",type:"Spring bulb",zone:"O3",zoneName:"Spring Bulbs",sun:"Full sun",soilPH:"Sharp drainage (bulbs rot when wet)",water:"Natural rainfall; needs sharp drainage",size:"1–2 ft",bloomTime:"Apr–May",prune:"Deadhead after bloom; let foliage die back naturally",feed:"At planting (bulb food)",ease:"Easy but often short-lived here",careFlags:["plant in fall, 6–8 in deep","short-lived in wet PNW","sharp drainage","squirrels may dig bulbs"],note:"Plant bulbs in October–November, 6–8 inches deep. Our wet summers rot tulip bulbs, so many gardeners here treat them as annuals or plant them in the sharpest-draining, sunniest spot. Let the foliage yellow before removing it.",timeline:["","","","bloom","bloom","","","","","plant","plant",""]},
  {name:"Hyacinth",type:"Spring bulb (fragrant)",zone:"O3",zoneName:"Spring Bulbs",sun:"Full / part sun",soilPH:"Well-drained",water:"Natural rainfall; good drainage",size:"8–12 in",bloomTime:"Mar–Apr (very fragrant)",prune:"Deadhead; let foliage die back",feed:"At planting",ease:"Easy; perennializes better than tulips",careFlags:["plant in fall, 4–6 in deep","fragrant","perennializes here","wear gloves (bulbs irritate skin)"],note:"Plant in fall, 4–6 inches deep. It blooms very early and is intensely fragrant, and it perennializes more reliably than tulips in our climate. Wear gloves when handling — the bulbs can irritate skin.",timeline:["","","bloom","bloom","","","","","","plant","plant",""]},
  {name:"Blueberry",type:"Edible deciduous shrub (great fall color)",zone:"O4",zoneName:"Edible Accent",sun:"Full sun 6+ hrs (for fruit)",soilPH:"Very acidic 4.5–5.5 (the key requirement)",water:"Consistent, especially while fruiting; shallow roots — mulch",size:"3–6 ft (highbush)",bloomTime:"Apr–May bloom; Jun–Aug fruit",prune:"Late winter, from year 3 — remove old/weak canes",feed:"Acidic (rhododendron/azalea) fertilizer in spring",ease:"Easy in PNW (ideal climate)",careFlags:["needs 2+ varieties for cross-pollination","very acidic soil","net from birds","shallow roots — mulch"],note:"The PNW is prime blueberry country. Give very acidic soil and plant at least two varieties (e.g. early + mid + late) for cross-pollination and a longer harvest. Net the bushes from birds. Mulch to protect the shallow roots; prune lightly in late winter from about year 3.",timeline:["","prune","feed","bloom","bloom","bloom","bloom","bloom","","","",""]},
  {name:"Japanese barberry",type:"Deciduous shrub (colorful, thorny foliage)",zone:"O4",zoneName:"Foliage Accent",sun:"Full sun (best color) to part shade",soilPH:"Adaptable, well-drained; drought-tolerant once established",water:"Low once established",size:"2–6 ft (dwarf to full)",bloomTime:"Minor yellow flowers Apr; grown for red/gold foliage",prune:"Anytime; shears well as a hedge (wear gloves — thorns)",feed:"Minimal",ease:"Very easy / low-maintenance",careFlags:["thorny — good barrier hedge","invasive in some states (not WA)","drought-tolerant","best color in full sun"],note:"Extremely low-maintenance — tough, drought-tolerant, and thorny (makes a good barrier hedge). Note it's considered invasive in parts of the US (banned in some eastern states; not in Washington) because birds spread the berries — choose a sterile or dwarf cultivar if that's a concern. Best foliage color in full sun.",timeline:["","","","bloom","","","prune","","","","",""]}
 ],
 tasks:[
  {season:"Late winter (Feb–Mar)",items:["Prune roses, and prune panicle/smooth hydrangeas &amp; blueberries.","Cut back any remaining dead perennial foliage.","Feed the acid-lovers (rhododendron, azalea, camellia, blueberry) as growth resumes.","Camellia japonica is blooming."]},
  {season:"Early spring (Mar–Apr)",items:["Hyacinth and camellia japonica bloom.","Start Sluggo at hosta &amp; peony emergence.","Mulch all the beds.","Put peony rings and hollyhock stakes in early."]},
  {season:"Spring (Apr–May)",items:["Rhododendron, azalea, tulips, and peony bloom.","Deadhead spent bulbs but leave the foliage to die back.","Feed roses."]},
  {season:"After bloom (May–Jun)",items:["Prune rhododendron, azalea, camellia, and bigleaf hydrangea right after flowering.","Deadhead spent rhododendron trusses and roses."]},
  {season:"Summer (Jun–Aug)",items:["Roses, hydrangea, shasta daisy, and hollyhock bloom; blueberries fruit (net from birds).","Deep-water hydrangea and blueberry; deadhead roses and shasta.","Watch for blackspot, rust, and mildew — keep airflow. Stop feeding roses by late August."]},
  {season:"Fall (Sep–Nov)",items:["Plant tulip and hyacinth bulbs.","Cut peony and shasta foliage to the ground; divide hosta and shasta.","Best time to plant or move shrubs in the PNW — then mulch.","Camellia sasanqua blooms."]},
  {season:"Winter (Dec–Jan)",items:["Mostly dormant; camellia buds forming.","Plan and order. Protect containers in hard freezes."]}
 ]
};
```

- [ ] **Step 2: Verify the JS still parses (no syntax errors)**

Run:
```bash
cd "/Users/sandeepgangarapu/Library/Mobile Documents/com~apple~CloudDocs/projects/2026-HugoWebsite"
node --check <(sed -n '/^<script>/,/^<\/script>/p' static/garden/index.html | sed '1d;$d')
echo "exit: $?"
```
Expected: no output from `node --check` and `exit: 0` (syntax OK). If it prints a SyntaxError, fix the data block before continuing.

- [ ] **Step 3: Commit**

```bash
git add static/garden/index.html
git commit -m "Add ornamentals data and color-code map"
```

---

### Task 3: Render the zone map (`ornZones`)

**Files:**
- Modify: `static/garden/index.html` (add function after `guides()`, ~line 367; add init call, ~line 376)

- [ ] **Step 1: Add the `ornZones` render function**

Find the end of the `guides()` function (~line 367):

```javascript
  document.getElementById("guidewrap").innerHTML=h;
}
```

Insert this immediately **after** that closing brace:

```javascript

// ---- ornamentals: zone map ----
function ornZones(){
  const byZone={};
  ODATA.ornamentals.forEach(p=>{(byZone[p.zone]=byZone[p.zone]||[]).push(p.name);});
  document.getElementById("ornzonemap").innerHTML=ODATA.zones.map(z=>
    `<div class="bedzone"><span class="z ${z.sunClass}">${z.icon} ${z.name}</span>`+
    `<div class="bedrow"><span class="bedtag">${z.id}</span><div><b>${z.tag}</b><br><small>${(byZone[z.id]||[]).join(" &middot; ")}</small></div></div>`+
    `<div class="bedrow"><small>${z.site}</small></div></div>`
  ).join("");
}
```

- [ ] **Step 2: Wire `ornZones()` into init**

Find the init line (~line 376):

```javascript
buildPanel();bedMap();calendar();choreGrid();guides();render();
```

Replace it with:

```javascript
buildPanel();bedMap();calendar();choreGrid();guides();render();ornZones();
```

- [ ] **Step 3: Verify syntax and render**

Run:
```bash
cd "/Users/sandeepgangarapu/Library/Mobile Documents/com~apple~CloudDocs/projects/2026-HugoWebsite"
node --check <(sed -n '/^<script>/,/^<\/script>/p' static/garden/index.html | sed '1d;$d') && echo "syntax OK"
```
Expected: `syntax OK`.

Then open `static/garden/index.html` in a browser, click the **Ornamentals** nav chip, and confirm the **Best Grouping — 4 Zones** map shows 4 zone cards (O1 Woodland Shade Bed, O2 Sunny Cottage Border, O3 Spring Bulbs, O4 Edible & Foliage Accents), each listing its member plants and a site description. Confirm O1 has the shade (blue) badge and O2–O4 have the sun (amber) badge. Confirm no errors in the browser console.

- [ ] **Step 4: Commit**

```bash
git add static/garden/index.html
git commit -m "Render ornamentals zone map"
```

---

### Task 4: Render the plant cards (`ocard` + `ornCards`)

**Files:**
- Modify: `static/garden/index.html` (add functions after `ornZones()`; add init call)

- [ ] **Step 1: Add the `ocard` and `ornCards` functions**

Find the end of the `ornZones()` function you just added:

```javascript
    `<div class="bedrow"><small>${z.site}</small></div></div>`
  ).join("");
}
```

Insert this immediately **after** that closing brace:

```javascript

// ---- ornamentals: cards ----
function ocard(p){
  const ML=["J","F","M","A","M","J","J","A","S","O","N","D"];
  const strip=p.timeline.map(c=>`<span style="background:${c&&OCODE[c]?OCODE[c][0]:'#e7e0c8'}"></span>`).join("");
  const mlab=ML.map(m=>`<span>${m}</span>`).join("");
  const flags=p.careFlags.map(f=>`<span class="flag">${f}</span>`).join("");
  return `<div class="pc" tabindex="0" role="button" aria-expanded="false">
    <div class="top">
      <h3>${p.name}</h3>
      <div class="var">${p.type}</div>
      <div class="badges"><span class="b yard">${p.zoneName}</span><span class="b cat">${p.sun}</span><span class="b start">${p.ease}</span></div>
      <div class="strip">${strip}</div>
      <div class="mlabels">${mlab}</div>
    </div>
    <div class="detail">
      <table>
        <tr><td>Sun</td><td>${p.sun}</td></tr>
        <tr><td>Soil/pH</td><td>${p.soilPH}</td></tr>
        <tr><td>Water</td><td>${p.water}</td></tr>
        <tr><td>Size</td><td>${p.size}</td></tr>
        <tr><td>Bloom</td><td>${p.bloomTime}</td></tr>
        <tr><td>Prune</td><td>${p.prune}</td></tr>
        <tr><td>Feed</td><td>${p.feed}</td></tr>
      </table>
      <div class="flags">${flags}</div>
      <div class="note">${p.note}</div>
    </div>
    <div class="tip">${p.note.length>110?p.note.slice(0,108)+"&hellip;":p.note}</div>
  </div>`;
}
function ornCards(){
  document.getElementById("orngallery").innerHTML=ODATA.ornamentals.map(ocard).join("");
  document.querySelectorAll("#orngallery .pc").forEach(el=>{
    const toggle=()=>{const x=el.classList.toggle("exp");el.setAttribute("aria-expanded",String(x));};
    el.onclick=toggle;
    el.onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();toggle();}};
  });
}
```

- [ ] **Step 2: Wire `ornCards()` into init**

Find the init line:

```javascript
buildPanel();bedMap();calendar();choreGrid();guides();render();ornZones();
```

Replace it with:

```javascript
buildPanel();bedMap();calendar();choreGrid();guides();render();ornZones();ornCards();
```

- [ ] **Step 3: Verify syntax and render**

Run:
```bash
cd "/Users/sandeepgangarapu/Library/Mobile Documents/com~apple~CloudDocs/projects/2026-HugoWebsite"
node --check <(sed -n '/^<script>/,/^<\/script>/p' static/garden/index.html | sed '1d;$d') && echo "syntax OK"
```
Expected: `syntax OK`.

Then reload `static/garden/index.html` in the browser. Under **Plants** (in the Ornamentals section), confirm 13 cards render (Rhododendron, Azalea, Camellia, Hydrangea, Hosta, Roses, Peony, Shasta daisy, Hollyhock, Tulips, Hyacinth, Blueberry, Japanese barberry), each with a zone/sun/ease badge row and a 12-segment color strip. Tap a card and confirm it expands to show the Sun/Soil/Water/Size/Bloom/Prune/Feed table, the care flags, and the note. Tap again to collapse. No console errors.

- [ ] **Step 4: Commit**

```bash
git add static/garden/index.html
git commit -m "Render ornamentals plant cards with expand toggle"
```

---

### Task 5: Render the bloom & care calendar (`ornCalendar`)

**Files:**
- Modify: `static/garden/index.html` (add function after `ornCards()`; add init call)

- [ ] **Step 1: Add the `ornCalendar` function**

Find the end of the `ornCards()` function you just added:

```javascript
    el.onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();toggle();}};
  });
}
```

Insert this immediately **after** that closing brace (this is the second `});}` — the one that closes `ornCards`, right before any later function; if unsure, insert right before the `// ---- wire up ----` comment):

```javascript

// ---- ornamentals: bloom & care calendar ----
function ornCalendar(){
  document.getElementById("ornlegend").innerHTML=Object.values(OCODE).map(([c,l])=>`<span><span class="sw" style="background:${c}"></span>${l}</span>`).join("");
  let h="<tr><th>Plant</th>"+MONTHS.map(m=>`<th>${m}</th>`).join("")+"</tr>";
  ODATA.ornamentals.forEach(p=>{ h+=`<tr><td class="cn">${p.name}</td>`+p.timeline.map(c=>`<td class="cell" style="background:${c&&OCODE[c]?OCODE[c][0]:'#fff'}"></td>`).join("")+"</tr>";});
  document.getElementById("orncaltable").innerHTML=h;
}
```

- [ ] **Step 2: Wire `ornCalendar()` into init**

Find the init line:

```javascript
buildPanel();bedMap();calendar();choreGrid();guides();render();ornZones();ornCards();
```

Replace it with:

```javascript
buildPanel();bedMap();calendar();choreGrid();guides();render();ornZones();ornCards();ornCalendar();
```

- [ ] **Step 3: Verify syntax and render**

Run:
```bash
cd "/Users/sandeepgangarapu/Library/Mobile Documents/com~apple~CloudDocs/projects/2026-HugoWebsite"
node --check <(sed -n '/^<script>/,/^<\/script>/p' static/garden/index.html | sed '1d;$d') && echo "syntax OK"
```
Expected: `syntax OK`.

Then reload the page. Under **Bloom & Care Calendar**, confirm a legend with four swatches (In bloom / fruit · Prune · Plant bulb · Feed) and a table with a row per plant and 12 month columns, with colored cells matching each plant's timeline (e.g., Rhododendron pink in Apr–May, brown in Jun; Tulips green in Oct–Nov; Camellia pink in Feb–Apr and Oct–Dec). No console errors.

- [ ] **Step 4: Commit**

```bash
git add static/garden/index.html
git commit -m "Render ornamentals bloom & care calendar"
```

---

### Task 6: Render the seasonal care tasks (`ornTasks`)

**Files:**
- Modify: `static/garden/index.html` (add function after `ornCalendar()`; add init call)

- [ ] **Step 1: Add the `ornTasks` function**

Find the end of the `ornCalendar()` function you just added:

```javascript
  document.getElementById("orncaltable").innerHTML=h;
}
```

Insert this immediately **after** that closing brace:

```javascript

// ---- ornamentals: seasonal care tasks ----
function ornTasks(){
  document.getElementById("orntasks").innerHTML=ODATA.tasks.map(t=>
    `<div class="guide"><h3>${t.season}</h3><ul>${t.items.map(i=>`<li>${i}</li>`).join("")}</ul></div>`
  ).join("");
}
```

- [ ] **Step 2: Wire `ornTasks()` into init**

Find the init line:

```javascript
buildPanel();bedMap();calendar();choreGrid();guides();render();ornZones();ornCards();ornCalendar();
```

Replace it with:

```javascript
buildPanel();bedMap();calendar();choreGrid();guides();render();ornZones();ornCards();ornCalendar();ornTasks();
```

- [ ] **Step 3: Verify syntax and render**

Run:
```bash
cd "/Users/sandeepgangarapu/Library/Mobile Documents/com~apple~CloudDocs/projects/2026-HugoWebsite"
node --check <(sed -n '/^<script>/,/^<\/script>/p' static/garden/index.html | sed '1d;$d') && echo "syntax OK"
```
Expected: `syntax OK`.

Then reload the page. Under **Seasonal Care Tasks**, confirm 7 cards (Late winter, Early spring, Spring, After bloom, Summer, Fall, Winter), each with a bulleted task list. No console errors.

- [ ] **Step 4: Commit**

```bash
git add static/garden/index.html
git commit -m "Render ornamentals seasonal care tasks"
```

---

### Task 7: Full verification and final check

**Files:**
- No code changes — verification only.

- [ ] **Step 1: JS syntax check**

Run:
```bash
cd "/Users/sandeepgangarapu/Library/Mobile Documents/com~apple~CloudDocs/projects/2026-HugoWebsite"
node --check <(sed -n '/^<script>/,/^<\/script>/p' static/garden/index.html | sed '1d;$d') && echo "syntax OK"
```
Expected: `syntax OK`.

- [ ] **Step 2: Hugo build**

Run:
```bash
hugo --gc --minify
```
Expected: build completes with no error.

- [ ] **Step 3: Confirm all data is present**

Run:
```bash
grep -o 'name:"[^"]*"' static/garden/index.html | grep -E 'Rhododendron|Azalea|Camellia|Hydrangea|Hosta|Roses|Peony|Shasta|Hollyhock|Tulips|Hyacinth|Blueberry|barberry' | wc -l
```
Expected: prints `13` (all 13 ornamentals present in the data).

- [ ] **Step 4: Manual browser checklist**

Open `static/garden/index.html` in a browser and confirm:
- The **Ornamentals** nav chip scrolls to the new section.
- Zone map shows 4 zones with correct plants and sun/shade badges.
- 13 plant cards render; tapping expands/collapses each with full care details.
- Bloom & Care calendar shows the legend + a colored row per plant.
- Seasonal Care Tasks shows 7 season cards.
- The existing veggie sections (Bed Map, Plants, Calendar, Monthly Chores, Care Guides) are unchanged and still work (search, filters, card expand, month highlight).
- No errors in the browser console.

- [ ] **Step 5: Final commit (if any uncommitted changes remain)**

```bash
git status
# if clean, nothing to do; otherwise:
git add static/garden/index.html
git commit -m "Finalize ornamentals section"
```
