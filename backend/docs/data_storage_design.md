# 数据统一存储方案设计

## 1. 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                     应用层 (App Layer)                    │
│  - 主脑 (Master Brain)                                    │
│  - 技能模块 (Skills)                                      │
│  - 路由层 (Routes)                                        │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Repository层 (Repository Layer)             │
│  - UserRepository                                         │
│  - SessionRepository                                      │
│  - MessageRepository                                      │
│  - ConsultationRecordRepository                          │
│  - ContractRecordRepository                              │
│  - ...                                                    │
└──────┬────────────────────────────┬──────────────────────┘
       │                            │
┌──────▼────────────┐    ┌─────────▼─────────┐
│   缓存层 (Cache)  │    │   数据库层 (DB)   │
│  - Redis          │    │  - PostgreSQL    │
│  - CacheManager   │    │  - SQLAlchemy    │
└───────────────────┘    └───────────────────┘
```

## 2. Repository层设计

### 2.1 基础Repository接口

```python
class BaseRepository(Generic[T]):
    """
    基础Repository接口
    
    提供通用的CRUD操作
    """
    
    def __init__(self, model: Type[T], cache_manager: CacheManager = None):
        self.model = model
        self.cache_manager = cache_manager
    
    # CRUD操作
    def create(self, **kwargs) -> T
    def get_by_id(self, id: int) -> Optional[T]
    def get_by(self, **kwargs) -> Optional[T]
    def get_all(self, **kwargs) -> List[T]
    def update(self, id: int, **kwargs) -> Optional[T]
    def delete(self, id: int) -> bool
    def count(self, **kwargs) -> int
```

### 2.2 缓存策略

#### 缓存键命名规范
```
格式: {prefix}:{resource}:{identifier}

示例:
- user:1 (用户ID为1的用户信息)
- user:openid:oXXX (openid为oXXX的用户信息)
- session:1 (会话ID为1的会话信息)
- session:user:1:active (用户1的活跃会话列表)
- message:session:1 (会话1的消息列表)
- user_type:1 (用户1的用户类型)
- scenario:session:1 (会话1的场景类型)
```

#### 缓存过期时间策略
| 资源类型 | 缓存时间 | 说明 |
|---------|---------|------|
| 用户信息 | 1小时 | 用户基本信息变更频率低 |
| 用户类型 | 1小时 | 用户类型变更频率低 |
| 会话信息 | 1小时 | 会话信息变更频率中等 |
| 消息列表 | 10分钟 | 消息列表变更频率高 |
| 场景类型 | 1小时 | 场景类型变更频率低 |
| 系统配置 | 1小时 | 系统配置变更频率低 |

#### 缓存更新策略
- **写穿透**: 先更新数据库，再更新缓存
- **Cache-Aside**: 读时先查缓存，缓存没有则查数据库并写入缓存
- **失效策略**: 数据更新时主动失效相关缓存

## 3. 数据一致性保障

### 3.1 事务管理
```python
class TransactionManager:
    """事务管理器"""
    
    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
        with get_db_context() as db:
            try:
                yield db
                db.commit()
            except Exception as e:
                db.rollback()
                raise
```

### 3.2 写穿透策略
```python
def create_user(self, **kwargs):
    """创建用户（写穿透）"""
    with transaction():
        # 1. 写入数据库
        user = self.model(**kwargs)
        db.add(user)
        db.commit()
        
        # 2. 更新缓存
        cache_key = f"user:{user.id}"
        self.cache_manager.set(cache_key, user.to_dict(), ttl=3600)
        
        return user
```

### 3.3 缓存失效策略
```python
def update_user(self, id: int, **kwargs):
    """更新用户（缓存失效）"""
    with transaction():
        # 1. 更新数据库
        user = db.query(self.model).filter_by(id=id).first()
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.commit()
        
        # 2. 失效缓存
        cache_keys = [
            f"user:{id}",
            f"user:openid:{user.openid}",
            f"user:phone:{user.phone}"
        ]
        for cache_key in cache_keys:
            self.cache_manager.delete(cache_key)
        
        return user
