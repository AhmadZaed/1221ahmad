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
