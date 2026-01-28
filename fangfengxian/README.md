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
│   └── home-indicator/        # Home 指示条组件
│       ├── home-indicator.wxml
│       ├── home-indicator.wxss
│       ├── home-indicator.js
│       └── home-indicator.json
├── pages/                     # 页面目录
│   ├── login/                 # 登录页
│   └── guide/                 # 指引页（首页）
│       └── article/           # 文章详情页（子页面）
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
    "home-indicator": "../../components/home-indicator/home-indicator"
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
  <home-indicator></home-indicator>
</view>
```

## 下一步计划
- [ ] 添加更多公共组件（如底部导航、弹窗、加载提示等）
- [ ] 优化组件性能
- [ ] 添加组件单元测试
- [ ] 完善组件文档和示例
