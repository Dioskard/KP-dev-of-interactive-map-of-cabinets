from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///markers.db'

db = SQLAlchemy(app)
# Модель для маркеров
class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.String(50))  # добавляем поле для этажа
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    info = db.Column(db.String(200))  # информация о маркере

with app.app_context():
    db.create_all()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/map/<floor>')
def map_view(floor):
    markers = Marker.query.filter_by(floor=floor).all()
    return render_template('map.html', floor=floor, markers=markers)

@app.route('/add_marker', methods=['POST'])
def add_marker():
    data = request.json
    floor = data.get('floor')
    x = data.get('x')
    y = data.get('y')
    info = data.get('info')
    marker = Marker(floor=floor, x=x, y=y, info=info)
    db.session.add(marker)
    db.session.commit()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)