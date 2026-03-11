from extractor import extract_all
from map_view import sort_by_time
from geopy.geocoders import Nominatim
import time


def get_date_time_range(images_data):
    images_with_datetime = [image for image in images_data if image.get('datetime')]
    if len(images_with_datetime) == 0:
        return {'range': 'not enough data to find time range'}
    elif len(images_with_datetime) == 1:
        return {'start': images_with_datetime[0]['datetime'], 'end': 'not enough data for ending range'}
    else:
        return {'start': images_with_datetime[0]['datetime'], 'end': images_with_datetime[-1]['datetime']}

def get_total_images(images_data):
    return len(images_data)

def get_images_with_gps(images_data):
    return sum(1 for image in images_data if image.get('latitude'))

def get_unique_cameras(images_data):
    # מחזיר סט של מצלמות או סט ריק אם אין
    unique_cameras = {
        f"{image['camera_make']} {image['camera_model']}"
        for image in images_data
        if image.get('camera_make') and image.get('camera_model')
    }
    return unique_cameras  # עדיף להחזיר מבנה נתונים ריק מאשר טקסט שגיאה

def get_device_changes(images_data):
    change_dates = []
    i = 1
    while i < len(images_data):
        current = images_data[i]
        prev = images_data[i - 1]

        curr_device = f"{current.get('camera_make')} {current.get('camera_model')}"
        prev_device = f"{prev.get('camera_make')} {prev.get('camera_model')}"

        # בדיקה ששני המכשירים קיימים והם שונים
        if current.get('camera_make') and prev.get('camera_make'):
            if curr_device != prev_device:
                change_time = current.get('datetime', 'Unknown Date')
                change_dates.append(
                    f"Device changed on {change_time} from {prev_device} to {curr_device}"
                )
        i += 1

    if not change_dates:
        return ["no device changes found"]
    return change_dates

def get_area_name(lat, lon):
    try:
        geolocator = Nominatim(user_agent="my_image_intel_project_v1")
        location = geolocator.reverse((lat, lon), language='en', timeout=1)
        if location:
            address = location.raw.get('address', {})
            city = address.get('city') or address.get('town') or address.get('village') or "Unknown Area"
            return city
    except Exception:
        return "Area (Service Offline)"
    return "Unknown Area"

def get_location_clusters(images_data):
    clusters = {}
    for img in images_data:
        lat = img.get('latitude')
        lon = img.get('longitude')
        if lat and lon:
            # עיגול לספרה אחת (כ-11 ק"מ) כדי לתפוס אזור עירוני שלם
            location_key = (round(lat, 1), round(lon, 1))
            clusters[location_key] = clusters.get(location_key, 0) + 1
    return clusters

def get_area_insights(images_data):
    insights = []
    clusters = get_location_clusters(images_data)

    for (lat, lon), count in clusters.items():
        if count >= 3:
            city_name = get_area_name(lat, lon)
            insights.append(f"Detected concentration of {count} images in {city_name}")
            time.sleep(1)  # הגנה מחסימה

    if not insights:
        return ['no area clusters detected']
    return insights

def get_insights(images_data):
    insight_list = []

    unique_devices = get_unique_cameras(images_data)
    count_devices = len(unique_devices)
    if count_devices > 0:
        insight_list.append(f"Unique devices found: {count_devices}")
    else:
        insight_list.append("No camera metadata found in images")

    device_changes = get_device_changes(images_data)
    if device_changes and "no device changes found" in device_changes[0]:
        if count_devices == 1:
            insight_list.append("all images were taken with the same device")
        else:
            insight_list.append("No device changes detected between images.")
    else:
        insight_list.extend(device_changes)

    area_notices = get_area_insights(images_data)
    if area_notices and "no area clusters detected" in area_notices[0]:
        insight_list.append("no significant concentrations of images found")
    else:
        insight_list.extend(area_notices)

    return insight_list

def analyze(images_data):
    if not isinstance(images_data, list) or len(images_data) == 0:
        return {
            'total_images': 0,
            'images_with_gps': 0,
            'unique_cameras': [],
            'date_range': {'range': 'No valid images found'},
            'insights': ['The analyzer received no images to process. Check the folder path.']
        }

    images_data = sort_by_time(images_data)

    return {
        'total_images': get_total_images(images_data),
        'images_with_gps': get_images_with_gps(images_data),
        'unique_cameras': list(get_unique_cameras(images_data)),
        'date_range': get_date_time_range(images_data),
        'insights': get_insights(images_data)
    }
