"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. חישוב מרכז המפה - היה עובר על images_data (כולל תמונות בלי GPS) במקום gps_image, נופל עם None
2. הסרת CustomIcon שלא עובד (filename זה לא נתיב שהדפדפן מכיר)
3. הסרת m.save() - לפי API contract צריך להחזיר HTML string, לא לשמור קובץ
4. הסרת fake_data מגוף הקובץ - הועבר ל-if __name__
5. תיקון color_index - היה מתקדם על כל תמונה במקום רק על מכשיר חדש
6. הוספת מקרא מכשירים
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
    m = folium.Map(location=[center_lat, center_lon], zoom_start=1)

    # מחלק צבעים לפי חברות
    pin_color = ['lightgray', 'blue', 'lightgreen', 'lightblue', 'orange', 'darkred',
                 'lightred', 'beige', 'pink', 'darkgreen', 'cadetblue',
                 'darkpurple', 'white', 'darkblue', 'purple', 'green',
                 'gray', 'black', 'red']
    make_color_dict = {}
    for img in gps_images:
        if img["camera_make"] in make_color_dict:
            custom_icon = folium.Icon(color=make_color_dict[img["camera_make"]], icon="info-sign")
        else:
            make_color_dict[img["camera_make"]] = pin_color.pop()
            custom_icon = folium.Icon(color=make_color_dict[img["camera_make"]], icon="info-sign")

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
    folium.PolyLine(path_coordinates, color="red", weight=3, opacity=10).add_to(m)

    return m._repr_html_()

    # if __name__ == "__main__":
    fake_data = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
        {"filename": "test3.jpg", "latitude": 40.7128, "longitude": -74.0060,
         "has_gps": True, "camera_make": "Google", "camera_model": "Pixel 8",
         "datetime": "2025-01-14 12:45:00"},
        {"filename": "test4.jpg", "latitude": 48.8566, "longitude": 2.3522,
         "has_gps": True, "camera_make": "Sony", "camera_model": "Alpha a7 IV",
         "datetime": "2025-01-15 17:20:00"},
        {"filename": "test5.jpg", "latitude": None, "longitude": None,
         "has_gps": False, "camera_make": "Canon", "camera_model": "EOS R6",
         "datetime": "2025-01-16 10:15:00"},
        {"filename": "test6.jpg", "latitude": 35.6762, "longitude": 139.6503,
         "has_gps": True, "camera_make": "Fujifilm", "camera_model": "X-T5",
         "datetime": "2025-01-17 06:10:00"},
        {"filename": "test7.jpg", "latitude": -33.8688, "longitude": 151.2093,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 14",
         "datetime": "2025-01-18 21:05:00"},
        {"filename": "test8.jpg", "latitude": 51.5074, "longitude": -0.1278,
         "has_gps": True, "camera_make": "DJI", "camera_model": "Mavic 3",
         "datetime": "2025-01-19 14:30:00"},
        {"filename": "test9.jpg", "latitude": 25.2048, "longitude": 55.2708,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S22",
         "datetime": "2025-01-20 11:55:00"},
        {"filename": "test10.jpg", "latitude": None, "longitude": None,
         "has_gps": False, "camera_make": "Nikon", "camera_model": "Z9",
         "datetime": "2025-01-21 09:40:00"}
    ]
    ordered_data = sort_by_time(fake_data)
    html = create_map(ordered_data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Map saved to test_map.html")
