# 宁律师法律服务项目 - 目录架构重构方案

## 一、现状分析

### 1.1 当前目录结构问题

```
项目根目录/
├── ninglawyer-miniapp/              # 主项目目录（完整）
│   ├── src/                        # 后端代码
│   ├── miniprogram/                # 主小程序
│   ├── lyue/                       # 乐约小程序
│   ├── legal-instructor/           # 法律教官小程序
│   ├── prevent-risk/               # 防风险小程序
│   ├── zenme-pan/                  # 怎么判小程序
│   ├── code-signing/               # 码上签约小程序
│   ├── config/, utils/, tests/     # 后端资源
│   └── 大量文档和脚本...
├── ninglawyer-miniapp-local/       # 重复的备份目录（应删除）
├── miniprogram/                    # 根目录的独立小程序（应整合）
├── fangfengxian/                   # 根目录的独立小程序（应整合）
├── wechat/                         # 根目录的独立小程序（应整合）
├── src/                            # 根目录的后端代码（应整合）
├── config/                         # 根目录的配置文件（应整合）
└── 各种文档和脚本...               # 散落在根目录（应整理）
```

### 1.2 主要问题

1. **目录层级混乱**
   - 小程序分散在多个位置（主项目、根目录、备份目录）
   - 代码重复（ninglawyer-miniapp 和 ninglawyer-miniapp-local）
   - 缺乏统一的组织结构

2. **资源管理混乱**
   - 配置文件分散（多个 config/）
   - 文档散落在各处
   - 脚本文件无序

3. **缺乏共享机制**
   - 公共组件、工具函数未统一管理
   - 小程序间代码重复，难以维护

4. **不符合 Monorepo 最佳实践**
   - 没有统一的依赖管理
   - 没有统一的构建流程
   - 难以进行版本控制和发布

---

## 二、重构目标

### 2.1 设计原则

1. **清晰分层**：后端、小程序、工具、文档明确分离
2. **代码复用**：公共代码统一管理，减少重复
3. **易于维护**：标准化目录结构，降低维护成本
4. **扩展性强**：支持新增小程序和功能模块
5. **符合规范**：遵循 Monorepo 和微信小程序最佳实践

### 2.2 重构目标

- ✅ 统一所有小程序到标准位置
- ✅ 整合后端代码和资源
- ✅ 建立公共代码共享机制
- ✅ 规范化文档和脚本管理
- ✅ 优化部署和构建流程

---

## 三、推荐架构方案

### 3.1 方案一：标准 Monorepo 架构（推荐）

