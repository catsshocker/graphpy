from core.node import Node
from core.serializer import register_node
@register_node
class mul_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self._a = self.add_input_socket("a", int)
        self._b = self.add_input_socket("b", int)
        self._result = self.add_output_socket("result", int)

    def execute(self):
        print(f"Executing {self.name}...")
        a = self._a.read()
        b = self._b.read()
        print(f"Read inputs: a={a}, b={b}")
        if a is not None and b is not None:
            r = a * b
            self._result.write(r)
            print(f"Wrote result: {r}")