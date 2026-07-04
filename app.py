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

    # הגדרות מתוקנות לטיפול בבעיית הפורמטים והמשך שימוש בעוגיות שהעלית
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # שילוב וידאו ואודיו, או הפורמט הטוב ביותר שזמין קומפלט
        'outtmpl': 'downloaded_video.dat',
        'nocheckcertificate': True,
        'cookiefile': 'cookies.txt',          # שימוש בקובץ העוגיות הקיים במאגר
        'ignoreerrors': True,                  # מניעת קריסה במקרה של שגיאות פורמט משניות
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        if not info:
            return "שגיאה: לא ניתן היה לחלץ את פורמט הווידאו המבוקש שרת הוגבל."
        filename = ydl.prepare_filename(info)
    
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