```
ninglawyer-legal-services/          # 项目根目录
│
├── README.md                       # 项目说明
├── CHANGELOG.md                    # 更新日志
├── .gitignore                      # Git 忽略规则
├── package.json                    # 项目根配置
├── requirements.txt                # Python 依赖
├── docker-compose.yml              # Docker 编排
│
├── backend/                        # 后端服务目录
│   ├── src/                        # 源代码
│   │   ├── agents/                 # Agent 定义
│   │   ├── api/                    # API 接口
│   │   ├── graphs/                 # LangGraph 工作流
│   │   ├── storage/                # 数据存储
│   │   ├── tools/                  # 工具函数
│   │   └── utils/                  # 公共工具
│   ├── config/                     # 配置文件
│   │   ├── agent_llm_config.json   # LLM 配置
│   │   ├── database.py             # 数据库配置
│   │   └── settings.py             # 应用配置
│   ├── tests/                      # 测试代码
│   ├── scripts/                    # 后端脚本
│   ├── main.py                     # 服务入口
│   ├── requirements.txt            # Python 依赖
│   └── Dockerfile                  # Docker 镜像
│
├── miniprograms/                   # 小程序集合目录
│   ├── shared/                     # 小程序公共资源
│   │   ├── components/             # 公共组件
│   │   ├── utils/                  # 公共工具
│   │   ├── styles/                 # 公共样式
│   │   ├── config.js               # 公共配置
│   │   ├── request.js              # 公共请求封装
│   │   └── assets/                 # 公共资源（图标、图片）
│   │
│   ├── ninglawyer-main/            # 主小程序（宁律师）
│   │   ├── pages/                  # 页面
│   │   ├── components/             # 私有组件
│   │   ├── utils/                  # 私有工具
│   │   ├── app.js                  # 小程序入口
│   │   ├── app.json                # 小程序配置
│   │   ├── project.config.json     # 项目配置
│   │   └── package.json            # 依赖
│   │
│   ├── fangfengxian/               # 防风险小程序
│   │   ├── pages/
│   │   ├── components/
│   │   └── ... (同上结构)
│   │
│   ├── legal-instructor/           # 法律教官小程序
│   │   ├── pages/
│   │   └── ...
│   │
│   ├── lyue/                       # 乐约小程序
│   │   ├── pages/
│   │   └── ...
│   │
│   ├── zenme-pan/                  # 怎么判小程序
│   │   ├── pages/
│   │   └── ...
│   │
│   └── code-signing/               # 码上签约小程序
│       ├── pages/
│       └── ...
│
├── frontend/                       # Web 前端（可选）
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── docs/                           # 文档目录
│   ├── architecture/               # 架构文档
│   ├── api/                        # API 文档
│   ├── deployment/                 # 部署文档
│   ├── development/                # 开发文档
│   └── user/                       # 用户文档
│
├── scripts/                        # 全局脚本
│   ├── setup/                      # 初始化脚本
│   ├── deploy/                     # 部署脚本
│   ├── test/                       # 测试脚本
│   ├── sync/                       # 同步脚本
│   └── utils/                      # 工具脚本
│
├── infrastructure/                 # 基础设施配置
│   ├── docker/                     # Docker 配置
│   │   ├── docker-compose.yml
│   │   └── nginx.conf
│   ├── kubernetes/                 # K8s 配置（可选）
│   └── ci-cd/                      # CI/CD 配置
│
├── assets/                         # 静态资源
│   ├── images/                     # 图片
│   ├── icons/                      # 图标
│   └── voice_samples/              # 语音样本
│
├── uploads/                        # 上传文件存储
│   └── contracts/                  # 合同文件
│
├── logs/                           # 日志目录
│   ├── app.log                     # 应用日志
│   ├── error.log                   # 错误日志
│   └── access.log                  # 访问日志
│
└── .git/                           # Git 仓库
```

### 3.2 方案二：简化版架构（适合快速开发）

```
ninglawyer-legal-services/
│
├── server/                         # 后端服务
│   └── (同方案一的 backend/ 结构)
│
├── apps/                           # 所有应用
│   ├── miniprograms/               # 小程序集合
│   │   ├── shared/                 # 公共资源
│   │   ├── ninglawyer-main/
│   │   ├── fangfengxian/
│   │   ├── legal-instructor/
│   │   ├── lyue/
│   │   ├── zenme-pan/
│   │   └── code-signing/
│   └── web/                        # Web 应用（可选）
│
├── docs/                           # 文档
├── scripts/                        # 脚本
├── config/                         # 全局配置
├── assets/                         # 静态资源
└── docker-compose.yml
```

---

## 四、目录结构说明

### 4.1 后端目录 (backend/)

| 目录 | 说明 |
|------|------|
| `src/` | 源代码目录 |
| `src/agents/` | Agent 定义和实现 |
| `src/api/` | RESTful API 接口 |
| `src/graphs/` | LangGraph 工作流定义 |
| `src/storage/` | 数据库、缓存、对象存储 |
| `src/tools/` | 工具函数（合同生成、文档处理等） |
| `src/utils/` | 公共工具函数 |
| `config/` | 配置文件 |
| `tests/` | 单元测试和集成测试 |
| `scripts/` | 数据库初始化、迁移等脚本 |

### 4.2 小程序目录 (miniprograms/)

