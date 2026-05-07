from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

# 1. 初始化 Flask
app = Flask(__name__)

# 2. 载入配置
app.config.from_object(Config)

# 3. 初始化数据库插件
db = SQLAlchemy(app)

# 4. 开启跨域 (非常重要！否则你的 Vue 按钮无法调用这个接口)
CORS(app)

# 5. 定义一个简单的测试路由
@app.route('/api/test', methods=['GET'])
def test_connection():
    return jsonify({
        "status": "success",
        "message": "后端已成功读取 .env 并启动！",
        "database_target": app.config['MYSQL_DB']
    })

if __name__ == '__main__':
    # 启动服务器
    app.run(debug=True, port=5000)