To prep this for **Cursor IDE** and future export into your Wellspring book as a
visual infographic (PDF, PNG, or interactive HTML), here’s how to break it down
**cleanly, modularly, and debug-free**, turning your draft into something ready
for engineering and design review.

---

## **✅ 1. Summary (Add to Project Doc or Readme)**

```
### 📊 Visualization Task: Regional ASAM Level Capacity Distribution & Gap Analysis

This module generates a data-driven infographic suite using RAND data and regional estimates for California’s SUD treatment capacity by ASAM level.

#### 📌 Visual Outputs:
1. **Regional heatmap** of ASAM bed capacity per 100k population
2. **Pie charts** comparing current capacity vs estimated need by region
3. **Bar chart** showing utilization & wait time by facility type
4. **Bubble map** gap analysis of underserved counties (with population overlays)

#### 🎯 Data Notes:
- Santa Clara = 351 SUD beds
- Sacramento = needs 417 beds / 100k
- Regions: Northern, Central, Southern CA
- Includes population density, access overlays, demographic gaps
```

---

## **✅ 2. Fix the Python Code Snippet (Ready for Cursor)**

Here’s a clean and corrected version, modularized for reuse and clarity:

```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Assume df contains: ['County', 'Region', 'Population', 'Gap_Percentage']
regions = {
    'Northern California': ['Shasta', 'Humboldt', 'Butte', 'Yolo'],
    'Central California': ['Fresno', 'Tulare', 'Merced', 'Kern'],
    'Southern California': ['Los Angeles', 'Orange', 'San Diego', 'Riverside']
}

region_positions = {
    'Northern California': (0.1, 0.8),
    'Central California': (0.5, 0.5),
    'Southern California': (0.8, 0.2)
}

# Position assignment
positions = {}
cols = 3
for region, counties in regions.items():
    base_x, base_y = region_positions[region]
    for i, county in enumerate(counties):
        positions[county] = (
            base_x + (i % cols) * 0.1,
            base_y - (i // cols) * 0.1
        )

# Begin figure
bubble_fig, bubble_ax = plt.subplots(figsize=(10, 6))

# Plot county bubbles
for _, row in df.iterrows():
    county = row['County']
    x, y = positions.get(county, (0.5, 0.5))
    size = np.sqrt(row['Population']) * 0.01
    gap = row['Gap_Percentage']

    if gap <= 0:
        color = '#10B981'  # Green = surplus
    elif gap < 15:
        color = '#FBBF24'  # Yellow = slight gap
    elif gap < 30:
        color = '#F97316'  # Orange = mid gap
    else:
        color = '#EF4444'  # Red = high gap

    bubble_ax.scatter(x, y, s=size * 100, color=color, alpha=0.7, edgecolors='white')
    bubble_ax.text(x, y, county, fontsize=8, ha='center')

# Add region labels
for region, (x, y) in region_positions.items():
    bubble_ax.text(x, y + 0.1, region, fontsize=12, fontweight='bold')

# Color bar (legend for gap)
norm = Normalize(vmin=0, vmax=50)
cmap = plt.cm.RdYlGn_r
gap_sm = ScalarMappable(norm=norm, cmap=cmap)
gap_sm.set_array([])
cbar = bubble_fig.colorbar(gap_sm, ax=bubble_ax)
cbar.set_label('Gap in ASAM Bed Capacity (%)')

# Legend for population bubble sizes
legend_sizes = [500000, 1000000, 2000000]
legend_bubbles = [
    plt.scatter([], [], s=np.sqrt(s) * 0.01 * 100, color='gray', alpha=0.5)
    for s in legend_sizes
]
bubble_ax.legend(
    legend_bubbles, ['500K', '1M', '2M'],
    title="County Population", loc='upper right'
)

bubble_ax.set_title('ASAM SUD Treatment Bed Capacity Gap by County (California)', fontsize=14)
bubble_ax.axis('off')
bubble_fig.tight_layout()
plt.show()
```

---

## **✅ 3. Design Export Notes for Infographic (Book Format)**

When exporting this visual for **Wellspring Book**:

- **Save as high-resolution **.png** or **.svg** using
  **plt.savefig("asam_gap_analysis.png", dpi=300)
- Use **consistent typefaces**: match your book’s font system (e.g. Source Sans
  Pro or whatever’s used in InDesign)
- Add title + caption: _“Figure X: Gap in ASAM Level SUD Bed Capacity per
  County, Adjusted for Population (RAND, 2025)”_

Optional: Export alternative dark mode version for slides or digital companion.

---

## **✅ Optional: Supabase / Notion Metadata Sync**

If you’re tracking infographics:

```
// InfographicMeta.ts
type InfographicMeta = {
  id: string;
  title: string;
  region: 'Northern' | 'Central' | 'Southern';
  source: 'RAND';
  related_chapters: string[];
  gap_range: [number, number];
  filename: string;
}
```

---

Want me to create sample **pie chart code**, bar chart, or companion **SVG
template** to match the book’s style next?
