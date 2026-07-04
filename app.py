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

    # הגדרות מתוקנות המדמות בצורה מלאה לקוח אינטרנט מובנה כדי למנוע את דרישת הבוטים
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.dat',
        'nocheckcertificate': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['web_creator', 'tv'],
            }
        },
        # הוספת כותרת דפדפן מותאמת אישית כדי למנוע זיהוי של השרת כבוט
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        }
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
