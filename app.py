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

    # שימוש ב-API חלופי יציב שאינו דורש הרשמה או מפתח
    api_url = f"https://co.wuk.sh/api/json"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": video_url,
        "isAudioOnly": True,
        "aFormat": "mp3"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()

        if response_data.get("status") in ["stream", "redirect"]:
            download_url = response_data.get("url")
            
            file_response = requests.get(download_url, stream=True)
            filename = "downloaded_audio.mp3"
            
            with open(filename, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return send_file(filename, as_attachment=True, download_name="audio.mp3")
        else:
            # אם גם השרת הזה מחזיר שגיאה, ננסה גישת הורדה ישירה חלופית
            fallback_url = f"https://api.jet-dl.top/api/download?url={video_url}&format=mp3"
            file_response = requests.get(fallback_url, stream=True)
            if file_response.status_code == 200:
                filename = "downloaded_audio.mp3"
                with open(filename, 'wb') as f:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return send_file(filename, as_attachment=True, download_name="audio.mp3")
            
            return f"שגיאה בקבלת קובץ השמע: {response_data.get('text', 'השרתים המתווכים עמוסים כרגע')}"

    except Exception as e:
        return f"שגיאה בתהליך ההורדה: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
