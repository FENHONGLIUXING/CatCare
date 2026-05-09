# models.py
from flask_sqlalchemy import SQLAlchemy

# 这里不指定具体的 db 实例，而是定义类
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # 如果你后面想用统一的 db，可以先这样定义

class GlobalCounter(db.Model):
    __tablename__ = 'global_counter'
    id = db.Column(db.Integer, primary_key=True)
    count_value = db.Column(db.Integer, default=0)