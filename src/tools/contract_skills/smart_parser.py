"""
智能输入解析器 V2.0
Smart Input Parser - 使用 LLM 智能解析用户输入，支持多种格式和自然语言
"""

from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
import os
import re
import json
from datetime import datetime


class SmartInputParser:
    """智能输入解析器"""
    
    def __init__(self, ctx=None):
        """
        初始化解析器
        
        Args:
            ctx: 上下文
        """
        self.ctx = ctx
        
        # 初始化 LLM
        api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
        base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
        
        self.llm = ChatOpenAI(
            model="doubao-seed-1-8-251228",
            api_key=api_key,
            base_url=base_url,
            temperature=0.3,  # 较低的温度，提高准确性
            top_p=0.9,
            max_tokens=2000,
        )
        
        # 预编译正则表达式
        self._compile_regex_patterns()
    
    def _compile_regex_patterns(self):
        """编译常用的正则表达式模式"""
        self.patterns = {
            # 日期模式
            'date_cn': r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            'date_slash': r'(\d{4})/(\d{1,2})/(\d{1,2})',
            'date_dash': r'(\d{4})-(\d{1,2})-(\d{1,2})',
            
            # 金额模式
            'amount': r'(\d+(?:\.\d+)?)\s*(?:元|块|万|千)',
            'salary': r'(\d+(?:\.\d+)?)\s*(?:元/月|块/月|万/月|千/月)',
            
            # 电话号码
            'phone': r'1[3-9]\d{9}',
            
            # 身份证号
            'id_card': r'[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]',
        }
    
    def _preprocess_input(self, user_input: str) -> str:
        """
        预处理用户输入，统一格式
        
        Args:
            user_input: 原始输入
            
        Returns:
            处理后的输入
        """
        if not user_input:
            return ""
        
        # 清理空白字符
        text = user_input.strip()
        
        # 统一分隔符
        text = text.replace('，', ',').replace('。', '.').replace('；', ';')
        
        # 处理表格格式
        if '|' in text and '\n' in text:
            text = self._convert_table_to_text(text)
        
        return text
    
    def _convert_table_to_text(self, text: str) -> str:
        """
        将表格格式转换为文本格式
        
        Args:
            text: 表格格式文本
            
        Returns:
            转换后的文本
        """
        lines = text.split('\n')
        result = []
        
        for line in lines:
            if '|' in line:
                # 去除首尾的 | 和多余的空格
                cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                if cells:
                    # 尝试识别键值对
                    if len(cells) >= 2:
                        result.append(f"{cells[0]}：{cells[1]}")
                    else:
                        result.append(cells[0])
        
        return '\n'.join(result)
    
    def _extract_with_regex(self, text: str, pattern_name: str) -> List[str]:
        """
        使用正则表达式提取信息
        
        Args:
            text: 文本
            pattern_name: 模式名称
            
        Returns:
            提取的结果列表
        """
        if pattern_name not in self.patterns:
            return []
        
        pattern = self.patterns[pattern_name]
        matches = re.findall(pattern, text)
        return matches
    
    def _normalize_date(self, date_str: str) -> str:
        """
        标准化日期格式
        
        Args:
            date_str: 日期字符串
            
        Returns:
            标准化后的日期（YYYY年MM月DD日）
        """
        # 尝试解析各种格式
        for pattern_name in ['date_cn', 'date_slash', 'date_dash']:
            matches = self._extract_with_regex(date_str, pattern_name)
            if matches:
                year, month, day = matches[0]
                return f"{year}年{int(month):02d}月{int(day):02d}日"
        
        return date_str
    
    def _normalize_amount(self, amount_str: str) -> float:
        """
        标准化金额
        
        Args:
            amount_str: 金额字符串
            
        Returns:
            标准化后的金额
        """
        # 提取数字
        match = re.search(r'(\d+(?:\.\d+)?)', amount_str)
        if match:
            amount = float(match.group(1))
            
            # 处理单位
            if '万' in amount_str:
                amount *= 10000
            elif '千' in amount_str:
                amount *= 1000
            
            return amount
        
        return 0.0
    
    def _extract_key_value_pairs(self, text: str) -> Dict[str, str]:
        """
        从文本中提取键值对
        
        Args:
            text: 文本
            
        Returns:
            键值对字典
        """
        pairs = {}
        
        # 模式1：键：值
        matches = re.findall(r'([^：:\n]+)[：:]\s*([^：:\n]+)', text)
        for key, value in matches:
            pairs[key.strip()] = value.strip()
        
        # 模式2：键是值
        matches = re.findall(r'([^是\n]+)是([^，。\n]+)', text)
        for key, value in matches:
            pairs[key.strip()] = value.strip()
        
        return pairs
    
    def _enhance_llm_extraction(self, prompt: str, user_input: str) -> Dict[str, Any]:
        """
        增强的 LLM 提取方法，添加预提取和后处理
        
        Args:
            prompt: 提示词
            user_input: 用户输入
            
        Returns:
            提取的信息字典
        """
        # 预处理输入
        processed_input = self._preprocess_input(user_input)
        
        # 预提取键值对
        kv_pairs = self._extract_key_value_pairs(processed_input)
        
        # 在 prompt 中添加预提取的上下文
        enhanced_prompt = prompt
        if kv_pairs:
            kv_context = "\n已识别的键值对：\n"
            for key, value in kv_pairs.items():
                kv_context += f"- {key}：{value}\n"
            enhanced_prompt = prompt.replace("文本内容：\n", f"文本内容：\n{kv_context}\n")
        
        try:
            response = self.llm.invoke(enhanced_prompt)
            content = response.content
            
            # 转换为字符串
            if isinstance(content, list):
                result = ""
                for item in content:
                    if isinstance(item, dict):
                        result += str(item)
                    else:
                        result += str(item)
                result = result.strip()
            else:
                result = str(content).strip()
            
            # 提取 JSON 部分
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                result = result.split("```")[1].split("```")[0].strip()
            
            parsed_data = json.loads(result)
            
            # 后处理：标准化数据
            processed_data = self._post_process_extraction(parsed_data)
            
            # 过滤掉 null 值
            return {k: v for k, v in processed_data.items() if v is not None and v != ""}
            
        except Exception as e:
            print(f"LLM 提取失败: {e}")
            # 降级使用正则提取
            return self._fallback_extraction(processed_input, kv_pairs)
    
    def _post_process_extraction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        后处理提取的数据，标准化格式
        
        Args:
            data: 原始数据
            
        Returns:
            处理后的数据
        """
        result = {}
        
        for key, value in data.items():
            if value is None or value == "":
                continue
            
            # 处理日期字段
            if 'date' in key.lower() and isinstance(value, str):
                result[key] = self._normalize_date(value)
            # 处理金额字段
            elif any(kw in key.lower() for kw in ['salary', 'amount', 'bonus', 'fee']):
                if isinstance(value, str):
                    result[key] = self._normalize_amount(value)
                else:
                    result[key] = value
            # 处理布尔字段
            elif value in ['true', '是', '有', 'yes']:
                result[key] = True
            elif value in ['false', '否', '无', 'no']:
                result[key] = False
            else:
                result[key] = value
        
        return result
    
    def _fallback_extraction(self, text: str, kv_pairs: Dict[str, str]) -> Dict[str, Any]:
        """
        降级提取方法，使用正则表达式和键值对
        
        Args:
            text: 文本
            kv_pairs: 已提取的键值对
            
        Returns:
            提取的信息字典
        """
        result = {}
        
        # 从键值对中提取
        for key, value in kv_pairs.items():
            # 根据关键字段名映射
            if '单位' in key and '名称' in key:
                result['employer_name'] = value
            elif '姓名' in key and '劳动' not in key:
                result['employee_name'] = value
            elif '身份证' in key:
                result['employee_id'] = value
            elif '电话' in key or '手机' in key:
                result['employee_contact'] = value
            elif '地址' in key:
                result['employee_address'] = value
            elif '工资' in key or '薪酬' in key or '薪资' in key:
                result['base_salary'] = self._normalize_amount(value)
            elif '日期' in key:
                if '开始' in key or '生效' in key:
                    result['start_date'] = self._normalize_date(value)
                elif '结束' in key or '到期' in key:
                    result['end_date'] = self._normalize_date(value)
        
        # 使用正则提取额外信息
        # 提取电话号码
        phones = self._extract_with_regex(text, 'phone')
        if phones and 'employee_contact' not in result:
            result['employee_contact'] = phones[0]
        
        # 提取身份证号
        id_cards = self._extract_with_regex(text, 'id_card')
        if id_cards and 'employee_id' not in result:
            result['employee_id'] = id_cards[0]
        
        # 提取金额
        amounts = self._extract_with_regex(text, 'salary')
        if amounts and 'base_salary' not in result:
            result['base_salary'] = self._normalize_amount(amounts[0] + '元')
        
        return result
    
    def parse_basic_info(self, user_input: str) -> Dict[str, Any]:
        """
        解析基本信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            解析出的信息字典
        """
        prompt = f"""
