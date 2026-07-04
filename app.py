from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <form action="/download" method="get">
            <input type="text" name="url" placeholder="הכנס לינק מיוטיוב">
            <button type="submit">הורד סרטון</button>
        </form>
    '''

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return "נא לספק לינק"

    # הגדרות בסיסיות ויציבות
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.dat',
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            if not info:
                return "שגיאה: לא ניתן היה לחלץ את המידע מהסרטון."
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        # הצגת שגיאה מפורטת ומניעת קריסת השרת ל-500
        if "Sign in to confirm you’re not a bot" in str(e):
            return "שגיאה: כתובת ה-IP של שרת ה-Render נחסמה על ידי יוטיוב. יש להשתמש ב-Proxy או להריץ את הקוד על שרת עם IP ביתי."
        return f"שגיאה בהורדה: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
