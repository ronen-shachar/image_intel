"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.
"""

import folium


def sort_by_time(arr):
    sorted_arr = sorted(arr, key=lambda x: x["datetime"])
    return sorted_arr


# פונקציה ליצירת מפה
def create_map(images_data):
    gps_images = [img for img in images_data if img["has_gps"]]

    if not gps_images:
        return "<h2>No GPS data found</h2>"

    # מתחיל את המפה באמצע
    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    # יוצר איבר מפה
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        dragging=True,
        scrollWheelZoom=True,
        tap=True
    )

    # מחלק צבעים לפי חברות
    pin_color = ['blue', 'lightgreen', 'lightblue', 'orange', 'darkred',
                 'lightred', 'beige', 'pink', 'darkgreen', 'cadetblue',
                 'darkpurple', 'white', 'darkblue', 'purple', 'green',
                 'gray', 'black', 'red']
    make_color_dict = {}
    for img in gps_images:
        if img["camera_make"] in make_color_dict:
            custom_icon = folium.Icon(color=make_color_dict[img["camera_make"]], icon="info-sign")
        else:
            try:
                make_color_dict[img["camera_make"]] = pin_color.pop()
                custom_icon = folium.Icon(color=make_color_dict[img["camera_make"]], icon="info-sign")
            except IndexError:
                make_color_dict[img["camera_make"]] = "lightgray"
                custom_icon = folium.Icon(color="lightgray", icon="info-sign")

        # בונה את הפופאפ באופן מסודר
        html_content = f"""
                <div style="font-family: 'Arial', sans-serif; font-size: 12px; line-height: 1.5; width: 180px;">
                    <b style="color: #2c3e50; font-size: 14px;">IMAGE INFO</b><br>
                    <hr style="margin: 5px 0; border: 0; border-top: 1px solid #ccc;">
                    <b>FILE:</b> {img['filename']}<br>
                    <b>DATE:</b> {img['datetime']}<br>
                    <b>MAKE:</b> {img["camera_make"]}<br>
                    <b>MODEL:</b> {img['camera_model']}
                </div>
                """
        # מגדיר גודל לפופאפ
        iframe = folium.IFrame(html_content, width=190, height=120)
        # בונה את הפופאפ בפועל
        popup = folium.Popup(iframe, max_width=200)
        # בונה את הנקודת ציון
        folium.Marker(
            location=[img["latitude"], img["longitude"]],
            popup=popup,
            icon=custom_icon
        ).add_to(m)

    # בונה את הקו
    path_coordinates = [[img["latitude"], img["longitude"]] for img in gps_images]
    folium.PolyLine(path_coordinates, color="black", weight=3, opacity=10).add_to(m)

    return m._repr_html_()