// ============================================================
// SavATree NDVI Change Detection — Wakefield, MA Test
// Platform: Google Earth Engine Code Editor
// URL: https://code.earthengine.google.com/
// ============================================================
// HOW TO RUN:
// 1. Go to https://code.earthengine.google.com/
// 2. Sign in with a Google account (free for non-commercial use)
// 3. Paste this entire script into the code editor
// 4. Click "Run"
// 5. The map will show NDVI layers — toggle them in the Layers panel
// 6. The Console tab will show statistics and decline numbers
// ============================================================

// ----- CONFIGURATION -----

// Wakefield, MA — bounding box around Lake Quannapowitt area
// Covers residential neighborhoods, some commercial, town center
var wakefield = ee.Geometry.Rectangle([-71.095, 42.485, -71.055, 42.510]);

// Also define a wider area for the 6-town territory (for later expansion)
var sixTowns = ee.Geometry.Rectangle([-71.22, 42.44, -70.96, 42.60]);

// Time windows — peak growing season for best NDVI signal
var summer2023start = '2023-06-15';
var summer2023end = '2023-09-15';
var summer2025start = '2025-06-15';
var summer2025end = '2025-09-15';

// Fallback: use 2024 if 2025 imagery isn't available yet
var summer2024start = '2024-06-15';
var summer2024end = '2024-09-15';

// Cloud cover threshold
var maxCloud = 20;

// NDVI thresholds
var ndviVegetationMin = 0.4;   // Minimum to count as vegetation
var declineModerate = -0.10;    // 10% decline = flagged
var declineSevere = -0.20;      // 20% decline = severe

// ----- HELPER FUNCTIONS -----

// Calculate NDVI from Sentinel-2 image
function addNDVI(image) {
  var ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
  return image.addBands(ndvi);
}

// Cloud masking for Sentinel-2 L2A (using SCL band)
function maskS2clouds(image) {
  var scl = image.select('SCL');
  // SCL classes: 3=cloud shadow, 7=unclassified, 8=cloud medium, 9=cloud high, 10=thin cirrus
  var mask = scl.neq(3).and(scl.neq(7)).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));
  return image.updateMask(mask);
}

// ----- BUILD NDVI COMPOSITES -----

print('========================================');
print('SavATree NDVI Analysis — Wakefield, MA');
print('========================================');

// 2023 baseline composite
var s2_2023 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(wakefield)
  .filterDate(summer2023start, summer2023end)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', maxCloud))
  .map(maskS2clouds)
  .map(addNDVI);

var ndvi2023 = s2_2023.select('NDVI').median().clip(wakefield);
print('2023 scenes used:', s2_2023.size());

// Try 2025 first, fall back to 2024
var s2_2025 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(wakefield)
  .filterDate(summer2025start, summer2025end)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', maxCloud))
  .map(maskS2clouds)
  .map(addNDVI);

var recentCount = s2_2025.size();
print('2025 scenes found:', recentCount);

// Build recent NDVI — use 2025 if available, else 2024
var s2_2024 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(wakefield)
  .filterDate(summer2024start, summer2024end)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', maxCloud))
  .map(maskS2clouds)
  .map(addNDVI);

print('2024 scenes found:', s2_2024.size());

// Use 2025 if we have data, otherwise fall back to 2024
var ndviRecent = ee.Algorithms.If(
  recentCount.gt(0),
  s2_2025.select('NDVI').median().clip(wakefield),
  s2_2024.select('NDVI').median().clip(wakefield)
);
ndviRecent = ee.Image(ndviRecent);

var comparisonYear = ee.Algorithms.If(recentCount.gt(0), '2025', '2024');
print('Comparison year:', comparisonYear);

// ----- CALCULATE CHANGE -----

var ndviChange = ndviRecent.subtract(ndvi2023).rename('NDVI_Change');

// Create vegetation mask (only analyze pixels that WERE vegetated in 2023)
var vegMask = ndvi2023.gt(ndviVegetationMin);

// Apply vegetation mask to change
var vegChange = ndviChange.updateMask(vegMask);

// Classify decline levels
var moderateDecline = vegChange.lt(declineModerate).and(vegChange.gte(declineSevere));
var severeDecline = vegChange.lt(declineSevere);
var anyDecline = vegChange.lt(declineModerate);

// ----- STATISTICS -----

print('\n--- NDVI Statistics ---');

// Mean NDVI values
var stats2023 = ndvi2023.reduceRegion({
  reducer: ee.Reducer.mean().combine(ee.Reducer.minMax(), null, true),
  geometry: wakefield,
  scale: 10,
  maxPixels: 1e8
});
print('2023 NDVI stats:', stats2023);

var statsRecent = ndviRecent.reduceRegion({
  reducer: ee.Reducer.mean().combine(ee.Reducer.minMax(), null, true),
  geometry: wakefield,
  scale: 10,
  maxPixels: 1e8
});
print('Recent NDVI stats:', statsRecent);

