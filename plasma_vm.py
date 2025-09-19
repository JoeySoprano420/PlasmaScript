# plasma_vm.py
# PlasmaScript Virtual Execution Compiler Environment
# Author: Violet + ChatGPT
# License: MIT

from lark import Lark, Transformer

# -------------------------
# 1. Grammar
# -------------------------
plasma_grammar = r"""
?start: statement+

?statement: var_decl
          | print_stmt
          | func_def
          | if_stmt
          | for_stmt
          | return_stmt
          | end_stmt
          | expr

var_decl: "let" NAME "=" expr
print_stmt: "Print" "(" expr ")"
func_def: "Func" NAME "(" [params] ")" block
params: NAME ("," NAME)*
return_stmt: "return" expr
if_stmt: "if" expr block ("else" block)?
for_stmt: "for" NAME "in" expr block
end_stmt: "end" | "run"

block: "{" statement* "}"

?expr: atom
     | expr OP expr   -> binop
     | "-" expr       -> neg
     | NAME "(" [args] ")" -> func_call

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
    LOAD_CONST = "LOAD_CONST"
    LOAD_VAR   = "LOAD_VAR"
    STORE_VAR  = "STORE_VAR"
    BINARY_OP  = "BINARY_OP"
    PRINT      = "PRINT"
    JUMP_IF_FALSE = "JUMP_IF_FALSE"
    JUMP       = "JUMP"
    FUNC_DEF   = "FUNC_DEF"
    CALL_FUNC  = "CALL_FUNC"
    RETURN     = "RETURN"
    ITER_BEGIN = "ITER_BEGIN"
    ITER_NEXT  = "ITER_NEXT"
    END        = "END"

# -------------------------
# 3. Compiler (AST → Bytecode)
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
        name = str(items[0])
        params = [str(p) for p in items[1].children] if hasattr(items[1], "children") else []
        block = items[-1]
        self.bytecode.append((OpCode.FUNC_DEF, (name, params, block)))

    def func_call(self, items):
        name = str(items[0])
        args = items[1:] if len(items) > 1 else []
        for arg in args[0]:
            self.bytecode.append(arg)
        self.bytecode.append((OpCode.CALL_FUNC, (name, len(args[0]))))

    def return_stmt(self, items):
        self.bytecode.append(items[0])
        self.bytecode.append((OpCode.RETURN, None))

    def if_stmt(self, items):
        cond, block = items[0], items[1]
        self.bytecode.append(cond)
        jmp_false_idx = len(self.bytecode)
        self.bytecode.append((OpCode.JUMP_IF_FALSE, None))
        for stmt in block.children:
            self.bytecode.append(stmt)
        if len(items) > 2:
            jmp_end_idx = len(self.bytecode)
            self.bytecode.append((OpCode.JUMP, None))
            self.bytecode[jmp_false_idx] = (OpCode.JUMP_IF_FALSE, len(self.bytecode))
            for stmt in items[2].children:
                self.bytecode.append(stmt)
            self.bytecode[jmp_end_idx] = (OpCode.JUMP, len(self.bytecode))
        else:
            self.bytecode[jmp_false_idx] = (OpCode.JUMP_IF_FALSE, len(self.bytecode))

    def for_stmt(self, items):
        varname, iterable, block = str(items[0]), items[1], items[2]
        self.bytecode.append(iterable)
        self.bytecode.append((OpCode.ITER_BEGIN, varname))
        loop_start = len(self.bytecode)
        self.bytecode.append((OpCode.ITER_NEXT, (varname, loop_start)))
        for stmt in block.children:
            self.bytecode.append(stmt)

    def end_stmt(self, _):
        self.bytecode.append((OpCode.END, None))

# -------------------------
# 4. Virtual Machine
# -------------------------
class PlasmaVM:
    def __init__(self, consts, bytecode):
        self.consts = consts
        self.bytecode = bytecode
        self.vars = {}
        self.stack = []
        self.ip = 0
        self.funcs = {}

    def run(self):
        while self.ip < len(self.bytecode):
            instr = self.bytecode[self.ip]
            self.ip += 1
            if isinstance(instr, tuple):
                op, arg = instr
                if op == OpCode.LOAD_CONST:
                    self.stack.append(self.consts[arg])
                elif op == OpCode.LOAD_VAR:
                    self.stack.append(self.vars.get(arg, None))
                elif op == OpCode.STORE_VAR:
                    val = self.stack.pop()
                    self.vars[arg] = val
                elif op == OpCode.PRINT:
                    val = self.stack.pop()
                    print(val)
                elif op == OpCode.BINARY_OP:
                    b = self.stack.pop(); a = self.stack.pop()
                    self.stack.append(self._binop(a, b, arg))
                elif op == OpCode.END:
                    print("Program finished.")
                    return
                else:
                    raise Exception(f"Unknown opcode: {op}")
            else:
                # Precompiled expression tuple
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
# 5. Entry Point
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
    let greeting = "hello Shay!"
    Print(greeting)
    let a = 6
    let b = 7
    Print(a * b)
    end
    '''
    compile_and_run(code)
