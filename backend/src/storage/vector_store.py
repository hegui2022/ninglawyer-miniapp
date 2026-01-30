"""
向量存储管理
"""
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import os


class VectorStore:
    """向量存储类"""
    
    def __init__(self):
        self.host = os.getenv('MILVUS_HOST', 'localhost')
        self.port = int(os.getenv('MILVUS_PORT', 19530))
        self.collection_name = os.getenv('MILVUS_COLLECTION', 'law_knowledge')
        
        # 连接到 Milvus
        connections.connect(host=self.host, port=self.port)
        
        # 创建或获取集合
        self._init_collection()
    
    def _init_collection(self):
        """初始化集合"""
        # 定义字段
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]
        
        schema = CollectionSchema(fields, description="法律知识库")
        
        # 创建集合
        try:
            self.collection = Collection(self.collection_name, schema=schema)
            print(f"✓ 创建集合 {self.collection_name}")
        except Exception as e:
            # 集合已存在，直接获取
            self.collection = Collection(self.collection_name)
            print(f"✓ 获取集合 {self.collection_name}")
    
    def insert(self, content, embedding, metadata=None):
        """插入数据"""
        data = [[content], [embedding], [metadata or {}]]
        self.collection.insert(data)
        self.collection.flush()
        print(f"✓ 插入数据成功")
    
    def search(self, embedding, top_k=10):
        """搜索相似数据"""
        # 创建索引
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "IP",
            "params": {"nlist": 128}
        }
        self.collection.create_index("embedding", index_params)
        self.collection.load()
        
        # 搜索
        results = self.collection.search(
            data=[embedding],
            anns_field="embedding",
            param={"metric_type": "IP", "params": {"nprobe": 10}},
            limit=top_k
        )
        
        return results


def get_vector_store():
    """获取向量存储实例"""
    return VectorStore()
