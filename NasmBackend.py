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
