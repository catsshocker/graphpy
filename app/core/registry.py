#core.registry.py

class NodeRegistry:
    _registry = {}

    @classmethod
    def register(cls, node_class):
        node_name = node_class.__name__
        print(f"註冊節點類別: {node_name} ({node_class.__module__}.{node_class.__name__})")
    
        if node_name in cls._registry:
            # 取得已存在類別的路徑，方便除錯
            existing_cls = cls._registry[node_name]
            raise RuntimeError(
                f"❌ 節點名稱衝突！'{node_name}' 已經被註冊過。\n"
                f"已有類別：{existing_cls.__module__}.{existing_cls.__name__}\n"
                f"當前類別：{cls.__module__}.{cls.__name__}\n"
                f"請確保節點類別名稱是唯一的。"
            )
        cls._registry[node_class.__name__] = node_class

    @classmethod
    def registry(cls):
        return cls._registry
