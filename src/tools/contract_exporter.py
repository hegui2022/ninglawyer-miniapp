"""
合同导出工具
Contract Export Tool - 导出合同为 Word/PDF 格式
"""

from typing import Dict, Any
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

# 可选导入
try:
    from docx2pdf import convert  # type: ignore
except ImportError:
    convert = None

try:
    from comtypes import client  # type: ignore
except ImportError:
    client = None


class ContractExporter:
    """合同导出器"""
    
    def __init__(self):
        self.export_dir = "/tmp/contracts"
        os.makedirs(self.export_dir, exist_ok=True)
    
    def export_to_word(self, contract_text: str, filename: str = None) -> str:
        """
        导出合同为 Word 格式
        
        Args:
            contract_text: 合同文本
            filename: 文件名（可选）
            
        Returns:
            导出文件的路径
        """
        if not filename:
            filename = f"contract_{self._generate_timestamp()}.docx"
        
        # 创建 Word 文档
        doc = Document()
        
        # 分段处理合同文本
        paragraphs = contract_text.split('\n')
        
        for para_text in paragraphs:
            para_text = para_text.strip()
            if not para_text:
                doc.add_paragraph()  # 空行
                continue
            
            # 判断是否为标题（以 # 开头）
            if para_text.startswith('#'):
                # 标题
                title = para_text.lstrip('#').strip()
                heading = doc.add_heading(title, level=1)
                heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
                heading.style.font.size = Pt(18)
            elif para_text.startswith('##'):
                # 二级标题
                title = para_text.lstrip('#').strip()
                heading = doc.add_heading(title, level=2)
                heading.style.font.size = Pt(16)
            elif para_text.startswith('###'):
                # 三级标题
                title = para_text.lstrip('#').strip()
                heading = doc.add_heading(title, level=3)
                heading.style.font.size = Pt(14)
            else:
                # 普通段落
                # 判断是否为条款标题（以"一、"开头）
                if para_text.startswith(('一、', '二、', '三、', '四、', '五、', 
                                       '六、', '七、', '八、', '九、', '十、',
                                       '十一、', '十二、')):
                    para = doc.add_paragraph(para_text)
                    for run in para.runs:
                        run.font.size = Pt(14)
                        run.font.bold = True
                # 判断是否为子条款（以数字开头，如"1."）
                elif para_text[0].isdigit() and ('.' in para_text or '、' in para_text[:5]):
                    para = doc.add_paragraph(para_text)
                    for run in para.runs:
                        run.font.size = Pt(12)
                else:
                    para = doc.add_paragraph(para_text)
                    for run in para.runs:
                        run.font.size = Pt(12)
        
        # 保存文档
        filepath = os.path.join(self.export_dir, filename)
        doc.save(filepath)
        
        return filepath
    
    def export_to_pdf(self, contract_text: str, filename: str = None) -> str:
        """
        导出合同为 PDF 格式
        
        Args:
            contract_text: 合同文本
            filename: 文件名（可选）
            
        Returns:
            导出文件的路径
        """
        # 先导出为 Word
        word_filepath = self.export_to_word(contract_text, filename)
        
        # 将 Word 转换为 PDF
        if not filename:
            filename = os.path.basename(word_filepath).replace('.docx', '.pdf')
        else:
            filename = filename.replace('.docx', '.pdf')
        
        pdf_filepath = os.path.join(self.export_dir, filename)
        
        # 使用 docx2pdf 转换
        if convert is not None:
            convert(word_filepath, pdf_filepath)
            return pdf_filepath
        elif client is not None:
            # 如果没有 docx2pdf，使用其他方法
            word = client.CreateObject('Word.Application')
            word.Visible = False
            
            doc = word.Documents.Open(os.path.abspath(word_filepath))
            doc.SaveAs(os.path.abspath(pdf_filepath), FileFormat=17)  # 17 = PDF
            doc.Close()
            word.Quit()
            
            return pdf_filepath
        else:
            # 如果都失败，返回 Word 文件路径
            return word_filepath
    
    def _generate_timestamp(self) -> str:
        """生成时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")


# 创建实例
contract_exporter = ContractExporter()
