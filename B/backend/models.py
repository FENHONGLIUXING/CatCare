from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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