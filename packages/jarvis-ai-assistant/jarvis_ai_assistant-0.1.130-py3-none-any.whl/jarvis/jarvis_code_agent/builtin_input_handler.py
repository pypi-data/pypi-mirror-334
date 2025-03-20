import re
from typing import Any, Tuple

from jarvis.jarvis_utils.output import PrettyOutput, OutputType


def builtin_input_handler(user_input: str, agent: Any) -> Tuple[str, bool]:
    """
    处理内置的特殊输入标记，并追加相应的提示词
    
    参数：
        user_input: 用户输入
        agent: 代理对象
        
    返回：
        Tuple[str, bool]: 处理后的输入和是否需要进一步处理
    """
    # 查找特殊标记
    special_tags = re.findall(r"'<([^>]+)>'", user_input)
    
    if not special_tags:
        return user_input, False
    
    # 使用集合去重
    processed_tags = set()
    # 处理每个标记
    for tag in special_tags:
        if tag in processed_tags:
            continue
        processed_tags.add(tag)
        
        if tag == "CodeBase":
            user_input = user_input.replace(f"'<{tag}>'", "")
            user_input += "\n请使用ask_codebase工具查询代码库"
        elif tag == "Web":
            user_input = user_input.replace(f"'<{tag}>'", "")
            user_input += "\n请使用search_web工具进行网页搜索"
        elif tag == "RAG":
            user_input = user_input.replace(f"'<{tag}>'", "")
            user_input += "\n请使用rag工具进行知识库检索"
        # 移除对未知标记的警告输出
    
    return user_input, False