请从以下文本中提取用人单位和劳动者的基本信息，以 JSON 格式返回：

需要提取的字段：
- employer_name: 用人单位名称
- employer_address: 用人单位地址
- employer_legal_rep: 法定代表人
- employer_contact: 联系电话
- employee_name: 劳动者姓名
- employee_id: 身份证号码
- employee_address: 住址
- employee_contact: 联系电话
- employee_emergency_contact: 紧急联系人

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. 注意区分用人单位和劳动者的信息
4. 支持键值对、段落、表格等多种输入格式
5. 对模糊信息进行合理推断

JSON：
"""
        
        return self._enhance_llm_extraction(prompt, user_input)
    
    def parse_intern_info(self, user_input: str) -> Dict[str, Any]:
        """
        解析实习协议基本信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            解析出的信息字典
        """
        prompt = f"""
请从以下文本中提取实习协议的基本信息，以 JSON 格式返回：

需要提取的字段：
- employer_name: 实习单位名称
- employer_address: 实习单位地址
- employer_contact: 实习单位联系人
- employer_phone: 实习单位联系电话
- intern_name: 实习生姓名
- school_name: 学校名称
- major: 所学专业
- student_id: 学号
- phone: 联系电话
- emergency_contact: 紧急联系人及电话

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. 支持自然语言描述