```

## 4. 数据持久化方案

### 4.1 会话和对话数据持久化

#### 会话管理
```python
class SessionRepository(BaseRepository[Session]):
    """会话Repository"""
    
    def create_session(self, user_id: int, skill_type: str, **kwargs) -> Session:
        """创建会话"""
        return self.create(
            user_id=user_id,
            skill_type=skill_type,
            title=f"{skill_type}会话",
            **kwargs
        )
    
    def get_active_session(self, user_id: int, skill_type: str) -> Optional[Session]:
        """获取用户活跃会话"""
        cache_key = f"session:user:{user_id}:{skill_type}:active"
        
        # 先查缓存
        session = self.cache_manager.get(cache_key)
        if session:
            return session
        
        # 查数据库
        session = self.get_by(
            user_id=user_id,
            skill_type=skill_type,
            is_active=True
        )
        
        # 写入缓存
        if session:
            self.cache_manager.set(cache_key, session.to_dict(), ttl=3600)
        
        return session
```

#### 消息管理
```python
class MessageRepository(BaseRepository[Message]):
    """消息Repository"""
    
    def create_message(self, session_id: int, role: str, content: str) -> Message:
        """创建消息"""
        message = self.create(
            session_id=session_id,
            role=role,
            content=content
        )
        
        # 失效会话消息列表缓存
        cache_key = f"message:session:{session_id}"
        self.cache_manager.delete(cache_key)
        
        return message
    
    def get_session_messages(self, session_id: int, limit: int = 50) -> List[Message]:
        """获取会话消息列表"""
        cache_key = f"message:session:{session_id}"
        
        # 先查缓存
        messages = self.cache_manager.get(cache_key)
        if messages:
            return messages[-limit:]
        
        # 查数据库
        messages = self.get_all(
            session_id=session_id,
            order_by=Message.created_at
        )
        
        # 写入缓存（只缓存最近50条）
        cached_messages = messages[-50:]
        self.cache_manager.set(cache_key, [m.to_dict() for m in cached_messages], ttl=600)
        
        return cached_messages
```

### 4.2 用户类型和场景判断持久化

#### 用户类型缓存
```python
class UserRepository(BaseRepository[User]):
    """用户Repository"""
    
    def get_user_type(self, user_id: int) -> str:
        """获取用户类型（带缓存）"""
        cache_key = f"user_type:{user_id}"
        
        # 先查缓存
        user_type = self.cache_manager.get(cache_key)
        if user_type:
            return user_type
        
        # 查数据库
        user = self.get_by_id(user_id)
        if user:
            user_type = user.subscription_type
            # 写入缓存
            self.cache_manager.set(cache_key, user_type, ttl=3600)
            return user_type
        
        # 默认类型
        return "basic"
```

#### 场景类型缓存
```python
class SessionRepository(BaseRepository[Session]):
    """会话Repository"""
    
    def get_session_scenario(self, session_id: int) -> str:
        """获取会话场景类型（带缓存）"""
        cache_key = f"scenario:session:{session_id}"
        
        # 先查缓存
        scenario = self.cache_manager.get(cache_key)
        if scenario:
            return scenario
        
        # 查数据库（从会话扩展表获取）
        # ...
        
        return "general"
```

## 5. 实现计划

### Phase 1: Repository层基础 (P0)
- [ ] 创建BaseRepository基类
- [ ] 创建TransactionManager
- [ ] 实现UserRepository
- [ ] 实现SessionRepository
- [ ] 实现MessageRepository

### Phase 2: 数据持久化 (P0)
- [ ] 集成会话创建到路由流程
- [ ] 集成消息创建到技能执行流程
- [ ] 实现历史查询功能
- [ ] 实现数据导出功能

### Phase 3: 缓存策略 (P1)
- [ ] 统一缓存键命名
- [ ] 实现缓存读写策略
- [ ] 实现缓存失效策略
- [ ] 实现缓存预热

### Phase 4: 数据一致性 (P1)
- [ ] 实现写穿透策略
- [ ] 实现缓存失效策略
- [ ] 实现事务管理
- [ ] 实现并发控制

### Phase 5: 数据备份和迁移 (P2)
- [ ] 实现定期备份
- [ ] 实现备份验证
- [ ] 实现快速恢复
- [ ] 实现数据迁移工具

## 6. 测试方案

### 单元测试
- Repository CRUD操作测试
- 缓存读写测试
- 缓存失效测试
- 事务回滚测试

### 集成测试
- 会话创建和查询测试
- 消息创建和查询测试
- 缓存一致性测试
- 并发访问测试

### 性能测试
- 数据库查询性能测试
- 缓存命中率测试
- 并发请求测试
- 数据一致性测试
