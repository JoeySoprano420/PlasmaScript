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

class LLVMBackend:
    # … existing …

    def _declare_func(self, node):
        # dynamic arg count support
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
            ptr = self.builder.alloca(ir.IntType(32), name=node.params[i])
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
        # literals, binops, vars handled as before …
        if isinstance(expr, CallNode):
            args = [self._eval_expr(a) for a in expr.args]
            return self.builder.call(self.funcs[expr.name], args)

class LLVMBackend:
    def __init__(self, ast):
        self.ast = ast
        self.module = ir.Module(name="plasmascript")
        self.printf = None
        self.funcs = {}
        self.locals = {}
        self.builder = None

    def _declare_func(self, node):
        fnty = ir.FunctionType(ir.IntType(32), [ir.IntType(32)]*len(node.params))
        fn = ir.Function(self.module, fnty, name=node.name)
        if node.export: fn.attributes.add("dllexport")
        self.funcs[node.name] = fn
        return fn

    def _eval_expr(self, expr):
        # … literals, binops …
        if isinstance(expr, VarNode):
            if expr.name in self.locals:
                return self.builder.load(self.locals[expr.name], expr.name)
            elif expr.name in self.funcs:
                return self.funcs[expr.name]  # function pointer
        if isinstance(expr, CallNode):
            callee = self._eval_expr(expr.func)
            args = [self._eval_expr(a) for a in expr.args]
            return self.builder.call(callee, args)

class LLVMBackend:
    def _eval_expr(self, expr):
        if isinstance(expr, LambdaNode):
            # Step 1: declare anonymous function
            fnty = ir.FunctionType(ir.IntType(32), [ir.IntType(32)]*len(expr.params))
            fn = ir.Function(self.module, fnty, name=f"lambda_{id(expr)}")
            block = fn.append_basic_block("entry")
            builder = ir.IRBuilder(block)

            # Step 2: store captured vars
            captures = {}
            for i, name in enumerate(expr.captures):
                if name in self.locals:
                    captures[name] = self.locals[name]

            # Step 3: generate body
            local_map = {}
            for i, arg in enumerate(fn.args):
                ptr = builder.alloca(ir.IntType(32), name=expr.params[i])
                builder.store(arg, ptr)
                local_map[expr.params[i]] = ptr
            # simple return body
            for stmt in expr.body.children:
                if isinstance(stmt, ReturnNode):
                    val = self._eval_expr(stmt.expr)
                    builder.ret(val)
            if not block.is_terminated:
                builder.ret(ir.Constant(ir.IntType(32), 0))

            # Step 4: return fn pointer as closure (no heap object yet)
            return fn

