import core
from base_lib import *

if __name__ == "__main__":
    G = core.NodesGroup()
    const1 = G.add_node(const_node("const1", 100))
    const2 = G.add_node(const_node("const2", 90))
    const3 = G.add_node(const_node("const3", 1))
    const4 = G.add_node(const_node("const4", 5))

    turtle_begin =  G.add_node(turtle_begin_node("turtle_begin"))
    turtle_forward1 = G.add_node(turtle_forward_node("turtle_forward1"))
    turtle_turn = G.add_node(turtle_turn_node("turtle_turn"))
    turtle_forward2 = G.add_node(turtle_forward_node("turtle_forward2"))
    turtle_done = G.add_node(turtle_done_node("turtle_done"))
    G.add_link(const1.out, turtle_forward1.distance)
    G.add_link(const2.out, turtle_turn.angle)
    G.add_link(const1.out, turtle_forward2.distance)

    G.add_link(turtle_begin.turtle_out, turtle_forward1.turtle_in)
    G.add_link(turtle_forward1.turtle_out, turtle_turn.turtle_in)
    G.add_link(turtle_turn.turtle_out, turtle_forward2.turtle_in)
    G.add_link(turtle_forward2.turtle_out, turtle_done.turtle_in)

    G.execute()
    # G._test_async_execute()
