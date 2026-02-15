from core.node import Node
from turtle import Turtle
from core.serializer import register_node
@register_node
class turtle_begin_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self._turtle_out = self.add_output_socket("turtle_out", Turtle)
        self._t = Turtle()

    def execute(self):
        print(f"Executing {self.name}...")
        self._turtle_out.write(self._t)
