def create_timeline(images_data):
    try:
        dated_images = [img for img in images_data if img["datetime"]]
    except KeyError:
        print("images without datetime!")
        return None
    dated_images.sort(key=lambda x: x["datetime"])

    html = '<div style="position:relative; padding:20px;">'
    html += '<div style="position:absolute; left:50%; width:2px; height:100%; background:#333;"></div>'

    pin_color = ['blue', 'orange', 'green', 'purple', 'pink', 'brown', 'cadetblue',
                 'black', 'red']
    color_dict = {}
    for img in dated_images:
        dt_obj = img["datetime"].split()[0]
        if dt_obj in color_dict:
            continue
        try:
            color_dict[dt_obj] = pin_color.pop()
        except IndexError:
            color_dict[dt_obj] = "lightgray"
    for i, img in enumerate(dated_images):
        date_only = img["datetime"].split()[0]
        text_color = color_dict[date_only]
        side = "left" if i % 2 == 0 else "right"
        html += f'''
        <div style="margin:20px 0; text-align:{side}; color: {text_color};">
            <strong>{img["datetime"]}</strong><br>
            {img["filename"]}<br>
            <small>{img.get("camera_model", "Unknown")}</small>
        </div>'''

    html += '</div>'
    return html

