#!/usr/bin/env python3
"""
宁律师法律咨询小程序矩阵 - 主入口
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from src.api.routes import register_routes
from src.storage.db import init_db
from src.middleware import setup_logging, init_error_handlers

# 导入技能模块以自动注册
import src.skills  # 这会触发技能注册

# 创建 Flask 应用
app = Flask(__name__)

# 配置 CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# 配置应用
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json;charset=utf-8'

# 设置日志系统
setup_logging(app)

# 注册错误处理器
init_error_handlers(app)

# 注册路由
register_routes(app)

# 初始化数据库
@app.before_request
def before_first_request():
    init_db()

# 健康检查接口
@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'service': 'ninglawyer-miniapp',
        'version': '1.0.0-alpha'
    })

# API 根路径
@app.route('/')
def index():
    """API 根路径"""
    return jsonify({
        'service': '宁律师法律咨询小程序矩阵',
        'version': '1.0.0-alpha',
        'endpoints': {
            'consultation': '/api/consultation',
            'contract': '/api/contract',
            'risk': '/api/risk'
        }
    })

if __name__ == '__main__':
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"""
    ========================================
    宁律师法律咨询小程序矩阵
    ========================================
    服务地址: http://{host}:{port}
    健康检查: http://{host}:{port}/health
    API 文档: http://{host}:{port}/api
    ========================================
    """)
    
    app.run(host=host, port=port, debug=debug)
