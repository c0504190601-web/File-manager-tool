import os
import sys

try:
    import requests
except ModuleNotFoundError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

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

    # שימוש ב-API חלופי מבוסס GET פשוט כדי לעקוף חסימות DNS וסגירת פורטים
    fallback_api_url = f"https://api.jet-dl.top/api/download?url={video_url}&format=mp3"

    try:
        # פנייה ישירה להורדת קובץ הסטרים
        file_response = requests.get(fallback_api_url, stream=True, timeout=30)
        
        if file_response.status_code == 200:
            filename = "downloaded_audio.mp3"
            with open(filename, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return send_file(filename, as_attachment=True, download_name="audio.mp3")
        else:
            # ניסיון שני עם מנוע הורדה חלופי נוסף במקרה והראשון מחזיר שגיאה
            backup_url = f"https://addyoutube.com/api/v1/download?url={video_url}"
            backup_response = requests.get(backup_url, stream=True, timeout=30)
            if backup_response.status_code == 200:
                filename = "downloaded_audio.mp3"
                with open(filename, 'wb') as f:
                    for chunk in backup_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return send_file(filename, as_attachment=True, download_name="audio.mp3")
            
            return f"שגיאה: השרתים המתווכים חסומים כרגע בסינון ה-DNS של השרת. קוד תגובה: {file_response.status_code}"

    except Exception as e:
        return f"שגיאת תקשורת ברשת (DNS/Connection): {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
