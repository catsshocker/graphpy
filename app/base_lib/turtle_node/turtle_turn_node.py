from core.node import Node
from turtle import Turtle


class turtle_turn_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self.turtle_in = self.add_input_socket("turtle_in", Turtle)
        self.angle = self.add_input_socket("angle", float)
        self.turtle_out = self.add_output_socket("turtle_out", Turtle)

    def execute(self):
        print(f"Executing {self.name}...")
        print(f"turtle_in: {self.turtle_in.read()}, angle: {self.angle.read()}")
        turtle = self.turtle_in.read()
        angle = self.angle.read()
        if turtle is not None and angle is not None:
            turtle.left(angle)
            self.turtle_out.write(turtle)