JSON：
"""
        
        return self._enhance_llm_extraction(prompt, user_input)
    
    def parse_retired_info(self, user_input: str) -> Dict[str, Any]:
        """
        解析退休返聘协议基本信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            解析出的信息字典
        """
        prompt = f"""
请从以下文本中提取退休返聘协议的基本信息，以 JSON 格式返回：

需要提取的字段：
- employer_name: 用人单位名称
- employer_address: 用人单位地址
- employer_contact: 联系人
- employer_phone: 联系电话
- retiree_name: 退休人员姓名
- id_card: 身份证号码
- retirement_certificate: 退休证号码
- former_employer: 原工作单位
- address: 住址
- phone: 联系电话
- emergency_contact: 紧急联系人

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. 支持自然语言描述

JSON：
"""
        
        return self._enhance_llm_extraction(prompt, user_input)
    
    def parse_project_info(self, user_input: str) -> Dict[str, Any]:
        """
        解析项目制合同基本信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            解析出的信息字典
        """
        prompt = f"""
请从以下文本中提取项目制合同的基本信息，以 JSON 格式返回：

需要提取的字段：
- employer_name: 甲方（委托方）单位名称
- employer_address: 甲方单位地址
- employer_legal_rep: 甲方法定代表人
- employer_contact: 甲方联系电话
- employee_name: 乙方（承接方）姓名
- employee_id: 乙方身份证号码
- employee_address: 乙方住址
- employee_phone: 乙方联系电话
- emergency_contact: 紧急联系人

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. 区分甲方和乙方信息

JSON：
"""
        
        return self._enhance_llm_extraction(prompt, user_input)
    
    def parse_dispatch_info(self, user_input: str) -> Dict[str, Any]:
        """
        解析劳务派遣合同基本信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            解析出的信息字典
        """
        prompt = f"""
