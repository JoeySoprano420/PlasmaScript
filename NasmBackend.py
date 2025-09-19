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

class NASMBackend:
    # … existing …

    def _eval_expr(self, expr):
        if isinstance(expr, CallNode):
            # Evaluate args right-to-left (x64 Windows ABI)
            for arg in reversed(expr.args):
                self._eval_expr(arg)
                self.text.append("    push rax")
            self.text.append(f"    call {expr.name}")
            self.text.append(f"    add rsp, {len(expr.args)*8}")
        elif isinstance(expr, NumberNode):
            self.text.append(f"    mov eax, {expr.value}")
        elif isinstance(expr, BinOpNode):
            self._eval_expr(expr.left)
            self.text.append("    push rax")
            self._eval_expr(expr.right)
            self.text.append("    mov rbx, rax")
            self.text.append("    pop rax")
            if expr.op == "+": self.text.append("    add eax, ebx")
            elif expr.op == "-": self.text.append("    sub eax, ebx")
            elif expr.op == "*": self.text.append("    imul eax, ebx")
            elif expr.op == "/":
                self.text.append("    cdq")
                self.text.append("    idiv ebx")

class NASMBackend:
    def _eval_expr(self, expr):
        if isinstance(expr, VarNode):
            if expr.name in self.funcs:
                self.text.append(f"    mov rax, {expr.name}")  # function address
        elif isinstance(expr, CallNode):
            self._eval_expr(expr.func)  # put callee address in RAX
            self.text.append("    push rax")  # save
            for arg in reversed(expr.args):
                self._eval_expr(arg)
                self.text.append("    push rax")
            self.text.append("    pop rax")   # restore func addr into RAX
            self.text.append("    call rax")  # indirect call
            self.text.append(f"    add rsp, {len(expr.args)*8}")

class NASMBackend:
    def _eval_expr(self, expr):
        if isinstance(expr, LambdaNode):
            # emit an anonymous function
            label = f"lambda_{id(expr)}"
            self.globals.add(label)
            self.text.append(f"{label}:")
            for stmt in expr.body.children:
                if isinstance(stmt, ReturnNode):
                    self._eval_expr(stmt.expr)
                    self.text.append("    ret")
            return label

; closure layout [fn_addr][captured1][captured2]...
; RAX = closure object ptr

    mov rcx, <size>
    call malloc
    mov [rax], <fn_addr>
    mov [rax+8], <capture1>
    mov [rax+12], <capture2>

    mov rbx, [rax]    ; fn_addr
    lea rcx, [rax+8]  ; env pointer
    call rbx

class NASMBackend:
    def _eval_expr(self, expr):
        if isinstance(expr, MallocNode):
            self.text.append("    mov rcx, <size_reg>")
            self.text.append("    call malloc")
        elif isinstance(expr, FreeNode):
            self.text.append("    mov rcx, rax  ; ptr to free")
            self.text.append("    call free")
        elif isinstance(expr, StoreNode):
            # assume rax=ptr, rbx=offset, rcx=value
            self.text.append("    mov [rax+rbx], ecx")
        elif isinstance(expr, LoadNode):
            # assume rax=ptr, rbx=offset
            self.text.append("    mov eax, [rax+rbx]")

