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
    from extractor import extract_all

    path = r'C:\Users\esti7\PycharmProjects\PythonProject\image-intel\image_intel\images'
    data = extract_all(path)
    map_html = create_map(data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(map_html)
    print("המפה נוצרה! פתחי את הקובץ test_map.html בדפדפן.")
