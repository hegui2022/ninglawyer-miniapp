# 图标文件说明

由于项目使用图标文件，但实际PNG图片无法直接创建，
请按照以下步骤添加图标：

1. 准备以下图标文件（每个图标大小建议：81x81 px）：
   - home.png (首页图标)
   - home-active.png (首页选中图标)
   - consult.png (咨询图标)
   - consult-active.png (咨询选中图标)
   - contract.png (合同图标)
   - contract-active.png (合同选中图标)
   - history.png (记录图标)
   - history-active.png (记录选中图标)
   - profile.png (我的图标)
   - profile-active.png (我的选中图标)

2. 将图标文件放入 miniprogram/static/icons/ 目录

3. 图标风格建议：
   - 简洁扁平化设计
   - 使用蓝色主题 (#1890ff)
   - 白色背景或透明背景

4. 临时解决方案：
   如果暂时没有图标，可以使用在线图标生成工具：
   - https://iconfont.cn/
   - https://www.flaticon.com/
   - https://www.iconfinder.com/

或者使用以下占位符颜色：
- 编辑 app.json，将 iconPath 改为空字符串使用文字标签
- 或者使用 base64 编码的图标
