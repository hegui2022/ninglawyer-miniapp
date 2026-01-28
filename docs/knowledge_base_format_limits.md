# 知识库格式和限制说明文档

## ✅ 测试结果

已成功导入用户上传的4个Word文档：
- `成功CEO临门一脚   数据合规管理1.docx` (12,903字符)
- `成功CEO临门一脚  数据合规管理2.docx` (17,463字符)
- `成功CEO临门一脚 数据合规管理3.docx` (47,241字符)
- `成功CEO临门一脚 数据合规管理4.docx` (59,613字符)

**总计**：137,350字符

---

## 📊 支持的格式

### 直接支持的格式

1. **纯文本（TXT）** ✅
   - 直接使用 `--content` 参数
   - 示例：`coze-coding-ai knowledge add --dataset "my_data" --content "文本内容"`

2. **URL** ✅
   - 支持从网页导入
   - 示例：`coze-coding-ai knowledge add --dataset "my_data" --url "https://example.com/doc.html"`

3. **Markdown（.md）** ✅
   - 推荐！结构化清晰
   - 支持标题、列表、表格等

### 需要转换的格式

1. **Word文档（.docx）** ⚠️
   - **不能直接导入**
   - 需要先转换为文本或Markdown
   - 使用 `python-docx` 库转换

2. **PDF文档（.pdf）** ⚠️
   - **不能直接导入**
   - 需要先转换为文本
   - 使用 `PyPDF2` 或 `pdfplumber` 库转换

3. **Excel文档（.xlsx）** ⚠️
   - **不能直接导入**
   - 需要先转换为文本
   - 使用 `pandas` 或 `openpyxl` 库转换

---

## 📏 大小限制

### 单次导入限制

根据测试结果：

| 参数 | 限制值 | 说明 |
|------|--------|------|
| **单次内容大小** | **至少 137,350 字符** | 已测试成功 |
| **单次文档大小** | 约 137 KB | 文本大小 |
| **建议单次大小** | 50,000 - 100,000 字符 | 分批导入更稳定 |

### 超大文档处理

**如果你的文档超过 137,350 字符**：

#### 方法 1：分批导入
```bash
# 分割文档为多个部分
coze-coding-ai knowledge add --dataset "my_data" --content "$(cat large_doc.md | head -c 50000)"
coze-coding-ai knowledge add --dataset "my_data" --content "$(cat large_doc.md | tail -c +50001 | head -c 50000)"
coze-coding-ai knowledge add --dataset "my_data" --content "$(cat large_doc.md | tail -c +100001)"
```

#### 方法 2：使用 Python SDK
```python
from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType

config = Config()
client = KnowledgeClient(config=config)

# 分块添加
large_text = "你的大文档内容"
chunk_size = 50000
for i in range(0, len(large_text), chunk_size):
    chunk = large_text[i:i+chunk_size]
    documents = [
        KnowledgeDocument(
            source=DataSourceType.TEXT,
            raw_data=chunk
        )
    ]
    client.add_documents(documents, table_name="my_data")
```

---

## 🔄 文档格式转换

### Word文档转换（.docx）

#### 步骤 1：安装依赖
```bash
pip install python-docx
```

#### 步骤 2：转换脚本
```python
from docx import Document

def convert_docx_to_text(file_path):
    doc = Document(file_path)
    content = []
    
    # 读取段落
    for para in doc.paragraphs:
        if para.text.strip():
            content.append(para.text.strip())
    
    # 读取表格
    for table in doc.tables:
        for row in table.rows:
            row_text = []
            for cell in row.cells:
                if cell.text.strip():
                    row_text.append(cell.text.strip())
            if row_text:
                content.append(" | ".join(row_text))
    
    return "\n\n".join(content)

# 使用
text = convert_docx_to_text("assets/document.docx")
print(text)
```

### PDF文档转换（.pdf）

#### 步骤 1：安装依赖
```bash
pip install PyPDF2
```

#### 步骤 2：转换脚本
```python
import PyPDF2

def convert_pdf_to_text(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        content = []
        for page in reader.pages:
            text = page.extract_text()
            if text.strip():
                content.append(text.strip())
        return "\n\n".join(content)

# 使用
text = convert_pdf_to_text("assets/document.pdf")
print(text)
```

