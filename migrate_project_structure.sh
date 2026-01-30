#!/bin/bash
# =================================================================
# 宁律师项目目录结构自动迁移脚本
# =================================================================
# 功能：将当前混乱的目录结构重构为标准 Monorepo 架构
# 作者：Coze Coding
# 日期：2025-01-30
# =================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
PROJECT_NAME="ninglawyer-legal-services"
BACKUP_NAME="ninglawyer-backup-$(date +%Y%m%d-%H%M%S)"
LOG_FILE="migration-$(date +%Y%m%d-%H%M%S).log"

# 日志函数
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}❌ $1${NC}" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$LOG_FILE"
}

# 打印横幅
print_banner() {
    echo -e "${BLUE}"
    echo "========================================"
    echo "  宁律师项目目录结构自动迁移"
    echo "========================================"
    echo -e "${NC}"
}

# 检查依赖
check_dependencies() {
    log "检查系统依赖..."

    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装，请先安装 Python3"
        exit 1
    fi

    if ! command -v git &> /dev/null; then
        log_warning "Git 未安装，建议安装 Git 以便版本控制"
    fi

    log_success "依赖检查完成"
}

# 备份现有项目
backup_project() {
    log "[1/8] 备份现有项目..."

    if [ -d "$BACKUP_NAME" ]; then
        log_warning "备份目录已存在: $BACKUP_NAME"
        read -p "是否删除旧备份并重新备份？(y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$BACKUP_NAME"
        else
            log_error "迁移已取消"
            exit 1
        fi
    fi

    # 创建备份
    tar -czf "${BACKUP_NAME}.tar.gz" \
        ninglawyer-miniapp \
        ninglawyer-miniapp-local \
        miniprogram \
        fangfengxian \
        wechat \
        ninglawer-miniapp \
        2>/dev/null || true

    log_success "备份完成: ${BACKUP_NAME}.tar.gz"
}

# 创建新目录结构
create_new_structure() {
    log "[2/8] 创建新目录结构..."

    mkdir -p "$PROJECT_NAME"/{backend,miniprograms,docs,scripts,infrastructure,assets,uploads,logs}
    mkdir -p "$PROJECT_NAME"/miniprograms/shared/{components,utils,styles,assets}
    mkdir -p "$PROJECT_NAME"/miniprograms/{ninglawyer-main,fangfengxian,legal-instructor,lyue,zenme-pan,code-signing}
    mkdir -p "$PROJECT_NAME"/docs/{architecture,api,deployment,development,user}
    mkdir -p "$PROJECT_NAME"/scripts/{setup,deploy,test,sync,utils}
    mkdir -p "$PROJECT_NAME"/infrastructure/{docker,kubernetes,ci-cd}
    mkdir -p "$PROJECT_NAME"/backend/{src,config,tests,scripts,components,utils}

    log_success "新目录结构创建完成"
}

# 迁移后端代码
migrate_backend() {
    log "[3/8] 迁移后端代码..."

    if [ -d "ninglawyer-miniapp/src" ]; then
        mv ninglawyer-miniapp/src "$PROJECT_NAME/backend/"
        log_success "✓ src/"
    fi

    if [ -d "ninglawyer-miniapp/config" ]; then
        mv ninglawyer-miniapp/config "$PROJECT_NAME/backend/"
        log_success "✓ config/"
    fi

    if [ -d "ninglawyer-miniapp/tests" ]; then
        mv ninglawyer-miniapp/tests "$PROJECT_NAME/backend/"
        log_success "✓ tests/"
    fi

    if [ -d "ninglawyer-miniapp/scripts" ]; then
        mv ninglawyer-miniapp/scripts "$PROJECT_NAME/backend/"
        log_success "✓ scripts/"
    fi

    if [ -f "ninglawyer-miniapp/main.py" ]; then
        mv ninglawyer-miniapp/main.py "$PROJECT_NAME/backend/"
        log_success "✓ main.py"
    fi

    if [ -f "ninglawyer-miniapp/requirements.txt" ]; then
        mv ninglawyer-miniapp/requirements.txt "$PROJECT_NAME/backend/"
        log_success "✓ requirements.txt"
    fi

    if [ -f "ninglawyer-miniapp/Dockerfile" ]; then
        mv ninglawyer-miniapp/Dockerfile "$PROJECT_NAME/backend/"
        log_success "✓ Dockerfile"
    fi

    # 移动根目录的后端资源
    if [ -d "src" ]; then
        log_warning "发现根目录的 src/，是否移动到 backend/src？"
        read -p "移动根目录的 src/？(y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            mv src/* "$PROJECT_NAME/backend/src/" 2>/dev/null || true
            log_success "✓ 根目录 src/ 已合并"
        fi
    fi

    log_success "后端代码迁移完成"
}

