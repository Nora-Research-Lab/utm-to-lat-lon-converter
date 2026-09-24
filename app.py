import gradio as gr
from utm_to_lat_lon_converter import utm_to_dd, dd_to_utm, dms_formatted

def convert(direction, easting, northing, zone, hemisphere, lat, lon):
    if direction == "UTM → Decimal Degrees":
        if easting is None or northing is None or zone is None or hemisphere is None:
            return "Please fill all UTM fields."
        try:
            result = utm_to_dd(float(easting), float(northing), int(zone), hemisphere)
        except (ValueError, TypeError) as e:
            return f"Invalid input: {e}"
        if "error" in result:
            return result["error"]
        lat_dd = result["latitude"]
        lon_dd = result["longitude"]
        dms_lat = dms_formatted(lat_dd, "lat")
        dms_lon = dms_formatted(lon_dd, "lon")
        return f"Latitude: {lat_dd:.6f}° ({dms_lat})\nLongitude: {lon_dd:.6f}° ({dms_lon})"
    else:
        if lat is None or lon is None:
            return "Please fill latitude and longitude."
        try:
            result = dd_to_utm(float(lat), float(lon))
        except (ValueError, TypeError) as e:
            return f"Invalid input: {e}"
        if "error" in result:
            return result["error"]
        return (f"Easting: {result['easting']:.2f} m\n"
                f"Northing: {result['northing']:.2f} m\n"
                f"Zone: {result['zone']}\n"
                f"Hemisphere: {result['hemisphere']}\n"
                f"Grid zone: {result['grid_zone']}")

with gr.Blocks(title="UTM ↔ Lat/Lon Converter") as demo:
    gr.Markdown("# UTM ↔ Lat/Lon Converter")
    direction = gr.Radio(["UTM → Decimal Degrees", "Decimal Degrees → UTM"],
                         label="Conversion direction", value="UTM → Decimal Degrees")
    with gr.Row():
        with gr.Column(scale=1, min_width=300) as utm_col:
            easting = gr.Number(label="Easting (m)", minimum=100000, maximum=1000000)
            northing = gr.Number(label="Northing (m)", minimum=0, maximum=10000000)
            zone = gr.Number(label="Zone number (1–60)", minimum=1, maximum=60, step=1)
            hemisphere = gr.Dropdown(["Northern", "Southern"], label="Hemisphere", value="Northern")
        with gr.Column(scale=1, min_width=300, visible=False) as dd_col:
            lat = gr.Number(label="Latitude (-90 to 90)", minimum=-90, maximum=90)
            lon = gr.Number(label="Longitude (-180 to 180)", minimum=-180, maximum=180)
    convert_btn = gr.Button("Convert")
    output = gr.Textbox(label="Result", lines=6)

    def toggle_panels(direction):
        utm_visible = direction == "UTM → Decimal Degrees"
        dd_visible = direction == "Decimal Degrees → UTM"
        return [gr.update(visible=utm_visible)] * 4 + [gr.update(visible=dd_visible)] * 2
    direction.change(toggle_panels, direction, [easting, northing, zone, hemisphere, lat, lon])

    convert_btn.click(
        convert,
        inputs=[direction, easting, northing, zone, hemisphere, lat, lon],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
