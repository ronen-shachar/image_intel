from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""


def has_gps(data: dict):
    if "GPSInfo" in data:
        return True
    return False


def convert_to_decimal(values):
    """פונקציית עזר להמרת DMS (מעלות, דקות, שניות) למספר עשרוני"""
    try:
        # פונקציה פנימית לחילוץ ערך (מטפל במקרה של (32, 1) או פשוט 32)
        def get_val(v):
            if isinstance(v, tuple) or isinstance(v, list):
                return float(v[0]) / float(v[1])
            return float(v)

        deg = get_val(values[0])
        min = get_val(values[1])
        sec = get_val(values[2])

        return deg + (min / 60.0) + (sec / 3600.0)
    except (IndexError, ZeroDivisionError, TypeError):
        return None


def latitude(data: dict):
    if "GPSInfo" not in data:
        return None

    gps_info = data["GPSInfo"]
    # מפתח 2 הוא Latitude, מפתח 1 הוא Ref
    lat_values = gps_info.get(2)
    lat_ref = gps_info.get(1)

    if not lat_values or not lat_ref:
        return None

    lat_decimal = convert_to_decimal(lat_values)
    if lat_decimal is not None and lat_ref == 'S':
        lat_decimal = -lat_decimal
    return lat_decimal


def longitude(data: dict):
    if "GPSInfo" not in data:
        return None

    gps_info = data["GPSInfo"]
    # מפתח 4 הוא Longitude, מפתח 3 הוא Ref
    lon_values = gps_info.get(4)
    lon_ref = gps_info.get(3)

    if not lon_values or not lon_ref:
        return None

    lon_decimal = convert_to_decimal(lon_values)
    if lon_decimal is not None and lon_ref == 'W':
        lon_decimal = -lon_decimal
    return lon_decimal

def datatime(data: dict):
    if "DateTime" not in data:
        return None
    return data.get("DateTime")

def camera_make(data: dict):
    make = data.get("Make")
    return make.strip('\x00').strip() if make else None


def camera_model(data: dict):
     model = data.get('Make')
     return model.strip('\x00').strip() if model else None
def extract_metadata(image_path):
    path = Path(image_path)
    # תיקון: טיפול בתמונה בלי EXIF - בלי זה, exif.items() נופל עם AttributeError
    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    # תיקון: הוסר print(data) שהיה כאן - הדפיס את כל ה-EXIF הגולמי על כל תמונה

    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }
    return exif_dict

def extract_all(folder_path: str) -> list[dict]:
    results = []
    path = Path(folder_path)
    if not path.is_dir():
        print(f"אזהרה: התיקייה {folder_path} לא נמצאה.")
        return []
    for file_path in path.iterdir():
        if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            data = extract_metadata(str(file_path))
            results.append(data)

    return results
print(extract_all ( r'C:\Users\esti7\PycharmProjects\PythonProject\image-intel\image_intel\images'))
