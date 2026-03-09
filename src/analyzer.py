def total_images(list_of_images):
    return len(list_of_images)






def images_with_datetime(list_of_images):
    count = 0
    for i in list_of_images:
        if i["datetime"]:
            count += 1
    return count


def unique_cameras(list_of_images):
    unique_list = []
    final_list = []
    for i in list_of_images:
        if i["camera_model"] not in unique_list:
            unique_list.append(i["camera_model"])
            final_list.append(f"{i["camera_make"]} {i["camera_model"]}")
    return final_list







