from extractor import extract_all
from pathlib import Path
from datetime import datetime


def clean_text(value, default="Unknown"):
    if not value:
        return default
    return str(value).replace("\x00", "").strip()


def format_datetime(value):
    if not value:
        return "N/A"

    try:
        dt = datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d %b %Y • %H:%M")
    except Exception:
        return str(value)


def format_location(value):
    if not value:
        return "Location does not exist."
    return str(value)


def build_device_name(img):
    make = clean_text(img.get("camera_make"), "")
    model = clean_text(img.get("camera_model"), "")

    full_name = f"{make} {model}".strip()

    if not full_name:
        return "Unknown"
    return full_name


def get_device_logo_html(img):
    make = clean_text(img.get("camera_make"), "").lower()
    model = clean_text(img.get("camera_model"), "").lower()
    text = f"{make} {model}"

    if "apple" in text or "iphone" in text:
        return '<img src="../src/static/logos/apple.png" class="device-logo" alt="Apple logo">'

    if "samsung" in text or "galaxy" in text or "sm-" in text:
        return '<img src="../src/static/logos/samsung.png" class="device-logo" alt="Samsung logo">'

    if "canon" in text:
        return '<img src="../src/static/logos/Canon.png" class="device-logo" alt="Canon logo">'

    if "sony" in text:
        return '<img src="../src/static/logos/sony.png" class="device-logo" alt="Sony logo">'

    if "lg" in text:
        return '<img src="../src/static/logos/lg.png" class="device-logo" alt="LG logo">'

    if "xiaomi" in text or "redmi" in text:
        return '<img src="../src/static/logos/xiaomi.png" class="device-logo" alt="Xiaomi logo">'

    return '<span class="device-emoji" aria-label="camera">📷</span>'


def build_events(images_data):
    sorted_data = sorted(
        images_data,
        key=lambda x: (x.get("datetime") is None, x.get("datetime") or "")
    )

    events_html = ""

    for img in sorted_data:
        filename = img.get("filename", "")
        image_path = f"../images/nigga/{filename}"

        device_name = build_device_name(img)
        device_logo_html = get_device_logo_html(img)
        location_text = format_location(img.get("location"))
        date_text = format_datetime(img.get("datetime"))

        events_html += f"""
<div class="event">

    <div class="date">
        {date_text}
    </div>

    <a href="{image_path}" target="_blank">
        <img src="{image_path}" class="photo" alt="{filename}">
    </a>

    <div class="device">
        {device_logo_html}
        <span class="label">Device:</span>
        <span>{device_name}</span>
    </div>

    <div class="location">
        <span class="label">📍 Location:</span>
        <span>{location_text}</span>
    </div>

</div>
"""

    return events_html


def generate_timeline_html(images_data):
    src_dir = Path(__file__).resolve().parent
    template_path = src_dir / "templates" / "timeline_template.html"

    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    events_html = build_events(images_data)
    final_html = template_html.replace("{{ EVENTS }}", events_html)

    return final_html


def main():
    base_dir = Path(__file__).resolve().parent.parent
    images_path = base_dir / "images" / "nigga"

    print("Extracting data...")
    extracted_data = extract_all(str(images_path))

    print("Generating timeline...")
    final_html = generate_timeline_html(extracted_data)

    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "timeline.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    print("-" * 40)
    print("SUCCESS!")
    print(f"Timeline created at: {output_file}")
    print("-" * 40)


if __name__ == "__main__":
    main()