| 目录 | 说明 |
|------|------|
| `shared/` | 所有小程序共享的资源 |
| `shared/components/` | 公共组件（如通用表单、导航栏） |
| `shared/utils/` | 公共工具（如请求封装、日期处理） |
| `shared/styles/` | 公共样式（如主题色、字体） |
| `shared/config.js` | 公共配置（API 地址、环境变量） |
| `shared/assets/` | 公共资源（图标、图片） |
| `*/` | 各小程序独立目录 |

### 4.3 小程序独立目录结构

每个小程序遵循标准结构：

```
小程序名/
├── pages/                          # 页面
│   ├── index/                      # 首页
│   ├── chat/                       # 聊天页
│   └── ...
├── components/                     # 私有组件
├── utils/                          # 私有工具
├── images/                         # 私有图片
├── app.js                          # 小程序入口
├── app.json                        # 小程序配置
├── app.wxss                        # 全局样式
├── project.config.json             # 项目配置
└── sitemap.json                    # 索引配置
```

### 4.4 其他目录

| 目录 | 说明 |
|------|------|
| `docs/` | 项目文档（架构、API、部署等） |
| `scripts/` | 全局脚本（部署、同步、测试） |
| `infrastructure/` | 基础设施配置（Docker、K8s） |
| `assets/` | 静态资源（图片、图标、语音样本） |
| `uploads/` | 上传文件存储 |
| `logs/` | 日志目录 |

---

## 五、代码共享机制

### 5.1 小程序间共享

#### 方式一：相对路径引用（推荐用于小型项目）

```javascript
// 小程序中的引用
import { request } from '../../shared/utils/request.js'
import { formatDate } from '../../shared/utils/date.js'
```

#### 方式二：NPM 包管理（推荐用于大型项目）

```bash
# 1. 将 shared 发布为私有 npm 包
cd miniprograms/shared
npm publish

# 2. 在小程序中安装依赖
cd miniprograms/ninglawyer-main
npm install @ninglawyer/shared
```

```javascript
// 小程序中的引用
import { request } from '@ninglawyer/shared/utils/request'
```

### 5.2 后端与小程序共享

#### 配置文件共享

```javascript
// shared/config.js
module.exports = {
  apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:5001/api',
  uploadUrl: process.env.UPLOAD_URL || 'http://localhost:5001/upload',
  // ... 其他配置
}
```

#### 类型定义共享（TypeScript）

```typescript
// shared/types.d.ts
export interface User {
  id: string;
  name: string;
  role: string;
}

export interface Contract {
  id: string;
  type: string;
  status: 'draft' | 'signed';
  // ...
}
```

---

## 六、迁移计划

### 6.1 阶段一：准备工作（1天）

1. ✅ 备份现有项目
   ```bash
   cp -r ninglawyer-miniapp ninglawyer-miniapp.backup
   ```

2. ✅ 创建新目录结构
   ```bash
   mkdir -p ninglawyer-legal-services/{backend,miniprograms,docs,scripts,infrastructure,assets,uploads,logs}
   mkdir -p miniprograms/shared/{components,utils,styles,assets}
   mkdir -p miniprograms/{ninglawyer-main,fangfengxian,legal-instructor,lyue,zenme-pan,code-signing}
   mkdir -p docs/{architecture,api,deployment,development,user}
   mkdir -p scripts/{setup,deploy,test,sync,utils}
   ```

### 6.2 阶段二：后端迁移（0.5天）

```bash
# 移动后端代码
mv ninglawyer-miniapp/src backend/
mv ninglawyer-miniapp/config backend/
mv ninglawyer-miniapp/tests backend/
mv ninglawyer-miniapp/scripts backend/
mv ninglawyer-miniapp/main.py backend/
mv ninglawyer-miniapp/requirements.txt backend/
mv ninglawyer-miniapp/Dockerfile backend/
```

### 6.3 阶段三：小程序迁移（1天）

