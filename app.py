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

    # הגדרות אופטימליות לעקיפת חסימות IP של שרתי ענן ללא עוגיות
    ydl_opts = {
        'format': 'worst/best', # עדיפות לפורמט בסיסי וקל יותר לעקיפת חסימות, ואם לא אז הכי טוב
        'outtmpl': 'downloaded_video.dat',
        'nocheckcertificate': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['safari', 'web'],
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            if not info:
                return "שגיאה: לא ניתן היה לחלץ את המידע מהסרטון בגלל הגבלות שרת."
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"שגיאה בהורדה: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
