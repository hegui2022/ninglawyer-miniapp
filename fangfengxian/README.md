# 防风险小程序组件化开发文档

## 项目概述
防风险小程序采用组件化开发架构，通过封装公共组件提高代码复用性，降低维护成本。

## 目录结构
```
fangfengxian/
├── components/                 # 组件目录
│   ├── nav-bar/               # 导航栏组件
│   │   ├── nav-bar.wxml
│   │   ├── nav-bar.wxss
│   │   ├── nav-bar.js
│   │   └── nav-bar.json
│   ├── content-card/          # 内容卡片组件
│   │   ├── content-card.wxml
│   │   ├── content-card.wxss
│   │   ├── content-card.js
│   │   └── content-card.json
│   ├── comment-list/          # 留言列表组件
│   │   ├── comment-list.wxml
│   │   ├── comment-list.wxss
│   │   ├── comment-list.js
│   │   └── comment-list.json
│   ├── home-indicator/        # Home 指示条组件
│   │   ├── home-indicator.wxml
│   │   ├── home-indicator.wxss
│   │   ├── home-indicator.js
│   │   └── home-indicator.json
│   └── tab-bar/               # TabBar 导航组件
│       ├── tab-bar.wxml
│       ├── tab-bar.wxss
│       ├── tab-bar.js
│       └── tab-bar.json
├── pages/                     # 页面目录
│   ├── login/                 # 登录页
│   ├── guide/                 # 指引页
│   │   └── article/           # 文章详情页
│   ├── obligation/            # 义务页（TabBar）
│   ├── manage/                # 管理页（TabBar）
│   ├── discover/              # 发现页（TabBar）
│   ├── profile/               # 我的页（TabBar）
│   └── department/            # 部门页面
├── images/                    # 图片资源
│   └── tabbar/                # TabBar 图标
└── app.json                   # 应用配置
```

## 组件说明

### 1. nav-bar 导航栏组件
**功能**: 提供统一的顶部导航栏，支持返回按钮和自定义标题。

**属性**:
- `title` (String): 导航栏标题
- `showBack` (Boolean): 是否显示返回按钮，默认 false

**事件**:
- `back`: 返回按钮点击事件

**使用示例**:
```xml
<nav-bar title="指引" showBack="{{true}}" bind:back="goBack"></nav-bar>
```

### 2. content-card 内容卡片组件
**功能**: 提供统一的内容卡片样式，支持标题、副标题和图标。

**属性**:
- `title` (String, 可选): 卡片标题
- `subtitle` (String, 可选): 卡片副标题
- `iconName` (String, 可选): 图标名称

**插槽**:
- `default`: 卡片内容区域

**使用示例**:
```xml
<content-card title="网络安全等级保护义务" subtitle="网络安" iconName="✏️">
  <view>卡片内容</view>
</content-card>
```

### 3. comment-list 留言列表组件
**功能**: 显示精选留言列表，支持点击交互。

**属性**:
- `comments` (Array): 留言数据，格式为 `{ name, time, content }`
- `showButton` (Boolean): 是否显示操作按钮，默认 true
- `buttonText` (String): 按钮文本，默认 '更多'

**事件**:
- `comment`: 留言操作事件

**使用示例**:
```xml
<comment-list
  comments="{{comments}}"
  showButton="{{true}}"
  buttonText="留言"
  bind:comment="handleComment"
></comment-list>
```

### 4. home-indicator Home 指示条组件
**功能**: 底部 Home 指示条，符合 iOS 设计规范。

**使用示例**:
```xml
<home-indicator></home-indicator>
```

### 5. tab-bar TabBar 导航组件
**功能**: 底部 TabBar 导航，支持页面切换。

**属性**:
- `currentPath` (String): 当前页面路径

**使用示例**:
```xml
<tab-bar currentPath="/pages/manage/manage"></tab-bar>
```

## 页面说明

### 1. 登录页 (pages/login)
**功能**: 提供微信登录和手机号登录方式。

**主要功能**:
- 微信一键登录
- 手机号登录
- 登录状态管理

### 2. 指引页 (pages/guide)
**功能**: 展示法律指引内容列表，支持展开/收起交互。

**主要功能**:
- 内容列表展示
- 展开/收起内容卡片
- 分类标签筛选
- TabBar 导航

**组件使用**:
- nav-bar: 顶部导航
- content-card: 内容卡片
- home-indicator: 底部指示条

### 3. 文章详情页 (pages/guide/article)
**功能**: 展示文章详细内容，支持付费阅读和留言功能。

**主要功能**:
- 文章内容展示
- 付费阅读功能
- 留言功能
- 返回导航

