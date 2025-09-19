class LLVMBackend:
    def __init__(self, ast):
        self.ast = ast
        self.module = ir.Module(name="plasmascript")
        self.module.triple = llvm.get_default_triple()
        self.printf = None
        self.imports = set()
        self.builder = None
        self.func = None
        self.locals = {}  # variable map

    def _eval_expr(self, expr):
        if isinstance(expr, NumberNode):
            return ir.Constant(ir.IntType(32), expr.value)
        elif isinstance(expr, StringNode):
            s = expr.value + "\0"
            cstr = ir.Constant(ir.ArrayType(ir.IntType(8), len(s)), bytearray(s.encode("utf8")))
            gv = ir.GlobalVariable(self.module, cstr.type, name=f"str{len(self.locals)}")
            gv.linkage = 'internal'; gv.global_constant = True; gv.initializer = cstr
            return self.builder.bitcast(gv, ir.IntType(8).as_pointer())
        elif isinstance(expr, VarNode):
            return self.builder.load(self.locals[expr.name], name=expr.name)
        elif isinstance(expr, BinOpNode):
            l = self._eval_expr(expr.left)
            r = self._eval_expr(expr.right)
            if expr.op == "+": return self.builder.add(l, r)
            if expr.op == "-": return self.builder.sub(l, r)
            if expr.op == "*": return self.builder.mul(l, r)
            if expr.op == "/": return self.builder.sdiv(l, r)
        else:
            raise NotImplementedError(expr)

    def _print(self, expr):
        val = self._eval_expr(expr)
        if val.type.is_pointer:   # string
            self.builder.call(self.printf, [val])
        else:  # number
            fmt = "%d\n\0"
            cstr = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
            gv = ir.GlobalVariable(self.module, cstr.type, name="fmt")
            gv.linkage = 'internal'; gv.global_constant = True; gv.initializer = cstr
            ptr = self.builder.bitcast(gv, ir.IntType(8).as_pointer())
            self.builder.call(self.printf, [ptr, val])
