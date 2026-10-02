from core.node import Node #引入基本節點物件定義
class mod_node(Node):
    def __init__(self, name=None):
        super().__init__(name)
        self._a = self.add_input_socket("a", int)  #新增輸入端口a，資料類型為int
        self._b = self.add_input_socket("b", int)  #新增輸入端口b，資料類型為int
        self._result = self.add_output_socket("result", int)  #新增輸出端口result，資料類型為int

    def execute(self):
        print(f"Executing {self.name}...")
        a = self._a.read()                      #從輸入端口a讀取資料
        b = self._b.read()                      #從輸入端口b讀取資料
        print(f"Read inputs: a={a}, b={b}")
        if a is not None and b is not None:
            r = a % b
            self._result.write(r)               #將計算結果寫入輸出端口result
            print(f"Wrote result: {r}")