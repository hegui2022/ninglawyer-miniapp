#!/usr/bin/env python3
"""
项目启动验证脚本
验证所有必要的组件是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("  宁律师法律咨询小程序 - 启动验证")
print("=" * 60)
print()

all_passed = True

# 1. 检查 Python 版本
print("1️⃣  检查 Python 版本...")
python_version = sys.version_info
if python_version >= (3, 9):
    print(f"   ✅ Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    print(f"   ❌ Python 版本过低: {python_version.major}.{python_version.minor}.{python_version.micro}")
    print(f"   💡 请升级到 Python 3.9 或更高版本")
    all_passed = False

# 2. 检查必要的文件
print()
print("2️⃣  检查必要的文件...")
required_files = [
    "src/main.py",
    "requirements.txt",
    ".env",
    "miniprogram/app.json",
    "miniprogram/app.js",
]

for file in required_files:
    file_path = project_root / file
    if file_path.exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} 不存在")
        all_passed = False

# 3. 检查数据库
print()
print("3️⃣  检查数据库...")
try:
    from src.database import init_db, check_db_connection
    init_db()
    if check_db_connection():
        print("   ✅ 数据库连接正常")
    else:
        print("   ❌ 数据库连接失败")
        all_passed = False
except Exception as e:
    print(f"   ❌ 数据库检查失败: {str(e)}")
    all_passed = False

# 4. 检查关键依赖
print()
print("4️⃣  检查关键依赖...")
required_packages = [
    "flask",
    "sqlalchemy",
    "langchain",
]

for package in required_packages:
    try:
        __import__(package)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} 未安装")
        all_passed = False

# 5. 检查配置
print()
print("5️⃣  检查配置...")
try:
    from dotenv import load_dotenv
    from pathlib import Path
    
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"   ✅ 环境变量已加载")
    else:
        print(f"   ❌ .env 文件不存在")
        all_passed = False
except Exception as e:
    print(f"   ❌ 配置检查失败: {str(e)}")
    all_passed = False

# 6. 检查 API 路由
print()
print("6️⃣  检查 API 路由...")
try:
    from src.api.routes import api_bp
    print(f"   ✅ API 蓝图已注册")
    print(f"   📋 已注册的端点: {len(api_bp.deferred_functions)}")
except Exception as e:
    print(f"   ❌ API 路由检查失败: {str(e)}")
    all_passed = False

# 7. 检查技能注册
print()
print("7️⃣  检查技能注册...")
try:
    import src.skills
    from src.utils.skill_registry import skill_registry
    
    print(f"   ✅ 技能注册表已初始化")
    print(f"   📋 已注册技能:")
    for skill_id, skill_info in skill_registry._skills.items():
        print(f"      - {skill_info.get('name')}: {skill_info.get('description')}")
    print(f"   📊 总计: {len(skill_registry._skills)} 个技能")
except Exception as e:
    print(f"   ❌ 技能注册检查失败: {str(e)}")
    all_passed = False

# 8. 检查小程序文件
print()
print("8️⃣  检查小程序文件...")
miniprogram_dir = project_root / "miniprogram"
if miniprogram_dir.exists():
    pages_dir = miniprogram_dir / "pages"
    if pages_dir.exists():
        page_count = len([d for d in pages_dir.iterdir() if d.is_dir()])
        print(f"   ✅ 小程序页面: {page_count} 个")
    else:
        print(f"   ❌ 小程序 pages 目录不存在")
        all_passed = False
else:
    print(f"   ❌ 小程序目录不存在")
    all_passed = False

# 总结
print()
print("=" * 60)
if all_passed:
    print("  ✅ 所有检查通过！可以启动项目")
    print()
    print("  启动命令:")
    print("    python3 src/main.py")
    print()
    print("  或使用启动脚本:")
    print("    ./start.sh      # Linux/Mac")
    print("    start.bat       # Windows")
else:
    print("  ❌ 部分检查失败，请修复后再启动")
    sys.exit(1)

print("=" * 60)
