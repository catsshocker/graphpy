from .node_item import NodeUI
class NodeFactory:
    @staticmethod
    def spawn_node(node_class,scene,group,position=(0,0)):
        new_node = node_class()
        # print(new_node.name)
        ui_object = NodeUI(new_node)
        ui_object.setPos(*position)
        scene.addItem(ui_object)
        group.add_node(new_node)
        