// Change statistics
var changeStats = vegChange.reduceRegion({
  reducer: ee.Reducer.mean().combine(ee.Reducer.minMax(), null, true)
    .combine(ee.Reducer.stdDev(), null, true),
  geometry: wakefield,
  scale: 10,
  maxPixels: 1e8
});
print('Change stats (veg areas only):', changeStats);

// Count pixels by category
var totalVegPixels = vegMask.reduceRegion({
  reducer: ee.Reducer.sum(),
  geometry: wakefield,
  scale: 10,
  maxPixels: 1e8
});
print('Total vegetated pixels:', totalVegPixels);

var moderatePixels = moderateDecline.reduceRegion({
  reducer: ee.Reducer.sum(),
  geometry: wakefield,
  scale: 10,
  maxPixels: 1e8
});
print('Moderate decline pixels (10-20%):', moderatePixels);

var severePixels = severeDecline.reduceRegion({
  reducer: ee.Reducer.sum(),
  geometry: wakefield,
  scale: 10,
  maxPixels: 1e8
});
print('Severe decline pixels (>20%):', severePixels);

// Area calculations (each pixel = 10m x 10m = 100 sq meters)
print('\n--- Area Estimates ---');
print('(Each pixel ≈ 100 sq meters = 0.025 acres)');
print('Check Console for pixel counts, multiply by 0.025 for acres');

// ----- VISUALIZATION -----

// NDVI color palette (brown → yellow → green → dark green)
var ndviVis = {
  min: -0.1,
  max: 0.9,
  palette: ['8B4513', 'D2691E', 'FFD700', 'ADFF2F', '228B22', '006400']
};

// Change palette (red → yellow → white → light green → green)
var changeVis = {
  min: -0.3,
  max: 0.3,
  palette: ['FF0000', 'FF6600', 'FFCC00', 'FFFFFF', '90EE90', '228B22']
};

// Detection map — the money shot
// Create a classified image: 0=no decline, 1=moderate, 2=severe
var detectionMap = ee.Image(0)
  .where(moderateDecline, 1)
  .where(severeDecline, 2)
  .updateMask(vegMask)
  .rename('Detection');

var detectionVis = {
  min: 0,
  max: 2,
  palette: ['228B22', 'FF8C00', 'FF0000']  // green, orange, red
};

// ----- ADD LAYERS TO MAP -----

Map.centerObject(wakefield, 14);

// Base layers
Map.addLayer(ndvi2023, ndviVis, 'NDVI 2023 (Baseline)', false);
Map.addLayer(ndviRecent, ndviVis, 'NDVI Recent', false);

// Change layer
Map.addLayer(vegChange, changeVis, 'NDVI Change (Veg Areas)', true);

// Detection layer — THIS IS THE KEY OUTPUT
Map.addLayer(detectionMap, detectionVis, '🎯 DECLINE DETECTION', true);

// Outline the study area
var outline = ee.Image().byte().paint({
  featureCollection: ee.FeatureCollection([ee.Feature(wakefield)]),
  color: 1,
  width: 3
});
Map.addLayer(outline, {palette: '0000FF'}, 'Study Area Boundary');

// ----- LEGEND (printed to console) -----

print('\n========================================');
print('MAP LEGEND:');
print('========================================');
print('🎯 DECLINE DETECTION layer:');
print('  🟢 Green = Healthy / Stable vegetation');
print('  🟠 Orange = Moderate decline (10-20% NDVI drop)');
print('  🔴 Red = Severe decline (>20% NDVI drop)');
print('');
print('Toggle layers in the Layers panel (top right of map)');
print('');
print('NEXT STEPS:');
print('1. Zoom into red/orange areas — these are lead targets');
print('2. Right-click any spot to get lat/lng coordinates');
print('3. Cross-reference with Google Maps to identify the property');
print('4. Check property type (HOA, commercial, residential)');
print('5. Score using the ISA Digital Assessment form');
print('========================================');

// ----- EXPORT (optional — uncomment to save to Google Drive) -----

// Export NDVI change as GeoTIFF to Google Drive
// Uncomment these lines to save the data:

// Export.image.toDrive({
//   image: ndviChange.clip(wakefield),
//   description: 'Wakefield_NDVI_Change',
//   folder: 'SavATree_Analysis',
//   region: wakefield,
//   scale: 10,
//   crs: 'EPSG:4326',
//   maxPixels: 1e8
// });

// Export detection map
// Export.image.toDrive({
//   image: detectionMap.clip(wakefield),
//   description: 'Wakefield_Decline_Detection',
//   folder: 'SavATree_Analysis',
//   region: wakefield,
//   scale: 10,
//   crs: 'EPSG:4326',
//   maxPixels: 1e8
// });

// Export NDVI change for the full 6-town area (bigger analysis)
// Export.image.toDrive({
//   image: ndviChange.clip(sixTowns),
//   description: 'SixTowns_NDVI_Change',
//   folder: 'SavATree_Analysis',
//   region: sixTowns,
//   scale: 10,
//   crs: 'EPSG:4326',
//   maxPixels: 1e9
// });
