import os
from dotenv import load_dotenv

# 加载当前目录下的 .env 文件
load_dotenv()

class Config:
    # 从 .env 读取配置，读取不到则用默认值
    MYSQL_USER = os.getenv('DB_USER', 'root')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD', '')
    MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
    MYSQL_PORT = os.getenv('DB_PORT', '3306')
    MYSQL_DB = os.getenv('DB_NAME', 'catcare')

    # 构造 SQLAlchemy 数据库连接字符串
    # 格式：mysql+pymysql://用户名:密码@地址:端口/数据库名
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    
    # 禁用追踪对象修改，提升性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 安全秘钥
    SECRET_KEY = os.getenv('SECRET_KEY', 'bintian-dev-key')