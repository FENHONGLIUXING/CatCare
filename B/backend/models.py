from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GlobalCounter(db.Model):
    __tablename__ = 'global_counter'
    id = db.Column(db.Integer, primary_key=True)
    count_value = db.Column(db.Integer, default=0)

class Cat(db.Model):
    __tablename__ = 'cats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='在校')
    image_url = db.Column(db.String(255), nullable=True)

class FeedingRecord(db.Model):
    __tablename__ = 'feeding_records'
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('cats.id'), nullable=False)
    food_type = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False)