"""
方法论管理模块
该模块提供了加载和搜索方法论的实用工具。
包含以下功能：
- 创建方法论嵌入向量
- 加载和处理方法论数据
- 构建和搜索方法论索引
- 生成方法论提示
"""
import os
import yaml
import numpy as np
import faiss
from typing import Dict, Any, List
from jarvis.jarvis_utils.output import PrettyOutput, OutputType
from jarvis.jarvis_utils.embedding import load_embedding_model
from jarvis.jarvis_utils.config import dont_use_local_model
def _create_methodology_embedding(embedding_model: Any, methodology_text: str) -> np.ndarray:
    """
    为方法论文本创建嵌入向量。
    
    参数：
        embedding_model: 使用的嵌入模型
        methodology_text: 要创建嵌入的文本
        
    返回：
        np.ndarray: 嵌入向量
    """
    try:
        # 截断长文本
        max_length = 512
        text = ' '.join(methodology_text.split()[:max_length])
        
        # 使用sentence_transformers模型获取嵌入向量
        embedding = embedding_model.encode([text], 
                                          convert_to_tensor=True,
                                          normalize_embeddings=True)
        vector = np.array(embedding.cpu().numpy(), dtype=np.float32)
        return vector[0]  # 返回第一个向量，因为我们只编码了一个文本
    except Exception as e:
        PrettyOutput.print(f"创建方法论嵌入向量失败: {str(e)}", OutputType.ERROR)
        return np.zeros(1536, dtype=np.float32)
def make_methodology_prompt(data: Dict[str, str]) -> str:
    """
    从方法论数据生成格式化提示
    
    参数：
        data: 方法论数据字典
        
    返回：
        str: 格式化后的提示字符串
    """
    ret = """这是处理以往问题的标准方法论，如果当前任务类似，可以参考使用，如果不相关，请忽略：\n""" 
    for key, value in data.items():
        ret += f"问题: {key}\n方法论: {value}\n"
    return ret

def load_methodology(user_input: str) -> str:
    """
    加载方法论并构建向量索引以进行相似性搜索。
    
    参数：
        user_input: 要搜索方法论的输入文本
        
    返回：
        str: 相关的方法论提示，如果未找到方法论则返回空字符串
    """
    from yaspin import yaspin
    user_jarvis_methodology = os.path.expanduser("~/.jarvis/methodology")
    if not os.path.exists(user_jarvis_methodology):
        return ""
    
    try:
        with yaspin(text="加载方法论文件...", color="yellow") as spinner:
            with open(user_jarvis_methodology, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if dont_use_local_model():
                spinner.text = "加载方法论文件完成"
                spinner.ok("✅")
                return make_methodology_prompt(data)
        
        with yaspin(text="初始化数据结构...", color="yellow") as spinner:
            methodology_data: List[Dict[str, str]] = []
            vectors: List[np.ndarray] = []
            ids: List[int] = []
            spinner.text = "初始化数据结构完成"
            spinner.ok("✅")
            
            with yaspin(text="加载嵌入模型...", color="yellow") as spinner:
                embedding_model = load_embedding_model()
                spinner.text = "加载嵌入模型完成"
                spinner.ok("✅")
            
            with yaspin(text="创建测试嵌入...", color="yellow") as spinner:
                test_embedding = _create_methodology_embedding(embedding_model, "test")
                embedding_dimension = len(test_embedding)
                spinner.text = "创建测试嵌入完成"
                spinner.ok("✅")
            
            with yaspin(text="处理方法论数据...", color="yellow") as spinner:
                for i, (key, value) in enumerate(data.items()):
                    methodology_text = f"{key}\n{value}"
                    embedding = _create_methodology_embedding(embedding_model, methodology_text)
                    vectors.append(embedding)
                    ids.append(i)
                    methodology_data.append({"key": key, "value": value})
                spinner.text = "处理方法论数据完成"
                spinner.ok("✅")
            
            if vectors:
                with yaspin(text="构建索引...", color="yellow") as spinner:
                    vectors_array = np.vstack(vectors)
                    hnsw_index = faiss.IndexHNSWFlat(embedding_dimension, 16)
                    hnsw_index.hnsw.efConstruction = 40
                    hnsw_index.hnsw.efSearch = 16
                    methodology_index = faiss.IndexIDMap(hnsw_index)
                    methodology_index.add_with_ids(vectors_array, np.array(ids)) # type: ignore
                    spinner.text = "构建索引完成"
                    spinner.ok("✅")
                
                with yaspin(text="执行搜索...", color="yellow") as spinner:
                    query_embedding = _create_methodology_embedding(embedding_model, user_input)
                    k = min(3, len(methodology_data))
                    distances, indices = methodology_index.search(
                        query_embedding.reshape(1, -1), k
                    ) # type: ignore
                    spinner.text = "执行搜索完成"
                    spinner.ok("✅")
                
                with yaspin(text="处理搜索结果...", color="yellow") as spinner:
                    relevant_methodologies = {}
                    for dist, idx in zip(distances[0], indices[0]):
                        if idx >= 0:
                            similarity = 1.0 / (1.0 + float(dist))
                            methodology = methodology_data[idx]
                            if similarity >= 0.5:
                                relevant_methodologies[methodology["key"]] = methodology["value"]
                    spinner.text = "处理搜索结果完成"
                    spinner.ok("✅")

                
                if relevant_methodologies:
                    return make_methodology_prompt(relevant_methodologies)
            return make_methodology_prompt(data)
    except Exception as e:
        return ""
