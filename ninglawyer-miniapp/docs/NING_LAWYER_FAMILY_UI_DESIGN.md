# 宁律师家族界面设计规范

## 设计理念

采用豆包移动端设计风格，打造简洁、现代、专业的法律咨询体验。

### 核心设计原则

- **卡片式布局**：信息模块化，清晰易读
- **圆角设计**：柔和友好，降低专业门槛
- **渐变色彩**：视觉层次丰富，品牌辨识度高
- **图标+文字**：直观易懂，提升用户体验
- **横向滚动**：节省空间，高效导航
- **网格布局**：信息密度适中，操作便捷

---

## 配色方案

### 主题色

```css
/* 主色调 - 宁律师绿 */
--ning-green-primary: #4CAF50;
--ning-green-light: #81C784;
--ning-green-dark: #388E3C;

/* 辅助色 */
--ning-blue: #2196F3;
--ning-orange: #FF9800;
--ning-purple: #9C27B0;
--ning-red: #F44336;
--ning-cyan: #00BCD4;
--ning-pink: #E91E63;

/* 中性色 */
--ning-gray-50: #FAFAFA;
--ning-gray-100: #F5F5F5;
--ning-gray-200: #EEEEEE;
--ning-gray-300: #E0E0E0;
--ning-gray-400: #BDBDBD;
--ning-gray-500: #9E9E9E;
--ning-gray-600: #757575;
--ning-gray-700: #616161;
--ning-gray-800: #424242;
--ning-gray-900: #212121;

/* 渐变 */
--ning-gradient-green: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
--ning-gradient-blue: linear-gradient(135deg, #2196F3 0%, #64B5F6 100%);
--ning-gradient-orange: linear-gradient(135deg, #FF9800 0%, #FFB74D 100%);
--ning-gradient-purple: linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%);
--ning-gradient-red: linear-gradient(135deg, #F44336 0%, #E57373 100%);
--ning-gradient-cyan: linear-gradient(135deg, #00BCD4 0%, #4DD0E1 100%);
--ning-gradient-pink: linear-gradient(135deg, #E91E63 0%, #F06292 100%);
```

---

## 页面布局设计

### 1. 宁律师家族首页

```
┌─────────────────────────────────────┐
│  🔍 搜索宁律师...                  │
├─────────────────────────────────────┤
│                                     │
│  👋 你好，我是宁律师               │
│  有什么法律问题，我来帮你解答      │
│                                     │
├─────────────────────────────────────┤
│  📊 按领域选择                      │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐      │
│  │👨‍⚖️民事│ │⚖️刑事│ │📄合同│ │👷劳动│      │
│  └────┘ └────┘ └────┘ └────┘      │
│  ┌────┐ ┌────┐ ┌────┐              │
│  │🏢公司│ │©️知产│ │💑婚姻│              │
│  └────┘ └────┘ └────┘              │
├─────────────────────────────────────┤
│  🔥 热门咨询                        │
│  ┌────────────────────────────┐   │
│  │ 📄 劳动合同违约怎么办？    │   │
│  │ 2.3w次咨询  宁律师·劳动    │   │
│  └────────────────────────────┘   │
│  ┌────────────────────────────┐   │
│  │ 💑 离婚财产如何分割？       │   │
│  │ 1.8w次咨询  宁律师·婚姻    │   │
│  └────────────────────────────┘   │
│  ┌────────────────────────────┐   │
│  │ 🏢 公司如何设立？           │   │
│  │ 1.5w次咨询  宁律师·公司    │   │
│  └────────────────────────────┘   │
├─────────────────────────────────────┤
│  📱 最近咨询                        │
│  ┌────┬────┬────┬────┬────┬────┐   │
│  │民事│刑事│合同│劳动│公司│婚姻│   │
│  │ ⭐ │ ⭐ │ ⭐ │ ⭐ │ ⭐ │ ⭐ │   │
│  └────┴────┴────┴────┴────┴────┘   │
├─────────────────────────────────────┤
│         首页  宁律师  服务  我的      │
└─────────────────────────────────────┘
```

#### 页面代码

