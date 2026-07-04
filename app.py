import os
import sys

# התקנת yt-dlp אוטומטית אם היא חסרה בשרת
try:
    import yt_dlp
except ModuleNotFoundError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

from flask import Flask, request, send_file

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

    output_filename = 'downloaded_audio'
    output_file_path = f"{output_filename}.mp3"

    # הגדרות עבור yt-dlp להורדת אודיו בלבד והמרה ל-MP3
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'timeout': 60,
    }

    try:
        # מחיקת קובץ ישן אם קיים כדי למנוע כפילויות
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        if os.path.exists(output_file_path):
            return send_file(output_file_path, as_attachment=True, download_name="audio.mp3")
        else:
            return "שגיאה: הקובץ לא נוצר בהצלחה בשרת"

    except Exception as e:
        return f"שגיאה פנימית בהורדה ישירה מיוטיוב: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
