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

    # הגדרות המפעילות אימות OAuth ומאפשרות אינטראקציה לצורך קבלת קוד אישור בדפדפן
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.dat',
        'nocheckcertificate': True,
        'yt_dlp_options': {'compat_opts': set()},
        'extractor_args': {
            'youtube': {
                'player_client': ['tv'],
                'oauth': True  # הפעלת מנגנון אימות רשמי של גוגל
            }
        },
    }

    # הסרת ה-try/except כדי לאפשר לקישור האימות להופיע בתוך ה-Logs ב-Render
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info)
    
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
