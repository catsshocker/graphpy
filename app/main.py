import core
from base_lib import *
from core.serializer import GraphSerializer, GraphLoader

if __name__ == "__main__":
    # G = core.NodesGroup()
    # const1 = G.add_node(const_node("const1", 100))
    # const2 = G.add_node(const_node("const2", 90))
    # const3 = G.add_node(const_node("const3", 1))
    # const4 = G.add_node(const_node("const4", 5))

    # turtle_begin =  G.add_node(turtle_begin_node("turtle_begin"))
    # turtle_forward1 = G.add_node(turtle_forward_node("turtle_forward1"))
    # turtle_turn = G.add_node(turtle_turn_node("turtle_turn"))
    # turtle_forward2 = G.add_node(turtle_forward_node("turtle_forward2"))
    # turtle_done = G.add_node(turtle_done_node("turtle_done"))
    
    # G.add_link(const1.outputSockets["Value"], turtle_forward1.inputSockets["distance"])
    # G.add_link(const2.outputSockets["Value"], turtle_turn.inputSockets["angle"])
    # G.add_link(const1.outputSockets["Value"], turtle_forward2.inputSockets["distance"])

    # G.add_link(turtle_begin.outputSockets["turtle_out"], turtle_forward1.inputSockets["turtle_in"])
    # G.add_link(turtle_forward1.outputSockets["turtle_out"], turtle_turn.inputSockets["turtle_in"])
    # G.add_link(turtle_turn.outputSockets["turtle_out"], turtle_forward2.inputSockets["turtle_in"])
    # G.add_link(turtle_forward2.outputSockets["turtle_out"], turtle_done.inputSockets["turtle_in"])

    G = GraphLoader.load_from_file("000.json")
    G.execute()
    print(G._serialize())
    # GraphSerializer.save_to_file(G,"000.json")
    # G._test_async_execute()
