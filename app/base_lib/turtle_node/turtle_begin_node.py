from core.node import Node
from turtle import Turtle

class turtle_begin_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self.turtle_out = self.add_output_socket("Turtle", Turtle)
        self.t = Turtle()

    def execute(self):
        print(f"Executing {self.name}...")
        self.turtle_out.write(self.t)
