![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# UTM to Lat/Lon Converter
 
*For GIS analysts and surveyors: instantly convert between UTM coordinates (easting, northing, zone, hemisphere) and decimal degrees (latitude, longitude) with optional DMS output.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** GIS & Spatial Analysis
 
A single-screen Gradio tool for bi-directional coordinate conversion between UTM (Universal Transverse Mercator) and geographic coordinates (decimal degrees).

Inputs and UI layout:
- A radio button group at the top labeled 'Conversion direction' with two options: 'UTM → Decimal Degrees' and 'Decimal Degrees → UTM'.
- When 'UTM → Decimal Degrees' is selected, the input panel shows:
  - Easting (float, meters)
  - Northing (float, meters)
  - Zone number (integer from 1 to 60)
  - Hemisphere (dropdown: 'Northern' or 'Southern')
- When 'Decimal Degrees → UTM' is selected, the input panel shows:
  - Latitude (float, decimal degrees, range -90 to 90)
  - Longitude (float, decimal degrees, range -180 to 180)
- A 'Convert' button.
- Output area: Displays the converted coordinates clearly. For UTM→DD: shows latitude and longitude in decimal degrees (to 6 decimal places) and also in DMS format (e.g., 45°30'15"N, 73°34'12"W). For DD→UTM: shows easting, northing (meters, 2 decimals), zone, and hemisphere. Also displays the UTM grid zone designation (e.g., 18N).

Core calculation (can be implemented using the pyproj library with EPSG codes; fallback pure-Python math with standard transverse Mercator formulas also acceptable):
- UTM→DD: Determine the central meridian for the zone (Zone→CM = (zone - 1)*6 - 180 + 3 for Northern; for Southern use same but adjust hemisphere). Use transverse Mercator inverse projection (iterative or using pyproj). Output lat/lon.
- DD→UTM: Compute UTM zone from longitude (zone = floor((lon + 180)/6) + 1). Use transverse Mercator forward projection. For southern hemisphere, northing includes 10,000,000 m offset. Apply necessary constants like scale factor 0.9996.
- The tool must validate inputs (e.g., latitude within -90 to 90, longitude within -180 to 180, UTM easting between approx 100,000 and 1,000,000 m, northing between 0 and 10,000,000 m) and display clear error messages.

No AI/ML component—pure geodetic calculation.
 
## Run it
 
```bash
docker build -t utm-to-lat-lon-converter .
docker run -p 7860:7860 utm-to-lat-lon-converter
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-24.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
