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

    # שימוש בנקודת הקצה המרכזית של ה-API
    cobalt_api_url = "https://api.cobalt.tools/"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": video_url,
        "downloadMode": "audio"  # הגדרה בסיסית להורדת שמע
    }

    try:
        response = requests.post(cobalt_api_url, json=payload, headers=headers)
        
        # הדפסת הסטטוס ללוגים של השרת
        print(f"Cobalt status code: {response.status_code}")
        
        try:
            response_data = response.json()
        except Exception:
            return f"השרת הציג תגובה שאינה JSON. טקסט מלא: {response.text}"

        if response_data.get("status") in ["tunnel", "redirect", "stream", "picker"]:
            download_url = response_data.get("url")
            if not download_url:
                return f"התקבל סטטוס הצלחה אך ללא קישור להורדה. תגובת השרת: {response_data}"
                
            file_response = requests.get(download_url, stream=True)
            filename = "downloaded_audio.mp3"
            
            with open(filename, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return send_file(filename, as_attachment=True, download_name="audio.mp3")
        else:
            # כאן אנחנו מציגים את התשובה המלאה מאיפיאיי של קובלט כדי להבין את הבעיה
            return f"שגיאה מפורטת מהשרת המתווך: {response_data}"

    except Exception as e:
        return f"שגיאה כללית בתהליך ההורדה: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
