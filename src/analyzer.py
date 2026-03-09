



def gps_count(list_of_images):
    return sum(i["has_gps"] for i in list_of_images)




















def date_range(list_of_images):
    sorted_list = sorted(list_of_images, key=lambda x: x["datetime"])
    return {"start" : sorted_list[0]["datetime"],"end": sorted_list[-1]["datetime"]}


def detect_camera_switches(images_data):
    sorted_images = sorted(
        [img for img in images_data if img["datetime"]],
        key=lambda x: x["datetime"]
    )
    switches = []
    for i in range(1, len(sorted_images)):
        prev_cam = sorted_images[i-1].get("camera_model")
        curr_cam = sorted_images[i].get("camera_model")
        if prev_cam and curr_cam and prev_cam != curr_cam:
            switches.append({
                "date": sorted_images[i]["datetime"],
                "from": prev_cam,
                "to": curr_cam
            })
    return switches







