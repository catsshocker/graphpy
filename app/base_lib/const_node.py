from core.node import Node

class const_node(Node):
    def __init__(self, name, value):
        super().__init__(name)
        self.out = self.add_output_socket("Value", type(value))
        self.out.write(value) # 初始化時就存入數值