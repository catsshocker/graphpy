from core.node import Node

class print_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self._input = self.add_input_socket("input", int)

    def execute(self):
        print(f"Executing {self.name}...")
        input_value = self._input.read()
        print(f"Read input: {input_value}")