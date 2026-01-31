# 数据存储现状分析

## 当前数据存储架构

### 1. 数据库层
- **开发环境**: SQLite (`ninglawyer.db`)
- **生产环境**: PostgreSQL
- **连接池**: pool_size=20, max_overflow=40
- **已配置索引**: 41个索引

### 2. 数据模型定义
| 表名 | 说明 | 主要字段 |
|------|------|---------|
| users | 用户表 | openid, unionid, phone, subscription_type, usage_stats |
| sessions | 会话表 | user_id, skill_type, title, is_active |
| messages | 消息表 | session_id, role, content |
| consultation_records | 咨询记录表 | user_id, session_id, domain, question, analysis |
| contract_records | 合同记录表 | user_id, session_id, contract_type, contract_content |
| desensitize_records | 脱敏记录表 | user_id, session_id, original_text, desensitized_text |
| file_records | 文件记录表 | user_id, filename, file_path, file_type |
| user_profiles | 用户档案表 | user_id, real_name, id_card, address |
| statistics | 统计表 | date, metric_type, metric_value |
| system_configs | 系统配置表 | key, value, description |
| skill_permissions | 技能权限表 | - |

### 3. 缓存层
- **缓存服务**: Redis
- **缓存管理器**: CacheManager（已实现但未充分使用）
- **缓存策略**:
  - 对话缓存：24小时
  - 用户类型缓存：1小时

### 4. 数据访问层
- **数据库连接**: database.py（已实现）
- **会话管理**: get_db(), get_db_context()
- **缺失**: 统一Repository层

## 当前存在的问题

### 1. 数据持久化问题
❌ **会话和对话数据没有持久化**
- 当前对话可能只保存在内存中
- 服务重启后对话历史丢失
- 无法查询历史对话

❌ **用户类型和场景判断没有持久化**
- 每次请求都需要重新判断
- 没有历史记录跟踪
- 无法进行用户画像分析

### 2. 缓存使用问题
❌ **缓存使用不充分**
- CacheManager已实现但没有在代码中使用
- 数据库查询没有缓存
- 重复查询导致性能问题

❌ **缓存策略不统一**
- 缺乏统一的缓存键命名规范
- 缓存过期时间不一致
- 没有缓存失效策略

### 3. 数据一致性问题
❌ **缓存和数据库不一致**
- 缓存更新后数据库可能未更新
- 没有事务保障
- 没有缓存失效机制

❌ **并发访问问题**
- 缺少并发控制
- 可能出现数据竞争
- 没有乐观锁/悲观锁机制

### 4. 数据访问问题
❌ **缺少统一Repository层**
- 数据访问分散在各个模块
- 没有统一的数据访问接口
- 代码重复，难以维护

❌ **缺少数据验证和转换**
- 数据验证不完善
- 没有统一的DTO/VO转换
- 缺少数据脱敏

### 5. 数据备份和迁移问题
❌ **缺少数据备份策略**
- 没有定期备份
- 没有备份验证
- 没有快速恢复机制

❌ **缺少数据迁移方案**
- 数据模型变更后迁移困难
- 没有版本管理
- 缺少数据迁移工具

## 改进方案

### 1. 实现统一Repository层
- 创建统一的Repository接口
- 实现各个表的Repository
- 统一数据访问方式
- 添加数据验证和转换

### 2. 实现统一缓存策略
- 统一缓存键命名规范
- 定义缓存过期时间策略
- 实现缓存失效机制
- 实现缓存预热

### 3. 实现数据一致性保障
- 实现写穿透策略
- 实现异步更新
- 实现最终一致性
- 添加事务管理

### 4. 实现数据持久化
- 持久化会话和对话数据
- 持久化用户类型和场景判断
- 实现历史查询功能
- 实现数据导出功能

### 5. 实现数据备份和迁移
- 实现定期备份
- 实现备份验证
- 实现快速恢复
- 实现数据迁移工具

## 优先级

| 优先级 | 任务 | 原因 |
|--------|------|------|
| P0 | 实现统一Repository层 | 解决数据访问分散问题 |
| P0 | 实现会话和对话数据持久化 | 解决数据丢失问题 |
| P1 | 实现统一缓存策略 | 提升性能 |
| P1 | 实现数据一致性保障 | 保证数据正确性 |
| P2 | 实现数据备份和迁移 | 提升可靠性 |
