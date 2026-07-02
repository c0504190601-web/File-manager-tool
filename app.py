from flask import Flask, render_template_string, request

app = Flask(__name__)

# ממשק פשוט שנראה כמו כלי לניהול קבצים
html_template = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>מערכת ניהול קבצים</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; }
        .container { border: 1px solid #ccc; padding: 20px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>מערכת ניהול קבצים אישית</h1>
        <p>ניתן להעלות קבצים לשרת לצורך גיבוי או העברה</p>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">העלה קובץ</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run()