**组件使用**:
- nav-bar: 顶部导航（带返回）
- content-card: 内容卡片
- comment-list: 留言列表
- home-indicator: 底部指示条

### 4. 管理页 (pages/manage)
**功能**: 企业管理首页，提供一键办公、部门入口、违规举报和审批功能。

**主要功能**:
- 一键办公：会议通知、出资协议、入股声明、上传文件（4个功能入口）
- 重点部门：人力资源部、销售部、财务部（3个部门卡片）
- 违规举报信：独立的举报功能入口
- 项目审批：事假申请、差旅费报销申请（2条审批记录）
- TabBar 导航

**页面特点**:
- 模块化垂直布局
- 浅灰色分割线和间距划分不同功能区块
- 色彩编码区分不同部门和审批类型（绿、红、蓝）

**组件使用**:
- nav-bar: 顶部导航
- tab-bar: 底部导航栏

### 5. 其他 TabBar 页面
- **义务页** (pages/obligation): 展示企业合规义务
- **发现页** (pages/discover): 发现和探索功能
- **我的页** (pages/profile): 个人中心和设置

### 6. 部门页面 (pages/department)
**功能**: 部门详情页面，支持员工招聘与入职流程管理。

**主要功能**:
- 工作阶段标签：招聘、入职、在职、离职（竖线分隔）
- 岗位列表：总监、会计、出纳等岗位头像（可横向滑动）
- 时间戳：标记消息发布时间
- 聊天消息区：审批结果卡片，带有红色"已批准"印章
- 底部聊天工具栏：语音/文字切换、输入框、功能面板
- 功能面板：搜索栏 + 6个快捷功能按钮

**页面特点**:
- 上下分区布局（头部标签、中部聊天、底部工具栏）
- 聊天气泡样式，带审批印章
- 底部工具栏支持语音/文字模式切换
- 点击加号按钮弹出功能面板（招聘计划、招聘公告等）

**组件使用**:
- nav-bar: 顶部导航（带返回）

## 组件化开发优势

### 1. 代码复用
公共组件可在多个页面中复用，减少重复代码编写。

### 2. 统一样式
通过组件统一 UI 风格，保证界面一致性。

### 3. 易于维护
修改组件即可更新所有使用该组件的页面，降低维护成本。

### 4. 模块化开发
组件独立开发、测试和调试，提高开发效率。

## 使用指南

### 创建新页面
1. 在 `pages/` 目录下创建页面文件夹
2. 创建页面文件: `wxml`, `wxss`, `js`, `json`
3. 在 `app.json` 中注册页面路径
4. 在页面的 `json` 文件中注册需要使用的组件

### 使用组件
在页面的 `json` 文件中引入组件:
```json
{
  "usingComponents": {
    "nav-bar": "../../components/nav-bar/nav-bar",
    "content-card": "../../components/content-card/content-card",
    "comment-list": "../../components/comment-list/comment-list",
    "home-indicator": "../../components/home-indicator/home-indicator",
    "tab-bar": "../../components/tab-bar/tab-bar"
  }
}
```

在页面的 `wxml` 文件中使用组件:
```xml
<view>
  <nav-bar title="页面标题" showBack="{{true}}" bind:back="goBack"></nav-bar>
  <content-card title="卡片标题">
    <!-- 内容 -->
  </content-card>
  <tab-bar currentPath="/pages/current/current"></tab-bar>
</view>
```

### TabBar 配置

在 `app.json` 中配置 TabBar:
```json
{
  "tabBar": {
    "color": "#999999",
    "selectedColor": "#4CAF50",
    "backgroundColor": "#FFFFFF",
    "borderStyle": "black",
    "list": [
      {
        "pagePath": "pages/obligation/obligation",
        "text": "义务",
        "iconPath": "images/tabbar/obligation.png",
        "selectedIconPath": "images/tabbar/obligation-active.png"
      },
      {
        "pagePath": "pages/manage/manage",
        "text": "管理",
        "iconPath": "images/tabbar/manage.png",
        "selectedIconPath": "images/tabbar/manage-active.png"
      },
      {
        "pagePath": "pages/discover/discover",
        "text": "发现",
        "iconPath": "images/tabbar/discover.png",
        "selectedIconPath": "images/tabbar/discover-active.png"
      },
      {
        "pagePath": "pages/profile/profile",
        "text": "我的",
        "iconPath": "images/tabbar/profile.png",
        "selectedIconPath": "images/tabbar/profile-active.png"
      }
    ]
  }
}
```

## 下一步计划
- [ ] 添加更多公共组件（如底部导航、弹窗、加载提示等）
- [ ] 优化组件性能
- [ ] 添加组件单元测试
- [ ] 完善组件文档和示例
