#!/usr/bin/env python3
"""
SavATree Satellite Lead Gen — NDVI Change Detection Pipeline
=============================================================
Target: Wakefield, MA (Lake Quannapowitt area) — expandable to 6 towns
Method: Sentinel-2 NDVI comparison via STAC API (no GEE account needed)
Data: Element84 Earth Search (free, no auth, Cloud Optimized GeoTIFFs)

SETUP:
    pip install pystac-client rasterio numpy matplotlib shapely pyproj scipy requests

RUN:
    python ndvi_change_detection.py

OUTPUT:
    - wakefield-ndvi-analysis.png  (4-panel visualization)
    - wakefield-ndvi-results.json  (machine-readable results)
    - wakefield-decline-hotspots.csv (lat/lng of decline clusters for lead targeting)
"""

import json
import csv
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import rasterio
from rasterio.warp import transform_bounds
from pystac_client import Client
from shapely.geometry import box
from scipy import ndimage
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION — Edit these for different areas
# ============================================================

# Test area: Wakefield, MA (Lake Quannapowitt neighborhood)
TARGET = {
    "name": "Wakefield",
    "state": "MA",
    "description": "Lake Quannapowitt area — established residential + town center",
    "bbox": [-71.095, 42.485, -71.055, 42.510]  # [west, south, east, north]
}

# Full 6-town territory (for later expansion)
SIX_TOWNS = {
    "name": "SavATree 6-Town Territory",
    "bbox": [-71.22, 42.44, -70.96, 42.60],
    "towns": ["Melrose", "Stoneham", "Wilmington", "Wakefield", "Reading", "North Reading"]
}

# Time windows (peak growing season = best NDVI signal)
BASELINE_PERIOD = ("2023-06-15", "2023-09-15")
COMPARISON_PERIODS = [
    ("2025-06-15", "2025-09-15"),  # Try 2025 first
    ("2024-06-15", "2024-09-15"),  # Fallback to 2024
]

# NDVI thresholds
NDVI_VEG_MIN = 0.4        # Minimum NDVI to count as vegetation
DECLINE_MODERATE = -0.10   # 10% decline = flagged
DECLINE_SEVERE = -0.20     # 20% decline = severe

# Cloud cover
MAX_CLOUD = 15  # percent (strict for quality)
MAX_CLOUD_RELAXED = 30  # fallback if not enough scenes

# Clustering
MIN_CLUSTER_PIXELS = 3  # Minimum pixels to count as a hotspot (3 px = ~300 sq m)

# Output directory (same folder as this script by default)
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# STAC API endpoint
STAC_URL = "https://earth-search.aws.element84.com/v1"

# ============================================================
# FUNCTIONS
# ============================================================

def search_imagery(catalog, date_range, bbox, max_cloud):
    """Search for Sentinel-2 L2A scenes."""
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{date_range[0]}/{date_range[1]}",
        query={"eo:cloud_cover": {"lt": max_cloud}},
        max_items=15
    )
    items = list(search.items())
    # Sort client-side by cloud cover (lowest first)
    items.sort(key=lambda x: x.properties.get("eo:cloud_cover", 100))
    return items


def download_band(item, band_name, bbox):
    """Download a spectral band clipped to bounding box."""
    href = item.assets[band_name].href
    with rasterio.open(href) as src:
        dst_bounds = transform_bounds("EPSG:4326", src.crs, *bbox)
        window = rasterio.windows.from_bounds(*dst_bounds, transform=src.transform)
        data = src.read(1, window=window).astype(np.float32)
        transform = rasterio.windows.transform(window, src.transform)
        return data, transform, src.crs


def calc_ndvi(nir, red):
    """Calculate NDVI: (NIR - Red) / (NIR + Red)"""
    denom = nir + red
    denom[denom == 0] = np.nan
    return (nir - red) / denom


def find_hotspot_centers(decline_mask, bbox, shape):
    """Find geographic centers of decline clusters."""
    labeled, num_features = ndimage.label(decline_mask)
    hotspots = []

    for i in range(1, num_features + 1):
        cluster = (labeled == i)
        pixel_count = np.sum(cluster)

        if pixel_count < MIN_CLUSTER_PIXELS:
            continue

        # Find centroid in pixel coordinates
        rows, cols = np.where(cluster)
        center_row = np.mean(rows)
        center_col = np.mean(cols)

        # Convert to lat/lng
        west, south, east, north = bbox
        lng = west + (center_col / shape[1]) * (east - west)
        lat = north - (center_row / shape[0]) * (north - south)

        # Approximate area
        area_sqm = pixel_count * 100  # 10m x 10m pixels
        area_acres = area_sqm / 4047

        hotspots.append({
            "cluster_id": i,
            "lat": round(lat, 6),
            "lng": round(lng, 6),
            "pixels": int(pixel_count),
            "area_sqm": int(area_sqm),
            "area_acres": round(area_acres, 3),
            "severity": "severe" if pixel_count >= 10 else "moderate"
        })

    # Sort by size (largest first)
    hotspots.sort(key=lambda h: h["pixels"], reverse=True)
    return hotspots


