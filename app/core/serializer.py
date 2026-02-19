import json
from .group import NodesGroup
from .registry import NodeRegistry


class GraphSerializer:
    """負責將 NodesGroup 轉為字典"""    
    @staticmethod
    def save_to_file(group, filename):
        """直接存成 JSON 檔案"""
        # 修正：這裡要呼叫上面定義的 serialize
        data = group._serialize() 
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"成功存檔至: {filename}")
        print(NodeRegistry.registry())
        # with open(filename+"nodes", 'w', encoding='utf-8') as f:
            # json.dump(NODE_REGISTRY, f, indent=4, ensure_ascii=False)


class GraphLoader:
    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        group = NodesGroup()
        group.uuid = data.get("group_uuid", group.uuid)
        for node_data in data["nodes"]:
            group.add_node(GraphLoader._deserialize_node(node_data))

        for link_data in data["links"]:
            from_node = group.nodes[link_data["node_from"]]
            to_node = group.nodes[link_data["node_to"]]
            from_socket = from_node.outputSockets[link_data["socket_from"]]
            to_socket = to_node.inputSockets[link_data["socket_to"]]
            group.add_link(from_socket, to_socket)
        
        return group

    @staticmethod
    def _deserialize_node(node_data):
        class_name = node_data["class"]
        node_cls = NodeRegistry.registry().get(class_name)
        if not node_cls:
            raise ValueError(f"未找到節點類別: {class_name}")
        node = node_cls(node_data["name"])
        node.uuid = node_data["uuid"]
        node.load_parm(node_data["param"])
        return node