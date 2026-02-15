import core
from base_lib import *

if __name__ == "__main__":
    G = core.NodesGroup()
    const1 = G.add_node(const_node("const1", 10))
    const2 = G.add_node(const_node("const2", 20))
    add = G.add_node(add_node("add"))
    G.add_link(const1.out, add.inputSockets[0])
    G.add_link(const2.out, add.inputSockets[1])
    

    const3 = G.add_node(const_node("const3", 5))
    add2 = G.add_node(add_node("add2"))
    G.add_link(add.outputSockets[0], add2.inputSockets[0])
    G.add_link(const3.out, add2.inputSockets[1])

    G.execute()
    print("Result:", add2.outputSockets[0].read())