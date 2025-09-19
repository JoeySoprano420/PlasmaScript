# plasma_vm_lists.py
# PlasmaScript VECE with Lists + map, filter, forEach
# Author: Violet + ChatGPT
# License: MIT

from lark import Lark, Transformer

# -------------------------
# 1. Grammar
# -------------------------
plasma_grammar = r"""
?start: program
?program: (statement)+

?statement: comment
          | var_decl
          | print_stmt
          | func_def
          | lambda_def
          | if_stmt
          | for_stmt
          | return_stmt
          | end_stmt
          | expr

comment: ";" /[^\n]/*

var_decl: "let" NAME "=" expr
print_stmt: "Print" "[" expr "]"

func_def: ("Prog"|"Main"|"Func") NAME? "(" [params] ")" block
lambda_def: "Func" "(" [params] ")" block   -> lambda_expr

params: NAME ("," NAME)*

return_stmt: "return" expr
if_stmt: "if" expr block ("else" block)?
for_stmt: "for" NAME "in" expr block
end_stmt: "end" | "run"

block: "{" statement* "}"

?expr: atom
     | expr OP expr   -> binop
     | "-" expr       -> neg
     | func_call
     | lambda_def     -> lambda_expr

func_call: NAME "(" [args] ")"
args: expr ("," expr)*

?atom: NUMBER        -> number
     | STRING        -> string
     | NAME          -> var
     | list_lit
     | "true"        -> true
     | "false"       -> false

list_lit: "[" [args] "]"

OP: "==" | "!=" | "<" | ">" | "<=" | ">=" | "+" | "-" | "*" | "/" | "%"

NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
STRING: ESCAPED_STRING
NUMBER: /\d+/

%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

# -------------------------
# 2. Bytecode Instructions
# -------------------------
class OpCode:
    LOAD_CONST   = "LOAD_CONST"
    LOAD_VAR     = "LOAD_VAR"
    STORE_VAR    = "STORE_VAR"
    BINARY_OP    = "BINARY_OP"
    PRINT        = "PRINT"
    FUNC_DEF     = "FUNC_DEF"
    CALL_FUNC    = "CALL_FUNC"
    RETURN       = "RETURN"
    END          = "END"

# -------------------------
# 3. Function Object
# -------------------------
class Function:
    def __init__(self, name, params, block, env, native=False, native_impl=None):
        self.name = name or "<lambda>"
        self.params = params
        self.block = block
        self.env = env
        self.native = native
        self.native_impl = native_impl

    def __repr__(self):
        return f"<Func {self.name}({','.join(self.params)}){' [native]' if self.native else ''}>"

# -------------------------
# 4. Compiler
# -------------------------
class Compiler(Transformer):
    def __init__(self):
        super().__init__()
        self.bytecode = []
        self.consts = []

    def add_const(self, value):
        if value not in self.consts:
            self.consts.append(value)
        return self.consts.index(value)

    def number(self, items):
        idx = self.add_const(int(items[0]))
        return (OpCode.LOAD_CONST, idx)

    def string(self, items):
        idx = self.add_const(str(items[0][1:-1]))
        return (OpCode.LOAD_CONST, idx)

    def true(self, _):
        idx = self.add_const(True)
        return (OpCode.LOAD_CONST, idx)

    def false(self, _):
        idx = self.add_const(False)
        return (OpCode.LOAD_CONST, idx)

    def var(self, items):
        return (OpCode.LOAD_VAR, str(items[0]))

    def var_decl(self, items):
        name, expr = str(items[0]), items[1]
        self.bytecode.append(expr)
        self.bytecode.append((OpCode.STORE_VAR, name))

    def print_stmt(self, items):
        self.bytecode.append(items[0])
        self.bytecode.append((OpCode.PRINT, None))

    def binop(self, items):
        a, op, b = items[0], items[1], items[2]
        self.bytecode.append(a)
        self.bytecode.append(b)
        self.bytecode.append((OpCode.BINARY_OP, op.value))

    def func_def(self, items):
        keyword = items[0]
        if keyword in ("Prog", "Main"):
            name = "main"
            params = []
            block = items[-1]
        else:
            name = str(items[1])
            params = [str(p) for p in items[2].children] if len(items) > 2 and hasattr(items[2], "children") else []
            block = items[-1]
        self.bytecode.append((OpCode.FUNC_DEF, (name, params, block)))

    def lambda_expr(self, items):
        params = [str(p) for p in items[0].children] if items and hasattr(items[0], "children") else []
        block = items[-1]
        self.bytecode.append((OpCode.FUNC_DEF, (None, params, block)))
        return None

    def func_call(self, items):
        name = str(items[0])
        args = items[1:] if len(items) > 1 else []
        for arg in args[0] if args else []:
            self.bytecode.append(arg)
        self.bytecode.append((OpCode.CALL_FUNC, (name, len(args[0]) if args else 0)))
        return None

    def return_stmt(self, items):
        self.bytecode.append(items[0])
        self.bytecode.append((OpCode.RETURN, None))

    def end_stmt(self, _):
        self.bytecode.append((OpCode.END, None))

# -------------------------
# 5. Virtual Machine
# -------------------------
class Frame:
    def __init__(self, return_ip, locals, closure_env):
        self.return_ip = return_ip
        self.locals = locals
        self.closure_env = closure_env

class PlasmaVM:
    def __init__(self, consts, bytecode):
        self.consts = consts
        self.bytecode = bytecode
        self.stack = []
        self.ip = 0
        self.funcs = {}
        self.call_stack = []
        self.globals = {}

        # install native higher-order functions
        self.funcs["map"] = Function("map", ["lst", "fn"], None, {}, native=True, native_impl=self._native_map)
        self.funcs["filter"] = Function("filter", ["lst", "fn"], None, {}, native=True, native_impl=self._native_filter)
        self.funcs["forEach"] = Function("forEach", ["lst", "fn"], None, {}, native=True, native_impl=self._native_foreach)

    def run(self):
        while self.ip < len(self.bytecode):
            instr = self.bytecode[self.ip]
            self.ip += 1
            if isinstance(instr, tuple):
                op, arg = instr
                if op == OpCode.LOAD_CONST:
                    self.stack.append(self.consts[arg])
                elif op == OpCode.LOAD_VAR:
                    val = None
                    if self.call_stack and arg in self.call_stack[-1].locals:
                        val = self.call_stack[-1].locals[arg]
                    elif self.call_stack and arg in self.call_stack[-1].closure_env:
                        val = self.call_stack[-1].closure_env[arg]
                    else:
                        val = self.globals.get(arg, None)
                    self.stack.append(val)
                elif op == OpCode.STORE_VAR:
                    val = self.stack.pop()
                    if self.call_stack:
                        self.call_stack[-1].locals[arg] = val
                    else:
                        self.globals[arg] = val
                elif op == OpCode.PRINT:
                    val = self.stack.pop()
                    print(val)
                elif op == OpCode.BINARY_OP:
                    b = self.stack.pop(); a = self.stack.pop()
                    self.stack.append(self._binop(a, b, arg))
                elif op == OpCode.FUNC_DEF:
                    name, params, block = arg
                    closure_env = dict(self.globals)
                    if self.call_stack:
                        closure_env.update(self.call_stack[-1].locals)
                        closure_env.update(self.call_stack[-1].closure_env)
                    func_obj = Function(name, params, block, closure_env)
                    if name:
                        self.funcs[name] = func_obj
                    self.stack.append(func_obj)
                elif op == OpCode.CALL_FUNC:
                    name, argc = arg
                    fn = None
                    if isinstance(name, str) and name in self.funcs:
                        fn = self.funcs[name]
                    elif self.stack and isinstance(self.stack[-1], Function):
                        fn = self.stack.pop()
                    if not fn:
                        raise Exception(f"Undefined function: {name}")
                    args = [self.stack.pop() for _ in range(argc)][::-1]
                    if fn.native:
                        res = fn.native_impl(*args)
                        self.stack.append(res)
                    else:
                        if len(args) != len(fn.params):
                            raise Exception(f"Function {fn.name} expected {len(fn.params)} args, got {len(args)}")
                        locals = dict(zip(fn.params, args))
                        self.call_stack.append(Frame(self.ip, locals, fn.env))
                        self.ip = self.bytecode.index(fn.block) + 1
                elif op == OpCode.RETURN:
                    ret_val = self.stack.pop() if self.stack else None
                    frame = self.call_stack.pop()
                    self.ip = frame.return_ip
                    self.stack.append(ret_val)
                elif op == OpCode.END:
                    print("Program finished.")
                    return
                else:
                    raise Exception(f"Unknown opcode: {op}")
            else:
                self.stack.append(instr)

    def _binop(self, a, b, op):
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/": return a / b
        if op == "%": return a % b
        if op == "==": return a == b
        if op == "!=": return a != b
        if op == "<": return a < b
        if op == ">": return a > b
        if op == "<=": return a <= b
        if op == ">=": return a >= b
        raise Exception(f"Unsupported op {op}")

    # -------------------------
    # Native Higher-Order Functions
    # -------------------------
    def _native_map(self, lst, fn):
        return [self._apply_function(fn, [item]) for item in lst]

    def _native_filter(self, lst, fn):
        return [item for item in lst if self._apply_function(fn, [item])]

    def _native_foreach(self, lst, fn):
        for item in lst:
            self._apply_function(fn, [item])
        return None

    def _apply_function(self, fn, args):
        if fn.native:
            return fn.native_impl(*args)
        if len(args) != len(fn.params):
            raise Exception(f"Function {fn.name} expected {len(fn.params)} args, got {len(args)}")
        locals = dict(zip(fn.params, args))
        self.call_stack.append(Frame(self.ip, locals, fn.env))
        saved_ip = self.ip
        self.ip = self.bytecode.index(fn.block) + 1
        self.run()
        self.ip = saved_ip
        return self.stack.pop() if self.stack else None

# -------------------------
# 6. Entry Point
# -------------------------
parser = Lark(plasma_grammar, start="start", parser="lalr")

def compile_and_run(code):
    tree = parser.parse(code)
    compiler = Compiler()
    compiler.transform(tree)
    vm = PlasmaVM(compiler.consts, compiler.bytecode)
    vm.run()

if __name__ == "__main__":
    code = '''
    let numbers = [1, 2, 3, 4, 5]

    let doubled = map(numbers, Func (n) { return n * 2 })
    Print [doubled]

    let evens = filter(numbers, Func (n) { return n % 2 == 0 })
    Print [evens]

    forEach(numbers, Func (n) { Print [n] })
    end
    '''
    compile_and_run(code)
