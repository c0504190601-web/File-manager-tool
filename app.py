import os
import requests
from flask import Flask, request, render_template_string, Response, stream_with_context

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>מוריד סרטונים - עוקף חסימה</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; background-color: #f8f9fa; padding-top: 50px; }
        .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: inline-block; width: 90%; max-width: 400px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #ff0000; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #cc0000; }
        .footer { margin-top: 20px; font-size: 0.8em; color: #666; }
    </style>
</head>
<body>
    <div class="card">
        <h2>הורדה מיוטיוב (Render)</h2>
        <p>עוקף חסימת נטפרי ובוטים</p>
        <form action="/download" method="get">
            <input type="text" name="url" placeholder="הדבק לינק מיוטיוב" required>
            <button type="submit">הורד עכשיו</button>
        </form>
        <div class="footer">ההורדה תתחיל אוטומטית תוך מספר שניות</div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return "נא לספק לינק"

    # פנייה ל-API של Cobalt - שירות חזק לעקיפת חסימות יוטיוב
    cobalt_api = "https://api.cobalt.tools/api/json"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "url": video_url,
        "vQuality": "720", # איכות טובה שאינה דורשת עיבוד כבד
        "isAudioOnly": False
    }

    try:
        # שלב 1: מבקשים מ-Cobalt קישור ישיר לקובץ הוידאו
        response = requests.post(cobalt_api, json=payload, headers=headers)
        data = response.json()

        if data.get('status') == 'error':
            return f"שגיאה מהשרת: {data.get('text')}"

        video_direct_url = data.get('url')
        if not video_direct_url:
            return "לא נמצא קישור להורדה."

        # שלב 2: הזרמת הקובץ דרך Render כדי לעקוף את נטפרי
        # אנחנו מורידים את הקובץ לשרת ב-Render ומשדרים אותו אליך בו-זמנית
        req = requests.get(video_direct_url, stream=True)
        
        def generate():
            for chunk in req.iter_content(chunk_size=8192):
                yield chunk

        return Response(
            stream_with_context(generate()),
            headers={
                "Content-Disposition": f"attachment; filename=video.mp4",
                "Content-Type": "video/mp4"
            }
        )

    except Exception as e:
        return f"שגיאה בתהליך: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
