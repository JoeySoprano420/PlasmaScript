# plasma_grammar.py
# PlasmaScript Grammar Specification using Lark
# Author: Violet + ChatGPT
# License: MIT

from lark import Lark

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

parser = Lark(plasma_grammar, start="start", parser="lalr")

if __name__ == "__main__":
    code = '''
    ; comment Prog () greeting {hello user} Print ["hello Shay!"] run

    let greeting: text = "hello Shay!"
    Func greet(name) {
        Print("hello " + name)
    }

    if greeting == "hello Shay!" {
        Print("Welcome back!")
    } else {
        Print("Hello, stranger.")
    }

    end
    '''
    tree = parser.parse(code)
    print(tree.pretty())
