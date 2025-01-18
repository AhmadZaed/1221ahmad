from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# הגדרת נתיב למסד נתונים SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

# יצירת מודל טבלה למסד הנתונים
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=True)  # קטגוריה
    neighborhood = db.Column(db.String(100), nullable=True)  # אזור

    def __repr__(self):
        return f'<Report {self.id}>'

# יצירת הטבלה במסד נתונים (אם לא קיימת)
with app.app_context():
    db.create_all()

@app.route('/submit_report', methods=['POST'])
def submit_report():
    description = request.form.get('description')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    file = request.files.get('image-upload')

    # בדיקת תקינות
    if not description or len(description) > 500:
        return jsonify({'status': 'error', 'message': 'יש להזין תיאור עד 500 תווים.'}), 400

    if not latitude or not longitude:
        return jsonify({'status': 'error', 'message': 'יש לבחור מיקום על המפה.'}), 400

    if not file:
        return jsonify({'status': 'error', 'message': 'יש להעלות תמונה.'}), 400

    if file.content_type not in ['image/jpeg', 'image/png']:
        return jsonify({'status': 'error', 'message': 'קובץ התמונה חייב להיות בפורמט JPEG או PNG.'}), 400

    if len(file.read()) > 5 * 1024 * 1024:  # 5MB
        return jsonify({'status': 'error', 'message': 'גודל הקובץ אינו יכול לעלות על 5MB.'}), 400

    # שמירת הקובץ בתיקייה
    file.seek(0)  # החזרת מצביע לקריאה
    image_filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

    # שמירת הדיווח במסד הנתונים
    new_report = Report(
        description=description,
        latitude=latitude,
        longitude=longitude,
        image_url=f'/uploads/{image_filename}'
    )
    db.session.add(new_report)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'הדיווח התקבל בהצלחה!',
        'data': {
            'description': description,
            'latitude': latitude,
            'longitude': longitude,
            'image_url': f'/uploads/{image_filename}'
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/get_reports', methods=['GET'])
def get_reports():
    # קבלת פרמטרים לסינון מהבקשה
    category = request.args.get('category')
    neighborhood = request.args.get('neighborhood')

    # שאילתה בסיסית
    query = Report.query

    # סינון לפי קטגוריה אם נבחרה
    if category:
        query = query.filter_by(category=category)

    # סינון לפי אזור (neighborhood) אם נבחר
    if neighborhood:
        query = query.filter(Report.neighborhood.like(f'%{neighborhood}%'))

    # הפקת הנתונים במבנה JSON
    reports = [
        {
            'id': report.id,
            'description': report.description,
            'latitude': report.latitude,
            'longitude': report.longitude,
            'image_url': report.image_url,
            'category': report.category,
            'neighborhood': report.neighborhood
        }
        for report in query.all()
    ]

    return jsonify(reports)
from flask import Flask, render_template, request

app = Flask(_name_)


ticket_data = {
    "12345": "הפנייה בסטטוס: בתהליך טיפול",
    "67890": "הפנייה בסטטוס: טופלה בהצלחה",
    "11223": "הפנייה בסטטוס: ממתינה לאישור"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_status', methods=['POST'])
def check_status():
    ticket_number = request.form['ticket_number']
    
    status = ticket_data.get(ticket_number, "לא נמצא סטטוס לפנייה זו")
    return render_template('index.html', status=status)

if _name_ == '_main_':
    app.run(debug=True)
    from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Dummy user credentials for demonstration
users = {
    'user1': 'password123',
    'admin': 'securepass'
}

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        if username in users and users[username] == password:
            return f"Welcome, {username}!"
        else:
            return "Invalid credentials, please try again.", 401
    return render_template_string(login_form)

# Embedded form (optional for simple example)
login_form = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login Form</h2>
    <form action="/login" method="post">
        <div>
            <label for="uname">Username</label>
            <input type="text" placeholder="Enter Username" name="uname" required>
        </div>
        <div>
            <label for="psw">Password</label>
            <input type="password" placeholder="Enter Password" name="psw" required>
        </div>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
