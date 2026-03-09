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
from datetime import datetime

def sort_by_time(arr):
    return sorted(arr,key=lambda x:datetime.strptime(x["datetime"],"%Y-%m-%d %H:%M:%S"))




def extract_center_of_map(list_location: list[dict]) -> list:

    if not list_location:
        return [32.0853, 34.7818] # For example returns -  Tel Aviv

    count = len(list_location)
    latitude_avg = sum(coord[0] for coord in list_location) / count
    longitude_avg = sum(coord[1] for coord in list_location) / count

    return [latitude_avg, longitude_avg]

def get_device_color(device_name):
    # returns a color for device
    colors = {'Samsung': 'blue', 'Apple': 'red', 'iPhone': 'red', 'Google': 'green', 'Xiaomi': 'orange'}
    brand = device_name.strip() if device_name else "Unknown"
    return colors.get(brand, 'gray')

def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    sorted_data = sort_by_time(images_data)
    valid_coords = [[loc["latitude"], loc["longitude"]] for loc in sorted_data if loc.get("has_gps")]
    center_map = extract_center_of_map(valid_coords)
    m = folium.Map(location=center_map, zoom_start=11)

    folium.PolyLine(
        locations=valid_coords, color="blue", weight=3, opacity=1
    ).add_to(m)

    for loc in images_data:
        if loc["has_gps"]:
            filename = loc["filename"]
            datetime = loc["datetime"]
            camera_make = loc["camera_make"]
            icon_color = get_device_color(camera_make)
            details = f"{filename=} - {datetime=} - {camera_make=}"

            folium.Marker([loc["latitude"], loc["longitude"]],
                          popup=details,
                          icon=folium.Icon(color=icon_color)
                          ).add_to(m)

    return m._repr_html_()



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
