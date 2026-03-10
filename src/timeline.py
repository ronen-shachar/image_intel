from extractor import *


def generate_timeline_html(images_data):
    # Sort data by datetime
    sorted_data = sorted(images_data, key=lambda x: x.get('datetime', ''))

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Intelligence Timeline Report</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background-color: #eef2f3; 
                padding: 40px; 
                color: #2c3e50;
            }
            .timeline { 
                border-left: 4px solid #3498db; 
                margin-left: 30px; 
                padding: 20px; 
            }
            .event { 
                margin-bottom: 25px; 
                position: relative; 
                padding-left: 25px;
                background: white;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                width: fit-content;
                min-width: 300px;
            }
            .event::before { 
                content: ''; 
                position: absolute; 
                left: -31px; 
                top: 18px; 
                width: 14px; 
                height: 14px; 
                background: #3498db; 
                border-radius: 50%; 
                border: 3px solid #eef2f3;
            }
            .date { 
                font-weight: bold; 
                color: #2980b9; 
                font-size: 1.1em; 
                margin-bottom: 8px;
            }
            h1 { 
                color: #2c3e50; 
                border-bottom: 3px solid #3498db; 
                padding-bottom: 15px;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            .label { font-weight: bold; color: #7f8c8d; }
        </style>
    </head>
    <body>
        <h1>Intelligence Field Report: Photo Timeline</h1>
        <div class="timeline">
    """

    for img in sorted_data:
        html_content += f"""
        <div class="event">
            <div class="date">{img.get('datetime', 'N/A')}</div>
            <div><span class="label">File:</span> {img.get('filename', 'Unknown')}</div>
            <div><span class="label">Device:</span> {img.get('camera_model', 'Unknown')}</div>
            <div><span class="label">Location:</span> {img.get('location', 'Unknown')}</div>
        </div>
        """

    html_content += "</div></body></html>"
    return html_content


if __name__ == "__main__":
    # Path to your images folder
    images_path = r'C:\Users\hilat\Desktop\image_intel\images\ready'

    print("Extracting data...")
    extracted_data = extract_all(images_path)

    print("Generating timeline...")
    final_html = generate_timeline_html(extracted_data)

    # Saving to file
    with open("my_timeline.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("-" * 30)
    print("SUCCESS! Timeline generated.")
    print(f"Open this file in your browser: my_timeline.html")
    print("-" * 30)