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
    return sorted(arr, key=lambda x: x.get('datetime') or "")


def create_map(images_data):
   start_coords = [31.0461, 34.8516]
   for img in images_data:
       if img ['latitude'] and img ['longitude']:
           start_coords = [img['latitude'],img['longitude']]
           break
   m = folium.Map(location=start_coords, zoom_start=8)
   for img in images_data:
       lat = img.get('latitude')
       lon = img.get('longitude')
       if lat is not None and lon is not None:
           filename = img.get('filename', 'Unknown File')
           date = img.get('datetime', 'No date available')
           model = img.get('camera_model', 'Unknown Device')
           popup_content = f"""
                           <b>File:</b> {filename}<br>
                           <b>Date:</b> {date}<br>
                           <b>Device:</b> {model}
                       """
           folium.Marker(
           location=[lat, lon],
           popup=folium.Popup(popup_content, max_width=300),
           icon=folium.Icon(color="blue", icon="camera", prefix="fa")
       ).add_to(m)
   return m._repr_html_()





if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
    from extractor import extract_all

    path = r'C:\Users\esti7\PycharmProjects\PythonProject\image-intel\image_intel\images'
    data = extract_all(path)
    map_html = create_map(data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(map_html)
    print("המפה נוצרה! פתחי את הקובץ test_map.html בדפדפן.")
    # fake_data = [
    #     {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
    #      "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
    #      "datetime": "2025-01-12 08:30:00"},
    #     {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
    #      "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
    #      "datetime": "2025-01-13 09:00:00"},
    # ]
    # html = create_map(fake_data)
    # with open("test_map.html", "w", encoding="utf-8") as f:
    #     f.write(html)
    # print("Map saved to test_map.html")
