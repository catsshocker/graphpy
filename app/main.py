import core
from base_lib import *

if __name__ == "__main__":
    G = core.NodesGroup()
    const1 = G.add_node(const_node("const1", 2))
    const2 = G.add_node(const_node("const2", 4))
    const3 = G.add_node(const_node("const3", 1))
    const4 = G.add_node(const_node("const4", 5))

    add1 = G.add_node(add_node("add1"))
    add2 = G.add_node(add_node("add2"))
    add3 = G.add_node(add_node("add3"))
    mul = G.add_node(mul_node("mul"))

    G.add_link(const1.out, add1.a)
    G.add_link(const2.out, add1.b)

    G.add_link(add1.result, add2.a)
    G.add_link(add1.result, add2.b)

    G.add_link(const3.out, mul.a)
    G.add_link(const4.out, mul.b)

    G.add_link(add2.result, add3.a)
    G.add_link(mul.result, add3.b)

    # G.execute()
    G._test_async_execute()
    print("add3 Result:", add3.result.read())