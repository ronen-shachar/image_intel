-# משימות הכנה לפני ההאקתון

חלקו את המסמך הזה לצוותים כמה ימים לפני ההאקתון.
כל צוות צריך להשקיע שעה-שעתיים מקסימום.

---

## רביעייה 1 - Data

### זוג A (extractor):
1. התקינו: `pip install Pillow piexif`
2. צלמו תמונה מהטלפון (עם GPS מופעל)
3. נסו להריץ את הקוד הזה ותראו מה יוצא:
```python
from PIL import Image
from PIL.ExifTags import TAGS

img = Image.open("your_photo.jpg")
exif = img._getexif()
if exif:
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        print(f"{tag}: {value}")
```
4. מה השדות שאתם מזהים? אילו שדות מעניינים?

### זוג B (map):
1. התקינו: `pip install folium`
2. נסו ליצור מפה פשוטה:
```python
import folium

m = folium.Map(location=[32.0853, 34.7818], zoom_start=12)
folium.Marker([32.0853, 34.7818], popup="תל אביב").add_to(m)
m.save("test_map.html")
```
3. פתחו את `test_map.html` בדפדפן - רואים מפה עם נקודה?

---

## רביעייה 2 - Visual

### זוג A (timeline):
1. חשבו: איך הייתם מציגים ציר זמן ב-HTML?
2. חפשו בגוגל "CSS timeline example" ותראו דוגמאות
3. בונוס: נסו `pip install matplotlib` ולצייר גרף פשוט

### זוג B (analyzer):
1. קראו על EXIF ומה אפשר ללמוד מתמונות
2. חשבו: אילו "דפוסים חשודים" אפשר לזהות? (החלפת מכשיר, חזרה למיקום, פערי זמן)
3. בונוס: כתבו פונקציה שמקבלת רשימת מילונים ומחזירה כמה מכשירים ייחודיים יש

---

## רביעייה 3 - App

### זוג A (Flask app):
1. התקינו: `pip install flask`
2. הרימו Flask app בסיסי:
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello Image Intel!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
```
3. גשו ל-`http://localhost:5000` - רואים את ההודעה?

### זוג B (report):
1. צרו דף HTML פשוט עם כותרת, טבלה, ועיצוב בסיסי
2. חפשו בגוגל "HTML CSS dashboard template" לקבל השראה

---

## צוות QA

1. התקינו: `pip install pytest`
2. כתבו בדיקה פשוטה והריצו:
```python
# test_basic.py
def test_addition():
    assert 1 + 1 == 2

def test_string():
    result = "hello world"
    assert "hello" in result
```
```bash
pytest test_basic.py -v
```
3. קראו על Code Review ב-GitHub - איך פותחים PR, איך מוסיפים הערות
