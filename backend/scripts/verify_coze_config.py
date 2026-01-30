"""
扣子API配置验证脚本
"""

import os
import sys


def verify_environment():
    """验证环境变量配置"""
    print("🔍 验证扣子API配置...\n")
    
    # 检查必需的环境变量
    required_vars = {
        "COZE_CLIENT_ID": "扣子Client ID",
        "COZE_CLIENT_SECRET": "扣子Client Secret",
    }
    
    optional_vars = {
        "COZE_API_BASE_URL": "扣子API基础URL（默认：https://api.coze.cn）",
    }
    
    all_ok = True
    
    # 检查必需变量
    print("📌 必需配置：")
    for var_name, var_desc in required_vars.items():
        value = os.getenv(var_name)
        if value:
            # 隐藏敏感信息
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"  ✅ {var_name}: {masked_value} ({var_desc})")
        else:
            print(f"  ❌ {var_name}: 未配置 ({var_desc})")
            all_ok = False
    
    # 检查可选变量
    print("\n📌 可选配置：")
    for var_name, var_desc in optional_vars.items():
        value = os.getenv(var_name)
        if value:
            print(f"  ✅ {var_name}: {value} ({var_desc})")
        else:
            print(f"  ⚠️  {var_name}: 未配置，将使用默认值 ({var_desc})")
    
    return all_ok


def test_connection():
    """测试连接"""
    print("\n🔗 测试连接...\n")
    
    try:
        from backend.src.services.coze_agent_service import get_coze_agent_service
        
        service = get_coze_agent_service()
        
        # 测试获取Token
        print("  测试获取Access Token...")
        token = service.auth.get_access_token()
        print(f"  ✅ Access Token获取成功: {token[:20]}...")
        
        # 测试获取Bot列表
        print("\n  测试获取Bot列表...")
        result = service.get_bot_list(page_size=5)
        
        if result.get("success"):
            total = result.get("total", 0)
            bots = result.get("bots", [])
            print(f"  ✅ 成功获取Bot列表，共 {total} 个Bot")
            
            if bots:
                print("\n  📋 可用的Bot:")
                for bot in bots[:5]:  # 只显示前5个
                    bot_id = bot.get("bot_id", "未知")
                    bot_name = bot.get("bot_name", "未知")
                    print(f"    - {bot_name} (ID: {bot_id})")
        else:
            print(f"  ❌ 获取Bot列表失败: {result.get('error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ 连接测试失败: {str(e)}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("  扣子API配置验证工具")
    print("=" * 60)
    print()
    
    # 验证环境变量
    env_ok = verify_environment()
    
    if not env_ok:
        print("\n❌ 配置验证失败，请配置必要的环境变量")
        print("\n📝 配置示例：")
        print("  export COZE_CLIENT_ID=your_client_id")
        print("  export COZE_CLIENT_SECRET=your_client_secret")
        print("  export COZE_API_BASE_URL=https://api.coze.cn")
        sys.exit(1)
    
    # 测试连接
    connection_ok = test_connection()
    
    print("\n" + "=" * 60)
    if connection_ok:
        print("  ✅ 配置验证通过！可以正常使用扣子API")
    else:
        print("  ❌ 配置验证失败，请检查配置")
    print("=" * 60)
    
    sys.exit(0 if connection_ok else 1)


if __name__ == "__main__":
    main()
