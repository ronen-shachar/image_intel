import folium
import extractor
from pathlib import Path

FOLIUM_SUPPORTED_COLORS = [
    'red', 'blue', 'green', 'purple', 'orange', 'darkred',
    'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
    'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
    'gray', 'black', 'lightgray'
]


def sort_by_time(arr):
    return sorted(arr, key=lambda x: (x["datetime"] is None, x["datetime"]))


def color_to_model(arr):
    colors_models = {}
    for i, img in enumerate(arr):
        model = img.get('camera_model', 'Unknown')
        if model not in colors_models:
            colors_models[model] = FOLIUM_SUPPORTED_COLORS[i % len(FOLIUM_SUPPORTED_COLORS)]
    return colors_models


def create_map(images_data):
    sorted_image_data = sort_by_time(images_data)
    colors_model = color_to_model(images_data)
    m = folium.Map()
    locations = []
    last_datetime = None

    for img in sorted_image_data:
        if img.get('latitude') is None or img.get('longitude') is None:
            continue

        if img.get("has_gps"):
            img_path = f"../images/nigga/{img['filename']}"
            camera_model = img["camera_model"].replace('\x00', "")

            html_content = f"""
            <img src="{img_path}" width="200"><br>
            <b>Name:</b> {img['filename']}<br>
            <b>Time:</b> {img['datetime']}<br>
            <b>Model:</b> {camera_model}<br>
            <b>Coordinates:</b> {img["latitude"]}, {img["longitude"]}
            """

            loc = [img["latitude"], img["longitude"]]
            locations.append(loc)

            popup = folium.Popup(html_content)
            icon_file = folium.Icon(color=colors_model[img['camera_model']])

            folium.Marker(
                location=loc,
                popup=popup,
                icon=icon_file,
                tooltip=f"{camera_model} {img['datetime']}"
            ).add_to(m)

            if len(locations) > 1:
                folium.PolyLine(
                    locations=[locations[-2], locations[-1]],
                    color="blue",
                    weight=5,
                    opacity=0.6,
                    tooltip=f"{last_datetime} ---> {img['datetime']}",
                    sticky=True
                ).add_to(m)

            last_datetime = img['datetime']

    if locations:
        m.fit_bounds(locations, max_zoom=12)

    header = '<meta http-equiv="content-type" content="text/html; charset=UTF-8" />'
    return header + m._repr_html_()


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    images_path = base_dir / "images" / "nigga"

    data = extractor.extract_all(str(images_path))
    html = create_map(data)

    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "test_map.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Map saved to {output_file}")