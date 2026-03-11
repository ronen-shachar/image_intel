from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta


# סך תמונות
def total_images(list_of_images):
    return len(list_of_images)


# סך תמונות עם gps
def gps_count(list_of_images):
    return sum(i["has_gps"] for i in list_of_images)


def images_with_datetime(list_of_images):
    count = 0
    for i in list_of_images:
        if i["datetime"]:
            count += 1
    return count


# טווח
def date_range(list_of_images):
    sorted_list = sorted(list_of_images, key=lambda x: x["datetime"])
    return {"start": sorted_list[0]["datetime"], "end": sorted_list[-1]["datetime"]}


# מכשירים שונים
def unique_cameras(list_of_images):
    unique_list = []
    final_list = []
    for i in list_of_images:
        if i["camera_model"] not in unique_list:
            unique_list.append(i["camera_model"])
            final_list.append(f"{i["camera_make"]} {i["camera_model"]}")
    return final_list


# בודק החלפת מכשירים
def detect_camera_switches(list_of_images):
    sorted_images = sorted(
        [img for img in list_of_images if img["datetime"]],
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


# יוצר מילון של {שם : (מיקום_א, מיקום_ר)}
def image_location(list_of_images):
    name_with_location = {img["filename"]: (float(img["latitude"]), float(img["longitude"])) for img in list_of_images}
    return name_with_location


# פונקציה לבדיקת חזרה למקום
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


# מקבל מ image_location
def is_within_1km(image_loc):
    list_within_1km = []
    for k, v in image_loc.items():
        location = v
        tamp_list = [location]
        for key, value in image_loc.items():
            location1 = value
            if key == k:
                continue
            distance = geodesic(location, location1).kilometers
            if distance <= 1:
                tamp_list.append(location1)
        if len(tamp_list) > 1:
            sorted_list = sorted(tamp_list)
            if sorted_list not in list_within_1km:
                list_within_1km.append(sorted_list)
    return list_within_1km


# מקבל מ is_within_1km
def get_city_name(location_list: list):
    city_list = []
    for i in location_list:
        loc = i[1]
        lat, lon = loc[0], loc[1]

        # צריך שם של משתמש
        geolocator = Nominatim(user_agent="my_image_intel_app")
        location = geolocator.reverse((lat, lon), language='he')

        if location and 'address' in location.raw:
            address = location.raw['address']
            city = address.get('city') or address.get('town') or address.get('village')
            city_list.append(f"ב {city} צולמו {len(i):,} תמונות")
        else:
            return "unknown"
    return city_list


# פונקציה שמוציאה רשימה של פערי זמו >12 שעות
def time_gap(list_of_images):
    s_list = sorted(list_of_images, key=lambda x: x["datetime"])
    gap_list = []
    fmt = '%Y:%m:%d %H:%M:%S'
    for i in range(len(s_list) - 1):
        threshold = timedelta(hours=12)
        t1 = datetime.strptime(s_list[i]["datetime"], fmt)
        t2 = datetime.strptime(s_list[i + 1]["datetime"], fmt)
        gap = abs(t1 - t2)
        if gap >= threshold:
            gap_list.append(f"הפער בין {s_list[i]["filename"]} ל-{s_list[i + 1]["filename"]} הוא {gap}")
    return gap_list


def total_analyzer(list_of_dicts):
    final_dict = {"total_images": total_images(list_of_dicts),
                  "images_with_gps": gps_count(list_of_dicts),
                  "images_with_datetime": images_with_datetime(list_of_dicts),
                  "unique_cameras": unique_cameras(list_of_dicts),
                  "date_range": date_range(list_of_dicts),
                  "insights": []}
    # בדיקת מכשירים שונים
    cameras_count = len(unique_cameras(list_of_dicts))
    if len(unique_cameras(list_of_dicts)) > 1:
        final_dict["insights"].append(f"נמצאו ({cameras_count}) מכשירים שונים - ייתכן שהסוכן החליף מכשירים")

        # בדיקת החלפת מכשירים
        switch_devices = detect_camera_switches(list_of_dicts)
        tamp_list = []
        for i in switch_devices:
            date = i["date"]
            from1 = i["from"]
            to = i["to"]
            c_date = f"{date[8:10]}/{date[5:7]}"
            msg1 = f"ב-{c_date} הסוכן עבר ממכשיר {from1} למכשיר {to}"
            tamp_list.append(msg1)
        for sen in tamp_list:
            final_dict["insights"].append(f"{sen}")

    # יוצר מילון של {שם : (מיקום_א, מיקום_ר)}
    name_with_location_dict = image_location(list_of_dicts)

    # בדיקת חזרה למקום
    return_to_location = back_to_location(name_with_location_dict)
    if return_to_location:
        for item in return_to_location:
            for cords, count in item.items():
                msg = f"הסוכן צילם באותו מקום {cords} {count} פעמים"
                final_dict["insights"].append(msg)

    # בדיקת מיקומים קרובים
    location_cluster_list = is_within_1km(name_with_location_dict)

    cluster_sen_list = get_city_name(location_cluster_list)
    if len(cluster_sen_list) > 0:
        for sen in cluster_sen_list:
            final_dict["insights"].append(f"{sen}")

    # בדיקת פערי זמן
    time_gaps = time_gap(list_of_dicts)
    if len(time_gaps) > 0:
        for sen in time_gaps:
            final_dict["insights"].append(f"{sen}")

    return final_dict
