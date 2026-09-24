import math
import pyproj

def dms_formatted(dec_deg, coord_type):
    """Convert decimal degrees to DMS string (e.g., 45°30'15"N)."""
    if coord_type == "lat":
        hemi = "N" if dec_deg >= 0 else "S"
    else:  # lon
        hemi = "E" if dec_deg >= 0 else "W"
    dec_deg = abs(dec_deg)
    deg = int(dec_deg)
    remainder = (dec_deg - deg) * 60
    minutes = int(remainder)
    seconds = (remainder - minutes) * 60
    return f"{deg}°{minutes}'{seconds:.0f}\"{hemi}"

def utm_to_dd(easting, northing, zone_number, hemisphere):
    """Convert UTM coordinates to geographic (decimal degrees)."""
    # Validate inputs
    if not (100000 <= easting <= 1000000):
        return {"error": "Easting must be between 100,000 and 1,000,000 m."}
    if not (0 <= northing <= 10000000):
        return {"error": "Northing must be between 0 and 10,000,000 m."}
    if not (1 <= zone_number <= 60):
        return {"error": "Zone number must be between 1 and 60."}
    if hemisphere not in ("Northern", "Southern"):
        return {"error": "Hemisphere must be 'Northern' or 'Southern'."}

    # Build UTM CRS
    if hemisphere == "Northern":
        epsg_code = 32600 + zone_number
    else:
        epsg_code = 32700 + zone_number

    try:
        utm_crs = pyproj.CRS.from_epsg(epsg_code)
        geographic_crs = pyproj.CRS.from_epsg(4326)
        transformer = pyproj.Transformer.from_crs(utm_crs, geographic_crs, always_xy=True)
        lon, lat = transformer.transform(easting, northing)
        # Ensure lat/lon in valid range
        if lat > 90 or lat < -90 or lon > 180 or lon < -180:
            return {"error": "Conversion resulted in invalid geographic coordinates."}
        return {"latitude": lat, "longitude": lon}
    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}

def dd_to_utm(lat, lon):
    """Convert decimal degrees to UTM coordinates."""
    if not (-90 <= lat <= 90):
        return {"error": "Latitude must be between -90 and 90."}
    if not (-180 <= lon <= 180):
        return {"error": "Longitude must be between -180 and 180."}

    # Compute UTM zone
    zone_number = int(math.floor((lon + 180) / 6) + 1)
    # Handle special cases near Norway and Svalbard (not implemented for simplicity)
    hemisphere = "Southern" if lat < 0 else "Northern"
    if hemisphere == "Northern":
        epsg_code = 32600 + zone_number
    else:
        epsg_code = 32700 + zone_number

    try:
        utm_crs = pyproj.CRS.from_epsg(epsg_code)
        geographic_crs = pyproj.CRS.from_epsg(4326)
        transformer = pyproj.Transformer.from_crs(geographic_crs, utm_crs, always_xy=True)
        easting, northing = transformer.transform(lon, lat)
        if easting < 100000 or easting > 1000000 or northing < 0 or northing > 10000000:
            return {"error": "Computed UTM coordinates out of expected range."}
        # Build grid zone designation (e.g., "18N")
        grid_zone = f"{zone_number}{'N' if hemisphere=='Northern' else 'S'}"
        return {"easting": easting, "northing": northing,
                "zone": zone_number, "hemisphere": hemisphere,
                "grid_zone": grid_zone}
    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}
