# 防风险小程序 - 快速开始

## 项目概述
这是一个基于微信小程序框架开发的企业合规风险管理平台，包含登录、指引、管理、发现、我的等核心功能模块。

## 代码位置
代码已保存在：`/workspace/projects/fangfengxian/`

## 下载方式

### 方式一：直接复制文件
1. 在您的本地创建项目文件夹
2. 从服务器复制 `fangfengxian/` 目录下的所有文件到您的本地

### 方式二：使用 git（推荐）
```bash
# 1. 初始化本地仓库
git init
git remote add origin <您的仓库地址>

# 2. 从服务器拉取代码
# （需要您先获取服务器访问权限）

# 3. 提交代码
git add .
git commit -m "feat: 初始化防风险小程序项目"
git push -u origin main
```

## 项目结构
```
fangfengxian/
├── app.js                  # 小程序入口文件
├── app.json                # 全局配置
├── app.wxss                # 全局样式
├── components/             # 公共组件
│   ├── nav-bar/           # 导航栏组件
│   ├── content-card/      # 内容卡片组件
│   ├── comment-list/      # 留言列表组件
│   ├── home-indicator/    # Home指示条组件
│   └── tab-bar/           # TabBar导航组件
├── pages/                  # 页面文件
│   ├── login/             # 登录页
│   ├── guide/             # 指引页
│   │   └── article/       # 文章详情页
│   ├── obligation/        # 义务页（TabBar）
│   ├── manage/            # 管理页（TabBar）
│   ├── discover/          # 发现页（TabBar）
│   ├── profile/           # 我的页（TabBar）
│   │   └── company/       # 我的公司子页面
│   │       ├── articles/              # 公司章程页
│   │       ├── data-compliance/      # 数据合规页
│   │       └── procurement-compliance/ # 采购合规页
│   └── department/        # 部门页面
├── images/                 # 图片资源
│   └── tabbar/            # TabBar图标
└── README.md              # 项目说明文档
```

## 功能模块

### 1. 登录页（pages/login）
- 微信登录
- 手机号登录

### 2. 指引页（pages/guide）
- 法律指引内容列表
- 展开/收起交互
- 文章详情页

### 3. 管理页（pages/manage）
- 一键办公：会议通知、出资协议、入股声明、上传文件
- 重点部门：人力资源部、销售部、财务部
- 违规举报信
- 项目审批

### 4. 发现页（pages/discover）
- 行业监管动态
- 合规培训
- 消息
- 合同场景师

### 5. 我的页（pages/profile）
- 个人信息展示
- 我的公司入口
- 我的岗位入口

### 6. 部门页面（pages/department）
- 工作阶段标签：招聘、入职、在职、离职
- 岗位列表
- 聊天消息区
- 底部聊天工具栏
- 功能面板

### 7. 我的公司子页面
- 公司页（pages/profile/company/company）：合规要闻、基础合规、采购合规、数据合规
- 数据合规页（pages/profile/company/data-compliance）：风险识别、管理制度
- 采购合规页（pages/profile/company/procurement-compliance）：风险识别、合规义务、权力清单
- 公司章程页（pages/profile/company/articles）：公司基本信息、组织架构、议事规则

## 开发指南

### 环境要求
- 微信开发者工具（最新版）
- 微信小程序开发账号

### 本地开发步骤

1. **下载微信开发者工具**
   - 访问：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html

2. **创建项目**
   - 打开微信开发者工具
   - 点击"+"创建新项目
   - 选择"小程序"
   - 填写项目名称和目录
   - AppID 使用测试号或自己的AppID
   - 选择"不使用云服务"

3. **导入代码**
   - 将下载的代码文件复制到项目目录
   - 确保目录结构与上述一致

4. **配置项目**
   - 在开发者工具中打开项目
   - 检查 `app.json` 配置是否正确
   - 确保 `pages` 路径正确

5. **运行项目**
   - 点击编译按钮
   - 在模拟器中查看效果
   - 调试工具可查看日志和错误

## 组件说明

### nav-bar 导航栏组件
```xml
<nav-bar title="页面标题" showBack="{{true}}" bind:back="goBack"></nav-bar>
```

### content-card 内容卡片组件
```xml
<content-card title="卡片标题" subtitle="副标题" iconName="🔔">
  <!-- 卡片内容 -->
</content-card>
```

### tab-bar TabBar导航组件
```xml
<tab-bar currentPath="/pages/current/current"></tab-bar>
```

## 注意事项

1. **TabBar图标**
   - 需要在 `images/tabbar/` 目录下放置图标文件
   - 图标尺寸：81px * 81px
   - 未选中：灰色 (#999999)
   - 选中：绿色 (#4CAF50)

2. **图片资源**
   - 当前使用 Emoji 作为占位
   - 可替换为实际设计图标

3. **API对接**
   - 当前使用 showToast 模拟交互
   - 需要对接后端 API 实现真实功能

4. **小程序配置**
   - 在 `app.json` 中配置 AppID
   - 配置服务器域名
   - 配置业务域名

## 常见问题

### Q: 项目无法运行？
A: 检查以下项：
1. 页面路径是否在 `app.json` 中注册
2. 组件是否在页面的 `json` 文件中引入
3. 文件路径是否正确（相对路径）

### Q: TabBar 不显示？
A: 检查以下项：
1. TabBar 配置中的页面路径是否正确
2. 页面是否已注册到 `app.json`
3. TabBar 图标文件是否存在

### Q: 样式不生效？
A: 检查以下项：
1. rpx 单位是否正确（750rpx = 屏幕宽度）
2. 样式是否在正确的文件中
3. 是否有样式冲突

## 后续开发建议

1. **完善功能**
   - 对接后端 API
   - 实现真实的数据交互
   - 完善表单验证

2. **优化体验**
   - 添加加载动画
   - 优化交互反馈
   - 添加错误提示

3. **代码规范**
   - 添加代码注释
   - 遵循命名规范
   - 提取公共方法

4. **测试上线**
   - 单元测试
   - 兼容性测试
   - 提交审核

## 技术支持
如有问题，请查看：
- 微信小程序官方文档：https://developers.weixin.qq.com/miniprogram/dev/framework/
- 项目 README.md：详细的项目说明和组件文档

## 版本信息
- 版本：1.0.0
- 更新日期：2024-01-28
