# plasma_vm_closures.py
# PlasmaScript VECE with Closures
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
          | if_stmt
          | for_stmt
          | return_stmt
          | end_stmt
          | expr

comment: ";" /[^\n]/*

var_decl: "let" NAME "=" expr
print_stmt: "Print" "[" expr "]"

func_def: ("Prog"|"Main"|"Func") NAME? "(" [params] ")" block
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

func_call: NAME "(" [args] ")"
args: expr ("," expr)*

?atom: NUMBER        -> number
     | STRING        -> string
     | NAME          -> var
     | list_lit
     | "true"        -> true
     | "false"       -> false

list_lit: "[" [args] "]"

OP: "==" | "!=" | "<" | ">" | "<=" | ">=" | "+" | "-" | "*" | "/"

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
    def __init__(self, name, params, block, env):
        self.name = name
        self.params = params
        self.block = block
        self.env = env  # closure environment snapshot

    def __repr__(self):
        return f"<Func {self.name}({','.join(self.params)})>"

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
        self.closure_env = closure_env  # captured outer scope

class PlasmaVM:
    def __init__(self, consts, bytecode):
        self.consts = consts
        self.bytecode = bytecode
        self.stack = []
        self.ip = 0
        self.funcs = {}
        self.call_stack = []
        self.globals = {}

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
                    # capture closure from current environment
                    closure_env = dict(self.globals)
                    if self.call_stack:
                        closure_env.update(self.call_stack[-1].locals)
                        closure_env.update(self.call_stack[-1].closure_env)
                    func_obj = Function(name, params, block, closure_env)
                    self.funcs[name] = func_obj
                    self.stack.append(func_obj)  # allow returning functions
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
        if op == "==": return a == b
        if op == "!=": return a != b
        if op == "<": return a < b
        if op == ">": return a > b
        if op == "<=": return a <= b
        if op == ">=": return a >= b
        raise Exception(f"Unsupported op {op}")

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
    # ✅ Closure example
    code = '''
    Func makeAdder(x) {
        Func adder(y) { return x + y }
        return adder
    }

    let add5 = makeAdder(5)
    Print [add5(10)]
    end
    '''
    compile_and_run(code)