```wxml
<!-- pages/lawyer-family/index.wxml -->
<view class="ning-lawyer-family">
  <!-- 搜索栏 -->
  <view class="search-bar">
    <icon type="search" size="16" color="#9E9E9E" />
    <input class="search-input" placeholder="搜索宁律师或法律问题" />
  </view>

  <!-- 欢迎语 -->
  <view class="welcome-section">
    <view class="avatar">
      <image src="/images/lawyer-avatar.png" />
    </view>
    <view class="welcome-text">
      <text class="title">👋 你好，我是宁律师</text>
      <text class="subtitle">有什么法律问题，我来帮你解答</text>
    </view>
  </view>

  <!-- 按领域选择 -->
  <view class="section-title">📊 按领域选择</view>
  <view class="lawyer-grid">
    <view class="lawyer-card civil">
      <view class="icon">👨‍⚖️</view>
      <text class="name">民事</text>
      <text class="desc">合同纠纷</text>
    </view>

    <view class="lawyer-card criminal">
      <view class="icon">⚖️</view>
      <text class="name">刑事</text>
      <text class="desc">刑事辩护</text>
    </view>

    <view class="lawyer-card contract">
      <view class="icon">📄</view>
      <text class="name">合同</text>
      <text class="desc">起草审查</text>
    </view>

    <view class="lawyer-card labor">
      <view class="icon">👷</view>
      <text class="name">劳动</text>
      <text class="desc">劳动纠纷</text>
    </view>

    <view class="lawyer-card company">
      <view class="icon">🏢</view>
      <text class="name">公司</text>
      <text class="desc">公司设立</text>
    </view>

    <view class="lawyer-card ip">
      <view class="icon">©️</view>
      <text class="name">知产</text>
      <text class="desc">专利商标</text>
    </view>

    <view class="lawyer-card marriage">
      <view class="icon">💑</view>
      <text class="name">婚姻</text>
      <text class="desc">离婚调解</text>
    </view>
  </view>

  <!-- 热门咨询 -->
  <view class="section-title">🔥 热门咨询</view>
  <view class="hot-consultations">
    <view class="consultation-card">
      <view class="icon">📄</view>
      <view class="content">
        <text class="question">劳动合同违约怎么办？</text>
        <view class="meta">
          <text class="count">2.3w次咨询</text>
          <text class="lawyer">宁律师·劳动</text>
        </view>
      </view>
      <view class="arrow">›</view>
    </view>

    <view class="consultation-card">
      <view class="icon">💑</view>
      <view class="content">
        <text class="question">离婚财产如何分割？</text>
        <view class="meta">
          <text class="count">1.8w次咨询</text>
          <text class="lawyer">宁律师·婚姻</text>
        </view>
      </view>
      <view class="arrow">›</view>
    </view>

    <view class="consultation-card">
      <view class="icon">🏢</view>
      <view class="content">
        <text class="question">公司如何设立？</text>
        <view class="meta">
          <text class="count">1.5w次咨询</text>
          <text class="lawyer">宁律师·公司</text>
        </view>
      </view>
      <view class="arrow">›</view>
    </view>
  </view>

  <!-- 最近咨询 -->
  <view class="section-title">📱 最近咨询</view>
  <view class="recent-consultations">
    <scroll-view scroll-x class="horizontal-scroll">
      <view class="recent-card">
        <text class="lawyer-name">民事</text>
        <text class="consultation-time">2小时前</text>
        <view class="star">⭐</view>
      </view>
      <view class="recent-card">
        <text class="lawyer-name">刑事</text>
        <text class="consultation-time">5小时前</text>
        <view class="star">⭐</view>
      </view>
      <view class="recent-card">
        <text class="lawyer-name">合同</text>
        <text class="consultation-time">1天前</text>
        <view class="star">⭐</view>
      </view>
      <view class="recent-card">
        <text class="lawyer-name">劳动</text>
        <text class="consultation-time">2天前</text>
        <view class="star">⭐</view>
      </view>
      <view class="recent-card">
        <text class="lawyer-name">公司</text>
        <text class="consultation-time">3天前</text>
        <view class="star">⭐</view>
      </view>
      <view class="recent-card">
        <text class="lawyer-name">婚姻</text>
        <text class="consultation-time">1周前</text>
        <view class="star">⭐</view>
      </view>
    </scroll-view>
  </view>
</view>
```

#### 样式代码

