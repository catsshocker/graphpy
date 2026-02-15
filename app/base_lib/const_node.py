from core.node import Node
from core.serializer import register_node
@register_node
class const_node(Node):
    def __init__(self, name, value = None):
        super().__init__(name)
        self._out = self.add_output_socket("Value", type(value))
        self._value = value

    def execute(self):
        self._out.write(self._value)
    
    def serialize_parm(self):
        return {"value": self._value}
    
    def load_parm(self, parm_dict):
        self._value = parm_dict.get("value")