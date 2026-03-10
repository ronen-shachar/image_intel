import piexif
import os
import sys
import json
import shutil
from PIL import Image
from datetime import datetime


SCENARIO = {
    "mission_name": "Operation Shadow Trail",
    "description": "סוכן חשוד תועד במספר מיקומים ברחבי ישראל במהלך 5 ימים. עליכם לנתח את המידע מהתמונות ולשחזר את המסלול שלו.",
    "images": [
        {
            "filename_prefix": "IMG_001",
            "gps_lat": 32.0853,
            "gps_lon": 34.7818,
            "location_name": "תל אביב - נמל",
            "datetime": "2025:01:12 08:30:00",
            "camera_make": "Samsung",
            "camera_model": "Galaxy S23",
            "comment": "פגישה ראשונה"
        },
        {
            "filename_prefix": "IMG_002",
            "gps_lat": 32.0804,
            "gps_lon": 34.7805,
            "location_name": "תל אביב - שדרות רוטשילד",
            "datetime": "2025:01:12 11:15:00",
            "camera_make": "Samsung",
            "camera_model": "Galaxy S23",
            "comment": "תנועה דרומה"
        },
        {
            "filename_prefix": "IMG_003",
            "gps_lat": 32.0667,
            "gps_lon": 34.7667,
            "location_name": "תל אביב - יפו",
            "datetime": "2025:01:12 14:00:00",
            "camera_make": "Samsung",
            "camera_model": "Galaxy S23",
            "comment": "אזור נמל יפו"
        },
        {
            "filename_prefix": "IMG_004",
            "gps_lat": 31.7683,
            "gps_lon": 35.2137,
            "location_name": "ירושלים - העיר העתיקה",
            "datetime": "2025:01:13 09:00:00",
            "camera_make": "Apple",
            "camera_model": "iPhone 15 Pro",
            "comment": "החלפת מכשיר!"
        },
        {
            "filename_prefix": "IMG_005",

            "location_name": "ירושלים - הר הזיתים",
            "datetime": "2025:01:13 12:30:00",
            "camera_make": "Apple",
            "camera_model": "iPhone 15 Pro",
            "comment": "נקודת תצפית"
        },
        {
            "filename_prefix": "IMG_006",
            "gps_lat": 31.7742,
            "gps_lon": 35.2258,
            "location_name": "ירושלים - מחנה יהודה",
            "datetime": "2025:01:13 16:45:00",
            "camera_make": "Apple",
            "camera_model": "iPhone 15 Pro",
            "comment": "פגישה שנייה"
        },
        {
            "filename_prefix": "IMG_007",
            "gps_lat": 32.7940,
            "gps_lon": 34.9896,
            "location_name": "חיפה - הכרמל",
            "datetime": "2025:01:14 10:00:00",
            "camera_make": "Apple",
            "camera_model": "iPhone 15 Pro",
            "comment": "נסיעה צפונה"
        },
        {
            "filename_prefix": "IMG_008",
            "gps_lat": 32.8115,
            "gps_lon": 34.9986,
            "location_name": "חיפה - נמל",
            "datetime": "2025:01:14 13:30:00",
            "camera_make": "Canon",
            "camera_model": "EOS R5",
            "comment": "מכשיר שלישי - מצלמה מקצועית"
        },
        {
            "filename_prefix": "IMG_009",
            "gps_lat": 31.2530,
            "gps_lon": 34.7915,
            "location_name": "באר שבע - העיר העתיקה",
            "datetime": "2025:01:15 09:30:00",
            "camera_make": "Samsung",
            "camera_model": "Galaxy S23",
            "comment": "חזרה למכשיר המקורי"
        },
        {
            "filename_prefix": "IMG_010",
            "gps_lat": 31.2620,
            "gps_lon": 34.8013,
            "location_name": "באר שבע - אוניברסיטת בן גוריון",
            "datetime": "2025:01:15 14:00:00",
            "camera_make": "Samsung",
            "camera_model": "Galaxy S23",
            "comment": "פגישה שלישית"
        },
        {
            "filename_prefix": "IMG_011",
            "gps_lat": 29.5569,
            "gps_lon": 34.9498,
            "location_name": "אילת - חוף",
            "datetime": "2025:01:16 11:00:00",
            "camera_make": "Samsung",
            "camera_model": "Galaxy S23",
            "comment": "ירידה דרומה"
        },
        {
            "filename_prefix": "IMG_012",
            "gps_lat": 29.5400,
            "gps_lon": 34.9415,
            "location_name": "אילת - נמל",
            "datetime": "2025:01:16 15:30:00",
            "camera_make": "Apple",
            "camera_model": "iPhone 15 Pro",
            "comment": "שוב החלפת מכשיר - נקודת יציאה?"
        },
    ]
}


def decimal_to_dms(decimal_degrees):
    is_negative = decimal_degrees < 0
    decimal_degrees = abs(decimal_degrees)
    degrees = int(decimal_degrees)
    minutes_float = (decimal_degrees - degrees) * 60
    minutes = int(minutes_float)
    seconds = round((minutes_float - minutes) * 60 * 10000)
    return is_negative, ((degrees, 1), (minutes, 1), (seconds, 10000))


