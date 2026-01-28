"""
合同导出工具
Contract Export Tool - 导出合同为 Word/PDF 格式
"""

from typing import Dict, Any, List
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

# PDF 生成库
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


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
        if not filename:
            filename = f"contract_{self._generate_timestamp()}.pdf"
        elif not filename.endswith('.pdf'):
            filename = filename.replace('.docx', '.pdf')
        
        pdf_filepath = os.path.join(self.export_dir, filename)
        
        # 优先使用 reportlab 直接生成 PDF
        if HAS_REPORTLAB:
            try:
                return self._generate_pdf_with_reportlab(contract_text, pdf_filepath)
            except Exception as e:
                print(f"PDF生成失败: {str(e)}")
        
        # 回退方案：尝试使用 docx2pdf 或 comtypes
        word_filepath = self.export_to_word(contract_text, filename.replace('.pdf', '.docx'))
        
        if convert is not None:
            try:
                convert(word_filepath, pdf_filepath)
                return pdf_filepath
            except Exception as e:
                print(f"docx2pdf转换失败: {str(e)}")
        
        if client is not None:
            try:
                word = client.CreateObject('Word.Application')
                word.Visible = False
                
                doc = word.Documents.Open(os.path.abspath(word_filepath))
                doc.SaveAs(os.path.abspath(pdf_filepath), FileFormat=17)  # 17 = PDF
                doc.Close()
                word.Quit()
                
                return pdf_filepath
            except Exception as e:
                print(f"Word自动化失败: {str(e)}")
        
        # 所有方法都失败，返回 Word 文件路径
        return word_filepath
    
    def _generate_pdf_with_reportlab(self, contract_text: str, filepath: str) -> str:
        """使用 reportlab 直接生成 PDF"""
        # 创建 PDF 文档
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )
        
        # 样式
        styles = getSampleStyleSheet()
        
        # 创建自定义样式
        title_style = ParagraphStyle(
            'ChineseTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=12*mm
        )
        
        heading_style = ParagraphStyle(
            'ChineseHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            alignment=TA_LEFT,
            spaceAfter=6*mm,
            spaceBefore=6*mm
        )
        
        normal_style = ParagraphStyle(
            'ChineseNormal',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            alignment=TA_JUSTIFY,
            leading=14,
            spaceAfter=2*mm
        )
        
        # 解析合同文本
        story = []
        lines = contract_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 2*mm))
                continue
            
            # 处理 Markdown 格式
            if line.startswith('#'):
                # 移除 # 号
                title_text = line.lstrip('#').strip()
                
                if line.startswith('###'):
                    # 三级标题
                    story.append(Paragraph(title_text, heading_style))
                elif line.startswith('##'):
                    # 二级标题
                    story.append(Paragraph(title_text, heading_style))
                else:
                    # 一级标题
                    story.append(Paragraph(title_text, title_style))
            elif line.startswith(('一、', '二、', '三、', '四、', '五、', 
                                 '六、', '七、', '八、', '九、', '十、')):
                # 大条款标题
                story.append(Paragraph(f"<b>{line}</b>", heading_style))
            else:
                # 普通段落
                story.append(Paragraph(line, normal_style))
        
        # 生成 PDF
        doc.build(story)
        
        return filepath
    
    def _generate_timestamp(self) -> str:
        """生成时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")


# 创建实例
contract_exporter = ContractExporter()
