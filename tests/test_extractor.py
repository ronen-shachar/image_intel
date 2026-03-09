from PIL import Image
import piexif
import os

# פונקציה לעזור להמיר GPS למעלות עשרוניות
def convert_to_degrees(value, ref):
    deg = value[0][0] / value[0][1]
    minute = value[1][0] / value[1][1]
    sec = value[2][0] / value[2][1]
    result = deg + (minute / 60.0) + (sec / 3600.0)
    if ref in ['S','W']:
        result = -result
    return result

# פונקציה שמוציאה את כל המידע מתמונה אחת
def extract_metadata(image_path: str) -> dict:
    data = {
        "filename": os.path.basename(image_path),
        "datetime": None,
        "latitude": None,
        "longitude": None,
        "camera_make": None,
        "camera_model": None,
        "has_gps": False
    }

    try:
        # פתיחת התמונה
        img = Image.open(image_path)
        exif_bytes = img.info.get("exif", b"")
        if not exif_bytes:
            return data

        exif_dict = piexif.load(exif_bytes)

        # מצלמה
        make = exif_dict["0th"].get(piexif.ImageIFD.Make)
        model = exif_dict["0th"].get(piexif.ImageIFD.Model)
        if make:
            data["camera_make"] = make.decode()
        if model:
            data["camera_model"] = model.decode()

        # תאריך ושעה
        datetime = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
        if datetime:
            data["datetime"] = datetime.decode()

        # GPS
        gps_ifd = exif_dict.get("GPS", {})
        if gps_ifd:
            data["has_gps"] = True
            gps_latitude = gps_ifd.get(piexif.GPSIFD.GPSLatitude)
            gps_latitude_ref = gps_ifd.get(piexif.GPSIFD.GPSLatitudeRef)
            gps_longitude = gps_ifd.get(piexif.GPSIFD.GPSLongitude)
            gps_longitude_ref = gps_ifd.get(piexif.GPSIFD.GPSLongitudeRef)

            if gps_latitude and gps_latitude_ref:
                data["latitude"] = convert_to_degrees(gps_latitude, gps_latitude_ref.decode())

            if gps_longitude and gps_longitude_ref:
                data["longitude"] = convert_to_degrees(gps_longitude, gps_longitude_ref.decode())

    except Exception as e:
        print("Error:", e)

    return data



# שימוש על תמונה אחת בתיקייה images/ready
metadata = extract_metadata("../images/ready/IMG_001.jpg")
print(metadata)

