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
    arr.sort(key=lambda x: x.get('datetime') or "")
    return arr


def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    gps_images = [img for img in images_data if img.get("has_gps")]

    if not gps_images:
        return "<h2>No GPS data found</h2>"

    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

    # צבעים לפי מכשיר
    device_colors = {
        "Samsung": "blue",
        "Apple": "red",
        "Xiaomi": "orange",
        "Huawei": "green",
        "Google": "purple",
        "OnePlus": "pink",
        "Sony": "darkred",
        "Oppo": "cadetblue"
    }

    # חלוקה לפי עם/בלי Timeline
    with_time = [img for img in gps_images if img.get("datetime")]
    without_time = [img for img in gps_images if not img.get("datetime")]

    # יוצרים את כל הנקודות
    for img in gps_images:
            color = device_colors.get(img.get("camera_make"), "gray")
            popup_text = f"{img.get('filename', '')}<br>{img.get('datetime', '')}<br>{img.get('camera_model', '')}"

            folium.Marker(
                location=[img["latitude"], img["longitude"]],
                popup=popup_text,
                icon=folium.Icon(color=color)
            ).add_to(m)

    # מוסיפים PolyLine רק אם יש יותר מנקודה אחת עם Timeline
    if len(with_time) > 1:
            sorted_images = sort_by_time(with_time)  # משתמש בפונקציה הקיימת שלך
            line_points = [[img["latitude"], img["longitude"]] for img in sorted_images]

            folium.PolyLine(line_points, color="purple").add_to(m)

    return m._repr_html_()


# if __name__ == "__main__":
#     # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
#     fake_data = [
#         {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
#          "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
#          "datetime": "2025-01-12 08:30:00"},
#         {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
#          "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
#          "datetime": "2025-01-13 09:00:00"},
#     ]
#     html = create_map(fake_data)
#     with open("test_map.html", "w", encoding="utf-8") as f:
#         f.write(html)
#     print("Map saved to test_map.html")
