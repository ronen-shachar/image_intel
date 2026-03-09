"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.
"""

import folium


def sort_by_time(arr):
    """ממיין את התמונות לפי סדר כרונולוגי"""
    # מניח שהתאריך נמצא במפתח 'datetime'. אם חסר, ישים בסוף.
    return sorted(arr, key=lambda x: x.get('datetime', ''))


def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    if not images_data:
        return "<html><body><h1>No data provided</h1></body></html>"

    # 1. סינון: ניקח רק תמונות שיש להן GPS חוקי
    gps_images = [
        img for img in images_data
        if img.get("has_gps") and img.get("latitude") is not None and img.get("longitude") is not None
    ]

    if not gps_images:
        return "<html><body><h1>No GPS data found in the provided images</h1></body></html>"

    # מיון התמונות לפי זמן (כדי שנוכל לחבר קו כרונולוגי)
    gps_images = sort_by_time(gps_images)

    # 2. חישוב מרכז המפה (ממוצע של כל הקואורדינטות התקינות)
    avg_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    avg_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    # 3. הכנת צבעים למכשירים (כדי לזהות איזה טלפון צילם מה)
    available_colors = ['blue', 'green', 'red', 'purple', 'orange', 'darkred', 'cadetblue', 'darkblue']
    device_colors = {}
    color_index = 0

    # 4. הוספת הסמנים למפה
    for img in gps_images:
        # יצירת שם המכשיר (למשל: Apple iPhone 15 Pro)
        device_name = f"{img.get('camera_make', 'Unknown')} {img.get('camera_model', 'Unknown')}".strip()

        # אם זה מכשיר חדש שעוד לא ראינו, ניתן לו צבע
        if device_name not in device_colors:
            device_colors[device_name] = available_colors[color_index % len(available_colors)]
            color_index += 1

        color = device_colors[device_name]

        # תוכן החלונית שקופצת שלוחצים על הסמן
        popup_text = f"""
        <div style="direction: ltr; font-family: Arial;">
            <b>File:</b> {img.get('filename')}<br>
            <b>Time:</b> {img.get('datetime')}<br>
            <b>Device:</b> {device_name}
        </div>
        """

        folium.Marker(
            location=[img['latitude'], img['longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=color, icon='camera', prefix='fa')  # סמל של מצלמה
        ).add_to(m)

    # בונוס מודיעיני: קו שמחבר את התמונות לפי סדר הזמן!
    coordinates = [[img['latitude'], img['longitude']] for img in gps_images]
    folium.PolyLine(coordinates, color="red", weight=2.5, opacity=0.7).add_to(m)

    # 5. במקום לשמור לקובץ (m.save), אנחנו מחזירים את ה-HTML כ-String לפי החוזה (API Contract)
    return m.get_root().render()


if __name__ == "__main__":
    # נתוני בדיקה של צוות ה-QA / המרצה
    fake_data = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]

    html = create_map(fake_data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Map saved to test_map.html")