### Excel文档转换（.xlsx）

#### 步骤 1：安装依赖
```bash
pip install pandas openpyxl
```

#### 步骤 2：转换脚本
```python
import pandas as pd

def convert_excel_to_text(file_path):
    # 读取所有工作表
    excel_file = pd.ExcelFile(file_path)
    content = []
    
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        content.append(f"## {sheet_name}\n\n")
        content.append(df.to_string())
    
    return "\n\n".join(content)

# 使用
text = convert_excel_to_text("assets/document.xlsx")
print(text)
```

---

## 💡 最佳实践

### 1. 推荐格式

**最佳**：Markdown（.md）
- ✅ 结构化清晰
- ✅ 支持标题、列表、表格
- ✅ 易于维护

**次选**：纯文本（.txt）
- ✅ 简单直接
- ✅ 兼容性好

**不推荐**：Word、PDF、Excel
- ❌ 需要转换
- ❌ 格式可能丢失

### 2. 文档结构建议

```markdown
# 文档标题

## 章节1

### 子章节
内容...

## 章节2

### 子章节
内容...

## 问答

### 问：问题？
答：答案...

## 法律条文

### 《法律名称》第X条
条文内容...

## 案例分析

### 案例名称
案情描述...
法律分析...
```

### 3. 分批建议

| 文档大小 | 建议方式 |
|---------|---------|
| < 50,000 字符 | 一次性导入 |
| 50,000 - 100,000 字符 | 建议分2-3批导入 |
| 100,000 - 200,000 字符 | 分批导入，每批50,000字符 |
| > 200,000 字符 | 使用 Python SDK 分块处理 |

### 4. 内容优化

**建议**：
- 使用清晰的标题结构
- 避免过多的格式符号
- 关键词明确，便于搜索
- 问答形式便于检索

**避免**：
- 过长的单段文字
- 复杂的嵌套表格
- 过多的特殊符号
- 图片、图表（无法索引）

---

## 📝 实际操作示例

### 示例 1：导入 Word 文档

```bash
# 步骤 1：转换 Word 为 Markdown
python scripts/convert_docx_to_md.py --input "assets/document.docx" --output "assets/document.md"

# 步骤 2：导入到知识库
coze-coding-ai knowledge add \
  --dataset "my_knowledge" \
  --content "$(cat assets/document.md)"

# 步骤 3：测试查询
coze-coding-ai knowledge search \
  --query "关键词" \
  --top-k 3
```

### 示例 2：导入多个文档

```bash
# 创建合并文档
cat assets/doc1.md assets/doc2.md assets/doc3.md > assets/combined.md

# 导入
coze-coding-ai knowledge add \
  --dataset "my_knowledge" \
  --content "$(cat assets/combined.md)"
```

### 示例 3：超大文档分批导入

```bash
# 假设文档有 300,000 字符
coze-coding-ai knowledge add \
  --dataset "my_knowledge" \
  --content "$(cat huge_doc.md | head -c 100000)"

coze-coding-ai knowledge add \
  --dataset "my_knowledge" \
  --content "$(cat huge_doc.md | tail -c +100001 | head -c 100000)"

coze-coding-ai knowledge add \
  --dataset "my_knowledge" \
  --content "$(cat huge_doc.md | tail -c +200001)"
```

---

## 🎯 总结

### ✅ 支持的格式
- 纯文本（TXT）
- URL（网页）
- Markdown（.md）✅ 推荐

### ⚠️ 需要转换
- Word文档（.docx）→ 转为 Markdown
- PDF文档（.pdf）→ 转为文本
- Excel文档（.xlsx）→ 转为文本

### 📏 大小限制
- **已测试**：137,350 字符（成功）
- **建议**：单次 50,000 - 100,000 字符
- **超大文档**：分批导入或使用 Python SDK

### 💡 最佳实践
- 使用 Markdown 格式
- 清晰的标题结构
- 关键词明确
- 大文档分批导入

---

## 📞 需要帮助？

如果你遇到问题：
1. 检查文档格式是否正确
2. 尝试分批导入
3. 使用 Python SDK 更灵活地处理
4. 联系技术支持
