from core.node import Node
from core.nodeSocket import SocketInputMode
class const_node(Node):
    def __init__(self, name = None, value = None):
        super().__init__(name)
        self.input = self.add_input_socket("Input", type(value), inputMode=SocketInputMode.KEYIN_ONLY)
        self._out = self.add_output_socket("Value", type(value))


    def execute(self):
        self._out.write(self.input.value)
    
    def serialize_parm(self):
        return {"value": self.input.value}
    
    def load_parm(self, parm_dict):
        self.input.value = parm_dict.get("value")