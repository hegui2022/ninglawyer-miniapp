"""
宁律师后端主程序
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from loguru import logger

from src.api.routes import api_bp
from src.utils.config import load_config

# 加载配置
config = load_config()

# 创建 Flask 应用
app = Flask(__name__)

# 配置 CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# 配置日志
logger.add(
    config.get('LOG_FILE', '/app/work/logs/bypass/app.log'),
    rotation="500 MB",
    retention="10 days",
    level=config.get('LOG_LEVEL', 'INFO')
)

# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api')

# 健康检查
@app.route('/health')
def health():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': 'ninglawyer-api',
        'version': '1.0.0'
    })

# 根路径
@app.route('/')
def index():
    """根路径"""
    return jsonify({
        'message': '宁律师法律咨询 API',
        'version': '1.0.0',
        'docs': '/docs'
    })

# 错误处理
@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({
        'error': 'Not Found',
        'message': '请求的资源不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    logger.error(f"Internal error: {error}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': '服务器内部错误'
    }), 500

# 启动应用
if __name__ == '__main__':
    port = config.get('API_PORT', 8080)
    debug = config.get('API_DEBUG', False)
    
    logger.info(f"Starting NingLawyer API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
