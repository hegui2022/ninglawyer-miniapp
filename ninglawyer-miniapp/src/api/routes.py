"""
API 路由
"""

from flask import Blueprint
from src.utils.logger import logger

# 创建蓝图
api_bp = Blueprint('api', __name__)

# 导入各个模块的路由
# from src.api.consultation import consultation_bp
# from src.api.contract import contract_bp
# from src.api.signing import signing_bp
# from src.api.verification import verification_bp
# from src.api.litigation import litigation_bp

# 注册蓝图
# api_bp.register_blueprint(consultation_bp, url_prefix='/consultation')
# api_bp.register_blueprint(contract_bp, url_prefix='/contract')
# api_bp.register_blueprint(signing_bp, url_prefix='/signing')
# api_bp.register_blueprint(verification_bp, url_prefix='/verification')
# api_bp.register_blueprint(litigation_bp, url_prefix='/litigation')

# 临时路由，用于测试
@api_bp.route('/test', methods=['GET'])
def test():
    """测试接口"""
    logger.info("测试接口被调用")
    return {
        'message': '宁律师 API 测试成功',
        'status': 'ok'
    }