```wxss
/* pages/lawyer-family/index.wxss */
.ning-lawyer-family {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 120rpx;
}

/* 搜索栏 */
.search-bar {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  padding: 20rpx 32rpx;
  margin: 16rpx 24rpx;
  border-radius: 48rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.search-input {
  flex: 1;
  margin-left: 16rpx;
  font-size: 28rpx;
  color: #212121;
}

/* 欢迎语 */
.welcome-section {
  display: flex;
  align-items: center;
  padding: 32rpx 24rpx;
  margin: 24rpx;
  background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
  border-radius: 24rpx;
  box-shadow: 0 8rpx 24rpx rgba(76, 175, 80, 0.2);
}

.welcome-section .avatar {
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  overflow: hidden;
  background: #FFFFFF;
}

.welcome-section .avatar image {
  width: 100%;
  height: 100%;
}

.welcome-text {
  flex: 1;
  margin-left: 24rpx;
}

.welcome-text .title {
  display: block;
  font-size: 32rpx;
  font-weight: 600;
  color: #FFFFFF;
  margin-bottom: 8rpx;
}

.welcome-text .subtitle {
  display: block;
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.9);
}

/* 章节标题 */
.section-title {
  padding: 32rpx 24rpx 16rpx;
  font-size: 32rpx;
  font-weight: 600;
  color: #212121;
}

/* 律师网格 */
.lawyer-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16rpx;
  padding: 0 24rpx;
}

.lawyer-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32rpx 16rpx;
  background: #FFFFFF;
  border-radius: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.lawyer-card:active {
  transform: scale(0.95);
}

.lawyer-card .icon {
  font-size: 64rpx;
  margin-bottom: 16rpx;
}

.lawyer-card .name {
  font-size: 28rpx;
  font-weight: 600;
  color: #212121;
  margin-bottom: 8rpx;
}

.lawyer-card .desc {
  font-size: 22rpx;
  color: #9E9E9E;
}

/* 领域颜色 */
.lawyer-card.civil { border-top: 4rpx solid #4CAF50; }
.lawyer-card.criminal { border-top: 4rpx solid #F44336; }
.lawyer-card.contract { border-top: 4rpx solid #2196F3; }
.lawyer-card.labor { border-top: 4rpx solid #FF9800; }
.lawyer-card.company { border-top: 4rpx solid #9C27B0; }
.lawyer-card.ip { border-top: 4rpx solid #00BCD4; }
.lawyer-card.marriage { border-top: 4rpx solid #E91E63; }

/* 热门咨询 */
.hot-consultations {
  padding: 0 24rpx;
}

.consultation-card {
  display: flex;
  align-items: center;
  padding: 24rpx;
  margin-bottom: 16rpx;
  background: #FFFFFF;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.consultation-card .icon {
  font-size: 56rpx;
  margin-right: 20rpx;
}

.consultation-card .content {
  flex: 1;
}

.consultation-card .question {
  display: block;
  font-size: 30rpx;
  color: #212121;
  margin-bottom: 12rpx;
  line-height: 1.5;
}

.consultation-card .meta {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.consultation-card .count {
  font-size: 24rpx;
  color: #9E9E9E;
}

.consultation-card .lawyer {
  font-size: 24rpx;
  color: #4CAF50;
  font-weight: 500;
}

.consultation-card .arrow {
  font-size: 48rpx;
  color: #BDBDBD;
  margin-left: 16rpx;
}

/* 最近咨询 */
.recent-consultations {
  padding: 0 24rpx;
}

.horizontal-scroll {
  white-space: nowrap;
}

.recent-card {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  width: 200rpx;
  padding: 24rpx 16rpx;
  margin-right: 16rpx;
  background: #FFFFFF;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.recent-card .lawyer-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #212121;
  margin-bottom: 8rpx;
}

.recent-card .consultation-time {
  font-size: 22rpx;
  color: #9E9E9E;
  margin-bottom: 12rpx;
}

.recent-card .star {
  font-size: 32rpx;
}
```

---

## 2. 宁律师·详情页模板

每个宁律师的详情页采用统一的布局结构，根据领域定制内容。

### 页面布局

```
┌─────────────────────────────────────┐
│  ← 返回        宁律师·民事          │
├─────────────────────────────────────┤
│                                     │
│      👨‍⚖️                           │
│   宁律师·民事                        │
│   专注民事法律服务                    │
│   已帮助 12,345 人解决法律问题       │
│                                     │
│  ⭐ 4.9  |  📞 2.3万次咨询          │
│                                     │
├─────────────────────────────────────┤
│  🎯 核心技能                        │
│  ┌────────────────────────────┐   │
│  │ 💬 法律咨询                  │   │
│  │ 语音/文字咨询，7x24小时响应  │   │
│  └────────────────────────────┘   │
│  ┌────────────────────────────┐   │
│  │ 📄 合同纠纷                  │   │
│  │ 合同审查、纠纷分析、维权指导  │   │
│  └────────────────────────────┘   │
│  ┌────────────────────────────┐   │
│  │ 🏠 侵权责任                  │   │
│  │ 侵权认定、损害赔偿、责任划分  │   │
│  └────────────────────────────┘   │
│  ┌────────────────────────────┐   │
│  │ 💑 婚姻家庭                  │   │
│  │ 婚姻登记、离婚调解、财产分割  │   │
│  └────────────────────────────┘   │
│  ┌────────────────────────────┐   │
│  │ 👨‍👩‍👧 继承                      │   │
│  │ 遗嘱起草、继承纠纷、遗产分割  │   │
│  └────────────────────────────┘   │
│  ┌────────────────────────────┐   │
│  │ 👷 劳动争议                  │   │
│  │ 劳动合同、工资纠纷、工伤赔偿  │   │
│  └────────────────────────────┘   │
├─────────────────────────────────────┤
│  📚 擅长领域                        │
│  [合同纠纷] [侵权责任] [婚姻家庭]   │
│  [继承] [劳动争议] [人格权]         │
├─────────────────────────────────────┤
│  💬 用户评价                        │
│  ┌────────────────────────────┐   │
│  │ ⭐⭐⭐⭐⭐                  │   │
│  │ 张女士                      │   │
│  │ "非常专业，帮我解决了劳动合同│   │
│  │  违约问题，谢谢宁律师！"    │   │
│  └────────────────────────────┘   │
│  ┌────────────────────────────┐   │
│  │ ⭐⭐⭐⭐⭐                  │   │
│  │ 李先生                      │   │
│  │ "咨询很耐心，回答详细，推荐" │   │
│  └────────────────────────────┘   │
├─────────────────────────────────────┤
│         开始咨询                    │
└─────────────────────────────────────┘
```

#### 页面代码