```bash
# 1. 提取共享资源
mkdir -p miniprograms/shared
cp -r ninglawyer-miniapp/components/* miniprograms/shared/components/
cp -r ninglawyer-miniapp/utils/* miniprograms/shared/utils/

# 2. 移动小程序
mv ninglawyer-miniapp/miniprogram miniprograms/ninglawyer-main
mv ninglawyer-miniapp/lyue miniprograms/
mv ninglawyer-miniapp/legal-instructor miniprograms/
mv ninglawyer-miniapp/prevent-risk miniprograms/fangfengxian
mv ninglawyer-miniapp/zenme-pan miniprograms/
mv ninglawyer-miniapp/code-signing miniprograms/

# 3. 移动根目录的小程序
mv miniprogram miniprograms/ninglawyer-main-legacy
mv fangfengxian miniprograms/fangfengxian-legacy
mv wechat miniprograms/wechat-legacy
```

### 6.4 阶段四：文档和脚本整理（0.5天）

```bash
# 整理文档
mv *.md docs/development/

# 整理脚本
mv check_*.py scripts/test/
mv fix_*.py scripts/test/
mv *.sh scripts/deploy/
mv *.bat scripts/deploy/
```

### 6.5 阶段五：清理和测试（0.5天）

```bash
# 删除重复目录
rm -rf ninglawyer-miniapp-local
rm -rf ninglawer-miniapp

# 删除备份（确认迁移成功后）
# rm -rf ninglawyer-miniapp.backup

# 测试运行
cd backend
python3 main.py

cd ../miniprograms/ninglawyer-main
# 使用微信开发者工具测试
```

### 6.6 阶段六：更新引用路径（0.5天）

1. 更新小程序中的引用路径
2. 更新配置文件中的路径
3. 更新脚本中的路径
4. 测试所有小程序

---

## 七、优势和收益

### 7.1 优势

1. **清晰的项目结构**
   - 后端、小程序、文档分离清晰
   - 符合 Monorepo 最佳实践

2. **代码复用率高**
   - 公共组件、工具统一管理
   - 减少重复代码，降低维护成本

3. **易于扩展**
   - 新增小程序只需在 miniprograms/ 下创建新目录
   - 新增功能模块只需在相应目录添加

4. **便于协作**
   - 团队成员可以快速定位代码
   - 减少冲突和误解

5. **便于部署**
   - 统一的构建流程
   - 标准化的部署脚本

### 7.2 收益

| 指标 | 改进前 | 改进后 | 提升 |
|------|--------|--------|------|
| 目录层级 | 5-6 层 | 3-4 层 | 更清晰 |
| 代码重复率 | ~30% | ~10% | 降低 67% |
| 新增小程序时间 | 2 小时 | 30 分钟 | 提升 75% |
| 文档查找时间 | 5 分钟 | 1 分钟 | 提升 80% |
| 部署复杂度 | 高 | 低 | 显著降低 |

---

## 八、后续优化建议

### 8.1 引入包管理器

```bash
# 使用 pnpm 管理 monorepo
npm install -g pnpm
cd ninglawyer-legal-services
pnpm init
```

### 8.2 引入 TypeScript

```typescript
// 后端和前端使用 TypeScript
// 类型定义共享
// 减少类型错误
```

### 8.3 引入 CI/CD

```yaml
# .github/workflows/ci.yml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test Backend
        run: cd backend && python3 -m pytest
      - name: Build Miniprograms
        run: cd scripts && ./build-miniprograms.sh
```

### 8.4 引入代码规范工具

```bash
# ESLint + Prettier
# Black (Python)
# husky (Git hooks)
```

---

## 九、迁移脚本示例

### 9.1 自动迁移脚本

