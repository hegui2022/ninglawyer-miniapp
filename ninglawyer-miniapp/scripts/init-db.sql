-- 宁律师小程序矩阵 - 数据库初始化脚本

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    openid VARCHAR(255) UNIQUE NOT NULL,
    nickname VARCHAR(100),
    avatar_url VARCHAR(500),
    phone VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建咨询记录表
CREATE TABLE IF NOT EXISTS consultations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    lawyer_type VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT,
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建合同表
CREATE TABLE IF NOT EXISTS contracts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建履约记录表
CREATE TABLE IF NOT EXISTS contract_fulfillments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_id UUID REFERENCES contracts(id),
    stage VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    due_date TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建维权记录表
CREATE TABLE IF NOT EXISTS legal_claims (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    claim_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    evidence TEXT[],
    status VARCHAR(20) DEFAULT 'processing',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建风险评估表
CREATE TABLE IF NOT EXISTS risk_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    risk_type VARCHAR(50) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    suggestions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_openid ON users(openid);
CREATE INDEX IF NOT EXISTS idx_consultations_user_id ON consultations(user_id);
CREATE INDEX IF NOT EXISTS idx_consultations_created_at ON consultations(created_at);
CREATE INDEX IF NOT EXISTS idx_contracts_user_id ON contracts(user_id);
CREATE INDEX IF NOT EXISTS idx_contract_fulfillments_contract_id ON contract_fulfillments(contract_id);
CREATE INDEX IF NOT EXISTS idx_legal_claims_user_id ON legal_claims(user_id);
CREATE INDEX IF NOT EXISTS idx_risk_assessments_user_id ON risk_assessments(user_id);

-- 插入测试数据（可选）
-- INSERT INTO users (openid, nickname) VALUES ('test_openid_001', '测试用户');
-- INSERT INTO consultations (user_id, lawyer_type, question, answer)
-- VALUES ((SELECT id FROM users WHERE openid = 'test_openid_001'), 'civil', '合同违约怎么办？', '根据《民法典》相关规定...');

COMMENT ON TABLE users IS '用户表';
COMMENT ON TABLE consultations IS '咨询记录表';
COMMENT ON TABLE contracts IS '合同表';
COMMENT ON TABLE contract_fulfillments IS '履约记录表';
COMMENT ON TABLE legal_claims IS '维权记录表';
COMMENT ON TABLE risk_assessments IS '风险评估表';
