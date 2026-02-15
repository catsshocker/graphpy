from core.node import Node
from core.serializer import register_node
from turtle import Turtle

@register_node
class turtle_forward_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self._turtle_in = self.add_input_socket("turtle_in", Turtle)
        self._distance = self.add_input_socket("distance", int)
        self._turtle_out = self.add_output_socket("turtle_out", Turtle)

    def execute(self):
        print(f"Executing {self.name}...")
        print(f"turtle_in: {self._turtle_in.read()}, distance: {self._distance.read()}")
        turtle = self._turtle_in.read()
        distance = distance = self._distance.read()
        if turtle is not None and distance is not None:
            turtle.forward(distance)
            self._turtle_out.write(turtle)