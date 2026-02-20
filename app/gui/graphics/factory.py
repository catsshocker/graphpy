from .node_item import NodeUI
class NodeFactory:
    @staticmethod
    def spawn_node(node_class,scene,group,position=(0,0)):
        new_node = node_class()
        new_node.group = group # 把 group 傳給 node，讓它能操作群組資料結構，例如建立連線時更新群組的 links 列表
        # print(new_node.name)
        ui_object = NodeUI(new_node)
        ui_object.setPos(*position)
        scene.addItem(ui_object)
        group.add_node(new_node)
        