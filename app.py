import os
import requests
from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <title>עוקף חסימה להורדה</title>
    <style>
        body { font-family: Arial; text-align: center; padding-top: 50px; background: #f0f0f0; }
        .container { background: white; padding: 30px; display: inline-block; border-radius: 15px; box-shadow: 0 0 15px rgba(0,0,0,0.2); }
        input { width: 300px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>הורדת סרטון (עוקף נטפרי)</h2>
        <form action="/get_link" method="get">
            <input type="text" name="url" placeholder="הדבק לינק יוטיוב כאן" required>
            <button type="submit">קבל קישור להורדה</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_link')
def get_link():
    youtube_url = request.args.get('url')
    if not youtube_url:
        return "נא להזין לינק"

    # שימוש ב-API חיצוני (למשל של שירות בשם loader.to או cobalt)
    # כאן נשתמש בדוגמה של API פשוט שמחזיר קישור ישיר
    try:
        # זוהי דוגמה לשימוש בשירות שנקרא Cobalt שפופולרי לעקיפות כאלו
        api_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "url": youtube_url,
            "vQuality": "720"
        }
        
        response = requests.post(api_url, json=data, headers=headers)
        res_data = response.json()
        
        if "url" in res_data:
            # אנחנו מפנים את המשתמש ישירות לקובץ הוידאו שהשרת מצא
            return redirect(res_data["url"])
        else:
            return f"השירות לא הצליח למצוא קישור: {res_data.get('text', 'שגיאה כללית')}"

    except Exception as e:
        return f"שגיאה: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
