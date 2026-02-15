from core.node import Node

class add_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self.add_input_socket("a", int)
        self.add_input_socket("b", int)
        self.add_output_socket("result", int)

    def execute(self):
        a = self.inputSockets[0].read()
        b = self.inputSockets[1].read()
        if a is not None and b is not None:
            result = a + b
            self.outputSockets[0].write(result)