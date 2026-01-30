# 静态资源文件说明

本目录需要准备以下静态资源文件：

## 图标文件 (icons/)

### 功能图标
- `home.png` / `home-active.png` - 首页图标 (选中/未选中)
- `consult.png` / `consult-active.png` - 咨询图标
- `contract.png` / `contract-active.png` - 合同图标
- `history.png` / `history-active.png` - 历史记录图标
- `profile.png` / `profile-active.png` - 个人中心图标

### 法律领域图标
- `civil.png` - 民事
- `criminal.png` - 刑事
- `company.png` - 公司
- `labor.png` - 劳动
- `marriage.png` - 婚姻
- `ip.png` - 知识产权
- `other.png` - 其他

### 通用图标
- `search.png` - 搜索
- `send.png` - 发送
- `arrow-right.png` - 右箭头
- `camera.png` - 相机
- `edit.png` - 编辑
- `phone.png` - 电话
- `notification.png` - 通知
- `settings.png` - 设置
- `about.png` - 关于
- `feedback.png` - 反馈
- `upload.png` - 上传
- `file.png` - 文件
- `wechat.png` - 微信
- `empty.png` - 空状态
- `consult-empty.png` - 咨询空状态

## 图片文件

- `logo.png` - 应用Logo (建议 512x512)
- `default-avatar.png` - 默认头像 (建议 200x200)

## 图标尺寸建议

- TabBar 图标: 81x81 px
- 功能图标: 48x48 px
- 领域图标: 64x64 px
- Logo: 512x512 px
- 头像: 200x200 px

## 获取方式

1. 从设计稿导出
2. 使用 IconFont (https://www.iconfont.cn/)
3. 使用免费图标库:
   - IconPark (https://iconpark.oceanengine.com/)
   - Flaticon (https://www.flaticon.com/)

## 临时解决方案

在开发阶段，可以使用占位图服务：
- https://via.placeholder.com/
- https://placehold.co/

例如：
```
/home.png -> https://via.placeholder.com/81x81/1890ff/ffffff?text=首页
```

注意：正式上线前请替换为实际的设计图标。
