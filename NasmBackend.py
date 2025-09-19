class NASMBackend:
    def __init__(self, ast):
        self.ast = ast
        self.data = []
        self.text = []
        self.externs = set(["printf"])
        self.locals = {}

    def _eval_expr(self, expr):
        if isinstance(expr, NumberNode):
            self.text.append(f"    mov eax, {expr.value}")
        elif isinstance(expr, StringNode):
            label = f"str{len(self.data)}"
            self.data.append(f'{label} db "{expr.value}", 0')
            self.text.append(f"    lea rcx, [rel {label}]")
        elif isinstance(expr, BinOpNode):
            self._eval_expr(expr.left)
            self.text.append("    push rax")
            self._eval_expr(expr.right)
            self.text.append("    mov rbx, rax")
            self.text.append("    pop rax")
            if expr.op == "+": self.text.append("    add eax, ebx")
            if expr.op == "-": self.text.append("    sub eax, ebx")
            if expr.op == "*": self.text.append("    imul eax, ebx")
            if expr.op == "/":
                self.text.append("    cdq")
                self.text.append("    idiv ebx")

class NASMBackend:
    def __init__(self, ast):
        self.ast = ast
        self.data, self.text = [], []
        self.externs, self.globals = set(["printf"]), set()
        self.funcs = {}

    def build(self):
        for node in self.ast:
            if isinstance(node, FuncNode):
                self._declare_func(node)
        for node in self.ast:
            if isinstance(node, FuncNode):
                self._define_func(node)
        return self._generate()

    def _declare_func(self, node):
        self.globals.add(node.name)

    def _define_func(self, node):
        self.text.append(f"{node.name}:")
        for stmt in node.body.children:
            if isinstance(stmt, ReturnNode):
                self._eval_expr(stmt.expr)
                self.text.append("    ret")
            elif isinstance(stmt, PrintNode):
                self._eval_expr(stmt.expr)
                self.text.append("    ; print logic here…")
        self.text.append("    xor eax, eax")
        self.text.append("    ret")

    def _eval_expr(self, expr):
        if isinstance(expr, CallNode):
            for arg in reversed(expr.args):  # push args
                self._eval_expr(arg)
                self.text.append("    push rax")
            self.text.append(f"    call {expr.name}")
            self.text.append(f"    add rsp, {len(expr.args)*8}")
        elif isinstance(expr, NumberNode):
            self.text.append(f"    mov eax, {expr.value}")

