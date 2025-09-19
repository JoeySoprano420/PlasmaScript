# plasma_vm_generators.py
# PlasmaScript VECE with generator expressions
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
     | list_comp
     | dict_comp
     | set_comp
     | gen_expr
     | tuple_lit

func_call: NAME "(" [args] ")"
args: expr ("," expr)*

?atom: NUMBER        -> number
     | STRING        -> string
     | NAME          -> var
     | list_lit
     | dict_lit
     | set_lit
     | "true"        -> true
     | "false"       -> false

list_lit: "[" [args] "]"
dict_lit: "{" [pairs] "}"
pairs: pair ("," pair)*
pair: NAME ":" expr
set_lit: "{" args "}"   -> set_lit_expr

tuple_lit: "(" args ")" -> tuple_expr

# --- Comprehensions ---
list_comp: "[" expr comp_clauses "]"
dict_comp: "{" expr ":" expr comp_clauses "}"
set_comp:  "{" expr comp_clauses "}"
gen_expr:  "(" expr comp_clauses ")"
comp_clauses: ("for" NAME "in" expr)+ ["if" expr]

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
    LIST_COMP    = "LIST_COMP"
    DICT_COMP    = "DICT_COMP"
    SET_COMP     = "SET_COMP"
    GEN_EXPR     = "GEN_EXPR"
    TUPLE        = "TUPLE"
    LIST         = "LIST"
    DICT         = "DICT"
    SET          = "SET"

# -------------------------
# 3. Compiler
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

    def tuple_expr(self, items):
        for arg in items[0].children:
            self.bytecode.append(arg)
        self.bytecode.append((OpCode.TUPLE, len(items[0].children)))

    def list_lit(self, items):
        if items:
            for arg in items[0].children:
                self.bytecode.append(arg)
            self.bytecode.append((OpCode.LIST, len(items[0].children)))
        else:
            self.bytecode.append((OpCode.LIST, 0))

    def set_lit_expr(self, items):
        for arg in items[0].children:
            self.bytecode.append(arg)
        self.bytecode.append((OpCode.SET, len(items[0].children)))

    def return_stmt(self, items):
        self.bytecode.append(items[0])
        self.bytecode.append((OpCode.RETURN, None))

    def end_stmt(self, _):
        self.bytecode.append((OpCode.END, None))

    def list_comp(self, items):
        expr, clauses, cond = self._extract_comp(items)
        self.bytecode.append((OpCode.LIST_COMP, (expr, clauses, cond)))

    def dict_comp(self, items):
        key_expr, val_expr = items[0], items[1]
        clauses, cond = self._extract_comp(items[2:])
        self.bytecode.append((OpCode.DICT_COMP, (key_expr, val_expr, clauses, cond)))

    def set_comp(self, items):
        expr, clauses, cond = self._extract_comp(items)
        self.bytecode.append((OpCode.SET_COMP, (expr, clauses, cond)))

    def gen_expr(self, items):
        expr, clauses, cond = self._extract_comp(items)
        self.bytecode.append((OpCode.GEN_EXPR, (expr, clauses, cond)))

    def _extract_comp(self, items):
        expr = items[0]
        clauses = items[1:-1] if len(items) > 2 else [items[1]]
        condition = items[-1] if str(items[-2]) == "if" else None
        return expr, clauses, condition

# -------------------------
# 4. Generator Object
# -------------------------
class Generator:
    def __init__(self, expr, clauses, cond, vm):
        self.expr = expr
        self.clauses = clauses
        self.cond = cond
        self.vm = vm
        self.state = [{}]  # stack of environments
        self.results = None
        self._build_iter()

    def _build_iter(self):
        self.results = []
        def eval_clauses(env, depth=0):
            if depth >= len(self.clauses):
                if self.cond is None or self.vm._eval_inline(self.cond, env):
                    self.results.append(self.vm._eval_inline(self.expr, env))
                return
            _, var, src = self.clauses[depth]
            source = self.vm._eval_inline(src, env)
            for item in source:
                env2 = env.copy()
                env2[var] = item
                eval_clauses(env2, depth+1)
        eval_clauses({})

    def __iter__(self):
        return iter(self.results)

    def __repr__(self):
        return f"<generator object at {hex(id(self))}>"

# -------------------------
# 5. Virtual Machine
# -------------------------
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
                    self.stack.append(self.globals.get(arg, None))
                elif op == OpCode.STORE_VAR:
                    self.globals[arg] = self.stack.pop()
                elif op == OpCode.PRINT:
                    print(self.stack.pop())
                elif op == OpCode.BINARY_OP:
                    b = self.stack.pop(); a = self.stack.pop()
                    self.stack.append(self._binop(a, b, arg))
                elif op == OpCode.LIST_COMP:
                    expr, clauses, cond = arg
                    result = []
                    self._eval_comprehension(expr, clauses, cond, result.append)
                    self.stack.append(result)
                elif op == OpCode.DICT_COMP:
                    key_expr, val_expr, clauses, cond = arg
                    result = {}
                    def add_item(k, v): result[k] = v
                    self._eval_comprehension((key_expr, val_expr), clauses, cond, lambda kv: add_item(kv[0], kv[1]))
                    self.stack.append(result)
                elif op == OpCode.SET_COMP:
                    expr, clauses, cond = arg
                    result = set()
                    self._eval_comprehension(expr, clauses, cond, result.add)
                    self.stack.append(result)
                elif op == OpCode.GEN_EXPR:
                    expr, clauses, cond = arg
                    gen = Generator(expr, clauses, cond, self)
                    self.stack.append(gen)
                elif op == OpCode.RETURN:
                    self.stack.append(None)
                elif op == OpCode.END:
                    print("Program finished.")
                    return

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

    def _eval_inline(self, expr, env):
        if isinstance(expr, tuple) and expr[0] == OpCode.LOAD_CONST:
            return self.consts[expr[1]]
        elif isinstance(expr, tuple) and expr[0] == OpCode.LOAD_VAR:
            return env.get(expr[1], self.globals.get(expr[1]))
        return expr

    def _eval_comprehension(self, expr, clauses, cond, collector):
        def eval_clauses(env, depth=0):
            if depth >= len(clauses):
                if cond is None or self._eval_inline(cond, env):
                    if isinstance(expr, tuple) and len(expr) == 2:  # dict comp
                        k = self._eval_inline(expr[0], env)
                        v = self._eval_inline(expr[1], env)
                        collector((k, v))
                    else:
                        collector(self._eval_inline(expr, env))
                return
            _, var, src = clauses[depth]
            source = self._eval_inline(src, env)
            for item in source:
                env2 = env.copy()
                env2[var] = item
                eval_clauses(env2, depth+1)
        eval_clauses({})

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
    let xs = [1, 2, 3, 4]

    let gen = (x * x for x in xs)

    for y in gen {
        Print [y]
    }

    end
    '''
    compile_and_run(code)
