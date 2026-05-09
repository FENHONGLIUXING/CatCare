from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
#from flask_migrate import Migrate


# 1. 初始化 Flask
app = Flask(__name__)

# 2. 载入配置
app.config.from_object(Config)

# 3. 初始化数据库插件
db = SQLAlchemy(app)
#migrate = Migrate(app, db)
CORS(app)

# --- 直接把模型写在这里 ---
class GlobalCounter(db.Model):
    __tablename__ = 'global_counter'
    id = db.Column(db.Integer, primary_key=True)
    count_value = db.Column(db.Integer, default=0)

# 5. 定义一个简单的测试路由
@app.route('/api/test', methods=['GET'])
def test_connection():
    return jsonify({
        "status": "success",
        "message": "后端已成功读取 .env 并启动！",
        "database_target": app.config['MYSQL_DB']
    })
# 获取当前计数值
@app.route('/api/get_count', methods=['GET'])
def get_count():
    # 尝试从数据库获取第一条（也是唯一一条）记录
    counter = GlobalCounter.query.first()
    
    # 如果数据库里什么都没有，先初始化一个
    if not counter:
        counter = GlobalCounter(count_value=0)
        db.session.add(counter)
        db.session.commit()
    
    return jsonify({"count": counter.count_value})

# 增加计数值
@app.route('/api/increment', methods=['POST'])
def increment():
    counter = GlobalCounter.query.first()
    if counter:
        counter.count_value += 1
        db.session.commit() # 关键：这一步才会把变动存入 MySQL
        return jsonify({"new_count": counter.count_value})
    
    return jsonify({"error": "Counter not found"}), 404

if __name__ == '__main__':
    # 启动服务器
    app.run(debug=True, port=5000)