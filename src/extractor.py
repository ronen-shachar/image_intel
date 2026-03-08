from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""


def clean_value(val):
    if isinstance(val, str):
        return val.strip('\x00').strip()
    return val


def dms_to_decimal(dms_tuple, ref):
    degrees = dms_tuple[0][0] / dms_tuple[0][1]
    minutes = dms_tuple[1][0] / dms_tuple[1][1]
    seconds = dms_tuple[2][0] / dms_tuple[2][1]
    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in [b'S', b'W', 'S', 'W']:
        decimal = -decimal
    return decimal


def has_gps(data: dict):
    return "GPSInfo" in data


def latitude(data: dict):
    gps_info = data.get("GPSInfo")
    if gps_info and 2 in gps_info:
        return dms_to_decimal(gps_info[2], gps_info.get(1))
    return None



def longitude(data: dict):
    gps_info = data.get("GPSInfo")
    if gps_info and 4 in gps_info:
        return dms_to_decimal(gps_info[4], gps_info.get(3))
    return None

def datatime(data: dict):
    dt = data.get("DateTimeOriginal") or data.get("DateTime")
    return str(dt) if dt else None



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

    exif_dict = {
        "filename": path.name,
        "datetime": clean_value(datatime(data)),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": clean_value(camera_make(data)),
        "camera_model": clean_value(camera_model(data)),
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
    results = []
    base_path = Path(folder_path)
    supported_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif', '.tiff', '.bmp'}
    if not base_path.is_dir():
        return results
    for file_path in base_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            try:
                metadata = extract_metadata(str(file_path))
                results.append(metadata)
            except Exception:
                continue
    return results

