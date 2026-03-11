from extractor import extract_all
def analyze(images_data: list[dict]) -> dict:
    res ={ "total_images":len(images_data),
         "images_with_gps":0,
         "unique_cameras":set(),
         "date_range":{"start": None, "end": None},
         "insights":[] }
    dates = []
    for img in images_data:
        if img.get('has_gps') is True:
           res ["images_with_gps"] += 1

        make = img.get('camera_make')
        model = img.get('camera_model')
        res["unique_cameras"].add(f"{make}{model}")

        dates .append(img.get('datetime'))
    res["date_range"]["start"] = min(d for d in dates if d is not None)
    res["date_range"]["end"] = max(d for d in dates if d is not None)
    insights = []
    if len (res["unique_cameras"]) > 1:
        insights.append(f"מכשירים שונים{len(res["unique_cameras"])}נמצאו")
    if res["images_with_gps"] >0:
        insights.append(f"קיימים נתוני מיקום עבור{res["images_with_gps"]}תמונות")
    res["insights"].append(str(insights))
    res["unique_cameras"] = list(res["unique_cameras"])
    return res

m = extract_all(r'C:\Users\esti7\PycharmProjects\PythonProject\image-intel\image_intel\images')
print('analyze!111!',analyze(m))
