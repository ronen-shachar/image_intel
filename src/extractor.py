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
    return "GPSInfo" in data


def latitude(data: dict):
    gps = data.get("GPSInfo")[2]
    ref = data.get("GPSInfo")[1]

    if not gps:
        return None

    degrees = gps[0]
    minutes = gps[1] / 60.0
    seconds = gps[2] / 3600.0

    decimal = degrees + minutes + seconds
    if ref != "N":
        decimal = -decimal
    return round(decimal, 6)


def longitude(data: dict):
    gps = data.get("GPSInfo")[4]
    ref = data.get("GPSInfo")[3]

    if not gps:
        return None

    degrees = gps[0]
    minutes = gps[1] / 60.0
    seconds = gps[2] / 3600.0

    decimal = degrees + minutes + seconds
    if ref != "E":
        decimal = -decimal
    return round(decimal, 6)

def datatime(data: dict):

    return data.get("DateTimeOriginal") or data.get("DateTime")


def camera_make(data: dict):
    if not data:
        return None
    return data.get('Make')


def camera_model(data: dict):
    if not data:
        return None
    return data.get('Model')


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.

    Args:
        image_path: נתיב לקובץ תמונה

    Returns:
        dict עם: filename, datetime, latitude, longitude,
              camera_make, camera_model, has_gps
    """
    path = Path(image_path)

    # תיקון: טיפול בתמונה בלי EXIF - בלי זה, exif.items() נופל עם AttributeError
    try:
        img = Image.open(image_path)
        exif = img.getexif()
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

    inner_exif = exif.get_ifd(0x8769)
    for tag_id, value in inner_exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

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


def extract_all(folder_path):
    """
    שולף EXIF מכל התמונות בתיקייה.

    Args:
        folder_path: נתיב לתיקייה

    Returns:
        list של dicts (כמו extract_metadata)
    """
    jpg_list=[]
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".jpg"):
            full_path = os.path.join(folder_path, filename)
            metadata = extract_metadata(full_path)
            jpg_list.append(metadata)
    return jpg_list
