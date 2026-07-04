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

    # שרת API יציב מבוסס תשתית ענן מוכרת
    api_url = f"https://api.savetube.me/download?url={video_url}&format=mp3"

    try:
        file_response = requests.get(api_url, stream=True, timeout=30)
        
        if file_response.status_code == 200:
            filename = "downloaded_audio.mp3"
            with open(filename, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return send_file(filename, as_attachment=True, download_name="audio.mp3")
        else:
            return f"השרת המתווך החזיר קוד שגיאה: {file_response.status_code}"

    except Exception as e:
        return f"שגיאת תקשורת ברשת (רשת השרת חסומה או בבנייה): {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