def create_exif_data(image_info):
    lat_neg, lat_dms = decimal_to_dms(image_info["gps_lat"])
    lon_neg, lon_dms = decimal_to_dms(image_info["gps_lon"])

    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: b"S" if lat_neg else b"N",
        piexif.GPSIFD.GPSLatitude: lat_dms,
        piexif.GPSIFD.GPSLongitudeRef: b"W" if lon_neg else b"E",
        piexif.GPSIFD.GPSLongitude: lon_dms,
    }

    zeroth_ifd = {
        piexif.ImageIFD.Make: image_info["camera_make"].encode(),
        piexif.ImageIFD.Model: image_info["camera_model"].encode(),
        piexif.ImageIFD.Software: b"ImageIntel Prep Tool",
    }

    exif_ifd = {
        piexif.ExifIFD.DateTimeOriginal: image_info["datetime"].encode(),
        piexif.ExifIFD.DateTimeDigitized: image_info["datetime"].encode(),
        piexif.ExifIFD.UserComment: b"UNICODE\x00" + image_info.get("comment", "").encode("utf-16le"),
    }

    exif_dict = {
        "0th": zeroth_ifd,
        "Exif": exif_ifd,
        "GPS": gps_ifd,
        "1st": {},
    }

    return piexif.dump(exif_dict)


def inject_exif_to_images(input_dir, output_dir):
    if not os.path.isdir(input_dir):
        print(f"[ERROR] input directory not found: {input_dir}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    image_files = sorted([
        f for f in os.listdir(input_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ])

    scenario_images = SCENARIO["images"]

    if len(image_files) < len(scenario_images):
        print(f"[WARNING] found {len(image_files)} images but scenario needs {len(scenario_images)}.")
        print(f"          only first {len(image_files)} scenario entries will be used.")
        scenario_images = scenario_images[:len(image_files)]

    if len(image_files) > len(scenario_images):
        print(f"[INFO] found {len(image_files)} images, scenario has {len(scenario_images)} entries.")
        print(f"       extra images will be copied without EXIF injection.")

    print(f"\n{'='*50}")
    print(f"  Operation Shadow Trail - EXIF Injection")
    print(f"{'='*50}\n")

    for i, (img_file, img_info) in enumerate(zip(image_files, scenario_images)):
        src_path = os.path.join(input_dir, img_file)
        ext = os.path.splitext(img_file)[1]

        if ext.lower() == ".png" or ext.lower() == ".webp":
            print(f"[CONVERT] {img_file} -> converting to JPEG for EXIF support")
            img = Image.open(src_path).convert("RGB")
            new_filename = f"{img_info['filename_prefix']}.jpg"
            dst_path = os.path.join(output_dir, new_filename)
            img.save(dst_path, "JPEG", quality=95)
        else:
            new_filename = f"{img_info['filename_prefix']}{ext}"
            dst_path = os.path.join(output_dir, new_filename)
            shutil.copy2(src_path, dst_path)

        exif_bytes = create_exif_data(img_info)
        piexif.insert(exif_bytes, dst_path)

        print(f"[OK] {img_file} -> {new_filename}")
        print(f"     Location: {img_info['location_name']}")
        print(f"     Date: {img_info['datetime']}")
        print(f"     Camera: {img_info['camera_make']} {img_info['camera_model']}")
        print()

    for img_file in image_files[len(scenario_images):]:
        src_path = os.path.join(input_dir, img_file)
        dst_path = os.path.join(output_dir, img_file)
        shutil.copy2(src_path, dst_path)
        print(f"[COPY] {img_file} (no EXIF injection)")

    scenario_file = os.path.join(output_dir, "scenario_answer_key.json")
    answer_key = {
        "mission": SCENARIO["mission_name"],
        "description": SCENARIO["description"],
        "timeline": []
    }
    for info in scenario_images:
        answer_key["timeline"].append({
            "file": f"{info['filename_prefix']}.jpg",
            "location": info["location_name"],
            "datetime": info["datetime"],
            "camera": f"{info['camera_make']} {info['camera_model']}",
            "note": info["comment"]
        })

    with open(scenario_file, "w", encoding="utf-8") as f:
        json.dump(answer_key, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"  Done! {len(scenario_images)} images processed.")
    print(f"  Output: {output_dir}")
    print(f"  Answer key: {scenario_file}")
    print(f"{'='*50}")
    print(f"\n  IMPORTANT: Don't upload scenario_answer_key.json to the student repo!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inject_exif.py <input_folder> [output_folder]")
        print()
        print("Example:")
        print("  python inject_exif.py ./my_photos ./ready_images")
        print()
        print("The script takes your photos and injects EXIF metadata")
        print("based on the 'Operation Shadow Trail' scenario.")
        print(f"You need at least {len(SCENARIO['images'])} images (have more? that's fine).")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(input_dir, "output")

    inject_exif_to_images(input_dir, output_dir)
