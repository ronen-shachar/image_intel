from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
from geopy.geocoders import Nominatim

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.
"""

geolocator = Nominatim(user_agent="image_intel")


def has_gps(data: dict):
    for i in data.keys():
        if i == 'GPSInfo':
            return True
    return False


def latitude(data: dict):
    try:
        north = data['GPSInfo'][2]
        return float(north[0] + (north[1] / 60) + (north[2] / 3600))
    except Exception:
        return None


def longitude(data: dict):
    try:
        east = data['GPSInfo'][4]
        return float(east[0] + (east[1] / 60) + (east[2] / 3600))
    except Exception:
        return None


def datatime(data: dict):
    try:
        return data['DateTimeOriginal'].replace(':', "-", 2)
    except Exception:
        return None


def camera_make(data: dict):
    try:
        return data['Make']
    except Exception:
        return None


def camera_model(data: dict):
    try:
        return data['Model']
    except Exception:
        return None


def location(data: dict):
    try:
        lat = latitude(data)
        lon = longitude(data)

        if lat is None or lon is None:
            return None

        my_location = geolocator.reverse((lat, lon))

        if my_location is None:
            return None

        address = my_location.raw.get("address", {})

        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
        )

        extra_place = (
            address.get("road")
            or address.get("suburb")
            or address.get("neighbourhood")
            or address.get("quarter")
        )

        if city and extra_place:
            return f"{city} - {extra_place}"

        if city:
            return city

        return None

    except Exception:
        return None


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.

    Args:
        image_path: נתיב לקובץ תמונה

    Returns:
        dict עם: filename, datetime, latitude, longitude,
        camera_make, camera_model, has_gps, location
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
            "has_gps": False,
            "location": None
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
        "has_gps": has_gps(data),
        "location": location(data)
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
    all_exif_list = []
    python_files = list(Path(folder_path).glob('*.jpg'))

    for file in python_files:
        all_exif_list.append(extract_metadata(file))

    return all_exif_list