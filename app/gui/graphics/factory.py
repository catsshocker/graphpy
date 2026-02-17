from .node_item import NodeUI
class NodeFactory:
    @staticmethod
    def spawn_node(node_class,scene,group):
        new_node = node_class()
        # print(new_node.name)
        ui_object = NodeUI(new_node)
        scene.addItem(ui_object)
        group.add_node(new_node)
        