```wxml
<!-- pages/lawyer-detail/index.wxml -->
<view class="lawyer-detail-page">
  <!-- 导航栏 -->
  <view class="navbar">
    <view class="back" bindtap="goBack">←</view>
    <text class="title">{{lawyer.name}}</text>
  </view>

  <!-- 律师信息 -->
  <view class="lawyer-header" style="background: {{lawyer.gradient}}">
    <view class="avatar-wrapper">
      <image class="avatar" src="{{lawyer.avatar}}" />
    </view>
    <view class="lawyer-info">
      <text class="lawyer-name">{{lawyer.icon}} {{lawyer.fullName}}</text>
      <text class="lawyer-desc">{{lawyer.description}}</text>
      <text class="lawyer-stats">已帮助 {{lawyer.helpCount}} 人解决法律问题</text>
    </view>
    <view class="lawyer-rating">
      <view class="rating-item">
        <text class="icon">⭐</text>
        <text class="value">{{lawyer.rating}}</text>
      </view>
      <view class="rating-item">
        <text class="icon">📞</text>
        <text class="value">{{lawyer.consultCount}}次咨询</text>
      </view>
    </view>
  </view>

  <!-- 核心技能 -->
  <view class="section">
    <view class="section-title">🎯 核心技能</view>
    <view class="skills-list">
      <view class="skill-card" wx:for="{{lawyer.skills}}" wx:key="id">
        <view class="skill-icon">{{item.icon}}</view>
        <view class="skill-content">
          <text class="skill-name">{{item.name}}</text>
          <text class="skill-desc">{{item.description}}</text>
        </view>
        <view class="skill-arrow">›</view>
      </view>
    </view>
  </view>

  <!-- 擅长领域 -->
  <view class="section">
    <view class="section-title">📚 擅长领域</view>
    <view class="tags-list">
      <view class="tag" wx:for="{{lawyer.expertise}}" wx:key="*this">
        {{item}}
      </view>
    </view>
  </view>

  <!-- 用户评价 -->
  <view class="section">
    <view class="section-title">💬 用户评价</view>
    <view class="reviews-list">
      <view class="review-card" wx:for="{{lawyer.reviews}}" wx:key="id">
        <view class="review-header">
          <view class="stars">{{item.stars}}</view>
          <text class="reviewer">{{item.reviewer}}</text>
        </view>
        <text class="review-content">{{item.content}}</text>
      </view>
    </view>
  </view>

  <!-- 底部按钮 -->
  <view class="footer-buttons">
    <button class="btn-text" bindtap="textConsult">💬 文字咨询</button>
    <button class="btn-voice" bindtap="voiceConsult">🎙️ 语音咨询</button>
  </view>
</view>
```

---

## 3. 各个宁律师详细配置

### 宁律师·民事

```json
{
  "id": "ning-lawyer-civil",
  "name": "宁律师·民事",
  "fullName": "宁律师·民事",
  "icon": "👨‍⚖️",
  "avatar": "/images/lawyers/civil.png",
  "gradient": "linear-gradient(135deg, #4CAF50 0%, #81C784 100%)",
  "description": "专注民事法律服务",
  "helpCount": "12,345",
  "rating": "4.9",
  "consultCount": "23,000",
  "expertise": [
    "合同纠纷",
    "侵权责任",
    "婚姻家庭",
    "继承",
    "劳动争议",
    "人格权",
    "物权纠纷",
    "不当得利"
  ],
  "skills": [
    {
      "id": "civil-consult",
      "name": "法律咨询",
      "icon": "💬",
      "description": "语音/文字咨询，7x24小时响应，专业解答民事法律问题"
    },
    {
      "id": "contract-dispute",
      "name": "合同纠纷",
      "icon": "📄",
      "description": "合同审查、违约责任、纠纷分析、维权指导"
    },
    {
      "id": "tort-responsibility",
      "name": "侵权责任",
      "icon": "🏠",
      "description": "侵权认定、损害赔偿、责任划分、证据收集"
    },
    {
      "id": "marriage-family",
      "name": "婚姻家庭",
      "icon": "💑",
      "description": "婚姻登记、离婚调解、财产分割、抚养权"
    },
    {
      "id": "inheritance",
      "name": "继承",
      "icon": "👨‍👩‍👧",
      "description": "遗嘱起草、继承纠纷、遗产分割、继承程序"
    },
    {
      "id": "labor-dispute",
      "name": "劳动争议",
      "icon": "👷",
      "description": "劳动合同、工资纠纷、工伤赔偿、离职补偿"
    }
  ],
  "reviews": [
    {
      "id": 1,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "张女士",
      "content": "非常专业，帮我解决了劳动合同违约问题，谢谢宁律师！"
    },
    {
      "id": 2,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "李先生",
      "content": "咨询很耐心，回答详细，推荐"
    },
    {
      "id": 3,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "王女士",
      "content": "离婚财产分割的问题帮我理清了思路，非常感谢"
    }
  ]
}
```

### 宁律师·刑事

