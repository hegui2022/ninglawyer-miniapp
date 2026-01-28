"""
智能输入解析器
Smart Input Parser - 使用 LLM 智能解析用户输入
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
import os


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

文本内容：
{user_input}

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

JSON：
"""
        
        try:
            response = self.llm.invoke(prompt)
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
            
            import json
            parsed_data = json.loads(result)
            
            # 过滤掉 null 值
            return {k: v for k, v in parsed_data.items() if v is not None and v != ""}
            
        except Exception as e:
            print(f"解析基本信息失败: {e}")
            return {}
    
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

文本内容：
{user_input}

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

JSON：
"""
        
        try:
            response = self.llm.invoke(prompt)
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
            
            import json
            parsed_data = json.loads(result)
            
            # 过滤掉 null 值
            return {k: v for k, v in parsed_data.items() if v is not None and v != ""}
            
        except Exception as e:
            print(f"解析合同期限失败: {e}")
            return {}
    
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

文本内容：
{user_input}

需要提取的字段：
- position: 工作岗位
- work_location: 工作地点
- job_responsibilities: 岗位职责（详细描述）
- can_change_location: 是否可以调整工作地点（true/false）

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. 岗位职责要提取完整的描述内容

JSON：
"""
        
        try:
            response = self.llm.invoke(prompt)
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
            
            import json
            parsed_data = json.loads(result)
            
            # 过滤掉 null 值
            return {k: v for k, v in parsed_data.items() if v is not None and v != ""}
            
        except Exception as e:
            print(f"解析工作内容失败: {e}")
            return {}
    
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

文本内容：
{user_input}

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

JSON：
"""
        
        try:
            response = self.llm.invoke(prompt)
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
            
            import json
            parsed_data = json.loads(result)
            
            # 过滤掉 null 值，并确保数字类型
            result_dict = {}
            for k, v in parsed_data.items():
                if v is not None and v != "":
                    # 尝试转为数字
                    if k in ["base_salary", "performance_bonus", "allowances", "pay_day"]:
                        try:
                            result_dict[k] = float(v)
                        except:
                            result_dict[k] = v
                    else:
                        result_dict[k] = v
            
            return result_dict
            
        except Exception as e:
            print(f"解析劳动报酬失败: {e}")
            return {}
    
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

文本内容：
{user_input}

需要提取的字段：
- has_compensation: 是否约定经济补偿（true/false）
- notice_period: 通知期（数字，单位：天）
- allow_termination: 允许单方解除（true/false）

注意事项：
1. 如果某个字段没有找到，设为 null
2. 只返回纯 JSON 格式，不要其他文字
3. notice_period 要转为数字

JSON：
"""
        
        try:
            response = self.llm.invoke(prompt)
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
            
            import json
            parsed_data = json.loads(result)
            
            # 过滤掉 null 值，并确保数字类型
            result_dict = {}
            for k, v in parsed_data.items():
                if v is not None and v != "":
                    if k in ["notice_period"]:
                        try:
                            result_dict[k] = float(v)
                        except:
                            result_dict[k] = v
                    else:
                        result_dict[k] = v
            
            return result_dict
            
        except Exception as e:
            print(f"解析合同解除失败: {e}")
            return {}


# 创建实例
smart_input_parser = SmartInputParser()
