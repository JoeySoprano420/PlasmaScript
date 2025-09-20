#!/usr/bin/env python3
# plasmascriptc.py
# PlasmaScript Compiler — LLVM + NASM backends
# Author: Violet + ChatGPT
# License: MIT

import os, subprocess, sys
import llvmlite.ir as ir
import llvmlite.binding as llvm
from lark import Lark, Transformer

# -------------------------
# Grammar
# -------------------------
plasma_grammar = r"""
?start: program
?program: (statement)+

?statement: comment
          | import_stmt
          | extern_stmt
          | export_func
          | func_def
          | inline_dgm
          | var_decl
          | print_stmt
          | return_stmt
          | end_stmt
          | expr

comment: ";" /[^\n]/*

import_stmt: "Import" STRING
extern_stmt: "Extern" STRING "Func" NAME "(" [params] ")"    -> extern_decl
export_func: "Export" "Func" NAME "(" [params] ")" block     -> export_def

var_decl: "let" NAME "=" expr
print_stmt: "Print" "[" expr "]"

func_def: ("Prog"|"Main"|"Func") NAME? "(" [params] ")" block
params: NAME (":" NAME)? ("," NAME (":" NAME)?)*

return_stmt: "return" expr
end_stmt: "end" | "run"

inline_dgm: "Inline" "{" dgm_call+ "}"
dgm_call: "dgm" "(" args ")"

block: "{" statement* "}"

?expr: atom
     | expr OP expr   -> binop
     | "-" expr       -> neg
     | func_call
     | tuple_lit

func_call: NAME "(" [args] ")"
args: expr ("," expr)*

?atom: NUMBER        -> number
     | STRING        -> string
     | NAME          -> var
     | list_lit
     | "true"        -> true
     | "false"       -> false

list_lit: "[" [args] "]"
tuple_lit: "(" args ")" -> tuple_expr

OP: "==" | "!=" | "<" | ">" | "<=" | ">=" | "+" | "-" | "*" | "/" | "%"

NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
STRING: ESCAPED_STRING
NUMBER: /\d+/

%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

# -------------------------
# AST Nodes
# -------------------------
class ImportNode: 
    def __init__(self, lib): self.lib = lib.strip('"')
class ExternNode:
    def __init__(self, linkage, name, params): self.linkage, self.name, self.params = linkage, name, params
class ExportFuncNode:
    def __init__(self, name, params, body): self.name, self.params, self.body = name, params, body
class InlineDgmNode:
    def __init__(self, codes): self.codes = codes
class FuncNode:
    def __init__(self, name, params, body): self.name, self.params, self.body = name, params, body
class PrintNode:
    def __init__(self, expr): self.expr = expr
class ReturnNode:
    def __init__(self, expr): self.expr = expr

# -------------------------
# Transformer
# -------------------------
class PlasmaTransformer(Transformer):
    def import_stmt(self, items): return ImportNode(str(items[0]))
    def extern_decl(self, items):
        return ExternNode(str(items[0]).strip('"'), str(items[1]), [str(x) for x in items[2:]])
    def export_def(self, items):
        return ExportFuncNode(str(items[0]), [], items[-1])
    def func_def(self, items):
        kw = str(items[0])
        name = "main" if kw in ("Prog","Main") else str(items[1])
        body = items[-1]
        return FuncNode(name, [], body)
    def print_stmt(self, items): return PrintNode(items[0])
    def return_stmt(self, items): return ReturnNode(items[0])
    def inline_dgm(self, items):
        codes = []
        for d in items: codes.extend(d)
        return InlineDgmNode(codes)
    def dgm_call(self, items): return [int(str(x)) for x in items]

# -------------------------
# LLVM Backend
# -------------------------
class LLVMBackend:
    def __init__(self, ast):
        self.ast = ast
        self.module = ir.Module(name="plasmascript")
        self.module.triple = llvm.get_default_triple()
        self.printf = None
        self.imports = set()

    def build(self):
        self._declare_printf()
        for node in self.ast:
            if isinstance(node, ImportNode): self.imports.add(node.lib)
            elif isinstance(node, ExternNode): self._declare_extern(node)
            elif isinstance(node, ExportFuncNode): self._export_func(node)
            elif isinstance(node, FuncNode): self._func(node)
        return str(self.module)

    def _declare_printf(self):
        ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        self.printf = ir.Function(self.module, ty, name="printf")

    def _declare_extern(self, node):
        fnty = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
        ir.Function(self.module, fnty, name=node.name)

    def _export_func(self, node):
        fnty = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
        fn = ir.Function(self.module, fnty, name=node.name)
        fn.attributes.add("dllexport")
        block = fn.append_basic_block("entry")
        builder = ir.IRBuilder(block)
        result = builder.add(fn.args[0], fn.args[1])
        builder.ret(result)

    def _func(self, node):
        fnty = ir.FunctionType(ir.IntType(32), [])
        fn = ir.Function(self.module, fnty, name=node.name)
        block = fn.append_basic_block("entry")
        builder = ir.IRBuilder(block)
        for stmt in node.body.children:
            if isinstance(stmt, PrintNode):
                s = "Hello PlasmaScript!\n\0"
                cstr = ir.Constant(ir.ArrayType(ir.IntType(8), len(s)), bytearray(s.encode("utf8")))
                gv = ir.GlobalVariable(self.module, cstr.type, name="msg")
                gv.linkage = 'internal'; gv.global_constant = True; gv.initializer = cstr
                ptr = builder.bitcast(gv, ir.IntType(8).as_pointer())
                builder.call(self.printf, [ptr])
            elif isinstance(stmt, InlineDgmNode):
                asm = "\n".join([f"mov eax, {c}" for c in stmt.codes])
                builder.asm(ir.FunctionType(ir.VoidType(), []), asm, "", side_effect=True)
        builder.ret(ir.Constant(ir.IntType(32), 0))

    def compile(self, output="plasmascript.exe"):
        with open("output.ll", "w") as f: f.write(str(self.module))
        subprocess.run(["clang", "output.ll", "-o", output] + [f"-l{lib}" for lib in self.imports])
        print(f"✅ LLVM build: {output}")

# -------------------------
# NASM Backend
# -------------------------
class NASMBackend:
    def __init__(self, ast):
        self.ast = ast
        self.data = []
        self.text = []
        self.externs = set()
        self.globals = set(["main"])

    def build(self):
        self.externs.add("printf")
        self.text.append("main:")
        for node in self.ast:
            if isinstance(node, PrintNode):
                self.data.append('msg db "Hello PlasmaScript NASM!", 10, 0')
                self.text.append("    lea rcx, [rel msg]")
                self.text.append("    call printf")
            elif isinstance(node, InlineDgmNode):
                for c in node.codes:
                    self.text.append(f"    mov eax, {c}")
            elif isinstance(node, ExternNode):
                self.externs.add(node.name)
        self.text.append("    xor eax, eax")
        self.text.append("    ret")
        return self._generate()

    def _generate(self):
        out = ["section .data"]
        out.extend(self.data)
        out.append("")
        for e in self.externs: out.append(f"extern {e}")
        out.append("")
        out.append("section .text")
        out.extend(self.text)
        return "\n".join(out)

    def compile(self, output="plasmascript_nasm.exe"):
        asm = self.build()
        with open("output.asm","w") as f: f.write(asm)
        subprocess.run(["nasm","-fwin64","output.asm","-o","output.obj"])
        subprocess.run(["gcc","output.obj","-o",output,"-lopengl32"])
        print(f"✅ NASM build: {output}")

# -------------------------
# CLI Entrypoint
# -------------------------
def main():
    if len(sys.argv) < 4:
        print("Usage: plasmascriptc file.ps -backend [llvm|nasm] -o output.exe")
        sys.exit(1)
    infile = sys.argv[1]
    backend = sys.argv[3]
    outfile = sys.argv[5] if len(sys.argv) > 5 else "a.exe"

    parser = Lark(plasma_grammar, start="program", parser="lalr")
    with open(infile) as f: code = f.read()
    tree = parser.parse(code)
    ast = PlasmaTransformer().transform(tree).children

    if backend == "llvm":
        LLVMBackend(ast).compile(outfile)
    elif backend == "nasm":
        NASMBackend(ast).compile(outfile)

if __name__ == "__main__":
    main()

