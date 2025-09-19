# plasma_interpreter.py
# PlasmaScript Interpreter using Lark
# Author: Violet + ChatGPT
# License: MIT

from lark import Lark, Transformer, v_args

plasma_grammar = r"""
?start: statement+

?statement: comment
          | var_decl
          | print_stmt
          | func_def
          | if_stmt
          | for_stmt
          | import_stmt
          | event_stmt
          | return_stmt
          | end_stmt
          | expr

comment: ";" /[^\n]/*

var_decl: "let" NAME [":" TYPE] "=" expr

print_stmt: "Print" "(" expr ")"

func_def: "Func" NAME "(" [params] ")" block
params: NAME ("," NAME)*

return_stmt: "return" expr

if_stmt: "if" expr block ("else" block)?

for_stmt: "for" NAME "in" expr block

import_stmt: "Import" STRING

event_stmt: "on" NAME block

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
     | object_lit
     | "true"        -> true
     | "false"       -> false

list_lit: "[" [args] "]"
object_lit: "{" [pair ("," pair)*] "}"
pair: NAME ":" expr

TYPE: "text" | "number" | "bool" | "list" | "object"

OP: "==" | "!=" | "<" | ">" | "<=" | ">=" | "+" | "-" | "*" | "/"

NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
STRING: ESCAPED_STRING
NUMBER: /\d+/

%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

# ------------------------
# Runtime Environment
# ------------------------

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.funcs = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: {name}")

    def set(self, name, value):
        self.vars[name] = value

    def define_func(self, name, params, block):
        self.funcs[name] = (params, block)

    def get_func(self, name):
        if name in self.funcs:
            return self.funcs[name]
        if self.parent:
            return self.parent.get_func(name)
        raise NameError(f"Undefined function: {name}")

# ------------------------
# AST Transformer
# ------------------------

class PlasmaInterpreter(Transformer):
    def __init__(self):
        super().__init__()
        self.global_env = Environment()
        self.env = self.global_env
        self.return_value = None

    # --- Literals ---
    def number(self, items):
        return int(items[0])

    def string(self, items):
        return str(items[0][1:-1])  # strip quotes

    def true(self, _):
        return True

    def false(self, _):
        return False

    def list_lit(self, items):
        return items

    def object_lit(self, items):
        return dict(items)

    def pair(self, items):
        return (items[0], items[1])

    def var(self, items):
        return self.env.get(str(items[0]))

    # --- Expressions ---
    def binop(self, items):
        a, op, b = items[0], items[1].value, items[2]
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
        raise Exception(f"Unknown operator {op}")

    def neg(self, items):
        return -items[0]

    def func_call(self, items):
        name = str(items[0])
        args = items[1:] if len(items) > 1 else []
        params, block = self.env.get_func(name)
        new_env = Environment(parent=self.env)
        for p, a in zip(params, args[0] if args else []):
            new_env.set(p, a)
        prev_env = self.env
        self.env = new_env
        self.visit(block)
        self.env = prev_env
        return self.return_value

    # --- Statements ---
    def var_decl(self, items):
        name = str(items[0])
        value = items[-1]
        self.env.set(name, value)

    def print_stmt(self, items):
        print(items[0])

    def func_def(self, items):
        name = str(items[0])
        params = [str(p) for p in items[1].children] if len(items) > 1 and hasattr(items[1], "children") else []
        block = items[-1]
        self.env.define_func(name, params, block)

    def return_stmt(self, items):
        self.return_value = items[0]

    def if_stmt(self, items):
        cond, block = items[0], items[1]
        if cond:
            self.visit(block)
        elif len(items) > 2:
            self.visit(items[2])

    def for_stmt(self, items):
        varname, iterable, block = str(items[0]), items[1], items[2]
        for val in iterable:
            self.env.set(varname, val)
            self.visit(block)

    def import_stmt(self, items):
        print(f"[Import placeholder] Would import {items[0]}")

    def event_stmt(self, items):
        print(f"[Event: {items[0]}] Block attached.")

    def end_stmt(self, _):
        print("Program finished.")
        exit(0)

    def block(self, items):
        for stmt in items:
            self.visit(stmt)

    def comment(self, _):
        pass  # ignore

# ------------------------
# Entry Point
# ------------------------

parser = Lark(plasma_grammar, start="start", parser="lalr")

def run_plasma(code):
    tree = parser.parse(code)
    PlasmaInterpreter().transform(tree)

if __name__ == "__main__":
    code = '''
    ; PlasmaScript demo

    let greeting: text = "hello Shay!"

    Func greet(name) {
        Print("hello " + name)
    }

    greet(greeting)

    if greeting == "hello Shay!" {
        Print("Welcome back!")
    } else {
        Print("Hello, stranger.")
    }

    for x in [1, 2, 3] {
        Print(x)
    }

    end
    '''
    run_plasma(code)
