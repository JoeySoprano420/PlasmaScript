# ⚡ PlasmaScript
 
⸻

🌌 PlasmaScript: The Language of Expressive Power

✨ Tagline

PlasmaScript is a professional-grade, production-ready programming language that merges poetic syntax with uncompromising systems power — a language where minimalism, expressiveness, and industrial integration converge.

⸻

🧩 Design Philosophy
	1.	Minimalist → Expressive
	•	Reads like pseudocode or conversation.
	•	Encourages flow and brevity, but compiles to tight machine code.
	2.	Functional → Imperative Hybrid
	•	Functions and closures are first-class values.
	•	Imperative constructs (loops, variables) coexist with lambdas, comprehensions, and higher-order abstractions.
	3.	Manual → Managed Memory
	•	Explicit malloc, free, store, load.
	•	Native memory library with arenas, bump allocators, and refcount APIs.
	•	Closures capture environments either automatically or under programmer control.
	4.	Industrial → Humanistic
	•	Direct FFI/ABI/ISA bindings for OpenGL, Vulkan, DirectX, Unity, Unreal.
	•	Inline Dodecagram (base-12) assembly for systems-level hackers.
	•	Syntax retains warmth and clarity: code feels written for people.

⸻

🔤 Syntax Landscape

Minimal Form

Prog () greeting {hello user} Print ["hello PlasmaScript!"] run

Canonical

Prog main() {
    Print ["Hello PlasmaScript!"]
}
end

Functional

Export Func add(a: number, b: number) { return a + b }

Prog main() {
    Print [add(6, 7)]
}
end

Lambda + Closure

Prog main() {
    let base = 10
    let makeAdder = Func(x) {
        return Func(y) { return x + y + base }
    }
    let add5 = makeAdder(5)
    Print [add5(3)]   ; prints 18
}
end

Memory + Interop

Import "opengl32"

Extern "C" Func glClear(mask: number)
Extern "C" Func glClearColor(r: number, g: number, b: number, a: number)

Prog main() {
    let env = malloc(16)
    store(env, 0, 42)
    Print [load(env, 0)]

    glClearColor(0.1, 0.2, 0.3, 1.0)
    glClear(0x00004000)

    free(env)
}
end


⸻

🧮 Core Features

Variables & Types
	•	Explicit but optional types (let x: number = 42)
	•	Types: number, text, bool, list, object, tuple, set, dict

Functions
	•	First-class, higher-order, and anonymous (Func(x,y){ return x+y })
	•	Closures capture variables automatically or with explicit malloc/store/load.
	•	Export/import across modules with ABI bindings.

Control Flow
	•	if / else, for in, comprehensions, generator expressions.
	•	Structured error handling: try / catch / throw.

Memory
	•	Manual: malloc, free, store, load.
	•	Arena allocator: arena_init / arena_alloc / arena_reset.
	•	Refcount: rc_alloc / retain / release.
	•	Bump allocator: bump_init / bump_alloc / bump_reset.

Data Structures
	•	Lists: [1,2,3]
	•	Tuples: (x,y)
	•	Dicts: {a: 1, b: 2}
	•	Sets: {1,2,3}
	•	Comprehensions: [ (x,y) for x in xs for y in ys ]
	•	Dict comprehensions: {x: x*x for x in xs}
	•	Set comprehensions: {x*x for x in xs}
	•	Generators: (x*x for x in xs)

⸻

⚙️ Compilation Model

PlasmaScript is AOT-compiled into .exe, .so, .dll, .dylib.
	•	Frontend: Parses .ps → AST → IR.
	•	Middle End: Optimizations (constant folding, loop unrolling, closure lowering).
	•	Backends:
	1.	LLVM IR → object → linked via clang/lld.
	2.	NASM emitter → raw x64 assembly → .exe.

Supports:
	•	FFI: C ABI, OpenGL, Vulkan, DirectX, Unity, Unreal.
	•	Inline Dodecagram: Inline { dgm(0xA1, 0xB2) }.
	•	WASM Interop: PlasmaScript functions exportable to WebAssembly.

⸻

🔌 Interoperability

External Libraries

Import "math"
Import "opengl32"

Extern/Export

Extern "C" Func glClear(mask: number)
Export Func add(a: number, b: number) { return a + b }

Inline Assembly

Inline { dgm(0xDE, 0xAD, 0xBE, 0xEF) }


⸻

