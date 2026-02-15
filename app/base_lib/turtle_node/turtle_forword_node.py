from core.node import Node
from turtle import Turtle


class turtle_forward_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self.turtle_in = self.add_input_socket("turtle_in", Turtle)
        self.distance = self.add_input_socket("distance", int)
        self.turtle_out = self.add_output_socket("turtle_out", Turtle)

    def execute(self):
        print(f"Executing {self.name}...")
        print(f"turtle_in: {self.turtle_in.read()}, distance: {self.distance.read()}")
        turtle = self.turtle_in.read()
        distance = distance = self.distance.read()
        if turtle is not None and distance is not None:
            turtle.forward(distance)
            self.turtle_out.write(turtle)