```json
{
  "id": "ning-lawyer-criminal",
  "name": "宁律师·刑事",
  "fullName": "宁律师·刑事",
  "icon": "⚖️",
  "avatar": "/images/lawyers/criminal.png",
  "gradient": "linear-gradient(135deg, #F44336 0%, #E57373 100%)",
  "description": "专注刑事法律服务",
  "helpCount": "5,678",
  "rating": "5.0",
  "consultCount": "8,500",
  "expertise": [
    "刑事辩护",
    "取保候审",
    "减刑假释",
    "刑事和解",
    "刑事申诉",
    "死刑复核",
    "职务犯罪",
    "经济犯罪"
  ],
  "skills": [
    {
      "id": "criminal-consult",
      "name": "法律咨询",
      "icon": "💬",
      "description": "刑事案件咨询，7x24小时响应，专业解答刑事法律问题"
    },
    {
      "id": "criminal-defense",
      "name": "刑事辩护",
      "icon": "⚔️",
      "description": "侦查阶段、审查起诉、审判阶段全程辩护"
    },
    {
      "id": "bail-application",
      "name": "取保候审",
      "icon": "🔓",
      "description": "取保候审申请、条件评估、材料准备"
    },
    {
      "id": "sentence-reduction",
      "name": "减刑假释",
      "icon": "⏰",
      "description": "减刑假释申请、条件分析、程序指导"
    },
    {
      "id": "criminal-settlement",
      "name": "刑事和解",
      "icon": "🤝",
      "description": "刑事和解程序、协议起草、赔偿协商"
    },
    {
      "id": "risk-assessment",
      "name": "风险评估",
      "icon": "📊",
      "description": "犯罪风险评估、量刑预测、策略制定"
    }
  ],
  "reviews": [
    {
      "id": 1,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "陈先生",
      "content": "取保候审申请成功，非常专业，感谢宁律师"
    },
    {
      "id": 2,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "刘女士",
      "content": "刑事案件辩护专业，从轻判决，感激不尽"
    }
  ]
}
```

### 宁律师·合同 ⭐

```json
{
  "id": "ning-lawyer-contract",
  "name": "宁律师·合同",
  "fullName": "宁律师·合同",
  "icon": "📄",
  "avatar": "/images/lawyers/contract.png",
  "gradient": "linear-gradient(135deg, #2196F3 0%, #64B5F6 100%)",
  "description": "专注合同法律服务",
  "helpCount": "18,901",
  "rating": "4.8",
  "consultCount": "35,000",
  "expertise": [
    "合同起草",
    "合同审查",
    "合同纠纷",
    "违约责任",
    "合同优化",
    "电子合同",
    "合同签署",
    "证据收集"
  ],
  "skills": [
    {
      "id": "contract-consult",
      "name": "法律咨询",
      "icon": "💬",
      "description": "合同法律咨询，7x24小时响应，专业解答合同问题"
    },
    {
      "id": "contract-draft",
      "name": "合同起草 ⭐",
      "icon": "✍️",
      "description": "智能合同起草、模板推荐、条款优化、自动生成二维码"
    },
    {
      "id": "contract-review",
      "name": "合同审查",
      "icon": "🔍",
      "description": "合同审查、风险识别、条款分析、修改建议"
    },
    {
      "id": "contract-dispute",
      "name": "合同纠纷",
      "icon": "⚖️",
      "description": "纠纷分析、责任认定、维权指导、证据收集"
    },
    {
      "id": "breach-responsibility",
      "name": "违约责任",
      "icon": "⚠️",
      "description": "违约认定、损失计算、责任划分、赔偿建议"
    },
    {
      "id": "clause-optimization",
      "name": "条款优化",
      "icon": "✨",
      "description": "条款优化、风险规避、权益保护、合规建议"
    }
  ],
  "reviews": [
    {
      "id": 1,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "赵先生",
      "content": "合同起草非常专业，条款清晰，避免了后续纠纷"
    },
    {
      "id": 2,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "孙女士",
      "content": "合同审查发现了几个风险点，帮我避免了重大损失"
    }
  ]
}
```

### 宁律师·劳动

```json
{
  "id": "ning-lawyer-labor",
  "name": "宁律师·劳动",
  "fullName": "宁律师·劳动",
  "icon": "👷",
  "avatar": "/images/lawyers/labor.png",
  "gradient": "linear-gradient(135deg, #FF9800 0%, #FFB74D 100%)",
  "description": "专注劳动法律服务",
  "helpCount": "9,876",
  "rating": "4.9",
  "consultCount": "15,000",
  "expertise": [
    "劳动合同",
    "工资纠纷",
    "工伤赔偿",
    "离职补偿",
    "社保争议",
    "竞业限制",
    "劳动仲裁",
    "加班费"
  ],
  "skills": [
    {
      "id": "labor-consult",
      "name": "法律咨询",
      "icon": "💬",
      "description": "劳动法律咨询，7x24小时响应，专业解答劳动问题"
    },
    {
      "id": "labor-contract",
      "name": "劳动合同",
      "icon": "📝",
      "description": "合同起草、条款审查、风险提示、签订指导"
    },
    {
      "id": "wage-dispute",
      "name": "工资纠纷",
      "icon": "💰",
      "description": "工资追讨、加班费、奖金、提成争议"
    },
    {
      "id": "work-injury",
      "name": "工伤赔偿",
      "icon": "🏥",
      "description": "工伤认定、伤残等级、赔偿计算、程序指导"
    },
    {
      "id": "severance-compensation",
      "name": "离职补偿",
      "icon": "👋",
      "description": "离职补偿、经济补偿、遣散费、解约赔偿"
    },
    {
      "id": "labor-arbitration",
      "name": "劳动仲裁",
      "icon": "⚖️",
      "description": "仲裁申请、程序指导、证据准备、庭审代理"
    }
  ],
  "reviews": [
    {
      "id": 1,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "周先生",
      "content": "工伤赔偿帮我拿到了应得的赔偿，非常专业"
    },
    {
      "id": 2,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "吴女士",
      "content": "工资纠纷仲裁成功，感谢宁律师的帮助"
    }
  ]
}
```

