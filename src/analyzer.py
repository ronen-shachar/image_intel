from map_view import sort_by_time
from geopy.geocoders import Nominatim
import time

def get_date_time_range(images_data):
    images_with_datetime = [image for image in images_data if image.get('datetime')]
    if len(images_with_datetime) == 0:
        datetime_range = {'range' : 'not enough data to find time range'}
    elif len(images_with_datetime) == 1:
        datetime_range = {'start' : images_with_datetime[0]['datetime'], 'end' : 'not enough data for ending range'}
    else:
        datetime_range = {'start' : images_with_datetime[0]['datetime'], 'end' : images_with_datetime[-1]['datetime']}
    return datetime_range

def get_total_images(images_data):
    return len(images_data)

def get_images_with_gps(images_data):
    return sum(1 for image in images_data if image.get('latitude'))

def get_unique_cameras(images_data):
    unique_cameras =  {image['camera_make'] + ' ' + image['camera_model'] for image in images_data if image['camera_make'] and image['camera_model']}
    if not unique_cameras:
        return 'no camera data data found'
    return unique_cameras


def get_device_changes(images_data):
    change_dates = []
    i = 1
    while i < len(images_data):
        current = images_data[i]
        prev = images_data[i - 1]

        curr_make = current.get('camera_make')
        curr_model = current.get('camera_model')
        prev_make = prev.get('camera_make')
        prev_model = prev.get('camera_model')

        if curr_make and curr_model and prev_make and prev_model:
            if (curr_make + curr_model) != (prev_make + prev_model):
                change_time = current.get('datetime', 'Unknown Date')

                change_dates.append(
                    f"device changed in {change_time} from {prev_make} {prev_model} to {curr_make} {curr_model}"
                )
        i += 1

    if not change_dates:
        return ["no device changes found"]
    return change_dates


def get_area_name(lat, lon):
    """
    הופך קואורדינטות לשם של עיר/יישוב (דורש אינטרנט).
    """
    try:
        # הגדרת סוכן משתמש (חובה לפי תנאי השימוש של השירות)
        geolocator = Nominatim(user_agent="my_image_intel_project_v1")

        # בקשת המיקום מהשרת
        location = geolocator.reverse((lat, lon), language='en', timeout=1)

        if location:
            address = location.raw.get('address', {})
            # חיפוש הדרגתי: עיר -> עיירה -> כפר
            city = address.get('city') or address.get('town') or address.get('village') or "Unknown Area"
            return city
    except Exception:
        return "Area (Service Offline)"
    return "Unknown Area"

def get_location_clusters(images_data):
    """
    מקבץ תמונות לפי מיקום גאוגרפי קרוב (עיגול ל-2 ספרות עשרוניות).
    """
    clusters = {}
    for img in images_data:
        lat = img.get('latitude')
        lon = img.get('longitude')
        if lat and lon:
            # עיגול ל-2 ספרות נותן רדיוס של כ-1.1 ק"מ
            location_key = (round(lat, 1), round(lon, 1))
            clusters[location_key] = clusters.get(location_key, 0) + 1
    return clusters


def get_area_insights(images_data):
    """
    מייצרת תובנות על ריכוזי תמונות בכל מקום בעולם.
    """
    insights = []
    clusters = get_location_clusters(images_data)

    for (lat, lon), count in clusters.items():
        if count >= 3:  # הגדרת "ריכוז" כ-3 תמונות ומעלה
            city_name = get_area_name(lat, lon)
            insights.append(f"Detected concentration of {count} images in {city_name}")
            # השהייה קלה כדי לא להיחסם מהשרת (חוקי ה-API של Nominatim)
            time.sleep(1)
    if len(insights) == 0:
        return ['no area clusters detected']
    return insights


def get_insights(images_data):
    insight_list = []

    unique_devices = get_unique_cameras(images_data)
    count_devices = len(unique_devices)
    if count_devices > 0:
        insight_list.append(f"unique devices found: {count_devices}")

    device_changes = get_device_changes(images_data)
    if device_changes and device_changes[0] != "no devices changes found":
        insight_list.extend(device_changes)

    area_notices = get_area_insights(images_data)
    insight_list.extend(area_notices)

    return insight_list

def analyze(images_data):
    if len(images_data) == 0:
        return 'no images in file'
    images_data = sort_by_time(images_data)
    insight_dict = {'total_images' : get_total_images(images_data),
                    'images_with_gps' : get_images_with_gps(images_data),
                    'unique_cameras' : get_unique_cameras(images_data),
                    'date_range' : get_date_time_range(images_data),
                    'insights' : get_insights(images_data)}
    return insight_dict

