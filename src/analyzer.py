from extractor import extract_all
from map_view import sort_by_time
from geopy.geocoders import Nominatim
import time


def get_date_time_range(images_data):
    images_with_datetime = [image for image in images_data if image.get('datetime')]
    if len(images_with_datetime) == 0:
        return {'range': 'אין מספיק נתונים למציאת טווח זמנים'}
    elif len(images_with_datetime) == 1:
        return {'start': images_with_datetime[0]['datetime'], 'end': 'אין מספיק נתונים לסיום הטווח'}
    else:
        return {'start': images_with_datetime[0]['datetime'], 'end': images_with_datetime[-1]['datetime']}

def get_total_images(images_data):
    return len(images_data)

def get_images_with_gps(images_data):
    return sum(1 for image in images_data if image.get('latitude'))

def get_unique_cameras(images_data):
    unique_cameras = {
        f"{image['camera_make']} {image['camera_model']}"
        for image in images_data
        if image.get('camera_make') and image.get('camera_model')
    }
    return unique_cameras

def get_device_changes(images_data):
    change_dates = []
    i = 1
    while i < len(images_data):
        current = images_data[i]
        prev = images_data[i - 1]

        curr_device = f"{current.get('camera_make')} {current.get('camera_model')}"
        prev_device = f"{prev.get('camera_make')} {prev.get('camera_model')}"

        if current.get('camera_make') and prev.get('camera_make'):
            if curr_device != prev_device:
                change_time = current.get('datetime', 'תאריך לא ידוע')
                change_dates.append(
                    f"החלפת מכשיר בתאריך {change_time} מ-{prev_device} ל-{curr_device}"
                )
        i += 1

    if not change_dates:
        return ["לא נמצאו החלפות מכשירים"]
    return change_dates

def get_area_name(lat, lon):
    try:
        geolocator = Nominatim(user_agent="my_image_intel_project_v1")
        location = geolocator.reverse((lat, lon), language='he', timeout=1) # שונה לעברית
        if location:
            address = location.raw.get('address', {})
            city = address.get('city') or address.get('town') or address.get('village') or "אזור לא ידוע"
            return city
    except Exception:
        return "אזור (שירות לא זמין)"
    return "אזור לא ידוע"

def get_location_clusters(images_data):
    clusters = {}
    for img in images_data:
        lat = img.get('latitude')
        lon = img.get('longitude')
        if lat and lon:
            location_key = (round(lat, 1), round(lon, 1))
            clusters[location_key] = clusters.get(location_key, 0) + 1
    return clusters

def get_area_insights(images_data):
    insights = []
    clusters = get_location_clusters(images_data)

    for (lat, lon), count in clusters.items():
        if count >= 3:
            city_name = get_area_name(lat, lon)
            insights.append(f"זוהה ריכוז של {count} תמונות באזור {city_name}")
            time.sleep(1)

    if not insights:
        return ['לא זוהו ריכוזי מיקום משמעותיים']
    return insights

def get_insights(images_data):
    insight_list = []

    unique_devices = get_unique_cameras(images_data)
    count_devices = len(unique_devices)
    if count_devices > 0:
        insight_list.append(f"מספר מכשירים ייחודיים שנמצאו: {count_devices}")
    else:
        insight_list.append("לא נמצא מידע על דגם המצלמה בתמונות")

    device_changes = get_device_changes(images_data)
    if device_changes and "לא נמצאו החלפות מכשירים" in device_changes[0]:
        if count_devices == 1:
            insight_list.append("בדיקת עקביות: כל התמונות צולמו באותו מכשיר")
        else:
            insight_list.append("לא זוהו החלפות מכשירים בין תמונות עוקבות")
    else:
        insight_list.extend(device_changes)

    area_notices = get_area_insights(images_data)
    if area_notices and "לא זוהו ריכוזי מיקום משמעותיים" in area_notices[0]:
        insight_list.append("ניתוח מיקום: לא נמצאו ריכוזים משמעותיים, המיקומים מפוזרים")
    else:
        insight_list.extend(area_notices)

    return insight_list

def analyze(images_data):
    if not isinstance(images_data, list) or len(images_data) == 0:
        return {
            'total_images': 0,
            'images_with_gps': 0,
            'unique_cameras': [],
            'date_range': {'range': 'לא נמצאו תמונות תקינות'},
            'insights': ['האנלייזר לא קיבל תמונות לעיבוד. בדוק את נתיב התיקייה.']
        }

    images_data = sort_by_time(images_data)

    return {
        'total_images': get_total_images(images_data),
        'images_with_gps': get_images_with_gps(images_data),
        'unique_cameras': list(get_unique_cameras(images_data)),
        'date_range': get_date_time_range(images_data),
        'insights': get_insights(images_data)
    }