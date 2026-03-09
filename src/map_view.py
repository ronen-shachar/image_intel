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
    # פונקציית עזר למיון התמונות לפי זמן. תמונות בלי זמן יקבלו תאריך עתידי כדי להיות בסוף.
    return sorted(arr, key=lambda x: x.get('datetime', '9999-12-31'))


def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    # תיקון 1: מסננים רק תמונות שיש להן באמת מיקום כדי שלא ניפול על None
    gps_images = [img for img in images_data if img.get('has_gps') and img.get('latitude') and img.get('longitude')]

    if not gps_images:
        m = folium.Map(location=[31.046, 34.851], zoom_start=7)  # ברירת מחדל ישראל אם אין מיקומים
        return m.get_root().render()  # תיקון 3: החזרת HTML string

    # תיקון 1 (המשך): חישוב המרכז רק מתוך התמונות התקינות
    avg_lat = sum(img['latitude'] for img in gps_images) / len(gps_images)
    avg_lon = sum(img['longitude'] for img in gps_images) / len(gps_images)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=11)

    gps_images = sort_by_time(gps_images)

    # תיקון 5: חלוקת צבעים שמתקדמת רק כשיש מכשיר חדש
    available_colors = ['blue', 'red', 'green', 'purple', 'orange', 'darkred', 'cadetblue']
    device_colors = {}
    color_index = 0

    for img in gps_images:
        device_name = f"{img.get('camera_make', 'Unknown')} {img.get('camera_model', '')}".strip()

        if device_name not in device_colors:
            device_colors[device_name] = available_colors[color_index % len(available_colors)]
            color_index += 1

        color = device_colors[device_name]

        # תיקון 2: שימוש באייקון רגיל ולא CustomIcon שעשה בעיות
        folium.Marker(
            location=[img['latitude'], img['longitude']],
            popup=f"{img.get('filename')} - {device_name}",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)

    # תיקון 6: הוספת מקרא
    legend_html = '''
     <div style="position: fixed; bottom: 50px; left: 50px; background-color:white; 
                 border:2px solid grey; z-index:9999; padding: 10px; border-radius: 5px;">
                 <b>מקרא מכשירים</b><br>
     '''
    for device, color in device_colors.items():
        legend_html += f'<span style="color:{color}; font-size:18px;">●</span> {device}<br>'
    legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(legend_html))

    # תיקון 3: החזרת מחרוזת HTML
    return m.get_root().render()


if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
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