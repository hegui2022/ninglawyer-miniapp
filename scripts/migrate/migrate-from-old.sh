#!/bin/bash
# =================================================================
# 宁律师项目快速迁移脚本
# =================================================================
# 功能：将现有的项目文件迁移到 Monorepo 架构
# =================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 打印横幅
print_banner() {
    echo -e "${BLUE}"
    echo "========================================"
    echo "  宁律师项目快速迁移脚本"
    echo "========================================"
    echo -e "${NC}"
}

# 迁移小程序
migrate_miniprogram() {
    local source_dir=$1
    local target_dir=$2

    if [ -d "$source_dir" ]; then
        log "迁移小程序: $source_dir -> $target_dir"
        cp -r "$source_dir"/* "ninglawyer-legal-services/$target_dir/"
        log_success "✓ 小程序迁移完成"
    else
        log_warning "源目录不存在: $source_dir"
    fi
}

# 主函数
main() {
    print_banner

    log "开始迁移..."

    # 1. 迁移后端代码
    log "[1/6] 迁移后端代码..."
    if [ -d "ninglawyer-miniapp/src" ]; then
        cp -r ninglawyer-miniapp/src/* ninglawyer-legal-services/backend/src/
        log_success "✓ 后端源代码迁移完成"
    fi

    if [ -d "ninglawyer-miniapp/config" ]; then
        cp -r ninglawyer-miniapp/config/* ninglawyer-legal-services/backend/config/
        log_success "✓ 后端配置迁移完成"
    fi

    if [ -f "ninglawyer-miniapp/main.py" ]; then
        cp ninglawyer-miniapp/main.py ninglawyer-legal-services/backend/
        log_success "✓ 后端入口文件迁移完成"
    fi

    if [ -f "ninglawyer-miniapp/requirements.txt" ]; then
        cp ninglawyer-miniapp/requirements.txt ninglawyer-legal-services/backend/
        log_success "✓ 后端依赖文件迁移完成"
    fi

    # 2. 迁移小程序
    log "[2/6] 迁移小程序..."
    migrate_miniprogram "ninglawyer-miniapp/miniprogram" "miniprograms/ninglawyer-main"
    migrate_miniprogram "ninglawyer-miniapp/prevent-risk" "miniprograms/fangfengxian"
    migrate_miniprogram "ninglawyer-miniapp/legal-instructor" "miniprograms/legal-instructor"
    migrate_miniprogram "ninglawyer-miniapp/lyue" "miniprograms/lyue"
    migrate_miniprogram "ninglawyer-miniapp/zenme-pan" "miniprograms/zenme-pan"
    migrate_miniprogram "ninglawyer-miniapp/code-signing" "miniprograms/code-signing"

    # 处理根目录的小程序
    if [ -d "miniprogram" ]; then
        log "迁移根目录小程序: miniprogram -> miniprograms/ninglawyer-main-legacy"
        cp -r miniprogram/* ninglawyer-legal-services/miniprograms/ninglawyer-main-legacy/
        log_success "✓ 根目录小程序迁移完成"
    fi

    # 3. 迁移资源文件
    log "[3/6] 迁移资源文件..."
    if [ -d "ninglawyer-miniapp/assets" ]; then
        cp -r ninglawyer-miniapp/assets/* ninglawyer-legal-services/assets/
        log_success "✓ 资源文件迁移完成"
    fi

    # 4. 迁移文档
    log "[4/6] 迁移文档..."
    if ls *.md 1> /dev/null 2>&1; then
        cp *.md ninglawyer-legal-services/docs/development/
        log_success "✓ 文档迁移完成"
    fi

    # 5. 迁移脚本
    log "[5/6] 迁移脚本..."
    if ls *.sh 1> /dev/null 2>&1; then
        cp *.sh ninglawyer-legal-services/scripts/deploy/
        log_success "✓ 脚本迁移完成"
    fi

    if ls *.py 1> /dev/null 2>&1; then
        cp *.py ninglawyer-legal-services/scripts/test/
        log_success "✓ Python 脚本迁移完成"
    fi

    # 6. 迁移基础设施配置
    log "[6/6] 迁移基础设施配置..."
    if [ -f "ninglawyer-miniapp/docker-compose.yml" ]; then
        cp ninglawyer-miniapp/docker-compose.yml ninglawyer-legal-services/infrastructure/docker/
        log_success "✓ Docker 配置迁移完成"
    fi

    # 创建 .gitkeep 文件
    touch ninglawyer-legal-services/uploads/.gitkeep
    touch ninglawyer-legal-services/logs/.gitkeep

    # 完成
    echo ""
    echo -e "${GREEN}========================================"
    echo "  迁移完成！"
    echo "========================================${NC}"
    echo ""
    echo -e "${BLUE}新项目位置:${NC} ninglawyer-legal-services/"
    echo ""
    echo -e "${YELLOW}后续步骤:${NC}"
    echo "  1. cd ninglawyer-legal-services/backend && python3 main.py  # 测试后端"
    echo "  2. cd packages/@ninglawyer/shared && npm install              # 安装共享包"
    echo "  3. cd miniprograms/ninglawyer-main && npm install              # 安装小程序依赖"
    echo "  4. 使用微信开发者工具打开 ninglawyer-legal-services/miniprograms/ninglawyer-main"
    echo ""
    echo -e "${YELLOW}重要提示:${NC}"
    echo "  - 小程序中的引用路径需要更新"
    echo "  - 建议查看 MIGRATION_GUIDE.md 了解详细信息"
    echo "  - 建议保留旧目录至少一周，以便回滚"
    echo ""
}

# 执行主函数
main
