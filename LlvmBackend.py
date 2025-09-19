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

class LLVMBackend:
    def __init__(self, ast):
        self.ast = ast
        self.module = ir.Module(name="plasmascript")
        self.printf = None
        self.funcs = {}
        self.locals = {}
        self.malloc = None

    def _declare_runtime(self):
        self.printf_ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        self.printf = ir.Function(self.module, self.printf_ty, name="printf")
        malloc_ty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(64)])
        self.malloc = ir.Function(self.module, malloc_ty, name="malloc")

    def _make_closure(self, fn, captured):
        # struct { fn_ptr, env_ptr }
        env_size = 4 * len(captured)  # assume i32 per capture
        env_ptr = self.builder.call(self.malloc, [ir.Constant(ir.IntType(64), env_size)])
        # store captures into env
        for i, (name, ptr) in enumerate(captured.items()):
            val = self.builder.load(ptr)
            gep = self.builder.gep(env_ptr, [ir.Constant(ir.IntType(32), i*4)])
            self.builder.store(val, gep)
        # pack closure {fn, env_ptr}
        closure_ty = ir.LiteralStructType([fn.type, env_ptr.type])
        closure = self.builder.alloca(closure_ty)
        fnptr = self.builder.bitcast(fn, fn.type)
        self.builder.store(fnptr, self.builder.gep(closure, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)]))
        self.builder.store(env_ptr, self.builder.gep(closure, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 1)]))
        return closure

class LLVMBackend:
    def _declare_runtime(self):
        # malloc/free
        malloc_ty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(64)])
        self.malloc = ir.Function(self.module, malloc_ty, name="malloc")
        free_ty = ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer()])
        self.free = ir.Function(self.module, free_ty, name="free")

    def _eval_expr(self, expr):
        if isinstance(expr, MallocNode):
            size = self._eval_expr(expr.size)
            return self.builder.call(self.malloc, [self.builder.sext(size, ir.IntType(64))])
        elif isinstance(expr, FreeNode):
            ptr = self._eval_expr(expr.ptr)
            self.builder.call(self.free, [ptr])
            return ir.Constant(ir.IntType(32), 0)
        elif isinstance(expr, StoreNode):
            ptr = self._eval_expr(expr.ptr)
            offset = self._eval_expr(expr.offset)
            addr = self.builder.gep(ptr, [offset])
            val = self._eval_expr(expr.value)
            self.builder.store(val, addr)
            return ir.Constant(ir.IntType(32), 0)
        elif isinstance(expr, LoadNode):
            ptr = self._eval_expr(expr.ptr)
            offset = self._eval_expr(expr.offset)
            addr = self.builder.gep(ptr, [offset])
            return self.builder.load(addr)

class LLVMBackend:
    def _declare_memory_lib(self):
        # malloc/free
        malloc_ty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(64)])
        self.malloc = ir.Function(self.module, malloc_ty, name="malloc")
        free_ty = ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer()])
        self.free = ir.Function(self.module, free_ty, name="free")

    def _eval_expr(self, expr):
        # Arena
        if isinstance(expr, ArenaInitNode):
            size = self._eval_expr(expr.size)
            return self.builder.call(self.malloc, [self.builder.sext(size, ir.IntType(64))])
        if isinstance(expr, ArenaResetNode):
            ptr = self._eval_expr(expr.ptr)
            self.builder.call(self.free, [ptr])
            return ir.Constant(ir.IntType(32), 0)
        # Refcounted objects
        if isinstance(expr, RcAllocNode):
            size = self._eval_expr(expr.size)
            raw = self.builder.call(self.malloc, [self.builder.sext(size, ir.IntType(64))])
            # prepend 4-byte refcount
            return raw
        if isinstance(expr, RetainNode):
            ptr = self._eval_expr(expr.ptr)
            # increment [ptr-4]
            return ir.Constant(ir.IntType(32), 0)
        if isinstance(expr, ReleaseNode):
            ptr = self._eval_expr(expr.ptr)
            # decrement [ptr-4], free if 0
            return ir.Constant(ir.IntType(32), 0)

