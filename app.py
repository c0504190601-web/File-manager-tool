import os
import sys
import subprocess

# פונקציה להתקנה אוטומטית של ספריות חסרות
def install_and_import(package):
    try:
        return __import__(package)
    except ImportError:
        print(f"מתקין את {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return __import__(package)

flask = install_and_import('flask')
yt_dlp = install_and_import('yt_dlp')

from flask import Flask, request, send_file, render_template_string

app = Flask(__name__)

# תיקייה לשמירת הקבצים באופן זמני
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <title>מוריד סרטונים מקצועי</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f4; }
        form { background: white; padding: 20px; display: inline-block; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input { padding: 10px; width: 300px; border: 1px solid #ccc; border-radius: 5px; }
        button { padding: 10px 20px; background: #ff0000; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #cc0000; }
        .msg { margin-top: 20px; color: #555; }
    </style>
</head>
<body>
    <h2>מוריד סרטוני YouTube</h2>
    <form action="/download" method="get">
        <input type="text" name="url" placeholder="הדבק לינק מיוטיוב כאן" required>
        <button type="submit">הורד עכשיו</button>
    </form>
    <div class="msg">ההורדה עשויה לקחת כמה שניות, נא להמתין.</div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return "נא לספק לינק תקין"

    # הגדרות עבור yt-dlp
    ydl_opts = {
        'format': 'best',  # מוריד את האיכות הכי טובה שיש בקובץ אחד (וידאו + סאונד)
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s', # שם הקובץ שיווצר
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # חילוץ מידע והורדה
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)
            
        # שליחת הקובץ למשתמש להורדה
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"שגיאה בהורדה: {str(e)}"

if __name__ == '__main__':
    # הרצת השרת
    app.run(debug=True, port=5000)
