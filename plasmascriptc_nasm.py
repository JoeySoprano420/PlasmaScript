# plasmascriptc_nasm.py
# PlasmaScript NASM Backend Compiler
# Author: Violet + ChatGPT
# License: MIT

import os, subprocess

class NASMEmitter:
    def __init__(self):
        self.asm = []
        self.data = []
        self.externs = set()
        self.globals = set()

    def emit(self, line): self.asm.append(line)
    def emit_data(self, line): self.data.append(line)

    def compile_prog(self, prog_name="main", body=None):
        self.emit("global main")
        self.externs.add("printf")
        self.emit("section .text")
        self.emit("main:")

        # Example: print string
        msg = "Hello from PlasmaScript NASM!"
        label = "msg"
        self.emit_data(f'{label} db "{msg}", 10, 0')
        self.emit(f"    lea rcx, [rel {label}]")
        self.emit(f"    call printf")

        # OpenGL sample calls
        self.externs.update(["glClear", "glClearColor"])

        # glClearColor(0.2,0.3,0.3,1.0)
        self.emit("    movq xmm0, __float64__(0.2)")
        self.emit("    movq xmm1, __float64__(0.3)")
        self.emit("    movq xmm2, __float64__(0.3)")
        self.emit("    movq xmm3, __float64__(1.0)")
        self.emit("    call glClearColor")

        # glClear(0x4000)
        self.emit("    mov ecx, 0x4000")
        self.emit("    call glClear")

        self.emit("    xor eax, eax")
        self.emit("    ret")

    def generate(self):
        out = []
        out.append("section .data")
        out.extend(self.data)
        out.append("")
        for ext in self.externs:
            out.append(f"extern {ext}")
        out.append("")
        out.extend(self.asm)
        return "\n".join(out)

def compile_to_exe(output="plasmascript_nasm.exe"):
    emitter = NASMEmitter()
    emitter.compile_prog()
    asm_code = emitter.generate()

    with open("output.asm", "w") as f:
        f.write(asm_code)

    # Assemble and link (Windows)
    subprocess.run(["nasm", "-fwin64", "output.asm", "-o", "output.obj"])
    subprocess.run(["gcc", "output.obj", "-o", output, "-lopengl32"])

    print(f"✅ NASM build complete: {output}")

if __name__ == "__main__":
    compile_to_exe()

def codegen_nasm(ast):
    asm = []
    data = []
    bss = []

    # counters
    labelc = {"if":0,"else":0,"endif":0,"for":0,"func":0}
    varmap_stack = [{}]
    varoff = [0]   # stack frame offsets

    def fresh_label(prefix):
        labelc[prefix]+=1
        return f"{prefix}{labelc[prefix]}"

    # allocate variable
    def alloc_var(name):
        varoff[-1]+=8
        slot=f"[rbp-{varoff[-1]}]"
        varmap_stack[-1][name]=slot
        return slot

    # lookup variable
    def lookup(name):
        for scope in reversed(varmap_stack):
            if name in scope: return scope[name]
        raise Exception(f"Undefined variable {name}")

    # lower RPN expr into NASM
    def lower_expr(expr):
        code=[]
        stack=[]
        for t in expr:
            if t["type"]=="Number":
                code.append(f"  mov rax,{t['value']}")
                stack.append("rax")
            elif t["type"]=="Var":
                slot=lookup(t["value"])
                code.append(f"  mov rax,{slot}")
                stack.append("rax")
            elif t["type"]=="Op":
                b=stack.pop(); a=stack.pop()
                if t["value"]=="+":
                    code.append(f"  add {a},{b}")
                    stack.append(a)
                elif t["value"]=="-":
                    code.append(f"  sub {a},{b}")
                    stack.append(a)
                elif t["value"]=="*":
                    code.append(f"  imul {a},{b}")
                    stack.append(a)
                elif t["value"]=="/":
                    code.append(f"  mov rdx,0")
                    code.append(f"  idiv {b}")
                    stack.append("rax")
        return code

    # header
    asm.append("section .data")
    asm.append("fmt: db \"%d\",10,0")
    asm.append("section .text")
    asm.append("global _start")

    asm.append("_start:")
    asm.append("  call main")
    asm.append("  mov rax,60")
    asm.append("  xor rdi,rdi")
    asm.append("  syscall")

    # generate
    i=0
    while i<len(ast):
        node=ast[i]

        # function declarations
        if node["type"]=="FunctionDecl":
            fname=node["name"]
            asm.append(f"{fname}:")
            asm.append("  push rbp")
            asm.append("  mov rbp,rsp")
            varmap_stack.append({})
            varoff.append(0)

            # map args into [rbp-]
            regs=["rdi","rsi","rdx","rcx","r8","r9"]
            for ai,a in enumerate(node["args"]):
                slot=alloc_var(a)
                asm.append(f"  mov {slot},{regs[ai]}")

        elif node["type"]=="ReturnExpr":
            code=lower_expr(node["expr"])
            asm.extend(code)
            asm.append("  mov rsp,rbp")
            asm.append("  pop rbp")
            asm.append("  ret")

        elif node["type"]=="AssignExpr":
            slot=alloc_var(node["name"])
            code=lower_expr(node["expr"])
            asm.extend(code)
            asm.append(f"  mov {slot},rax")

        elif node["type"]=="Print":
            # here we only support numbers
            if node["value"].isdigit():
                asm.append(f"  mov rdi,{node['value']}")
            else:
                slot=lookup(node["value"])
                asm.append(f"  mov rdi,{slot}")
            asm.append("  call print_int")

        elif node["type"]=="FunctionCall":
            args=node["args"]
            regs=["rdi","rsi","rdx","rcx","r8","r9"]
            for ai,a in enumerate(args):
                if a.isdigit():
                    asm.append(f"  mov {regs[ai]},{a}")
                else:
                    slot=lookup(a)
                    asm.append(f"  mov {regs[ai]},{slot}")
            asm.append(f"  call {node['name']}")

        elif node["type"]=="IfStart":
            lbl_else=fresh_label("else")
            lbl_end=fresh_label("endif")
            code=lower_expr(node["cond"])
            asm.extend(code)
            asm.append("  cmp rax,0")
            asm.append(f"  je {lbl_else}")
            node["else_label"]=lbl_else
            node["end_label"]=lbl_end

        elif node["type"]=="Else":
            lbl_end=fresh_label("endif")
            asm.append(f"  jmp {lbl_end}")
            asm.append(f"{node['else_label']}:")
            node["end_label"]=lbl_end

        elif node["type"]=="BlockEnd":
            if "end_label" in node:
                asm.append(f"{node['end_label']}:")

        elif node["type"]=="ForLoop":
            var=node["var"]
            start=node["start"]; end=node["end"]
            slot=alloc_var(var)
            lbl_loop=fresh_label("for")
            lbl_end=fresh_label("endfor")
            asm.append(f"  mov rax,{start}")
            asm.append(f"  mov {slot},rax")
            asm.append(f"{lbl_loop}:")
            asm.append(f"  mov rax,{slot}")
            asm.append(f"  cmp rax,{end}")
            asm.append(f"  jg {lbl_end}")

        i+=1

    # builtin print_int
    asm.append("print_int:")
    asm.append("  push rbp")
    asm.append("  mov rbp,rsp")
    asm.append("  mov rsi,rdi")
    asm.append("  mov rdi,fmt")
    asm.append("  xor rax,rax")
    asm.append("  call printf wrt ..plt")
    asm.append("  mov rsp,rbp")
    asm.append("  pop rbp")
    asm.append("  ret")

    return "\n".join(asm)
