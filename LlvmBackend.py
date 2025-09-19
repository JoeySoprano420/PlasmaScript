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

class LLVMBackend:
    def __init__(self, ast):
        self.ast = ast
        self.module = ir.Module(name="plasmascript")
        self.printf = None
        self.funcs = {}
        self.builder = None
        self.locals = {}

    def build(self):
        self._declare_printf()
        for node in self.ast:
            if isinstance(node, FuncNode):
                self._declare_func(node)
        for node in self.ast:
            if isinstance(node, FuncNode):
                self._define_func(node)
        return str(self.module)

    def _declare_printf(self):
        ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        self.printf = ir.Function(self.module, ty, name="printf")

    def _declare_func(self, node):
        fnty = ir.FunctionType(ir.IntType(32), [ir.IntType(32)]*len(node.params))
        fn = ir.Function(self.module, fnty, name=node.name)
        if node.export: fn.attributes.add("dllexport")
        self.funcs[node.name] = fn

    def _define_func(self, node):
        fn = self.funcs[node.name]
        block = fn.append_basic_block("entry")
        self.builder = ir.IRBuilder(block)
        self.locals = {}
        for i, arg in enumerate(fn.args):
            ptr = self.builder.alloca(ir.IntType(32), name=node.params[i] if i < len(node.params) else f"arg{i}")
            self.builder.store(arg, ptr)
            self.locals[node.params[i]] = ptr
        for stmt in node.body.children:
            if isinstance(stmt, ReturnNode):
                val = self._eval_expr(stmt.expr)
                self.builder.ret(val)
            elif isinstance(stmt, PrintNode):
                self._print(stmt.expr)
        if not block.is_terminated:
            self.builder.ret(ir.Constant(ir.IntType(32), 0))

    def _eval_expr(self, expr):
        if isinstance(expr, CallNode):
            args = [self._eval_expr(a) for a in expr.args]
            return self.builder.call(self.funcs[expr.name], args)
        # … (reuse number/string/binop handling from earlier) …