🛠 Toolchain
	•	Compiler: plasmascriptc → builds .exe via LLVM or NASM.
	•	REPL: interactive execution for scripts.
	•	Standard Library: memory, math, collections, graphics bindings.
	•	Package Manager: PlasmaHub (plasma add <lib>).
	•	LSP Support: VSCode plugin with syntax highlighting + debugging.

⸻

🚀 Use Cases
	•	Systems Programming → memory allocators, OS utilities, driver prototyping.
	•	Game Development → full FFI with Unity/Unreal, OpenGL/Vulkan/DirectX calls.
	•	Scientific Computing → closures, comprehensions, interop with C/Fortran libs.
	•	Creative Scripting → expressive syntax for “poetic” code (like meta-scripts).
	•	High-Performance Apps → AOT .exe with NASM-level optimizations.

⸻

🌍 Industries That Will Gravitate
	•	AAA Game Studios → direct graphics API interop + speed.
	•	Embedded Systems → AOT compilation, no runtime bloat.
	•	Finance / HPC → math-heavy, comprehension-rich code, native speed.
	•	Scientific Research → blends readability with native libraries.
	•	Creative Coding & Generative Art → poetic, expressive syntax.

⸻

🎨 Ethos

PlasmaScript is a language that bridges two worlds:
	•	The systems hacker, who wants raw pointers, arenas, NASM.
	•	The poetic coder, who wants to write:

Prog main() { Print ["hello universe"] } end



It is both industrial steel and lyrical plasma — a tool for engineers and dreamers alike.

⸻

✅ TL;DR

PlasmaScript is:
	•	Minimalist in surface syntax.
	•	Deep in semantics.
	•	Explicit in memory.
	•	Powerful in interop.
	•	Mainstream-ready for both creative scripting and systems programming.

From Hello World → to AAA graphics pipelines → to closures with arenas → PlasmaScript is the professional expressive language for the 21st century.

⸻


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

## ~~~~

⸻

🌌 PlasmaScript: Strategic Real-World Overview

⸻

👥 Who Will Use This Language?
	•	Systems Engineers & OS Developers — need fine-grained control of memory and performance while retaining clean syntax.
	•	Game Developers & Graphics Programmers — want seamless FFI with OpenGL, Vulkan, DirectX, Unity, Unreal.
	•	Scientific Researchers & HPC Teams — require expressive math (comprehensions, closures) with compiled performance.
	•	Creative Coders & Artists — attracted by its poetic minimal syntax (e.g., Prog main() { Print ["hello"] } end).
	•	Finance & AI Engineers — seeking deterministic AOT-compiled performance without runtime bloat.
	•	Embedded & Systems Integrators — leveraging manual memory management and direct ABI/ISA integration.

⸻

🏗 What Will It Be Used For?
	•	AAA Game Engines and mod scripting.
	•	Scientific simulations (physics, bioinformatics, ML preprocessing).
	•	High-frequency trading & finance apps (low latency, predictable memory).
	•	Embedded firmware and IoT control software.
	•	Creative scripting platforms for art, audio, generative visuals.
	•	Systems utilities (custom allocators, OS services, compiler toolchains).
	•	Interoperability glue between C/C++/Rust/Python ecosystems.

⸻

🏭 Industries & Sectors
	•	🎮 Gaming & Interactive Media
	•	🧪 Scientific Research & HPC
	•	🏦 Finance / Quantitative Computing
	•	📡 Embedded & Hardware Control
	•	🎨 Creative Arts & Design
	•	🛰 Aerospace & Defense (where deterministic execution is critical)
	•	⚙️ Compiler / Language R&D (meta-languages, tooling, DSLs).

⸻

💻 Real-World Projects & Software
	•	Cross-platform desktop apps (compiled to .exe, .so, .dylib).
	•	Engines: rendering cores, physics engines, AI/ML preprocessors.
	•	Toolchains: compilers, parsers, language servers.
	•	System services: custom memory managers, schedulers.
	•	Cloud services: WASM-enabled PlasmaScript backends.
	•	Artistic tools: live-coding environments, interactive installations.

⸻

📚 Learning Curve
	•	Beginner-friendly syntax (as approachable as Python).
	•	Gradual exposure to hardcore systems features (memory, ISA, ABI).
	•	Shallow slope for scripting → steeper climb for NASM/Dodecagram/FFI.
	•	Most developers can be productive in days, mastery of systems-level interop may take months.

⸻

