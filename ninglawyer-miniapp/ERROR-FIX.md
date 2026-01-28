# 🔧 错误修复与重新导入指南

## 已修复的问题

### ❌ 问题 1：组件引用错误
**错误信息**：
```
Couldn't found the '../../components/nav-bar/nav-bar.json' file relative to 'pages/guide/article/article'
```

**原因**：
- 仓库中包含旧版小程序目录（how-to-judge、manage-contract、prevent-risk 等）
- 这些旧版目录中可能存在对不存在组件的引用

**解决方案**：
✅ 已删除所有旧版小程序目录
✅ 只保留最新的 4 个小程序
✅ 所有组件引用已清理

### ❌ 问题 2：页面未注册
**错误信息**：
```
statistics 页面未在 app.json 中注册
```

**解决方案**：
✅ 已将 statistics 页面添加到 legal-instructor/app.json

## 🔄 重新导入小程序

### 步骤 1：清理本地旧代码

如果您之前已经下载了代码，请先删除：

**Windows 命令行**：
```cmd
cd C:\Users\Administrator
rd /s /q ninglawyer-miniapp
```

或者直接在文件资源管理器中删除 `ninglawyer-miniapp` 文件夹。

### 步骤 2：重新下载最新代码

```cmd
cd C:\Users\Administrator
git clone https://github.com/hegui2022/ninglawyer-miniapp.git
```

### 步骤 3：验证目录结构

下载完成后，检查目录结构是否正确：

```
ninglawyer-miniapp/
├── legal-instructor/      ← 法律教官主小程序
├── code-signing/         ← 码上签约小程序
├── lyue/                 ← 理约小程序
├── zenme-pan/            ← 怎么判小程序
└── README.md
```

**注意**：不应包含以下旧版目录（已删除）：
- ❌ how-to-judge
- ❌ manage-contract
- ❌ prevent-risk
- ❌ fangfengxian
- ❌ liyue
- ❌ mashangqianyue
- ❌ ning-lawyer
- ❌ zenmepan

## 📱 导入微信开发者工具

### 1. 导入法律教官

1. 打开微信开发者工具
2. 点击 **"+"** 号或 **"导入项目"**
3. 填写项目信息：
   ```
   项目目录：C:\Users\Administrator\ninglawyer-miniapp\legal-instructor
   AppID：填写你的 AppID（或选择"测试号"）
   项目名称：法律教官
   ```
4. 点击 **"导入"**

**检查点**：
- ✅ 编译成功，无错误
- ✅ 可以看到首页
- ✅ 页面导航正常

### 2. 导入码上签约

1. 在微信开发者工具中点击 **"+"** 号
2. 填写项目信息：
   ```
   项目目录：C:\Users\Administrator\ninglawyer-miniapp\code-signing
   AppID：同上
   项目名称：码上签约
   ```
3. 点击 **"导入"**

**检查点**：
- ✅ 编译成功，无错误
- ✅ 可以看到首页
- ✅ 底部导航栏显示

### 3. 导入理约

1. 在微信开发者工具中点击 **"+"** 号
2. 填写项目信息：
   ```
   项目目录：C:\Users\Administrator\ninglawyer-miniapp\lyue
   AppID：同上
   项目名称：理约
   ```
3. 点击 **"导入"**

**检查点**：
- ✅ 编译成功，无错误
- ✅ 可以看到首页

### 4. 导入怎么判

1. 在微信开发者工具中点击 **"+"** 号
2. 填写项目信息：
   ```
   项目目录：C:\Users\Administrator\ninglawyer-miniapp\zenme-pan
   AppID：同上
   项目名称：怎么判
   ```
3. 点击 **"导入"**

**检查点**：
- ✅ 编译成功，无错误
- ✅ 可以看到首页

## ⚠️ 如果仍然出现错误

### 错误 1：找不到页面

**错误信息**：
```
Page is not found
```

**解决方案**：
1. 检查 app.json 中的 pages 列表
2. 确保所有页面文件都存在
3. 清除编译缓存：在微信开发者工具中点击 **"清缓存"** → **"清除文件缓存"**

### 错误 2：图片加载失败

**错误信息**：
```
Image load fail
```

**原因**：当前使用网络图片占位符，需要网络连接。

**解决方案**：
1. 确保网络连接正常
2. 或替换为本地图片资源

### 错误 3：编译错误

**错误信息**：
```
Module is not defined
```

**解决方案**：
1. 检查 pages 目录下的文件是否完整
2. 确保 .js、.json、.wxml、.wxss 四个文件都存在
3. 清除缓存后重新编译

## 📊 当前小程序清单

✅ **已完成并修复**：
1. 法律教官（legal-instructor）
   - 首页、登录、咨询、律师家族
   - 消息通知、数据统计、个人中心

2. 码上签约（code-signing）
   - 首页、模板选择、合同起草
   - 合同预览、签署、列表、详情

3. 理约（lyue）
   - 首页、合同履约、履约提醒

4. 怎么判（zenme-pan）
   - 首页、违约判断、维权指导
   - 判例查询、案例详情

## 🎯 测试建议

### 基础测试
1. 分别导入 4 个小程序
2. 检查每个小程序是否能正常编译
3. 检查页面导航是否正常
4. 检查主要功能是否可用

### 完整流程测试
1. 在法律教官中进行咨询
2. 跳转到码上签约创建合同
3. 在理约中查看履约进度
4. 在怎么判中进行违约判断

## 📞 需要帮助？

如果仍然遇到问题，请：
1. 清除微信开发者工具缓存
2. 确保下载的是最新代码（最新提交：e6f560d）
3. 提供具体的错误信息

---

**修复日期**：2025-01-29
**修复内容**：删除旧版小程序、修复页面注册、清理组件引用
