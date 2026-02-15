from core.node import Node

class mul_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self.a = self.add_input_socket("a", int)
        self.b = self.add_input_socket("b", int)
        self.result = self.add_output_socket("result", int)

    def execute(self):
        print(f"Executing {self.name}...")
        a = self.a.read()
        b = self.b.read()
        print(f"Read inputs: a={a}, b={b}")
        if a is not None and b is not None:
            r = a * b
            self.result.write(r)
            print(f"Wrote result: {r}")