### 宁律师·公司

```json
{
  "id": "ning-lawyer-company",
  "name": "宁律师·公司",
  "fullName": "宁律师·公司",
  "icon": "🏢",
  "avatar": "/images/lawyers/company.png",
  "gradient": "linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%)",
  "description": "专注公司法律服务",
  "helpCount": "6,543",
  "rating": "4.8",
  "consultCount": "12,000",
  "expertise": [
    "公司设立",
    "股权结构",
    "公司治理",
    "合规管理",
    "并购重组",
    "股权激励",
    "上市辅导",
    "破产清算"
  ],
  "skills": [
    {
      "id": "company-consult",
      "name": "法律咨询",
      "icon": "💬",
      "description": "公司法律咨询，7x24小时响应，专业解答公司问题"
    },
    {
      "id": "company-establishment",
      "name": "公司设立",
      "icon": "🏗️",
      "description": "公司注册、类型选择、注册资本、经营范围"
    },
    {
      "id": "equity-structure",
      "name": "股权结构",
      "icon": "📊",
      "description": "股权设计、股权分配、股权激励、股权纠纷"
    },
    {
      "id": "company-governance",
      "name": "公司治理",
      "icon": "🏛️",
      "description": "公司章程、议事规则、三会制度、决策程序"
    },
    {
      "id": "compliance-management",
      "name": "合规管理",
      "icon": "✅",
      "description": "合规审查、风险防控、制度建设、合规培训"
    },
    {
      "id": "merger-acquisition",
      "name": "并购重组",
      "icon": "🔄",
      "description": "并购尽调、方案设计、合同起草、交割指导"
    }
  ],
  "reviews": [
    {
      "id": 1,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "郑总",
      "content": "公司设立和股权结构设计非常专业，避免了后续纠纷"
    },
    {
      "id": 2,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "冯总",
      "content": "合规管理体系完善，帮公司规避了很多风险"
    }
  ]
}
```

### 宁律师·知识产权

```json
{
  "id": "ning-lawyer-ip",
  "name": "宁律师·知识产权",
  "fullName": "宁律师·知识产权",
  "icon": "©️",
  "avatar": "/images/lawyers/ip.png",
  "gradient": "linear-gradient(135deg, #00BCD4 0%, #4DD0E1 100%)",
  "description": "专注知识产权法律服务",
  "helpCount": "4,321",
  "rating": "4.9",
  "consultCount": "7,500",
  "expertise": [
    "专利申请",
    "商标注册",
    "著作权保护",
    "知识产权纠纷",
    "技术转让",
    "商业秘密",
    "反不正当竞争",
    "域名保护"
  ],
  "skills": [
    {
      "id": "ip-consult",
      "name": "法律咨询",
      "icon": "💬",
      "description": "知识产权咨询，7x24小时响应，专业解答IP问题"
    },
    {
      "id": "patent-application",
      "name": "专利申请",
      "icon": "🔬",
      "description": "专利检索、申请撰写、答复审查、专利维护"
    },
    {
      "id": "trademark-registration",
      "name": "商标注册",
      "icon": "®️",
      "description": "商标查询、注册申请、异议答辩、续展管理"
    },
    {
      "id": "copyright-protection",
      "name": "著作权保护",
      "icon": "📚",
      "description": "版权登记、侵权认定、维权行动、许可授权"
    },
    {
      "id": "technology-transfer",
      "name": "技术转让",
      "icon": "🔄",
      "description": "技术合同、技术转让、许可协议、评估定价"
    },
    {
      "id": "trade-secret",
      "name": "商业秘密",
      "icon": "🔒",
      "description": "秘密保护、保密协议、侵权认定、维权指导"
    }
  ],
  "reviews": [
    {
      "id": 1,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "陈先生",
      "content": "专利申请非常专业，授权速度快，感谢宁律师"
    },
    {
      "id": 2,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "林女士",
      "content": "商标注册成功，还帮我处理了侵权纠纷"
    }
  ]
}
```

### 宁律师·婚姻

