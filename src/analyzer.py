from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def total_images(list_of_images):
    return len(list_of_images)


def gps_count(list_of_images):
    return sum(i["has_gps"] for i in list_of_images)


def images_with_datetime(list_of_images):
    count = 0
    for i in list_of_images:
        if i["datetime"]:
            count += 1
    return count


def date_range(list_of_images):
    sorted_list = sorted(list_of_images, key=lambda x: x["datetime"])
    return {"start": sorted_list[0]["datetime"], "end": sorted_list[-1]["datetime"]}


def unique_cameras(list_of_images):
    unique_list = []
    final_list = []
    for i in list_of_images:
        if i["camera_model"] not in unique_list:
            unique_list.append(i["camera_model"])
            final_list.append(f"{i["camera_make"]} {i["camera_model"]}")
    return final_list


def detect_camera_switches(images_data):
    sorted_images = sorted(
        [img for img in images_data if img["datetime"]],
        key=lambda x: x["datetime"]
    )
    switches = []
    for i in range(1, len(sorted_images)):
        prev_cam = sorted_images[i - 1].get("camera_model")
        curr_cam = sorted_images[i].get("camera_model")
        if prev_cam and curr_cam and prev_cam != curr_cam:
            switches.append({
                "date": sorted_images[i]["datetime"],
                "from": prev_cam,
                "to": curr_cam
            })
    return switches


def image_location(list_of_images):
    name_with_location={img["filename"]:(float(img["latitude"]),float(img["longitude"])) for img in list_of_images}
    return name_with_location


def back_to_location(name_with_location):
    list_of_locations = []
    for k, v in name_with_location.items():
        location = v
        tamp_loc = {v: 1}
        for k_1, v_1 in name_with_location.items():
            location_1 = v_1
            if location == location_1 and k != k_1:
                tamp_loc[v] += 1
        if tamp_loc[v] > 1:
            if tamp_loc not in list_of_locations:
                list_of_locations.append(tamp_loc)
    return list_of_locations


def is_within_1km(image_loc):
    list_within_1km = []
    for k,v in image_loc.items():
        location = v
        tamp_list = [location]
        for key,value in image_loc.items():
            location1 = value
            if key == k:
                continue
            distance = geodesic(location, location1).kilometers
            if distance <= 1:
                tamp_list.append(location1)
        if len(tamp_list) > 1:
            sorted_list=sorted(tamp_list)
            if sorted_list not in list_within_1km:
                list_within_1km.append(sorted_list)
    return list_within_1km





#מקבל מ is_within_1km
def get_city_name(location_list:list):
    city_list=[]
    for i in location_list:
        loc=i[1]
        lat,lon=loc[0],loc[1]

        #צריך שם של משתמש
        geolocator = Nominatim(user_agent="my_image_intel_app")
        location = geolocator.reverse((lat, lon), language='he')

        if location and 'address' in location.raw:
            address = location.raw['address']
            city = address.get('city') or address.get('town') or address.get('village')
            city_list.append(f"ב {city} צולמו {len(i):,} תמונות")
        else:
            return "unknown"
    return city_list




def total_analyzer(list_of_dicts):
    final_dict={"total_images":total_images(list_of_dicts),
    "images_with_gps": gps_count(list_of_dicts),
    "images_with_datetime": images_with_datetime(list_of_dicts),
    "unique_cameras": unique_cameras(list_of_dicts),
    "date_range": date_range(list_of_dicts),
    "insights": }
