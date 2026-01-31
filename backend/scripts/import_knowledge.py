#!/usr/bin/env python3
"""
知识库导入脚本
方便用户将文档导入到扣子知识库
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger


def import_text_content(content: str, dataset_name: str = "coze_doc_knowledge"):
    """
    导入文本内容到知识库
    
    Args:
        content: 文本内容
        dataset_name: 数据集名称
    """
    from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType
    from coze_coding_utils.runtime_ctx.context import new_context
    
    try:
        # 初始化客户端
        config = Config()
        client = KnowledgeClient(
            config=config,
            ctx=new_context(method="import_text")
        )
        
        # 创建文档
        doc = KnowledgeDocument(
            source=DataSourceType.TEXT,
            raw_data=content
        )
        
        # 导入文档
        response = client.add_documents(
            documents=[doc],
            table_name=dataset_name
        )
        
        if response.code == 0:
            logger.success(f"✅ 文本导入成功！文档ID: {response.doc_ids}")
            return True
        else:
            logger.error(f"❌ 文本导入失败：{response.msg}")
            return False
    
    except Exception as e:
        logger.error(f"❌ 导入文本时出错：{e}")
        return False


def import_url(url: str, dataset_name: str = "coze_doc_knowledge"):
    """
    导入URL内容到知识库
    
    Args:
        url: URL地址
        dataset_name: 数据集名称
    """
    from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType
    from coze_coding_utils.runtime_ctx.context import new_context
    
    try:
        # 初始化客户端
        config = Config()
        client = KnowledgeClient(
            config=config,
            ctx=new_context(method="import_url")
        )
        
        # 创建文档
        doc = KnowledgeDocument(
            source=DataSourceType.URL,
            url=url
        )
        
        # 导入文档
        response = client.add_documents(
            documents=[doc],
            table_name=dataset_name
        )
        
        if response.code == 0:
            logger.success(f"✅ URL导入成功！文档ID: {response.doc_ids}")
            return True
        else:
            logger.error(f"❌ URL导入失败：{response.msg}")
            return False
    
    except Exception as e:
        logger.error(f"❌ 导入URL时出错：{e}")
        return False


def import_file(file_path: str, dataset_name: str = "coze_doc_knowledge"):
    """
    导入文件内容到知识库
    
    Args:
        file_path: 文件路径
        dataset_name: 数据集名称
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用文本导入
        return import_text_content(content, dataset_name)
    
    except Exception as e:
        logger.error(f"❌ 导入文件时出错：{e}")
        return False


def import_directory(dir_path: str, dataset_name: str = "coze_doc_knowledge"):
    """
    批量导入目录中的所有文本文件到知识库
    
    Args:
        dir_path: 目录路径
        dataset_name: 数据集名称
    """
    import glob
    
    try:
        # 查找所有文本文件
        file_patterns = ["*.txt", "*.md", "*.rst", "*.html"]
        all_files = []
        
        for pattern in file_patterns:
            all_files.extend(glob.glob(os.path.join(dir_path, pattern)))
            all_files.extend(glob.glob(os.path.join(dir_path, "**", pattern), recursive=True))
        
        if not all_files:
            logger.warning(f"⚠️ 目录中未找到文本文件：{dir_path}")
            return True
        
        logger.info(f"🔍 找到 {len(all_files)} 个文件，开始导入...")
        
        success_count = 0
        fail_count = 0
        
        for file_path in all_files:
            logger.info(f"正在导入：{file_path}")
            if import_file(file_path, dataset_name):
                success_count += 1
            else:
                fail_count += 1
        
        logger.info(f"\n导入完成：成功 {success_count}，失败 {fail_count}")
        return fail_count == 0
    
    except Exception as e:
        logger.error(f"❌ 批量导入时出错：{e}")
        return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="知识库导入脚本")
    parser.add_argument("--type", choices=["text", "url", "file", "dir"], required=True, help="导入类型")
    parser.add_argument("--content", help="文本内容（仅type=text时使用）")
    parser.add_argument("--url", help="URL地址（仅type=url时使用）")
    parser.add_argument("--file", help="文件路径（仅type=file时使用）")
    parser.add_argument("--dir", help="目录路径（仅type=dir时使用）")
    parser.add_argument("--dataset", default="coze_doc_knowledge", help="数据集名称（默认: coze_doc_knowledge）")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("📚 知识库导入脚本")
    logger.info("=" * 60)
    logger.info("")
    
    # 根据类型执行导入
    if args.type == "text":
        if not args.content:
            logger.error("❌ 错误：type=text 需要提供 --content 参数")
            return 1
        success = import_text_content(args.content, args.dataset)
    
    elif args.type == "url":
        if not args.url:
            logger.error("❌ 错误：type=url 需要提供 --url 参数")
            return 1
        success = import_url(args.url, args.dataset)
    
    elif args.type == "file":
        if not args.file:
            logger.error("❌ 错误：type=file 需要提供 --file 参数")
            return 1
        success = import_file(args.file, args.dataset)
    
    elif args.type == "dir":
        if not args.dir:
            logger.error("❌ 错误：type=dir 需要提供 --dir 参数")
            return 1
        success = import_directory(args.dir, args.dataset)
    
    else:
        logger.error("❌ 错误：未知的导入类型")
        return 1
    
    logger.info("")
    if success:
        logger.success("=" * 60)
        logger.success("✅ 导入完成！")
        logger.success("=" * 60)
        return 0
    else:
        logger.error("=" * 60)
        logger.error("❌ 导入失败！")
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
