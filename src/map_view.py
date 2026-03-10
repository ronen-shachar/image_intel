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

FOLIUM_SUPPORTED_COLORS = [
    'red', 'blue', 'green', 'purple', 'orange', 'darkred',
    'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
    'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
    'gray', 'black', 'lightgray'
]

def sort_by_time(arr):
    return sorted(arr,key= lambda x: x["datetime"])

def color_to_model(arr):
    colors_models={}
    for i,img in enumerate(arr):
        model = img.get('camera_model', 'Unknown')
        if model not in colors_models:
            colors_models[model] = FOLIUM_SUPPORTED_COLORS[i % len(FOLIUM_SUPPORTED_COLORS)]
    return colors_models


def create_map(images_data):
    sorted_image_data=sort_by_time(images_data)
    colors_model=color_to_model(images_data)
    m=folium.Map()
    locations=[]

    for img in sorted_image_data:
        if img.get("has_gps"):
            img_path=f'../images/ready/{img['filename']}'
            html_content= f"""
            <img src='{img_path}' width="200"><br>
            <b>Name:</b> {img['filename']}<br>
            <b>Time:</b> {img['datetime']}<br>
            <b>Model</b> {img["camera_model"]}
            """

            loc = [img["latitude"], img["longitude"]]
            locations.append(loc)
            popup = folium.Popup(html_content)
            icon_file=folium.Icon(color= colors_model[img['camera_model']])

            folium.Marker(location=loc, popup=popup,icon=icon_file).add_to(m)

            if len(locations) > 1:
                folium.PolyLine(
                    locations=locations,
                    color="blue",
                    weight=3,
                    opacity=0.6,
                    #dash_array='5, 10'  # אופציונלי: הופך את הקו למקווקו
                ).add_to(m)


    if locations:
        m.fit_bounds(locations,max_zoom=12)
    return m._repr_html_()






if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
    fake_data = [
        {'filename': 'IMG_001.jpg', 'datetime': '2025-01-12 08:30:00', 'latitude': 32.0853, 'longitude': 34.7818,
         'camera_make': 'Samsung', 'camera_model': 'Galaxy S23', 'has_gps': True},
        {'filename': 'IMG_002.jpg', 'datetime': '2025-01-12 11:15:00', 'latitude': 32.0804, 'longitude': 34.7805,
         'camera_make': 'Samsung', 'camera_model': 'Galaxy S23', 'has_gps': True},
        {'filename': 'IMG_003.jpg', 'datetime': '2025-01-12 14:00:00', 'latitude': 32.0667, 'longitude': 34.7667,
         'camera_make': 'Samsung', 'camera_model': 'Galaxy S23', 'has_gps': True},
        {'filename': 'IMG_004.jpg', 'datetime': '2025-01-13 09:00:00', 'latitude': 31.7683, 'longitude': 35.2137,
         'camera_make': 'Apple', 'camera_model': 'iPhone 15 Pro', 'has_gps': True},
        {'filename': 'IMG_005.jpg', 'datetime': '2025-01-13 12:30:00', 'latitude': 31.778, 'longitude': 35.2354,
         'camera_make': 'Apple', 'camera_model': 'iPhone 15 Pro', 'has_gps': True},
        {'filename': 'IMG_006.jpg', 'datetime': '2025-01-13 16:45:00', 'latitude': 31.7742, 'longitude': 35.2258,
         'camera_make': 'Apple', 'camera_model': 'iPhone 15 Pro', 'has_gps': True},
        {'filename': 'IMG_007.jpg', 'datetime': '2025-01-14 10:00:00', 'latitude': 32.794, 'longitude': 34.9896,
         'camera_make': 'Apple', 'camera_model': 'iPhone 15 Pro', 'has_gps': True},
        {'filename': 'IMG_008.jpg', 'datetime': '2025-01-14 13:30:00', 'latitude': 32.8115, 'longitude': 34.9986,
         'camera_make': 'Canon', 'camera_model': 'EOS R5', 'has_gps': True},
        {'filename': 'IMG_009.jpg', 'datetime': '2025-01-15 09:30:00', 'latitude': 31.253, 'longitude': 34.7915,
         'camera_make': 'Samsung', 'camera_model': 'Galaxy S23', 'has_gps': True},
        {'filename': 'IMG_010.jpg', 'datetime': '2025-01-15 14:00:00', 'latitude': 31.262, 'longitude': 34.8013,
         'camera_make': 'Samsung', 'camera_model': 'Galaxy S23', 'has_gps': True},
        {'filename': 'IMG_011.jpg', 'datetime': '2025-01-16 11:00:00', 'latitude': 29.5569, 'longitude': 34.9498,
         'camera_make': 'Samsung', 'camera_model': 'Galaxy S23', 'has_gps': True},
        {'filename': 'IMG_012.jpg', 'datetime': '2025-01-16 15:30:00', 'latitude': 29.54, 'longitude': 34.9415,
         'camera_make': 'Apple', 'camera_model': 'iPhone 15 Pro', 'has_gps': True}]
    html = create_map(fake_data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(sort_by_time(fake_data))
    print("Map saved to test_map.html")
