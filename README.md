# PlasmaScript

---

# 🌟 PlasmaScript Specification

### Overview

PlasmaScript is a minimalist, expressive scripting language designed for clarity, poetic readability, and conversational coding. It borrows simplicity from BASIC, flexibility from Python, and structure from modern scripting languages. Its philosophy: **“Possible — therefore Try.”**

---

## 1. Program Structure

Minimal Hello World:

```plasmascript

 
Prog 
() greeting {hello user} Print ["hello Shay!"] 
run


Alternative form:

plasmascript

 
Main 
() greeting {hello user} Print ["hello Shay!"] 
end


Both forms are valid. `run` and `end` serve as interchangeable program terminators.

---

## 2. Comments

```plasmascript
; This is a comment
```

Single-line comments begin with `;`. Multi-line comments are not yet supported (roadmap).

---

## 3. Variables

```plasmascript
let x = 42
let greeting: text = "hello Shay!"
```

* `let` declares variables.
* Optional type annotation follows `:`.
* Variables are block-scoped.

---

## 4. Output

```plasmascript
Print("hello Shay!")
Print(greeting)
```

`Print` sends output to stdout. Arguments may be literals, variables, or expressions.

---

## 5. Functions

```plasmascript
Func greet(name) {
    Print("hello " + name)
}
```

Return values:

```plasmascript
Func add(a, b) {
    return a + b
}
```

* Functions begin with `Func`.
* Arguments are untyped unless annotated.
* `return` exits with a value.

---

## 6. Control Flow

### If / Else

```plasmascript
if name == "Shay" {
    Print("Welcome back!")
} else {
    Print("Hello, stranger.")
}
```

### For Loop

```plasmascript
for item in list {
    Print(item)
}
```

Future roadmap: while loops and switch-case.

---

## 7. Input

```plasmascript
let name = Input("What's your name?")
```

Captures user input as `text`.

---

## 8. Modules / Imports

```plasmascript
Import "math"
```

* Imports core or user-defined modules.
* Namespaces are implicit (future expansions will add explicit namespaces).

---

## 9. Data Types

| Type     | Example          |
| -------- | ---------------- |
| `text`   | `"hello world"`  |
| `number` | `42`             |
| `bool`   | `true`, `false`  |
| `list`   | `[1, 2, 3]`      |
| `object` | `{name: "Shay"}` |

---

## 10. Events (Optional)

```plasmascript
on start {
    Print("Program started.")
}
```

Events provide structured entry points (e.g., `start`, `exit`).

---

## 11. Ending a Program

```plasmascript
end
```

or

```plasmascript
run
```

---

## 12. Sample Programs

### Minimal Hello World

```plasmascript
; comment Prog () greeting {hello user} Print ["hello Shay!"] run
```

### Greeting User

```plasmascript
let name = Input("Enter your name: ")
if name == "Shay" {
    Print("Welcome back, Shay!")
} else {
    Print("Nice to meet you, " + name)
}
end
```

### Function Example

```plasmascript
Func multiply(a, b) {
    return a * b
}

Print(multiply(6, 7))
end
```

---

## 13. Design Philosophy

* **Minimalist**: Stripped syntax for readability.
* **Expressive**: Encourages conversational or poetic coding.
* **Flexible**: Evolves easily into scripting or interpreted execution.
* **Friendly**: Immediate onboarding for new coders.

---

⚡**PlasmaScript** to evolve from an interpreted VM into a **full AOT-compiled systems language** with:

* **Complete ABI + FFI** (foreign function interface)
* **ISA mappings** (down to CPU instructions)
* **Interop APIs** for OpenGL, Vulkan, DirectX, Unreal Engine, Unity
* **Imports/Exports** for shared libraries
* **Inlining of Dodecagram (base-12)** opcodes
* **Exposure to/from WebAssembly + HTTPS**
* **AOT compiler → `.exe` output**

---

# 🚀 PlasmaScript AOT Compiler Design

Here’s the blueprint to take PlasmaScript from VM → real `.exe` output:

---

## 1. **Frontend (Parsing + IR)**

* **Grammar**: Already defined (PlasmaScript syntax + comprehensions, functions, etc.)
* **AST**: Enriched with:

  * Function signatures (name, params, return type)
  * Imports/exports
  * FFI/ABI declarations (`Extern "C"`, `import lib` etc.)
  * Inline assembly / Dodecagram segments

### Example PlasmaScript FFI

```plasmascript
Import "opengl32"