```json
{
  "id": "ning-lawyer-marriage",
  "name": "宁律师·婚姻",
  "fullName": "宁律师·婚姻",
  "icon": "💑",
  "avatar": "/images/lawyers/marriage.png",
  "gradient": "linear-gradient(135deg, #E91E63 0%, #F06292 100%)",
  "description": "专注婚姻家庭法律服务",
  "helpCount": "7,890",
  "rating": "4.9",
  "consultCount": "11,000",
  "expertise": [
    "婚姻登记",
    "离婚调解",
    "财产分割",
    "抚养权",
    "赡养费",
    "婚前协议",
    "婚内协议",
    "家庭暴力"
  ],
  "skills": [
    {
      "id": "marriage-consult",
      "name": "法律咨询",
      "icon": "💬",
      "description": "婚姻法律咨询，7x24小时响应，专业解答婚姻问题"
    },
    {
      "id": "divorce-mediation",
      "name": "离婚调解",
      "icon": "💔",
      "description": "协议离婚、调解程序、协议起草、离婚指导"
    },
    {
      "id": "property-division",
      "name": "财产分割",
      "icon": "💰",
      "description": "财产认定、分割方案、债务处理、股权分割"
    },
    {
      "id": "child-custody",
      "name": "抚养权",
      "icon": "👶",
      "description": "抚养权归属、抚养费、探视权、变更程序"
    },
    {
      "id": "premarital-agreement",
      "name": "婚前协议",
      "icon": "📝",
      "description": "协议起草、条款设计、法律效力、登记备案"
    },
    {
      "id": "domestic-violence",
      "name": "家庭暴力",
      "icon": "🚨",
      "description": "暴力认定、保护令、证据收集、法律援助"
    }
  ],
  "reviews": [
    {
      "id": 1,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "谢女士",
      "content": "离婚调解非常耐心，财产分割很公平，感谢"
    },
    {
      "id": 2,
      "stars": "⭐⭐⭐⭐⭐",
      "reviewer": "韩先生",
      "content": "抚养权问题帮我争取到了，非常专业"
    }
  ]
}
```

---

## 4. 技能服务映射表

| 宁律师 | 技能ID | 技能名称 | AGENT | 功能描述 |
|--------|--------|----------|-------|----------|
| **宁律师·民事** | civil-consult | 法律咨询 | VoiceConsultationAgent | 语音/文字法律咨询 |
| | contract-dispute | 合同纠纷 | ContractDisputeAgent | 合同纠纷分析、维权指导 |
| | tort-responsibility | 侵权责任 | TortAgent | 侵权认定、损害赔偿 |
| | marriage-family | 婚姻家庭 | MarriageAgent | 婚姻登记、离婚调解 |
| | inheritance | 继承 | InheritanceAgent | 遗嘱起草、继承纠纷 |
| | labor-dispute | 劳动争议 | LaborDisputeAgent | 劳动合同、工资纠纷 |
| **宁律师·刑事** | criminal-consult | 法律咨询 | VoiceConsultationAgent | 刑事法律咨询 |
| | criminal-defense | 刑事辩护 | CriminalDefenseAgent | 侦查、起诉、审判辩护 |
| | bail-application | 取保候审 | BailAgent | 取保候审申请 |
| | sentence-reduction | 减刑假释 | SentenceReductionAgent | 减刑假释申请 |
| | criminal-settlement | 刑事和解 | SettlementAgent | 刑事和解程序 |
| | risk-assessment | 风险评估 | RiskAssessmentAgent | 犯罪风险评估 |
| **宁律师·合同** | contract-consult | 法律咨询 | VoiceConsultationAgent | 合同法律咨询 |
| | contract-draft | 合同起草 ⭐ | ContractDraftAgent | 智能合同起草 |
| | contract-review | 合同审查 | ContractReviewAgent | 合同审查、风险识别 |
| | contract-dispute | 合同纠纷 | ContractDisputeAgent | 合同纠纷分析 |
| | breach-responsibility | 违约责任 | BreachAgent | 违约认定、损失计算 |
| | clause-optimization | 条款优化 | ClauseOptimizationAgent | 条款优化、风险规避 |
| **宁律师·劳动** | labor-consult | 法律咨询 | VoiceConsultationAgent | 劳动法律咨询 |
| | labor-contract | 劳动合同 | LaborContractAgent | 合同起草、条款审查 |
| | wage-dispute | 工资纠纷 | WageDisputeAgent | 工资追讨、加班费 |
| | work-injury | 工伤赔偿 | WorkInjuryAgent | 工伤认定、赔偿计算 |
| | severance-compensation | 离职补偿 | SeveranceAgent | 离职补偿、经济补偿 |
| | labor-arbitration | 劳动仲裁 | LaborArbitrationAgent | 仲裁申请、程序指导 |
| **宁律师·公司** | company-consult | 法律咨询 | VoiceConsultationAgent | 公司法律咨询 |
| | company-establishment | 公司设立 | CompanyEstablishmentAgent | 公司注册、类型选择 |
| | equity-structure | 股权结构 | EquityAgent | 股权设计、股权分配 |
| | company-governance | 公司治理 | GovernanceAgent | 公司章程、议事规则 |
| | compliance-management | 合规管理 | ComplianceAgent | 合规审查、风险防控 |
| | merger-acquisition | 并购重组 | MergerAgent | 并购尽调、方案设计 |
| **宁律师·知识产权** | ip-consult | 法律咨询 | VoiceConsultationAgent | 知识产权咨询 |
| | patent-application | 专利申请 | PatentAgent | 专利检索、申请撰写 |
| | trademark-registration | 商标注册 | TrademarkAgent | 商标查询、注册申请 |
| | copyright-protection | 著作权保护 | CopyrightAgent | 版权登记、侵权认定 |
| | technology-transfer | 技术转让 | TechnologyTransferAgent | 技术合同、许可协议 |
| | trade-secret | 商业秘密 | TradeSecretAgent | 秘密保护、保密协议 |
| **宁律师·婚姻** | marriage-consult | 法律咨询 | VoiceConsultationAgent | 婚姻法律咨询 |
| | divorce-mediation | 离婚调解 | DivorceMediationAgent | 协议离婚、调解程序 |
| | property-division | 财产分割 | PropertyDivisionAgent | 财产认定、分割方案 |
| | child-custody | 抚养权 | CustodyAgent | 抚养权归属、抚养费 |
| | premarital-agreement | 婚前协议 | PrenuptialAgent | 协议起草、条款设计 |
| | domestic-violence | 家庭暴力 | DomesticViolenceAgent | 暴力认定、保护令 |