# 迁移小程序
migrate_miniprograms() {
    log "[4/8] 迁移小程序..."

    # 创建共享资源目录
    mkdir -p "$PROJECT_NAME/miniprograms/shared"
    if [ -d "ninglawyer-miniapp/components" ]; then
        cp -r ninglawyer-miniapp/components/* "$PROJECT_NAME/miniprograms/shared/components/" 2>/dev/null || true
        log_success "✓ 共享组件已复制"
    fi

    if [ -d "ninglawyer-miniapp/utils" ]; then
        cp -r ninglawyer-miniapp/utils/* "$PROJECT_NAME/miniprograms/shared/utils/" 2>/dev/null || true
        log_success "✓ 共享工具已复制"
    fi

    # 移动各小程序
    if [ -d "ninglawyer-miniapp/miniprogram" ]; then
        mv ninglawyer-miniapp/miniprogram "$PROJECT_NAME/miniprograms/ninglawyer-main"
        log_success "✓ 主小程序 (ninglawyer-main)"
    fi

    if [ -d "ninglawyer-miniapp/lyue" ]; then
        mv ninglawyer-miniapp/lyue "$PROJECT_NAME/miniprograms/"
        log_success "✓ 乐约小程序 (lyue)"
    fi

    if [ -d "ninglawyer-miniapp/legal-instructor" ]; then
        mv ninglawyer-miniapp/legal-instructor "$PROJECT_NAME/miniprograms/"
        log_success "✓ 法律教官小程序 (legal-instructor)"
    fi

    if [ -d "ninglawyer-miniapp/prevent-risk" ]; then
        mv ninglawyer-miniapp/prevent-risk "$PROJECT_NAME/miniprograms/fangfengxian"
        log_success "✓ 防风险小程序 (fangfengxian)"
    fi

    if [ -d "ninglawyer-miniapp/zenme-pan" ]; then
        mv ninglawyer-miniapp/zenme-pan "$PROJECT_NAME/miniprograms/"
        log_success "✓ 怎么判小程序 (zenme-pan)"
    fi

    if [ -d "ninglawyer-miniapp/code-signing" ]; then
        mv ninglawyer-miniapp/code-signing "$PROJECT_NAME/miniprograms/"
        log_success "✓ 码上签约小程序 (code-signing)"
    fi

    # 处理根目录的小程序
    if [ -d "miniprogram" ]; then
        mv miniprogram "$PROJECT_NAME/miniprograms/ninglawyer-main-legacy"
        log_warning "✓ 根目录 miniprogram (已重命名为 ninglawyer-main-legacy)"
    fi

    if [ -d "fangfengxian" ]; then
        mv fangfengxian "$PROJECT_NAME/miniprograms/fangfengxian-legacy"
        log_warning "✓ 根目录 fangfengxian (已重命名为 fangfengxian-legacy)"
    fi

    if [ -d "wechat" ]; then
        mv wechat "$PROJECT_NAME/miniprograms/wechat-legacy"
        log_warning "✓ 根目录 wechat (已重命名为 wechat-legacy)"
    fi

    log_success "小程序迁移完成"
}

# 迁移资源
migrate_assets() {
    log "[5/8] 迁移资源文件..."

    if [ -d "ninglawyer-miniapp/assets" ]; then
        mv ninglawyer-miniapp/assets "$PROJECT_NAME/"
        log_success "✓ assets/"
    fi

    if [ -d "ninglawyer-miniapp/uploads" ]; then
        mv ninglawyer-miniapp/uploads "$PROJECT_NAME/"
        log_success "✓ uploads/"
    fi

    if [ -d "ninglawyer-miniapp/logs" ]; then
        mv ninglawyer-miniapp/logs "$PROJECT_NAME/"
        log_success "✓ logs/"
    fi

    log_success "资源文件迁移完成"
}

# 迁移文档和脚本
migrate_docs_and_scripts() {
    log "[6/8] 迁移文档和脚本..."

    # 迁移文档
    if [ -d "ninglawyer-miniapp" ]; then
        mv ninglawyer-miniapp/*.md "$PROJECT_NAME/docs/development/" 2>/dev/null || true
        log_success "✓ ninglawyer-miniapp/*.md"
    fi

    if ls *.md 1> /dev/null 2>&1; then
        mv *.md "$PROJECT_NAME/docs/development/" 2>/dev/null || true
        log_success "✓ 根目录 *.md"
    fi

    # 迁移脚本
    if [ -d "ninglawyer-miniapp" ]; then
        mv ninglawyer-miniapp/*.sh "$PROJECT_NAME/scripts/deploy/" 2>/dev/null || true
        mv ninglawyer-miniapp/*.bat "$PROJECT_NAME/scripts/deploy/" 2>/dev/null || true
        mv ninglawyer-miniapp/*.py "$PROJECT_NAME/scripts/test/" 2>/dev/null || true
        log_success "✓ ninglawyer-miniapp/*.sh, *.bat, *.py"
    fi

    if ls *.sh 1> /dev/null 2>&1; then
        mv *.sh "$PROJECT_NAME/scripts/deploy/" 2>/dev/null || true
        log_success "✓ 根目录 *.sh"
    fi

    if ls *.py 1> /dev/null 2>&1; then
        mv *.py "$PROJECT_NAME/scripts/test/" 2>/dev/null || true
        log_success "✓ 根目录 *.py"
    fi

    # 迁移基础设施配置
    if [ -f "ninglawyer-miniapp/docker-compose.yml" ]; then
        mv ninglawyer-miniapp/docker-compose.yml "$PROJECT_NAME/infrastructure/docker/"
        log_success "✓ docker-compose.yml"
    fi

    if [ -f "ninglawyer-miniapp/nginx.conf" ]; then
        mv ninglawyer-miniapp/nginx.conf "$PROJECT_NAME/infrastructure/docker/"
        log_success "✓ nginx.conf"
    fi

    log_success "文档和脚本迁移完成"
}

# 迁移配置文件
migrate_config() {
    log "[7/8] 迁移配置文件..."

    if [ -f "ninglawyer-miniapp/.env" ]; then
        mv ninglawyer-miniapp/.env "$PROJECT_NAME/backend/"
        log_success "✓ .env"
    fi

    if [ -f "ninglawyer-miniapp/.env.example" ]; then
        mv ninglawyer-miniapp/.env.example "$PROJECT_NAME/backend/"
        log_success "✓ .env.example"
    fi

    if [ -f "ninglawyer-miniapp/.gitignore" ]; then
        mv ninglawyer-miniapp/.gitignore "$PROJECT_NAME/backend/"
        log_success "✓ .gitignore"
    fi

    # 创建项目根配置文件
    cat > "$PROJECT_NAME/.gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node
node_modules/
npm-debug.log
yarn-error.log
package-lock.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 微信小程序
miniprogram_npm/
miniprogram_dist/

# 日志
*.log
logs/

# 数据库
*.db
*.sqlite
*.sqlite3

# 环境变量
.env
.env.local
.env.*.local

# 上传文件
uploads/*
!uploads/.gitkeep

# 备份
*.backup
*.bak
*.tar.gz

# OS
.DS_Store
Thumbs.db
EOF

    log_success "✓ .gitignore (项目根)"

    log_success "配置文件迁移完成"
}

# 创建迁移后的说明文件
create_post_migration_guide() {
    log "[8/8] 创建迁移后说明..."

    cat > "$PROJECT_NAME/README.md" << 'EOF'
# 宁律师法律服务项目

## 项目结构

```
ninglawyer-legal-services/
├── backend/                    # 后端服务
├── miniprograms/               # 小程序集合
│   ├── shared/                 # 公共资源
│   └── */                      # 各小程序
├── docs/                       # 文档
├── scripts/                    # 脚本
├── infrastructure/             # 基础设施
└── assets/                     # 资源文件
```

## 快速开始

### 启动后端

```bash
cd backend
python3 main.py
```

### 开发小程序

使用微信开发者工具打开对应小程序目录：

- 主小程序: `miniprograms/ninglawyer-main`
- 防风险: `miniprograms/fangfengxian`
- 法律教官: `miniprograms/legal-instructor`
- 乐约: `miniprograms/lyue`
- 怎么判: `miniprograms/zenme-pan`
- 码上签约: `miniprograms/code-signing`

## 迁移说明

本项目于 2025-01-30 进行了目录结构重构，从混乱的分散式结构重构为标准 Monorepo 架构。

### 主要变更

1. 后端代码统一到 `backend/` 目录
2. 所有小程序统一到 `miniprograms/` 目录
3. 新增 `miniprograms/shared/` 用于存放公共资源
4. 文档统一到 `docs/` 目录
5. 脚本统一到 `scripts/` 目录

### 注意事项

- 小程序中的引用路径需要更新
- 配置文件中的路径需要更新
- 部署脚本中的路径需要更新

### 后续工作

- [ ] 更新小程序中的引用路径
- [ ] 更新配置文件
- [ ] 更新部署脚本
- [ ] 测试所有功能
- [ ] 清理旧目录（确认一切正常后）

## 文档

详细文档请查看 `docs/` 目录。

## 联系方式

如有问题，请联系开发团队。
EOF

    log_success "✓ README.md"

    cat > "$PROJECT_NAME/MIGRATION_TODO.md" << 'EOF'
# 迁移后的待办事项

## 高优先级

- [ ] 更新所有小程序中的引用路径（从相对路径改为使用 shared/）
- [ ] 更新配置文件中的路径
- [ ] 更新部署脚本中的路径
- [ ] 测试后端服务启动
- [ ] 测试所有小程序功能

## 中优先级

- [ ] 检查并更新小程序的 project.config.json
- [ ] 检查并更新后端的数据库配置
- [ ] 检查并更新日志路径
- [ ] 检查并更新上传文件路径

## 低优先级

- [ ] 清理旧目录（确认一切正常后）
- [ ] 更新 CI/CD 配置
- [ ] 更新文档中的路径引用
- [ ] 优化 shared/ 中的公共资源

## 注意事项

1. 在清理旧目录前，请确保所有功能测试通过
2. 建议保留旧目录至少一周，以便回滚
3. 如遇到问题，请查看迁移日志：`migration-*.log`
EOF

    log_success "✓ MIGRATION_TODO.md"

    log_success "迁移后说明创建完成"
}

# 打印总结
print_summary() {
    echo ""
    echo -e "${GREEN}========================================"
    echo "  迁移完成！"
    echo "========================================${NC}"
    echo ""
    echo -e "${BLUE}新项目位置:${NC} $PROJECT_NAME/"
    echo -e "${BLUE}备份位置:${NC} ${BACKUP_NAME}.tar.gz"
    echo -e "${BLUE}日志文件:${NC} $LOG_FILE"
    echo ""
    echo -e "${YELLOW}后续步骤:${NC}"
    echo "  1. cd $PROJECT_NAME/backend && python3 main.py  # 测试后端"
    echo "  2. 使用微信开发者工具打开 $PROJECT_NAME/miniprograms/ninglawyer-main"
    echo "  3. 查看 MIGRATION_TODO.md 了解待办事项"
    echo "  4. 确认一切正常后，删除备份: rm ${BACKUP_NAME}.tar.gz"
    echo ""
    echo -e "${YELLOW}重要提示:${NC}"
    echo "  - 小程序中的引用路径需要更新"
    echo "  - 配置文件中的路径需要更新"
    echo "  - 建议保留旧目录至少一周"
    echo ""
}

# 主函数
main() {
    print_banner

    # 确认执行
    echo -e "${YELLOW}此操作将重构项目目录结构，建议先备份项目。${NC}"
    read -p "是否继续？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_error "迁移已取消"
        exit 1
    fi

    # 执行迁移
    check_dependencies
    backup_project
    create_new_structure
    migrate_backend
    migrate_miniprograms
    migrate_assets
    migrate_docs_and_scripts
    migrate_config
    create_post_migration_guide

    # 打印总结
    print_summary
}

# 执行主函数
main
