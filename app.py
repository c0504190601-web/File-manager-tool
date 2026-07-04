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

    # הגדרות מתוקנות: שילוב של העוגיות ולקוח אנדרואיד לעקיפת מגבלות חילוץ הפורמטים
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.dat',
        'nocheckcertificate': True,
        'cookiefile': 'cookies.txt',          # שימוש בקובץ העוגיות שהעלית
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}}, # אילוץ לקוח אנדרואיד לעקיפת ה-n challenge[cite: 1]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        if not info:
            return "שגיאה: לא ניתן היה לחלץ את פורמט הווידאו המבוקש."
        filename = ydl.prepare_filename(info)
    
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
