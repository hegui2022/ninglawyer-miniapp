-- 法律案例数据库表设计
-- 创建时间: 2025

-- ============================================
-- 1. 案例主表
-- ============================================
CREATE TABLE IF NOT EXISTS legal_cases (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL COMMENT '标题',
    subtitle VARCHAR(500) NOT NULL COMMENT '副标题',
    basic_facts TEXT COMMENT '基本案情（HTML格式）',
    judgment_essence TEXT COMMENT '裁判要旨（HTML格式）',
    judgment_result TEXT COMMENT '裁判结果（HTML格式）',
    dispute_foci JSONB COMMENT '争议焦点（JSON数组）',
    related_index JSONB COMMENT '关联索引（JSON格式）',
    keywords JSONB COMMENT '关键词（JSON数组）',
    
    status VARCHAR(20) DEFAULT 'draft' COMMENT '状态：draft-草稿, published-已发布',
    created_by VARCHAR(100) COMMENT '创建人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_legal_cases_title ON legal_cases(title);
CREATE INDEX idx_legal_cases_status ON legal_cases(status);
CREATE INDEX idx_legal_cases_created_at ON legal_cases(created_at);

-- ============================================
-- 2. 历审程序表
-- ============================================
CREATE TABLE IF NOT EXISTS case_proceedings (
    id BIGSERIAL PRIMARY KEY,
    case_id BIGINT NOT NULL REFERENCES legal_cases(id) ON DELETE CASCADE,
    
    procedure_type VARCHAR(50) COMMENT '审理程序',
    court VARCHAR(200) COMMENT '审理法院',
    case_number VARCHAR(200) COMMENT '案号',
    judgment_type VARCHAR(50) COMMENT '裁判类型',
    judgment_date DATE COMMENT '裁判日期',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_case_proceedings_case_id ON case_proceedings(case_id);

-- ============================================
-- 3. 主要法条表
-- ============================================
CREATE TABLE IF NOT EXISTS case_laws (
    id BIGSERIAL PRIMARY KEY,
    case_id BIGINT NOT NULL REFERENCES legal_cases(id) ON DELETE CASCADE,
    
    law_name VARCHAR(200) NOT NULL COMMENT '法律名称',
    article_numbers VARCHAR(500) NOT NULL COMMENT '法条序号',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_case_laws_case_id ON case_laws(case_id);

-- ============================================
-- 示例数据（可选）
-- ============================================
-- INSERT INTO legal_cases (title, subtitle, basic_facts, judgment_essence, judgment_result, dispute_foci, status, created_by)
-- VALUES ('示例案例', '这是一个示例', '<p>案情描述</p>', '<p>裁判要旨</p>', '<p>裁判结果</p>', '["焦点1", "焦点2"]', 'published', 'admin');
