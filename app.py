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

    # שירות הורדה שמשתמש בטכניקת עקיפה מובנית
    api_url = "https://snapsave.app/api/ajaxSearch"
    payload = {'url': video_url}
    
    try:
        response = requests.post(api_url, data=payload)
        # זה יאפשר לנו למשוך את הקישור הישיר ל-MP3 שהמנוע שלהם מייצר
        return f"נא להשתמש בקישור הבא: {response.text}"
    except Exception as e:
        return f"שגיאה בעבודה מול השירות: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