请从以下文本中提取劳务派遣合同的基本信息，以 JSON 格式返回：

需要提取的字段：
- dispatch_company: 劳务派遣单位（甲方）名称
- dispatch_address: 劳务派遣单位地址
- workplace_name: 用工单位（乙方）名称
- workplace_address: 用工单位地址
- employee_name: 劳动者（丙方）姓名
- employee_id: 劳动者身份证号码

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. 区分甲方（派遣单位）、乙方（用工单位）、丙方（劳动者）

JSON：
"""
        
        return self._enhance_llm_extraction(prompt, user_input)
    
    def parse_contract_term(self, user_input: str) -> Dict[str, Any]:
        """
        解析合同期限信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            解析出的信息字典
        """
        prompt = f"""
请从以下文本中提取合同期限相关信息，以 JSON 格式返回：

需要提取的字段：
- contract_type: 合同类型（fixed_term/no_fixed_term/task_based）
- start_date: 合同开始日期（YYYY年MM月DD日格式）
- end_date: 合同结束日期（YYYY年MM月DD日格式，如果是无固定期限则为 null）
- has_probation: 是否约定试用期（true/false）
- probation_start_date: 试用期开始日期（YYYY年MM月DD日格式）
- probation_end_date: 试用期结束日期（YYYY年MM月DD日格式）
- probation_salary_ratio: 试用期工资比例（如 80%）

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. contract_type 的值只能是：fixed_term, no_fixed_term, task_based
4. 支持自然语言描述，如"3年"、"无固定期限"、"有试用期3个月"
5. 试用期工资比例转换为百分比数字

JSON：
"""
        
        return self._enhance_llm_extraction(prompt, user_input)
    
    def parse_work_content(self, user_input: str) -> Dict[str, Any]:
        """
        解析工作内容信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            解析出的信息字典
        """
        prompt = f"""
请从以下文本中提取工作内容相关信息，以 JSON 格式返回：

需要提取的字段：
- position: 工作岗位
- work_location: 工作地点
- job_responsibilities: 岗位职责（详细描述）
- can_change_location: 是否可以调整工作地点（true/false）

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. 岗位职责要提取完整的描述内容
4. 支持自然语言描述，如"产品经理"、"北京"、"负责产品规划"
5. 对"可以调动"、"不固定地点"等描述进行语义判断

JSON：
"""
        
        return self._enhance_llm_extraction(prompt, user_input)
    
    def parse_salary(self, user_input: str) -> Dict[str, Any]:
        """
        解析劳动报酬信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            解析出的信息字典
        """
        prompt = f"""
请从以下文本中提取劳动报酬相关信息，以 JSON 格式返回：

需要提取的字段：
- salary_type: 工资类型（monthly/hourly/daily）
- base_salary: 基本工资（数字）
- performance_bonus: 绩效奖金（数字）
- allowances: 津贴补贴（数字）
- pay_day: 发薪日（数字，如15表示每月15日）
- overtime_calculation_base: 加班费计算基数（base_salary/total_salary）

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. 数字类型要转为数字，不是字符串
4. 支持自然语言描述，如"月薪8千"、"每月15号发工资"
5. 支持"万"、"千"等单位转换

JSON：
"""
        
        return self._enhance_llm_extraction(prompt, user_input)
    
    def parse_termination(self, user_input: str) -> Dict[str, Any]:
        """
        解析合同解除信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            解析出的信息字典
        """
        prompt = f"""
请从以下文本中提取合同解除相关信息，以 JSON 格式返回：

需要提取的字段：
- has_compensation: 是否约定经济补偿（true/false）
- notice_period: 通知期（数字，单位：天）
- allow_termination: 允许单方解除（true/false）

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. notice_period 要转为数字
4. 支持自然语言描述，如"提前30天通知"、"有经济补偿"
5. 对"可以离职"、"协商一致"等描述进行语义判断

JSON：
"""
        
        return self._enhance_llm_extraction(prompt, user_input)


# 创建实例
smart_input_parser = SmartInputParser()