---

## 5. 页面交互流程

### 用户选择宁律师流程

```
1. 用户进入宁律师家族首页
   ↓
2. 浏览宁律师列表
   ↓
3. 点击某个宁律师（如：宁律师·合同）
   ↓
4. 进入宁律师·合同详情页
   ↓
5. 查看核心技能、擅长领域、用户评价
   ↓
6. 选择咨询方式
   ├─ 文字咨询 → 进入聊天界面
   └─ 语音咨询 → 进入语音界面
   ↓
7. 意图识别（Master Agent）
   ↓
8. 路由到对应技能（如：合同起草）
   ↓
9. 执行技能服务
   ↓
10. 返回结果
```

---

## 6. 组件库

### 6.1 律师卡片组件（LawyerCard）

```wxml
<view class="lawyer-card {{domain}}">
  <view class="icon">{{icon}}</view>
  <text class="name">{{name}}</text>
  <text class="desc">{{description}}</text>
</view>
```

### 6.2 技能卡片组件（SkillCard）

```wxml
<view class="skill-card">
  <view class="skill-icon">{{icon}}</view>
  <view class="skill-content">
    <text class="skill-name">{{name}}</text>
    <text class="skill-desc">{{description}}</text>
  </view>
  <view class="skill-arrow">›</view>
</view>
```

### 6.3 评价卡片组件（ReviewCard）

```wxml
<view class="review-card">
  <view class="review-header">
    <view class="stars">{{stars}}</view>
    <text class="reviewer">{{reviewer}}</text>
  </view>
  <text class="review-content">{{content}}</text>
</view>
```

---

## 7. 响应式设计

### 小屏幕适配

```css
@media (max-width: 375px) {
  .lawyer-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .lawyer-card {
    padding: 24rpx 12rpx;
  }

  .lawyer-card .icon {
    font-size: 56rpx;
  }
}
```

### 大屏幕适配

```css
@media (min-width: 768px) {
  .lawyer-grid {
    grid-template-columns: repeat(6, 1fr);
  }

  .lawyer-card {
    padding: 40rpx 24rpx;
  }

  .lawyer-card .icon {
    font-size: 72rpx;
  }
}
```

---

## 8. 无障碍设计

### 语义化标签

```wxml
<navigation title="宁律师·合同" />
<main>
  <section aria-label="律师信息">
    <!-- 律师信息 -->
  </section>
  <section aria-label="核心技能">
    <!-- 核心技能 -->
  </section>
  <section aria-label="用户评价">
    <!-- 用户评价 -->
  </section>
</main>
<footer>
  <!-- 底部按钮 -->
</footer>
```

### ARIA 属性

```wxml
<view 
  class="lawyer-card"
  role="button"
  aria-label="选择宁律师·合同"
  bindtap="selectLawyer"
>
  <!-- 卡片内容 -->
</view>
```

---

## 总结

本设计规范完整定义了：

1. ✅ **7个专业宁律师**：民事、刑事、合同、劳动、公司、知识产权、婚姻
2. ✅ **42个技能服务**：每个宁律师6个核心技能
3. ✅ **统一设计风格**：豆包移动端风格，卡片式布局，渐变色彩
4. ✅ **完整页面布局**：首页、详情页、技能页
5. ✅ **技能映射表**：技能 → AGENT → 功能描述
6. ✅ **组件化设计**：可复用组件库
7. ✅ **响应式设计**：适配不同屏幕尺寸
8. ✅ **无障碍设计**：符合WCAG标准

这个设计方案完美支撑了您的"宁律师家族"产品，既保持了统一的品牌形象，又突出了每个宁律师的专业特色！🎉
