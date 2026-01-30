-- 宁律师项目数据库表结构（第一版）
-- 创建时间：2025-01-30
-- 数据库：PostgreSQL

-- ============================================
-- 1. 用户表（users）
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    -- 微信信息
    wechat_openid VARCHAR(100) UNIQUE,
    wechat_unionid VARCHAR(100),
    -- 手机信息
    phone VARCHAR(20) UNIQUE,
    -- 基本信息
    name VARCHAR(50),
    avatar VARCHAR(500),
    -- 用户角色
    role VARCHAR(20) DEFAULT 'individual',  -- individual | enterprise_member
    -- 状态
    status VARCHAR(20) DEFAULT 'active',  -- active | inactive | banned
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_users_wechat_openid ON users(wechat_openid);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_role ON users(role);

-- ============================================
-- 2. 企业表（enterprises）
-- ============================================
CREATE TABLE IF NOT EXISTS enterprises (
    id SERIAL PRIMARY KEY,
    -- 企业基本信息
    name VARCHAR(200) NOT NULL,
    unified_code VARCHAR(50) UNIQUE,  -- 统一社会信用代码
    business_license VARCHAR(500),  -- 营业执照图片URL
    -- 认证信息
    verified BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMP,
    -- 联系信息
    contact_name VARCHAR(50),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(100),
    -- 地址信息
    address VARCHAR(500),
    province VARCHAR(50),
    city VARCHAR(50),
    -- 状态
    status VARCHAR(20) DEFAULT 'active',
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_enterprises_unified_code ON enterprises(unified_code);
CREATE INDEX idx_enterprises_verified ON enterprises(verified);

-- ============================================
-- 3. 用户-企业关系表（user_enterprise_relations）
-- ============================================
CREATE TABLE IF NOT EXISTS user_enterprise_relations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    enterprise_id INTEGER NOT NULL,
    -- 在企业中的角色
    role_in_enterprise VARCHAR(50),  -- 法务 | 老总 | 负责人 | 员工 | 董事 | 股东
    -- 部门（可选）
    department VARCHAR(100),
    -- 职位（可选）
    position VARCHAR(100),
    -- 状态
    status VARCHAR(20) DEFAULT 'active',
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (enterprise_id) REFERENCES enterprises(id) ON DELETE CASCADE,
    -- 唯一约束（一个用户在同一企业只能有一个关系）
    UNIQUE (user_id, enterprise_id)
);

-- 索引
CREATE INDEX idx_user_enterprise_user_id ON user_enterprise_relations(user_id);
CREATE INDEX idx_user_enterprise_enterprise_id ON user_enterprise_relations(enterprise_id);
CREATE INDEX idx_user_enterprise_role ON user_enterprise_relations(role_in_enterprise);

-- ============================================
-- 4. 合同记录表（contracts）
-- ============================================
CREATE TABLE IF NOT EXISTS contracts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    -- 合同基本信息
    contract_type VARCHAR(50),  -- 采购合同 | 服务合同 | 租赁合同 | 劳动合同 | 合作协议 | 保密协议 | 借款合同
    contract_title VARCHAR(200),
    contract_text TEXT,
    -- 合同状态
    status VARCHAR(20) DEFAULT 'draft',  -- draft | signed | archived
    -- 合同元数据
    party_a VARCHAR(200),  -- 甲方
    party_b VARCHAR(200),  -- 乙方
    contract_amount DECIMAL(18, 2),  -- 合同金额
    contract_start_date DATE,
    contract_end_date DATE,
    -- 扣子智能体生成的信息
    bot_id VARCHAR(100),  -- 使用的智能体ID
    bot_name VARCHAR(100),  -- 智能体名称
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX idx_contracts_user_id ON contracts(user_id);
CREATE INDEX idx_contracts_contract_type ON contracts(contract_type);
CREATE INDEX idx_contracts_status ON contracts(status);
CREATE INDEX idx_contracts_created_at ON contracts(created_at);

-- ============================================
-- 5. 用户反馈表（user_feedback）
-- ============================================
CREATE TABLE IF NOT EXISTS user_feedback (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    -- 反馈信息
    feedback_text TEXT NOT NULL,
    feedback_type VARCHAR(50),  -- bug | feature | other | complaint
    rating INTEGER,  -- 1-5星
    -- 关联信息
    related_consultation_id VARCHAR(100),  -- 关联的咨询ID
    -- 处理状态
    status VARCHAR(20) DEFAULT 'pending',  -- pending | processing | resolved
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 索引
CREATE INDEX idx_user_feedback_user_id ON user_feedback(user_id);
CREATE INDEX idx_user_feedback_type ON user_feedback(feedback_type);
CREATE INDEX idx_user_feedback_status ON user_feedback(status);
CREATE INDEX idx_user_feedback_created_at ON user_feedback(created_at);

-- ============================================
-- 6. 会话记录表（conversations）
-- 可选：如果需要保存重要的对话记录（比如企业认证相关）
-- ============================================
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    -- 会话信息
    session_id VARCHAR(100) UNIQUE,
    conversation_type VARCHAR(50),  -- consultation | contract | compliance | certification
    -- 会话内容
    user_message TEXT,
    bot_response TEXT,
    bot_id VARCHAR(100),
    bot_name VARCHAR(100),
    -- 元数据
    app_type VARCHAR(50),  -- ninglawyer | fangfengxian | contract
    extra_data JSONB,  -- 额外数据（灵活存储）
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 索引
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_session_id ON conversations(session_id);
CREATE INDEX idx_conversations_type ON conversations(conversation_type);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);

-- ============================================
-- 7. 验证码表（verification_codes）
-- 用于存储短信验证码
-- ============================================
CREATE TABLE IF NOT EXISTS verification_codes (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,
    code VARCHAR(10) NOT NULL,
    code_type VARCHAR(20) DEFAULT 'login',  -- login | register | bind_phone
    -- 过期时间（5分钟）
    expires_at TIMESTAMP NOT NULL,
    -- 是否已使用
    used BOOLEAN DEFAULT FALSE,
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_verification_codes_phone ON verification_codes(phone);
CREATE INDEX idx_verification_codes_code_type ON verification_codes(code_type);
CREATE INDEX idx_verification_codes_expires_at ON verification_codes(expires_at);

-- ============================================
-- 插入初始数据（可选）
-- ============================================

-- 创建管理员用户（密码需要在应用层加密）
INSERT INTO users (phone, name, role, status) VALUES
('13800000000', '系统管理员', 'admin', 'active')
ON CONFLICT (phone) DO NOTHING;

-- ============================================
-- 更新触发器（自动更新 updated_at 字段）
-- ============================================

-- 为所有有 updated_at 字段的表创建触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_enterprises_updated_at BEFORE UPDATE ON enterprises
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_enterprise_relations_updated_at BEFORE UPDATE ON user_enterprise_relations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contracts_updated_at BEFORE UPDATE ON contracts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_feedback_updated_at BEFORE UPDATE ON user_feedback
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 数据库表结构创建完成
-- ============================================
