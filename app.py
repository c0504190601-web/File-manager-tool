from flask import Flask, request, send_file
import requests
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

    # פנייה ל-API חיצוני של Cobalt כדי לעקוף את חסימת ה-IP של Render מול יוטיוב
    cobalt_api_url = "https://api.cobalt.tools/api/json"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # הגדרת הבקשה (הורדת אודיו/סאונד בלבד בצורה היציבה ביותר)
    payload = {
        "url": video_url,
        "isAudioOnly": True,
        "aFormat": "mp3"
    }

    try:
        # שליחת הבקשה לשרת המתווך
        response = requests.post(cobalt_api_url, json=payload, headers=headers)
        response_data = response.json()

        if response_data.get("status") == "stream" or response_data.get("status") == "redirect":
            download_url = response_data.get("url")
            
            # הורדת הקובץ בפועל אל שרת ה-Render שלך
            file_response = requests.get(download_url, stream=True)
            filename = "downloaded_audio.mp3"
            
            with open(filename, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return send_file(filename, as_attachment=True, download_name="audio.mp3")
        else:
            return f"שגיאה מהשרת המתווך: {response_data.get('text', 'לא ניתן לעבד את הקישור')}"

    except Exception as e:
        return f"שגיאה בתהליך ההורדה: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