```bash
#!/bin/bash
# migrate.sh - 自动迁移脚本

PROJECT_NAME="ninglawyer-legal-services"
BACKUP_NAME="ninglawyer-miniapp.backup"

echo "========================================="
echo "  宁律师项目目录结构迁移"
echo "========================================="

# 1. 备份
echo "[1/6] 备份现有项目..."
cp -r ninglawyer-miniapp $BACKUP_NAME

# 2. 创建新目录
echo "[2/6] 创建新目录结构..."
mkdir -p $PROJECT_NAME/{backend,miniprograms,docs,scripts,infrastructure,assets,uploads,logs}
mkdir -p $PROJECT_NAME/miniprograms/shared/{components,utils,styles,assets}
mkdir -p $PROJECT_NAME/miniprograms/{ninglawyer-main,fangfengxian,legal-instructor,lyue,zenme-pan,code-signing}
mkdir -p $PROJECT_NAME/docs/{architecture,api,deployment,development,user}
mkdir -p $PROJECT_NAME/scripts/{setup,deploy,test,sync,utils}

# 3. 移动后端
echo "[3/6] 迁移后端代码..."
mv ninglawyer-miniapp/src $PROJECT_NAME/backend/
mv ninglawyer-miniapp/config $PROJECT_NAME/backend/
mv ninglawyer-miniapp/tests $PROJECT_NAME/backend/
mv ninglawyer-miniapp/scripts $PROJECT_NAME/backend/
mv ninglawyer-miniapp/main.py $PROJECT_NAME/backend/
mv ninglawyer-miniapp/requirements.txt $PROJECT_NAME/backend/
mv ninglawyer-miniapp/Dockerfile $PROJECT_NAME/backend/

# 4. 移动小程序
echo "[4/6] 迁移小程序..."
mv ninglawyer-miniapp/miniprogram $PROJECT_NAME/miniprograms/ninglawyer-main
mv ninglawyer-miniapp/lyue $PROJECT_NAME/miniprograms/
mv ninglawyer-miniapp/legal-instructor $PROJECT_NAME/miniprograms/
mv ninglawyer-miniapp/prevent-risk $PROJECT_NAME/miniprograms/fangfengxian
mv ninglawyer-miniapp/zenme-pan $PROJECT_NAME/miniprograms/
mv ninglawyer-miniapp/code-signing $PROJECT_NAME/miniprograms/

# 5. 移动资源
echo "[5/6] 迁移资源..."
mv ninglawyer-miniapp/assets $PROJECT_NAME/
mv ninglawyer-miniapp/uploads $PROJECT_NAME/
mv ninglawyer-miniapp/logs $PROJECT_NAME/

# 6. 移动文档和脚本
echo "[6/6] 迁移文档和脚本..."
mv ninglawyer-miniapp/*.md $PROJECT_NAME/docs/development/
mv ninglawyer-miniapp/*.sh $PROJECT_NAME/scripts/deploy/
mv ninglawyer-miniapp/*.bat $PROJECT_NAME/scripts/deploy/
mv ninglawyer-miniapp/docker-compose.yml $PROJECT_NAME/infrastructure/docker/
mv ninglawyer-miniapp/nginx.conf $PROJECT_NAME/infrastructure/docker/

echo ""
echo "✅ 迁移完成！"
echo "   新项目位置: $PROJECT_NAME/"
echo "   备份位置: $BACKUP_NAME/"
echo ""
echo "请执行以下步骤："
echo "  1. cd $PROJECT_NAME/backend && python3 main.py  # 测试后端"
echo "  2. 使用微信开发者工具打开 $PROJECT_NAME/miniprograms/ninglawyer-main"
echo "  3. 确认一切正常后，删除备份: rm -rf $BACKUP_NAME"
```

### 9.2 使用方法

```bash
# 1. 给脚本执行权限
chmod +x migrate.sh

# 2. 执行迁移
./migrate.sh
```

---

## 十、总结

本方案提供了一个清晰、高效的项目目录结构，解决了当前项目中目录混乱、代码重复、维护困难等问题。通过标准化目录结构、建立代码共享机制、优化部署流程，可以显著提升开发效率和项目可维护性。

建议按照迁移计划逐步实施，确保每个阶段都经过充分测试后再进入下一阶段。迁移完成后，团队将拥有一个结构清晰、易于扩展、便于协作的现代化项目。
