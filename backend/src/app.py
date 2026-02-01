"""
Flask应用主文件
统一API网关，支持6个小程序调用
"""

import os
import sys
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from loguru import logger

# 加载环境变量
load_dotenv()

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import init_db, get_db
from routes.auth import auth_bp
from routes.consultation import consultation_bp
from routes.contract import contract_bp
from agents.master_brain import master_brain
from utils.skill_registry import skill_registry
from utils.mask import mask_log, mask_dict
from utils.env_config import check_required_env_vars, log_config
from api.v1_ninglawyer import v1_ninglawyer_bp

# ============================================
# 小程序标识映射
# ============================================

APP_IDS = {
    'miniprogram_civil': '民事咨询',
    'miniprogram_family': '婚姻家事',
    'miniprogram_contract_draft': '合同起草',
    'miniprogram_contract_review': '合同审查',
    'miniprogram_desensitize': '文本脱敏',
    'miniprogram_contract_reminder': '合同提醒'
}

# ============================================
# 配置日志
# ============================================

def setup_logging(app):
    """配置日志"""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', 'logs/app.log')
    
    # 确保日志目录存在
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    
    # 文件处理器
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # 配置app日志
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    # 配置第三方库日志
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    
    return app.logger


# ============================================
# 创建Flask应用
# ============================================

def create_app():
    """创建Flask应用"""
    # 检查必需的环境变量
    if not check_required_env_vars():
        raise RuntimeError("缺少必需的环境变量，请检查配置")
    
    # 记录配置信息
    log_config()
    
    app = Flask(__name__)
    
    # 配置CORS（支持环境变量限制域名）
    allowed_origins = os.getenv('ALLOWED_ORIGINS', '*')
    if allowed_origins != '*':
        allowed_origins_list = [origin.strip() for origin in allowed_origins.split(',')]
    else:
        allowed_origins_list = '*'
    
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins_list,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        },
        r"/health": {
            "origins": "*"
        }
    })
    
    # 配置日志
    logger = setup_logging(app)
    logger.info("Flask应用启动中...")
    
    # 配置数据库连接池
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 20,           # 连接池大小
        'max_overflow': 40,        # 最大溢出连接数
        'pool_timeout': 30,        # 连接超时时间（秒）
        'pool_recycle': 3600,      # 连接回收时间（秒）
        'pool_pre_ping': True,     # 连接前ping检查
    }
    
    # 配置
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key')
    app.config['JSON_AS_ASCII'] = False  # 支持中文
    
    # ============================================
    # 注册蓝图
    # ============================================
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(consultation_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(v1_ninglawyer_bp, url_prefix='/api/v1/ninglawyer')  # 宁律师V1 API
    
    logger.info("蓝图注册完成")
    
    # ============================================
    # 注册所有技能
    # ============================================
    
    try:
        from skills import register_all_skills
        register_all_skills()
        logger.info("技能注册完成")
    except Exception as e:
        logger.error(f"技能注册失败: {str(e)}")
    
    # ============================================
    # 初始化数据库
    # ============================================
    
    try:
        init_db()
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
    
    # ============================================
    # 健康检查接口
    # ============================================
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """健康检查"""
        return jsonify({
            "status": "ok",
            "service": "legal-assistant-backend",
            "version": "1.0.0",
            "skills": list(skill_registry.list_skills().keys())
        })
    
    # ============================================
    # 统一聊天接口（支持所有小程序）
    # ============================================
    
    @app.route('/api/v1/chat', methods=['POST'])
    def chat():
        """
        统一聊天接口
        所有小程序都调用这个接口
        """
        try:
            data = request.json
            user_input = data.get('message', '')
            user_id = data.get('user_id')
            app_id = data.get('app_id', 'default')
            
            # 验证参数
            if not user_input:
                return jsonify({
                    "success": False,
                    "error": "缺少参数: message"
                }), 400
            
            # 根据app_id获取小程序名称
            app_name = APP_IDS.get(app_id, '通用')
            logger.info(f"收到聊天请求 - 小程序: {app_name} ({app_id}), 用户: {user_id}, 消息: {user_input[:50]}...")
            
            # 构建上下文
            context = {
                'app_id': app_id,
                'app_name': app_name,
                'user_id': user_id
            }
            
            # 主脑路由
            result = master_brain.route(
                user_input=user_input,
                user_id=user_id,
                context=context
            )
            
            logger.info(f"聊天请求完成 - 技能: {result.get('skill_used')}, 场景: {result.get('scenario_used')}")
            
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"聊天接口异常: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    # ============================================
    # 技能执行接口（直接调用指定技能）
    # ============================================
    
    @app.route('/api/v1/skills/<skill_name>', methods=['POST'])
    def execute_skill(skill_name):
        """
        直接调用指定技能
        支持小程序定制功能
        """
        try:
            data = request.json
            user_input = data.get('message', '')
            user_id = data.get('user_id')
            app_id = data.get('app_id', 'default')
            
            # 验证参数
            if not user_input:
                return jsonify({
                    "success": False,
                    "error": "缺少参数: message"
                }), 400
            
            # 检查技能是否存在
            if not skill_registry.skill_exists(skill_name):
                return jsonify({
                    "success": False,
                    "error": f"技能不存在: {skill_name}"
                }), 404
            
            logger.info(f"执行技能 - 技能: {skill_name}, 小程序: {app_id}, 用户: {user_id}")
            
            # 构建上下文
            context = {
                'user_id': user_id,
                'app_id': app_id,
                'app_name': APP_IDS.get(app_id, '通用')
            }
            
            # 执行技能
            result = skill_registry.execute(
                skill_name=skill_name,
                user_input=user_input,
                context=context
            )
            
            # 处理返回结果
            if isinstance(result, str):
                # 技能返回字符串，包装成标准格式
                return jsonify({
                    "success": True,
                    "reply": result,
                    "skill_used": skill_name
                })
            else:
                # 技能返回字典，直接返回
                return jsonify(result)
        
        except Exception as e:
            logger.error(f"技能执行异常: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    # ============================================
    # 技能列表接口
    # ============================================
    
    @app.route('/api/v1/skills', methods=['GET'])
    def list_skills():
        """
        获取所有技能列表
        """
        try:
            category = request.args.get('category')
            skills = skill_registry.list_skills(category)
            
            result = {
                "success": True,
                "skills": [
                    {
                        "name": skill_name,
                        "description": skill_info.get('description', ''),
                        "category": skill_info.get('category', '')
                    }
                    for skill_name, skill_info in skills.items()
                ]
            }
            
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"获取技能列表异常: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    # ============================================
    # 404错误处理
    # ============================================
    
    @app.errorhandler(404)
    def not_found(error):
        """404错误处理"""
        return jsonify({
            "success": False,
            "message": "接口不存在"
        }), 404
    
    # ============================================
    # 500错误处理
    # ============================================
    
    @app.errorhandler(500)
    def internal_error(error):
        """500错误处理"""
        return jsonify({
            "success": False,
            "message": "服务器内部错误"
        }), 500
    
    # ============================================
    # 全局异常处理
    # ============================================
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """全局异常处理"""
        logger.error(f"未捕获的异常: {str(error)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(error)}"
        }), 500
    
    logger.info("Flask应用创建完成")
    
    return app


# ============================================
# 运行应用
# ============================================

if __name__ == '__main__':
    app = create_app()
    
    # 获取配置
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # 运行应用
    app.run(
        host=host,
        port=port,
        debug=debug
    )
