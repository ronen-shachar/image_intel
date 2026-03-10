from extractor import extract_all
from map_view import sort_by_time

def create_timeline(images_data_list):
    # 1. הגדרת משתנה ה-CSS (עיצוב) - שים לב לשימוש ב-f-string
    html_start = f"""
    <div class="timeline-wrapper" style="font-family: Arial; max-width: 700px; margin: auto; direction: ltr;">
        <style>
            .timeline-container {{ 
                position: relative; 
                padding-left: 30px; 
                border-left: 3px solid #007bff; 
            }}
            .event-card {{ 
                background: white; 
                margin-bottom: 20px; 
                padding: 15px; 
                border-radius: 8px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            }}
            .map-btn {{ 
                color: white; 
                background: #28a745; 
                padding: 5px 10px; 
                text-decoration: none; 
                border-radius: 4px; 
            }}
        </style>
        <h2 style="text-align: center;">Activity Timeline</h2>
        <div class="timeline-container">
    """

    # 2. יצירת תוכן הכרטיסים בעזרת לולאה
    cards_html = ""
    for image in images_data_list:
        cards_html += f"""
            <div class="event-card">
                <div style="color: #007bff; font-weight: bold;">{image['datetime']}</div>
                <div style="margin: 10px 0;">
                    <strong>Device:</strong> {image['camera_make']} {image['camera_model']}<br>
                    <strong>Location:</strong> {image['latitude']:.4f}, {image['longitude']:.4f}
                </div>
                <a href="https://www.google.com/maps?q={image['latitude']},{image['longitude']}" target="_blank" class="map-btn">
                    Open Map
                </a>
            </div>
        """

    html_end = "</div></div>"

    return html_start + cards_html + html_end