# ============================================================
# MAIN ANALYSIS
# ============================================================

def main():
    bbox = TARGET["bbox"]
    name = TARGET["name"]

    print("=" * 60)
    print(f"SavATree NDVI Change Detection — {name}, {TARGET['state']}")
    print("=" * 60)

    # Step 1: Connect to STAC catalog
    print("\n[1/6] Connecting to satellite data catalog...")
    try:
        catalog = Client.open(STAC_URL)
        print(f"  Connected to: {STAC_URL}")
    except Exception as e:
        print(f"  ERROR: Could not connect to STAC API: {e}")
        print("  Make sure you have internet access and the API is reachable.")
        sys.exit(1)

    # Step 2: Search for imagery
    print(f"\n[2/6] Searching for Sentinel-2 imagery...")

    # Baseline (2023)
    print(f"  Baseline: {BASELINE_PERIOD[0]} to {BASELINE_PERIOD[1]}")
    items_baseline = search_imagery(catalog, BASELINE_PERIOD, bbox, MAX_CLOUD)
    if not items_baseline:
        print(f"  Relaxing cloud filter to {MAX_CLOUD_RELAXED}%...")
        items_baseline = search_imagery(catalog, BASELINE_PERIOD, bbox, MAX_CLOUD_RELAXED)
    print(f"  Found {len(items_baseline)} baseline scenes")

    if not items_baseline:
        print("  ERROR: No baseline imagery found. Try expanding the date range.")
        sys.exit(1)

    # Comparison (try each period in order)
    items_comparison = []
    comparison_label = ""
    for period in COMPARISON_PERIODS:
        print(f"  Comparison: {period[0]} to {period[1]}")
        items_comparison = search_imagery(catalog, period, bbox, MAX_CLOUD)
        if not items_comparison:
            items_comparison = search_imagery(catalog, period, bbox, MAX_CLOUD_RELAXED)
        if items_comparison:
            comparison_label = f"Summer {period[0][:4]}"
            print(f"  Found {len(items_comparison)} comparison scenes")
            break
        print(f"  No scenes found for this period, trying next...")

    if not items_comparison:
        print("  ERROR: No comparison imagery found.")
        sys.exit(1)

    scene_base = items_baseline[0]
    scene_comp = items_comparison[0]

    print(f"\n  Baseline scene: {scene_base.id}")
    print(f"    Date: {scene_base.datetime.strftime('%Y-%m-%d')}, "
          f"Cloud: {scene_base.properties.get('eo:cloud_cover', 'N/A')}%")
    print(f"  Comparison scene: {scene_comp.id}")
    print(f"    Date: {scene_comp.datetime.strftime('%Y-%m-%d')}, "
          f"Cloud: {scene_comp.properties.get('eo:cloud_cover', 'N/A')}%")

    # Step 3: Download bands
    print(f"\n[3/6] Downloading spectral bands (NIR + Red)...")
    red_base, transform_base, crs = download_band(scene_base, 'red', bbox)
    nir_base, _, _ = download_band(scene_base, 'nir', bbox)
    red_comp, transform_comp, _ = download_band(scene_comp, 'red', bbox)
    nir_comp, _, _ = download_band(scene_comp, 'nir', bbox)

    print(f"  Baseline: {red_base.shape[0]}x{red_base.shape[1]} pixels")
    print(f"  Comparison: {red_comp.shape[0]}x{red_comp.shape[1]} pixels")

    # Step 4: Calculate NDVI
    print(f"\n[4/6] Calculating NDVI...")
    ndvi_base = calc_ndvi(nir_base, red_base)
    ndvi_comp = calc_ndvi(nir_comp, red_comp)

    # Align dimensions if needed
    if ndvi_base.shape != ndvi_comp.shape:
        min_r = min(ndvi_base.shape[0], ndvi_comp.shape[0])
        min_c = min(ndvi_base.shape[1], ndvi_comp.shape[1])
        ndvi_base = ndvi_base[:min_r, :min_c]
        ndvi_comp = ndvi_comp[:min_r, :min_c]
        print(f"  Aligned to {min_r}x{min_c}")

    print(f"  Baseline NDVI — Mean: {np.nanmean(ndvi_base):.3f}")
    print(f"  Comparison NDVI — Mean: {np.nanmean(ndvi_comp):.3f}")

    # Step 5: Detect decline
    print(f"\n[5/6] Detecting canopy decline...")
    ndvi_change = ndvi_comp - ndvi_base
    veg_mask = ndvi_base > NDVI_VEG_MIN
    veg_change = np.where(veg_mask, ndvi_change, np.nan)

    moderate_mask = (veg_change < DECLINE_MODERATE) & (veg_change >= DECLINE_SEVERE)
    severe_mask = veg_change < DECLINE_SEVERE
    any_decline = veg_change < DECLINE_MODERATE

    total_veg = np.sum(veg_mask)
    n_moderate = int(np.nansum(moderate_mask))
    n_severe = int(np.nansum(severe_mask))
    n_total_decline = n_moderate + n_severe

    print(f"  Vegetated pixels: {total_veg:,}")
    print(f"  Moderate decline (10-20%): {n_moderate:,} ({n_moderate/total_veg*100:.1f}%)")
    print(f"  Severe decline (>20%): {n_severe:,} ({n_severe/total_veg*100:.1f}%)")

    # Find hotspot clusters
    all_decline = np.nan_to_num(any_decline, nan=0).astype(bool)
    hotspots = find_hotspot_centers(all_decline, bbox, ndvi_base.shape)

    print(f"\n  Decline hotspot clusters: {len(hotspots)}")
    for h in hotspots[:10]:
        print(f"    #{h['cluster_id']}: ({h['lat']}, {h['lng']}) — "
              f"{h['pixels']} px, ~{h['area_acres']} acres")

    # Step 6: Generate outputs
    print(f"\n[6/6] Generating outputs...")

    # --- Visualization ---
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    fig.suptitle(f"SavATree Canopy Analysis — {name}, {TARGET['state']}\n"
                 f"NDVI Change: Summer 2023 → {comparison_label}",
                 fontsize=16, fontweight='bold', y=0.98)

    ndvi_cmap = LinearSegmentedColormap.from_list('ndvi',
        ['#8B4513', '#D2691E', '#FFD700', '#ADFF2F', '#228B22', '#006400'])
    change_cmap = LinearSegmentedColormap.from_list('change',
        ['#FF0000', '#FF6600', '#FFCC00', '#FFFFFF', '#90EE90', '#228B22'])
    detect_cmap = ListedColormap(['#228B22', '#FF8C00', '#FF0000'])

    extent = [bbox[0], bbox[2], bbox[1], bbox[3]]

    # Panel 1: NDVI 2023
    im1 = axes[0, 0].imshow(ndvi_base, cmap=ndvi_cmap, vmin=-0.1, vmax=0.9, extent=extent)
    axes[0, 0].set_title(f'NDVI — Summer 2023\n({scene_base.datetime.strftime("%Y-%m-%d")})')
    plt.colorbar(im1, ax=axes[0, 0], label='NDVI', shrink=0.8)

    # Panel 2: NDVI Recent
    im2 = axes[0, 1].imshow(ndvi_comp, cmap=ndvi_cmap, vmin=-0.1, vmax=0.9, extent=extent)
    axes[0, 1].set_title(f'NDVI — {comparison_label}\n({scene_comp.datetime.strftime("%Y-%m-%d")})')
    plt.colorbar(im2, ax=axes[0, 1], label='NDVI', shrink=0.8)

    # Panel 3: Change map
    change_display = np.where(veg_mask, ndvi_change, np.nan)
    im3 = axes[1, 0].imshow(change_display, cmap=change_cmap, vmin=-0.3, vmax=0.3, extent=extent)
    axes[1, 0].set_title('NDVI Change (Vegetated Areas)\nRed = Decline, Green = Growth')
    plt.colorbar(im3, ax=axes[1, 0], label='NDVI Change', shrink=0.8)

    # Panel 4: Detection map (the money shot)
    detection = np.zeros_like(ndvi_base)
    detection[veg_mask] = 0  # Stable
    detection[moderate_mask] = 1
    detection[severe_mask] = 2
    detection_masked = np.ma.masked_where(~veg_mask, detection)

    im4 = axes[1, 1].imshow(detection_masked, cmap=detect_cmap, vmin=0, vmax=2, extent=extent)
    axes[1, 1].set_title('Canopy Decline Detection\n(Lead Generation Targets)')

    # Plot hotspot markers
    for h in hotspots[:15]:
        color = 'red' if h['severity'] == 'severe' else 'orange'
        axes[1, 1].plot(h['lng'], h['lat'], 'o', color=color, markersize=8,
                         markeredgecolor='white', markeredgewidth=1.5)

    legend_patches = [
        mpatches.Patch(color='#228B22', label='Healthy / Stable'),
        mpatches.Patch(color='#FF8C00', label=f'Moderate Decline ({n_moderate:,} px)'),
        mpatches.Patch(color='#FF0000', label=f'Severe Decline ({n_severe:,} px)'),
    ]
    axes[1, 1].legend(handles=legend_patches, loc='lower right', fontsize=9,
                       framealpha=0.9, edgecolor='black')

    for ax in axes.flat:
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    png_path = os.path.join(OUTPUT_DIR, f'{name.lower()}-ndvi-analysis.png')
    plt.savefig(png_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {png_path}")

    # --- JSON Results ---
    veg_vals = veg_change[~np.isnan(veg_change)]
    results = {
        "test_area": TARGET,
        "imagery": {
            "baseline": {
                "scene_id": scene_base.id,
                "date": scene_base.datetime.strftime("%Y-%m-%d"),
                "cloud_cover": scene_base.properties.get("eo:cloud_cover")
            },
            "comparison": {
                "scene_id": scene_comp.id,
                "date": scene_comp.datetime.strftime("%Y-%m-%d"),
                "cloud_cover": scene_comp.properties.get("eo:cloud_cover"),
                "label": comparison_label
            }
        },
        "analysis": {
            "total_pixels": int(ndvi_base.shape[0] * ndvi_base.shape[1]),
            "vegetated_pixels": int(total_veg),
            "moderate_decline_pixels": n_moderate,
            "severe_decline_pixels": n_severe,
            "total_decline_pixels": n_total_decline,
            "moderate_pct": round(n_moderate / total_veg * 100, 2),
            "severe_pct": round(n_severe / total_veg * 100, 2),
            "moderate_acres": round(n_moderate * 100 / 4047, 2),
            "severe_acres": round(n_severe * 100 / 4047, 2),
            "mean_ndvi_baseline": round(float(np.nanmean(ndvi_base)), 4),
            "mean_ndvi_comparison": round(float(np.nanmean(ndvi_comp)), 4),
            "mean_change": round(float(np.mean(veg_vals)), 4),
            "hotspot_clusters": len(hotspots)
        },
        "hotspots": hotspots[:30],
        "thresholds": {
            "vegetation_min_ndvi": NDVI_VEG_MIN,
            "moderate_decline": DECLINE_MODERATE,
            "severe_decline": DECLINE_SEVERE
        }
    }

    json_path = os.path.join(OUTPUT_DIR, f'{name.lower()}-ndvi-results.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  Saved: {json_path}")

    # --- Hotspot CSV (for lead targeting) ---
    csv_path = os.path.join(OUTPUT_DIR, f'{name.lower()}-decline-hotspots.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'cluster_id', 'lat', 'lng', 'pixels', 'area_sqm', 'area_acres',
            'severity', 'google_maps_link'
        ])
        writer.writeheader()
        for h in hotspots:
            h_copy = h.copy()
            h_copy['google_maps_link'] = (
                f"https://www.google.com/maps/@{h['lat']},{h['lng']},18z"
            )
            writer.writerow(h_copy)
    print(f"  Saved: {csv_path}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"""
Test Area: {name}, {TARGET['state']} ({TARGET['description']})
Comparison: Summer 2023 → {comparison_label}

NDVI Statistics:
  Baseline Mean: {results['analysis']['mean_ndvi_baseline']}
  Recent Mean: {results['analysis']['mean_ndvi_comparison']}
  Mean Change: {results['analysis']['mean_change']}

Canopy Decline:
  Vegetated area: {total_veg:,} pixels (~{total_veg * 100 / 4047:.0f} acres)
  Moderate decline: {n_moderate:,} px ({results['analysis']['moderate_pct']}%) — ~{results['analysis']['moderate_acres']} acres
  Severe decline: {n_severe:,} px ({results['analysis']['severe_pct']}%) — ~{results['analysis']['severe_acres']} acres
  Total flagged: {n_total_decline:,} pixels

Hotspot Clusters: {len(hotspots)}
  Top 5 clusters:""")

    for h in hotspots[:5]:
        print(f"    #{h['cluster_id']}: {h['lat']}, {h['lng']} — "
              f"{h['area_acres']} acres ({h['severity']})")
        print(f"      Maps: https://www.google.com/maps/@{h['lat']},{h['lng']},18z")

    verdict = "DETECTION WORKS" if n_total_decline > 10 else "LOW DETECTION"
    icon = "✅" if n_total_decline > 10 else "⚠️"
    print(f"\nVERDICT: {icon} {verdict}")
    if n_total_decline > 10:
        print("  Significant canopy decline detected. This approach can identify leads.")
    else:
        print("  Little decline detected. May need threshold adjustment or different time window.")

    print(f"\nOutput files:")
    print(f"  📊 {png_path}")
    print(f"  📋 {json_path}")
    print(f"  📍 {csv_path}")
    print("\nDone!")

    return results


if __name__ == '__main__':
    main()
