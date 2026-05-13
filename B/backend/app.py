from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
import os
import uuid

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

from models import db, Cat, FeedingRecord

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test_connection():
    return jsonify({
        "status": "success",
        "message": "后端已成功读取 .env 并启动！",
        "database_target": app.config['MYSQL_DB']
    })

@app.route('/api/cats', methods=['GET'])
def get_cats():
    cats = Cat.query.all()
    result = []
    for cat in cats:
        result.append({
            'id': cat.id,
            'name': cat.name,
            'description': cat.description,
            'status': cat.status,
            'image_url': cat.image_url
        })
    return jsonify(result)

@app.route('/api/cats', methods=['POST'])
def add_cat():
    name = request.form.get('name')
    description = request.form.get('description', '')
    status = request.form.get('status', '在校')

    if not name:
        return jsonify({"error": "缺少必要字段"}), 400

    image_url = None
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename:
            ext = os.path.splitext(file.filename)[1]
            filename = str(uuid.uuid4()) + ext
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_url = f'/static/uploads/{filename}'

    new_cat = Cat(
        name=name,
        description=description,
        status=status,
        image_url=image_url
    )
    db.session.add(new_cat)
    db.session.commit()

    return jsonify({
        'id': new_cat.id,
        'name': new_cat.name,
        'description': new_cat.description,
        'status': new_cat.status,
        'image_url': new_cat.image_url
    }), 201

@app.route('/api/cats/<int:cat_id>', methods=['PUT'])
def update_cat(cat_id):
    cat = Cat.query.get(cat_id)
    if not cat:
        return jsonify({"error": "猫咪不存在"}), 404

    name = request.form.get('name')
    description = request.form.get('description', '')
    status = request.form.get('status', '')

    if name:
        cat.name = name
    if description is not None:
        cat.description = description
    if status:
        cat.status = status

    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename:
            ext = os.path.splitext(file.filename)[1]
            filename = str(uuid.uuid4()) + ext
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            cat.image_url = f'/static/uploads/{filename}'

    db.session.commit()

    return jsonify({
        'id': cat.id,
        'name': cat.name,
        'description': cat.description,
        'status': cat.status,
        'image_url': cat.image_url
    })

@app.route('/api/cats/<int:cat_id>', methods=['DELETE'])
def delete_cat(cat_id):
    cat = Cat.query.get(cat_id)
    if not cat:
        return jsonify({"error": "猫咪不存在"}), 404

    if cat.image_url:
        image_path = os.path.join(app.root_path, 'static', 'uploads', os.path.basename(cat.image_url))
        if os.path.exists(image_path):
            os.remove(image_path)

    FeedingRecord.query.filter_by(cat_id=cat_id).delete()
    db.session.delete(cat)
    db.session.commit()

    return jsonify({"message": "删除成功"})

@app.route('/api/feeding', methods=['GET'])
def get_feeding_records():
    records = FeedingRecord.query.order_by(FeedingRecord.time.desc()).limit(100).all()
    result = []
    for record in records:
        result.append({
            'id': record.id,
            'cat_id': record.cat_id,
            'food_type': record.food_type,
            'time': record.time.isoformat() if record.time else None
        })
    return jsonify(result)

@app.route('/api/cats-with-records', methods=['GET'])
def get_cats_with_records():
    from datetime import datetime, date, timedelta
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    cats = Cat.query.all()
    result = []
    for cat in cats:
        records = FeedingRecord.query.filter(
            FeedingRecord.cat_id == cat.id,
            FeedingRecord.time >= datetime(today.year, today.month, today.day),
            FeedingRecord.time < datetime(tomorrow.year, tomorrow.month, tomorrow.day)
        ).order_by(FeedingRecord.time.desc()).limit(3).all()
        
        if not records:
            continue
            
        feeding_list = []
        for record in records:
            feeding_list.append({
                'id': record.id,
                'food_type': record.food_type,
                'time': record.time.isoformat() if record.time else None
            })
        result.append({
            'id': cat.id,
            'name': cat.name,
            'image_url': cat.image_url,
            'feedings': feeding_list
        })
    return jsonify(result)

@app.route('/api/feeding', methods=['POST'])
def add_feeding_record():
    from datetime import datetime
    data = request.get_json()
    if not data or 'cat_id' not in data or 'food_type' not in data:
        return jsonify({"error": "缺少必要字段"}), 400
    time_value = datetime.now()
    if data.get('time'):
        time_value = datetime.fromisoformat(data['time'].replace('Z', '+00:00'))
    new_record = FeedingRecord(
        cat_id=data['cat_id'],
        food_type=data['food_type'],
        time=time_value
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({
        'id': new_record.id,
        'cat_id': new_record.cat_id,
        'food_type': new_record.food_type,
        'time': new_record.time.isoformat()
    }), 201

@app.route('/static/uploads/<filename>')
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5000)