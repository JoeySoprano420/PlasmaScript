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