Extern "C" Func glClear(mask: number)
Extern "C" Func glBegin(mode: number)
Extern "C" Func glEnd()

Func draw() {
    glClear(0x00004000)
    glBegin(0x0004)
    glEnd()
}
```

---

## 2. **Intermediate Representation (Dodecagram IR)**

We introduce **DGIR (Dodecagram IR)**, a 12-base opcode stream mapping directly to:

* **LLVM IR** (for portability to `.exe`, `.wasm`, `.dylib`)
* **NASM x64** (for raw `.exe` + ISA exposure)

**Dodecagram Mapping (0-3, a, b)**

| Symbol | Meaning          | Example |
| ------ | ---------------- | ------- |
| `0`    | Load const       | `0 idx` |
| `1`    | Load var         | `1 reg` |
| `2`    | Store var        | `2 reg` |
| `3`    | Call function    | `3 f`   |
| `a`    | Inline sys call  | `a id`  |
| `b`    | Inline wasm call | `b id`  |

---

## 3. **Backend (AOT Compilation)**

The backend supports multiple lowering targets:

1. **LLVM → MSVC/Clang → `.exe`**

   * Generates real object files, links to system libraries (`opengl32.lib`, `vulkan-1.lib`, `d3d11.lib`, `Unreal.lib`, `UnityNative.lib`).
2. **NASM x64 Direct Emitter**

   * Direct `.asm` → `nasm` → `.exe` for minimal runtime.
3. **WASM Export**

   * Compiles PlasmaScript modules to `.wasm` with `import/export`.
4. **HTTPS/Interop**

   * Built-in standard library bindings for HTTP(S) requests (like `fetch`).

---

## 4. **Interop Libraries**

* **OpenGL**: `Import "opengl32"` → resolves symbols via system loader.
* **Vulkan**: `Import "vulkan-1"` → bindings generated at compile.
* **DirectX**: `Import "d3d11"` → COM interface bridging.
* **Unreal/Unity**:

  * Export PlasmaScript modules as `.dll` with `extern "C"` entry points.
  * Unity: call via `DllImport` in C#.
  * Unreal: bind via plugin module.

---

## 5. **Inlining Dodecagrams**

### Example

```plasmascript
Inline {
    dgm(0xA1, 0xB2, 0x00)
}
```

Generates raw NASM instructions or LLVM inline assembly.

---

## 6. **AOT Pipeline**

```bash
plasmascriptc hello.ps -target exe -o hello.exe
plasmascriptc game.ps -target wasm -o game.wasm
plasmascriptc engine.ps -target dll -o engine.dll
```

---

## 7. **Example: OpenGL PlasmaScript Program**

```plasmascript
Import "opengl32"

Extern "C" Func glClear(mask: number)
Extern "C" Func glClearColor(r: number, g: number, b: number, a: number)

Prog main() {
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(0x00004000)
}
end
```

Compiles → `.exe` that links against `opengl32.lib` and runs natively.

---

## 8. **WASM + HTTPS Example**

```plasmascript
Import "https"

let resp = Fetch("https://example.com/data.json")
Print [resp]
```

Compiles → `.wasm` that can be imported into JS with async `fetch`.

---

## 9. **Libraries + API Dictionary**

* **Standard**: strings, lists, dicts, sets, math, io
* **Interop**: opengl, vulkan, directx, unreal, unity
* **Networking**: http, https, ws
* **System**: file, process, threads
* **Dodecagram**: `dgm()` inline low-level

---

✅ With this design:

* PlasmaScript is **a compiled language with VM + AOT compiler**
* Exposes **ABI/FFI** to every major runtime
* Can inline **DGIR (dodecagram base-12)**
* Exports `.exe`, `.dll`, `.wasm`, `.so`

---

⚡ 
