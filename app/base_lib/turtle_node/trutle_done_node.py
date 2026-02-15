from core.node import Node
from turtle import done as Td,Turtle
from core.serializer import register_node
@register_node
class turtle_done_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self._turtle_in = self.add_input_socket("turtle_in", Turtle)

    def execute(self):
        Td()