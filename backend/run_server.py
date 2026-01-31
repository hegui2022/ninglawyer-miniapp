#!/usr/bin/env python
"""
启动Flask服务器
"""

from src.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, threaded=True)