🌐 Interoperability
	•	FFI/ABI with C, C++, Rust, Zig.
	•	ISA exposure via NASM x64 backend.
	•	WASM integration for web/cloud deployment.
	•	Graphics stack interop: OpenGL, Vulkan, DirectX, Unity, Unreal.
	•	Library import/export like C (Extern "C" Func …).
	•	Dodecagram inline assembly for power-users.

⸻

🎯 Current Purposes & Use Cases
	•	✅ General scripting (print, loops, functions).
	•	✅ Systems programming (manual allocators, closures, FFI).
	•	✅ Mathematical pipelines (comprehensions, higher-order functions).
	•	✅ Compiler experiments (self-hosting, DSL integration).
	•	✅ Cross-platform AOT binaries (LLVM + NASM).
	•	✅ Interop with external APIs (graphics, OS, libraries).

Edge cases already covered:
	•	Inline memory ops (store/load).
	•	Closures with manual capture.
	•	Dict/set/list comprehensions.
	•	Generator expressions (lazy evaluation).
	•	Inline dodecagram ISA injection.

⸻

🕹 What Can It Do Now?
	•	Parse → Compile → Run .ps files into .exe (LLVM or NASM).
	•	Run programs that use:
	•	Functions, closures, lambdas.
	•	Comprehensions (list/dict/set/gen).
	•	Custom allocators (arena, bump, refcount).
	•	Imports/exports.
	•	External bindings (OpenGL, etc.).

⸻

📈 When Is It Preferred?
	•	When you need readability like Python but speed like C.
	•	When you want compiled executables but dislike C++ boilerplate.
	•	When you need tight memory control and modern closures.
	•	When working across graphics APIs or game engines.
	•	When doing embedded or HPC work that must compile to bare-metal binaries.

⸻

🌟 Where It Shines
	•	Crossing worlds: bridging creative scripting with hardcore systems.
	•	Interop-first: no runtime barrier — directly speaks C ABI, ISA, WASM.
	•	Expressiveness: developers can write readable DSL-like code.
	•	Performance: AOT compiled, low overhead, NASM-level control.

⸻

⚡ Performance & Startup
	•	Startup speed: near-instant (like C binaries, not like JVM/CLR).
	•	Execution speed: C/C++ class performance, NASM optimizable.
	•	Memory safety: manual, but with optional managed allocators.

⸻

🔒 Security & Safety
	•	Manual memory is risky — but PlasmaScript balances with:
	•	Refcounted allocator.
	•	Arena reset safety.
	•	Explicit free for ownership clarity.
	•	Sandboxing: WASM backend can run PlasmaScript safely in browser/cloud.
	•	Interop boundaries: FFI/ABI require explicit declarations.

⸻

💡 Why Choose PlasmaScript?
	•	Combines expressive scripting + systems-grade compilation.
	•	Eliminates gap between Python-like creativity and C-like execution.
	•	Supports all modern interop layers (graphics APIs, WASM, ISA).
	•	Provides both manual and managed memory models.
	•	Compiles to real executables with multiple backends.

⸻

🌠 Why Was It Created?

PlasmaScript was created to resolve the long-standing tension between:
	•	Ease of expression (Python, JavaScript, Ruby).
	•	Low-level control (C, Rust, Assembly).
	•	Industrial interop (graphics/game APIs, OS services).

It is designed as a dual-nature language:
	•	Minimal enough to write “Hello World” in one line.
	•	Powerful enough to build an engine, driver, or trading platform.

⸻

🚀 Future Directions
	•	JIT engine alongside AOT (for REPL/live coding).
	•	GPU compute shaders via PlasmaScript syntax.
	•	Auto-vectorization for HPC math kernels.
	•	Secure enclaves: PlasmaScript compiled for TEEs (Intel SGX, ARM TrustZone).
	•	Full package ecosystem (PlasmaHub).

⸻

✅ TL;DR

PlasmaScript is a professional, expressive, AOT-compiled language that:
	•	Reads like Python, compiles like C, interoperates like Rust.
	•	Bridges poetic minimalism with industrial-grade interop.
	•	Is equally at home in AAA game dev, scientific HPC, finance, embedded, or creative coding.
	•	Provides both raw memory control and safe allocators.
	•	Supports FFI/ABI/ISA/WASM without compromise.

It is the language for the engineer, the researcher, and the artist — born to unify speed, safety, and expressiveness in one plasma flow.

⸻


## ~~~~

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
