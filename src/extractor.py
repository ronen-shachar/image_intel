from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""


def dms_to_decimal(dms_tuple, ref):
    degrees = dms_tuple[0]
    minutes = dms_tuple[1]
    seconds = dms_tuple[2]
    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in [b'S', b'W', 'S', 'W']:
        decimal = -decimal
    return decimal


def has_gps(data: dict):
    return "GPSInfo" in data


def latitude(data: dict):
    try:
        gps = data.get("GPSInfo", {})
        return dms_to_decimal(gps[2], gps[1])
    except (KeyError, IndexError, TypeError):
        return None


def longitude(data: dict):
    try:
        gps = data.get("GPSInfo", {})
        return dms_to_decimal(gps[4], gps[3])
    except (KeyError, IndexError, TypeError):
        return None


def datatime(data: dict):
    return data.get("DateTimeOriginal")


def camera_make(data: dict):
    return data.get("Make")


def camera_model(data: dict):
    return data.get("Model")


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
    folder = Path(folder_path)
    return [extract_metadata(img) for img in [file for file in folder.iterdir() if file.is_file()]]
