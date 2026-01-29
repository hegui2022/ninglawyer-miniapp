# 导航栏组件

## 使用说明

### 在页面中引入组件

在页面的 JSON 文件中引入：

```json
{
  "usingComponents": {
    "nav-bar": "../../components/nav-bar/nav-bar"
  }
}
```

### 在页面中使用

```html
<nav-bar
  title="页面标题"
  background="#07C160"
  textColor="#ffffff"
  showBack="{{true}}"
  showHome="{{false}}"
  fixed="{{true}}">
</nav-bar>
```

## 属性说明

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| title | String | '' | 导航栏标题 |
| background | String | '#07C160' | 背景颜色 |
| textColor | String | '#ffffff' | 文字颜色 |
| showBack | Boolean | true | 是否显示返回按钮 |
| showHome | Boolean | false | 是否显示首页按钮 |
| fixed | Boolean | true | 是否固定在顶部 |

## 注意事项

1. 组件会自动适配不同设备的状态栏高度
2. 返回按钮会根据页面栈自动判断行为（返回上一页或返回首页）
3. 组件支持自定义背景颜色和文字颜色

## 图标说明

组件使用 Unicode 图标，无需额外图片资源：
- 返回图标：‹
- 首页图标：⌂
