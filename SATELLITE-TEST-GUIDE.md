# Satellite Test Guide — Wakefield, MA

## Quick Start: Two Ways to Run the Test

### Option A: Google Earth Engine (Fastest — 2 minutes)
**Best for:** Instant visual results, interactive map exploration

1. Go to [code.earthengine.google.com](https://code.earthengine.google.com/)
2. Sign in with any Google account (free, one-time signup)
3. Open `gee-ndvi-wakefield-test.js` from your working folder
4. Copy the entire script → paste into the code editor
5. Click **Run**
6. The map loads NDVI layers — toggle them in the **Layers** panel (top right)
7. Check the **Console** tab for statistics and pixel counts

**What you'll see:**
- NDVI Change layer: red = decline, green = growth
- Decline Detection layer: green = healthy, orange = moderate decline, red = severe
- Zoom into red/orange areas — these are lead targets
- Right-click any spot for lat/lng coordinates

### Option B: Python Pipeline (Full Analysis — 5 minutes)
**Best for:** Automated analysis, CSV output with hotspot coordinates, publication-quality visuals

**Setup (one time):**
```
pip install pystac-client rasterio numpy matplotlib shapely pyproj scipy requests
```

**Run:**
```
cd "C:\Users\MikeF\Desktop\Cassidy\Claude CoWork Jackson"
python ndvi_change_detection.py
```

**Output files:**
- `wakefield-ndvi-analysis.png` — 4-panel visualization (NDVI 2023, NDVI recent, change map, detection map)
- `wakefield-ndvi-results.json` — Full analysis results (machine-readable)
- `wakefield-decline-hotspots.csv` — Lat/lng of every decline cluster with Google Maps links

## What the Analysis Does

1. **Searches** for cloud-free Sentinel-2 satellite imagery (10m resolution)
2. **Downloads** NIR (Band 8) and Red (Band 4) spectral bands
3. **Calculates** NDVI for summer 2023 (baseline) and summer 2025 (or 2024 fallback)
4. **Detects** vegetation pixels that lost >10% NDVI (moderate) or >20% (severe)
5. **Clusters** adjacent decline pixels into hotspot groups
6. **Outputs** coordinates, area estimates, and Google Maps links for each hotspot

## Test Area: Wakefield, MA

**Bounding box:** -71.095, 42.485 to -71.055, 42.510

This covers the Lake Quannapowitt area — mix of:
- Established residential neighborhoods (mature trees)
- Town center / commercial
- Some public/institutional properties

## Interpreting Results

| NDVI Value | Meaning |
|-----------|---------|
| 0.6 – 0.9 | Healthy, dense canopy |
| 0.4 – 0.6 | Moderate vegetation |
| 0.2 – 0.4 | Sparse vegetation or stressed |
| < 0.2 | Bare soil, water, built surfaces |

| Change Category | Threshold | Action |
|----------------|-----------|--------|
| Severe decline | > 20% drop | Immediate outreach — high-priority lead |
| Moderate decline | 10-20% drop | Score and qualify — good lead candidate |
| Stable | < 10% change | Not flagged |
| Growth | Positive change | Not relevant (could be new planting) |

## Next Steps After Running

1. **Review the detection map** — are the flagged areas realistic?
2. **Click hotspot Google Maps links** — identify the actual property
3. **Classify property type** — HOA, commercial, residential, municipal
4. **Score using ISA form** — open `savatree-isa-digital-assessment.html`, use Lead Score tab
5. **Look up decision-makers** — Apollo/Clay for property managers, HOA boards
6. **Prepare outreach** — satellite imagery + ISA assessment = compelling pitch

## Expanding to All 6 Towns

To run the full territory analysis, edit `ndvi_change_detection.py`:

```python
# Change TARGET to use the full 6-town area:
TARGET = {
    "name": "SavATree-Territory",
    "state": "MA",
    "description": "Full 6-town service area",
    "bbox": [-71.22, 42.44, -70.96, 42.60]
}
```

Note: The full territory is much larger and will take longer to download and process.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| GEE says "not registered" | Sign up at [signup.earthengine.google.com](https://signup.earthengine.google.com/) (instant, free) |
| Python can't find pystac-client | Run `pip install pystac-client` (may need `pip3` on Mac) |
| "No scenes found" | Try relaxing cloud cover: change `MAX_CLOUD = 15` to `30` |
| rasterio install fails on Windows | Install via `conda install rasterio` or use [rasterio wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio) |
| STAC API timeout | Check internet connection; the API is occasionally slow for large areas |

## Deployment Discussion

For sharing HTML deliverables and hosting the analysis pipeline:

**Option 1: GitHub Pages (free, simplest)**
- Push HTML files to a GitHub repo
- Enable GitHub Pages in repo settings
- Files are viewable at `https://username.github.io/repo-name/`
- Great for: feasibility study, qualification framework, ISA form

**Option 2: Vercel (free tier, auto-deploy)**
- Connect a GitHub repo to Vercel
- Auto-deploys on every push
- Custom domain support
- Great for: interactive tools, if we build a dashboard later

**Option 3: GitHub repo only (no hosting)**
- Just use GitHub as a shared file store
- Jackson opens HTML files locally after cloning/downloading
- Simplest, no hosting needed

Recommended: Start with **GitHub Pages** — it's free, handles static HTML perfectly, and takes 5 minutes to set up.
