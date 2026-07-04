import os
import sys

# מנגנון התקנה אוטומטי בתוך הקוד לעקיפת תקלות בנייה בשרת
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

    cobalt_api_url = "https://api.cobalt.tools/api/json"
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
        response = requests.post(cobalt_api_url, json=payload, headers=headers)
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
            return f"שגיאה מהשרת המתווך: {response_data.get('text', 'לא ניתן לעבד את הקישור')}"

    except Exception as e:
        return f"שגיאה בתהליך ההורדה: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
