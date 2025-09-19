# plasmascriptc.py
# PlasmaScript AOT Compiler → .exe
# Author: Violet + ChatGPT
# License: MIT

import llvmlite.ir as ir
import llvmlite.binding as llvm
import subprocess
import os

# -----------------------------------
# 1. LLVM Module Setup
# -----------------------------------
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

module = ir.Module(name="plasmascript")
module.triple = llvm.get_default_triple()

# declare printf for Print
printf_ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
printf = ir.Function(module, printf_ty, name="printf")

# declare glClear + glClearColor
glclear_ty = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
glClear = ir.Function(module, glclear_ty, name="glClear")

glclearcolor_ty = ir.FunctionType(ir.VoidType(), [ir.DoubleType()]*4)
glClearColor = ir.Function(module, glclearcolor_ty, name="glClearColor")

# -----------------------------------
# 2. Hello World Main Function
# -----------------------------------
main_ty = ir.FunctionType(ir.IntType(32), [])
main_func = ir.Function(module, main_ty, name="main")
block = main_func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)

# Print "Hello PlasmaScript\n"
msg = "Hello PlasmaScript!\n\0"
cstr = ir.Constant(ir.ArrayType(ir.IntType(8), len(msg)),
                   bytearray(msg.encode("utf8")))
global_str = ir.GlobalVariable(module, cstr.type, name="str")
global_str.linkage = 'internal'
global_str.global_constant = True
global_str.initializer = cstr
str_ptr = builder.bitcast(global_str, ir.IntType(8).as_pointer())
builder.call(printf, [str_ptr])

# Call glClearColor(0.2, 0.3, 0.3, 1.0)
builder.call(glClearColor, [ir.Constant(ir.DoubleType(), 0.2),
                            ir.Constant(ir.DoubleType(), 0.3),
                            ir.Constant(ir.DoubleType(), 0.3),
                            ir.Constant(ir.DoubleType(), 1.0)])

# Call glClear(0x00004000)
builder.call(glClear, [ir.Constant(ir.IntType(32), 0x00004000)])

builder.ret(ir.Constant(ir.IntType(32), 0))

print("=== LLVM IR ===")
print(module)

# -----------------------------------
# 3. JIT or AOT Compile
# -----------------------------------
def compile_exe(output="plasmascript.exe"):
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    with llvm.create_mcjit_compiler(llvm.parse_assembly(str(module)), target_machine) as engine:
        engine.finalize_object()
        with open("output.o", "wb") as f:
            f.write(target_machine.emit_object(llvm.parse_assembly(str(module))))
    # link into exe
    subprocess.run(["clang", "output.o", "-o", output, "-lopengl32"])
    os.remove("output.o")
    print(f"✅ Built {output}")

if __name__ == "__main__":
    compile_exe()

# in plasmascriptc.py (extending)

def declare_extern(module, name, rettype, args):
    fnty = ir.FunctionType(rettype, args)
    return ir.Function(module, fnty, name=name)

# example inline Dodecagram as LLVM asm
def inline_dgm(builder, codes):
    asm_str = "; Dodecagram inline\n"
    for c in codes:
        asm_str += f"mov eax, {c}\n"
    builder.asm(ir.FunctionType(ir.VoidType(), []), asm_str, "", side_effect=True)
