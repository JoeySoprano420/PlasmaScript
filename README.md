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

⚡ Proper use:

To download, install, set up, and use PlasmaScript from https://github.com/JoeySoprano420/PlasmaScript:

**1. Download**
- Go to the PlasmaScript GitHub repo main page.
- Click the green “Code” button, then “Download ZIP” to get the source files, or clone it with:
  ```
  git clone https://github.com/JoeySoprano420/PlasmaScript.git
  ```

**2. Install**
- PlasmaScript is designed as a compiled language (not a Python package), so you’re looking for its compiler (`plasmascriptc`) in the repo.
- Check for a build script, executable, or install instructions in the repo. If not present, you may need to compile the compiler from source using Python or another build tool depending on the repo’s structure.

**3. Setup**
- PlasmaScript source files have a `.ps` extension.
- The compiler (`plasmascriptc`) can compile `.ps` files to executables, DLLs, or WASM modules using commands like:
  ```
  plasmascriptc program.ps -target exe -o program.exe
  plasmascriptc module.ps -target dll -o module.dll
  plasmascriptc script.ps -target wasm -o script.wasm
  ```
- There may also be a REPL for interactive scripting.

**4. Use**
- Write your PlasmaScript code in `.ps` files. Example Hello World:
  ```
  Prog main() {
      Print ["Hello PlasmaScript!"]
  }
  end
  ```
- Compile using the compiler as described above.
- PlasmaScript supports advanced features: functions, closures, manual memory management, FFI/ABI bindings for C/OpenGL/Vulkan/Unity/Unreal, inline assembly, and more.
- You can import external libraries:
  ```
  Import "opengl32"
  ```
- Use the REPL (if available) or run compiled executables directly.

**Summary:**  
Download the repo, locate or build the compiler (`plasmascriptc`), write your `.ps` code, and use the compiler to build/run your programs. PlasmaScript is intended for both creative scripting and hardcore systems programming, with extensive interoperability and compilation options. Check the README in the repo for further details and example programs.

## ``` Documentation



---

# 🐣 Part 1: The Simplest Program

Every language needs a “Hello World.” In PlasmaScript, there are **many ways** to say it, but here’s the simplest:

```plasmascript
Prog main() {
    Print ["Hello PlasmaScript!"]
}
end
```

**What this means:**

* `Prog main()` = “Start my program here.”
* `{ ... }` = The stuff inside happens when the program runs.
* `Print [...]` = Show text on the screen.
* `end` = Stop the program.

When you run this, the computer says:

```
Hello PlasmaScript!
```

---

# ✏️ Part 2: Talking to the Computer

You can store words or numbers in **variables** (like a labeled box).

```plasmascript
Prog main() {
    let name = "Shay"
    let age = 25
    Print ["My name is " + name]
    Print ["I am " + age]
}
end
```

👉 `let` means “create a new box and put something in it.”

* `name` holds text `"Shay"`.
* `age` holds the number `25`.
* `+` glues text together.

---

# 🔄 Part 3: Decisions (If/Else)

Programs can **decide** things:

```plasmascript
Prog main() {
    let user = "Shay"

    if user == "Shay" {
        Print ["Welcome back!"]
    } else {
        Print ["Hello, stranger."]
    }
}
end
```

👉 If the condition (`user == "Shay"`) is true, it runs the first block. Otherwise, it runs the `else` block.

---

# 🔁 Part 4: Loops

Loops repeat things automatically.

```plasmascript
Prog main() {
    let names = ["Ana", "Ben", "Clara"]

    for n in names {
        Print ["Hello " + n]
    }
}
end
```

👉 This greets every name in the list.
Output:

```
Hello Ana
Hello Ben
Hello Clara
```

---

# 🧩 Part 5: Functions

Functions are **mini-programs inside your program**.

```plasmascript
Func greet(name) {
    Print ["Hello " + name]
}

Prog main() {
    greet("Shay")
    greet("Ana")
}
end
```



---

# 🌀 Part 6: Returning Values

A function can **give something back** using `return`.

```plasmascript
Func add(a, b) {
    return a + b
}

Prog main() {
    let result = add(6, 7)
    Print ["The sum is " + result]
}
end
```

Output:

```
The sum is 13
```

---

# 🎭 Part 7: Anonymous Functions (Lambdas)

You don’t always need to give a function a name — sometimes you just want one on the spot:

```plasmascript
Prog main() {
    let square = Func(x) { return x * x }
    Print [square(5)]
}
end
```

Output: `25`

---

# 📚 Part 8: Collections

PlasmaScript has handy data structures:

* **List**: `[1,2,3]`
* **Tuple**: `(x,y)`
* **Dict** (dictionary): `{name: "Shay", age: 25}`
* **Set**: `{1,2,3}`

And **comprehensions** let you build them fast:

```plasmascript
Prog main() {
    let nums = [x*x for x in [1,2,3,4,5]]
    Print [nums]
}
end
```

Output: `[1,4,9,16,25]`

---

# ⚙️ Part 9: Memory (Advanced)

You can even **talk to memory directly** if you want full control:

```plasmascript
Prog main() {
    let ptr = malloc(32)      ; reserve space
    store(ptr, 0, 42)         ; put 42 in the first slot
    Print [load(ptr, 0)]      ; read it back
    free(ptr)                 ; release it
}
end
```

👉 This is for advanced users (like in C or C++), but PlasmaScript makes it available.

---

# 🌐 Part 10: Talking to Other Languages

PlasmaScript can **call C functions** or graphics libraries like OpenGL:

```plasmascript
Import "opengl32"

Extern "C" Func glClear(mask: number)

Prog main() {
    Print ["Clearing screen..."]
    glClear(0x00004000)
}
end
```

This lets PlasmaScript power **games, graphics, and scientific apps**.

---

# 🚀 How to Think About PlasmaScript

* Like **Python**: readable, beginner-friendly, flexible.
* Like **C**: compiled, fast, with manual memory control if you need it.
* Like **Rust/Go**: modern, safe features (arenas, refcount, managed allocators).
* Like **JS**: closures, lambdas, functional style.

It’s both **fun for beginners** and **serious for professionals**.

---

# ✅ Summary

As a **beginner**, the big things to remember:

1. **`Prog main() { ... } end`** is where your program starts.
2. **`Print [...]`** shows stuff on screen.
3. **`let`** makes variables (boxes for storing things).
4. **Functions** let you organize and reuse code.
5. **If / for** = decisions and loops.
6. Advanced users can control **memory, interop, and performance**.

---




---

# 📘 PlasmaScript Beginner’s Workbook

---

## 🟢 Lesson 1: Your First Program

👉 Every program starts with `Prog main() { ... } end`.

```plasmascript
Prog main() {
    Print ["Hello PlasmaScript!"]
}
end
```

When you run this, the computer prints:

```
Hello PlasmaScript!
```

✅ **Exercise 1.1**

* Change the message to say your name.
* Try writing it using the alternative form:

```plasmascript
Main main() {
    Print ["Hello World!"]
}
run
```

---

## 🟢 Lesson 2: Variables

Variables are like **boxes** that hold information.

```plasmascript
Prog main() {
    let name = "Shay"
    let age = 25
    Print ["Name: " + name]
    Print ["Age: " + age]
}
end
```

✅ **Exercise 2.1**

* Create a variable called `city`.
* Print a sentence like: *"I live in London."*

---

## 🟢 Lesson 3: Decisions

Programs can make **choices** with `if` and `else`.

```plasmascript
Prog main() {
    let mood = "happy"

    if mood == "happy" {
        Print ["Keep smiling!"]
    } else {
        Print ["Cheer up!"]
    }
}
end
```

✅ **Exercise 3.1**

* Write a program that checks if `age` is **18 or more**.
* Print `"Adult"` if true, otherwise `"Child"`.

---

## 🟢 Lesson 4: Loops

Loops let you **repeat** actions.

```plasmascript
Prog main() {
    let names = ["Ana", "Ben", "Clara"]

    for n in names {
        Print ["Hello " + n]
    }
}
end
```

✅ **Exercise 4.1**

* Make a list of 5 numbers.
* Print each number on a new line.

---

## 🟢 Lesson 5: Functions

Functions are **mini-programs** inside your program.

```plasmascript
Func greet(name) {
    Print ["Hello " + name]
}

Prog main() {
    greet("Shay")
    greet("Ana")
}
end
```

✅ **Exercise 5.1**

* Write a function called `square(x)` that returns `x * x`.
* Print the square of 5.

---

## 🟢 Lesson 6: Returning Values

Functions can **give back answers** with `return`.

```plasmascript
Func add(a, b) {
    return a + b
}

Prog main() {
    Print [add(6, 7)]
}
end
```

✅ **Exercise 6.1**

* Write a function called `subtract(a, b)`.
* Print `subtract(10, 3)`.

---

## 🟢 Lesson 7: Lambdas (Anonymous Functions)

Quick **one-time functions**:

```plasmascript
Prog main() {
    let square = Func(x) { return x * x }
    Print [square(4)]
}
end
```

✅ **Exercise 7.1**

* Make a lambda called `double` that doubles a number.
* Print `double(8)`.

---

## 🟢 Lesson 8: Collections

You can make **lists, sets, dicts, and tuples**.

```plasmascript
Prog main() {
    let squares = [x*x for x in [1,2,3,4,5]]
    Print [squares]
}
end
```

Output: `[1,4,9,16,25]`

✅ **Exercise 8.1**

* Make a list of names.
* Build a list `[ "Hello " + n for n in names ]`.
* Print it.

---

## 🟢 Lesson 9: Memory (Advanced but Fun)

PlasmaScript lets you peek under the hood:

```plasmascript
Prog main() {
    let ptr = malloc(16)       ; reserve 16 bytes
    store(ptr, 0, 42)          ; save a value
    Print [load(ptr, 0)]       ; read it back
    free(ptr)                  ; clean up
}
end
```

✅ **Exercise 9.1**

* Allocate memory.
* Store the number `99`.
* Print it.

---

## 🟢 Lesson 10: Talking to the Outside World

PlasmaScript can call **other languages** like C or graphics libraries.

```plasmascript
Import "opengl32"

Extern "C" Func glClear(mask: number)

Prog main() {
    Print ["Screen cleared!"]
    glClear(0x00004000)
}
end
```

✅ **Exercise 10.1**

* Write your own `Extern` function declaration for C’s `puts(text)`.
* Call it to print `"Plasma FFI works!"`.

---

# 🎓 Graduation Project

Build a **tiny calculator**:

```plasmascript
Func add(a, b) { return a + b }
Func sub(a, b) { return a - b }
Func mul(a, b) { return a * b }
Func div(a, b) { return a / b }

Prog main() {
    Print ["2 + 3 = " + add(2,3)]
    Print ["10 - 4 = " + sub(10,4)]
    Print ["6 * 7 = " + mul(6,7)]
    Print ["20 / 5 = " + div(20,5)]
}
end
```

✅ Try adding more operations (like modulus `%`) or extend it to read user input!

---

# ✨ Wrap-Up

* PlasmaScript is **easy to read**, like writing notes to yourself.
* It gives you **Python-like simplicity** *and* **C-like power**.
* Start with simple `Print` statements.
* Work up to loops, functions, lambdas, and interop.
* You can make **games, graphics, tools, or scientific apps** once you’re ready.

---



---

# 🔑 Entry Keywords: `Prog` vs `Main`

Both mean: *“Start my program here.”*

* **`Prog`** = short for **Program**.

  * Feels like a **technical keyword**, used when you’re writing in a formal or canonical style.
  * Example:

    ```plasmascript
    Prog main() {
        Print ["Hello PlasmaScript!"]
    }
    end
    ```

* **`Main`** = short for **Main function**.

  * Feels like **natural English**, or a looser, conversational style.
  * Example:

    ```plasmascript
    Main main() {
        Print ["Hello PlasmaScript!"]
    }
    run
    ```

👉 In practice, they are **synonyms**. PlasmaScript accepts either.
It’s about **style choice**:

* Use **`Prog`** when you want to emphasize *the whole program starts here*.
* Use **`Main`** when you want it to feel more like *this is the main function*.

---

# 🔑 Exit Keywords: `end` vs `run`

Both mean: *“That’s the end of my program.”*

* **`end`** = **formal closure**.

  * Fits with `Prog`.
  * Feels like closing a book.
  * Example:

    ```plasmascript
    Prog main() {
        Print ["Hello PlasmaScript!"]
    }
    end
    ```

* **`run`** = **executive closure**.

  * Fits with `Main`.
  * Feels like you’re pressing the “go” button.
  * Example:

    ```plasmascript
    Main main() {
        Print ["Hello PlasmaScript!"]
    }
    run
    ```

👉 Again, they are **interchangeable**. PlasmaScript lets you pick the one that *feels right for your code’s style*.

---

# 🎨 Why Both Exist

This was an intentional design choice:

* Some developers like **formal, structured syntax** → `Prog … end`.
* Some like **lightweight, conversational syntax** → `Main … run`.

It’s like having **two dialects** of the same language:

* **Formal dialect** (for engineers, compilers, technical docs).
* **Poetic dialect** (for creative coders, artists, or scripting contexts).

---

# ✅ Summary

* **`Prog`** and **`Main`** both start the program.
* **`end`** and **`run`** both finish it.
* They’re **synonyms**, but carry different *flavors*:

  * `Prog … end` = formal, structured.
  * `Main … run` = conversational, lightweight.

---



---

# 📜 PlasmaScript Program Entry/Exit Forms

PlasmaScript allows **two entry keywords** (`Prog`, `Main`) and **two exit keywords** (`end`, `run`).
That makes **4 possible combos**:

---

## 1️⃣ `Prog … end` ✅ **Canonical Form**

```plasmascript
Prog main() {
    Print ["Hello PlasmaScript!"]
}
end
```

* **Style**: Formal, structured, traditional.
* **Use Case**: Teaching, documentation, production-ready code.
* **Why**: Mirrors how many compiled languages (like C) use `main` and a strict `end`.
* **Status**: **Primary canonical form**.

---

## 2️⃣ `Main … run` ✅ **Conversational Form**

```plasmascript
Main main() {
    Print ["Hello PlasmaScript!"]
}
run
```

* **Style**: Lightweight, conversational, playful.
* **Use Case**: Quick scripts, creative coding, demos.
* **Why**: Reads like English: *“Main starts here… now run it.”*
* **Status**: **Accepted canonical variant** (equal to `Prog … end`).

---

## 3️⃣ `Prog … run` ⚡ **Hybrid Shortcut**

```plasmascript
Prog main() {
    Print ["Hello PlasmaScript!"]
}
run
```

* **Style**: Semi-formal hybrid.
* **Use Case**: Allowed for flexibility, but rare in style guides.
* **Why**: Sometimes users mix “start formally” with “finish conversationally.”
* **Status**: **Valid but informal** — not preferred in official codebases.

---

## 4️⃣ `Main … end` ⚡ **Hybrid Shortcut**

```plasmascript
Main main() {
    Print ["Hello PlasmaScript!"]
}
end
```

* **Style**: Semi-formal hybrid.
* **Use Case**: Useful if you prefer `Main` but still want strict closure.
* **Why**: Some users like `Main` but still think in terms of `end` blocks.
* **Status**: **Valid but informal** — works fine, but style guides steer you to either #1 or #2.

---

# 🎨 Why This Duality Exists

* PlasmaScript was designed to **welcome both beginners and professionals**.
* **Beginners** feel comfortable with `Main … run` (like telling a story).
* **Professionals** feel comfortable with `Prog … end` (like engineering precision).
* Hybrids (`Prog … run` and `Main … end`) exist because the parser doesn’t force rigidity — they reflect the *flexible, humanistic* ethos of the language.

---

# ✅ Summary Table

| Entry  | Exit  | Status         | Style          |
| ------ | ----- | -------------- | -------------- |
| `Prog` | `end` | Canonical      | Formal         |
| `Main` | `run` | Canonical      | Conversational |
| `Prog` | `run` | Valid (Hybrid) | Informal       |
| `Main` | `end` | Valid (Hybrid) | Informal       |

---



---

# 📜 PlasmaScript Hello World — All Four Forms

| #     | Entry / Exit Form            | Example Code                                                          | Notes                                                                   |
| ----- | ---------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **1** | `Prog … end` (**Canonical**) | `plasmascript Prog main() {     Print ["Hello PlasmaScript!"] } end ` | The **formal, structured** form. Used in docs, teaching, production.    |
| **2** | `Main … run` (**Canonical**) | `plasmascript Main main() {     Print ["Hello PlasmaScript!"] } run ` | The **conversational** form. Friendly, poetic, great for quick scripts. |
| **3** | `Prog … run` (Hybrid)        | `plasmascript Prog main() {     Print ["Hello PlasmaScript!"] } run ` | Works fine, but **mixes formal start with casual finish**.              |
| **4** | `Main … end` (Hybrid)        | `plasmascript Main main() {     Print ["Hello PlasmaScript!"] } end ` | Works fine, but **mixes casual start with strict closure**.             |

---

# ⚖️ Why Style Guides Avoid the Hybrids

Even though **all 4 are valid**, the hybrids are considered **stylistically inconsistent**:

* 🔹 **`Prog … run`** → Starts formal, ends casual.

  * Feels like starting a legal contract and ending with *“whatever, just go.”*
  * Not “wrong,” but it makes code harder to scan for beginners.

* 🔹 **`Main … end`** → Starts conversational, ends strict.

  * Feels like starting a poem and ending with a bureaucratic stamp.
  * Again, not wrong — just visually “off.”

---

## 🚦 Style Guide Principle

PlasmaScript emphasizes **flow and readability**. Style guides prefer **consistent entry/exit pairs**:

* If you want **formal precision** → use `Prog … end`.
* If you want **poetic minimalism** → use `Main … run`.

Mixing them is **allowed** (because the parser supports both), but it **creates mixed signals** for human readers — which is why style guides recommend sticking to one of the two canonical forms.

---

# ✅ Summary

* **Canonical forms**: `Prog … end` (formal), `Main … run` (conversational).
* **Hybrid forms**: valid, but stylistically discouraged.
* Style guides avoid hybrids because they **reduce consistency**, which is important in team projects, teaching material, and professional codebases.

---

 

---

# 📘 PlasmaScript Style Guide (Core Conventions)

---

## 1️⃣ Entry & Exit Forms

PlasmaScript provides two **canonical pairs** and two **hybrids**.

* ✅ **Preferred Canonical Forms**

  * `Prog … end` → **formal, structured**
  * `Main … run` → **conversational, lightweight**

* ⚠️ **Allowed but Discouraged**

  * `Prog … run`
  * `Main … end`

> **Rule of Thumb**: Pick one canonical form and use it consistently across your project.
>
> * Use `Prog … end` for libraries, production code, and teaching materials.
> * Use `Main … run` for quick scripts, creative coding, and demos.

---

## 2️⃣ Naming Conventions

### Variables

* Use **lowercase\_with\_underscores** for variables.

```plasmascript
let user_name = "Shay"
let total_score = 42
```

### Functions

* Use **camelCase** for functions.

```plasmascript
Func greetUser(name) {
    Print ["Hello " + name]
}
```

### Types & Modules

* Use **CapitalizedWords** (PascalCase).

```plasmascript
Import "Graphics"
let window: Window = createWindow()
```

### Constants

* Use **ALL\_CAPS** for constants.

```plasmascript
let PI = 3.14159
```

---

## 3️⃣ Indentation & Braces

* Always use **4 spaces** (no tabs).
* Opening brace `{` goes on the **same line**.
* Closing brace `}` goes on its **own line**.

✅ Correct:

```plasmascript
Func add(a, b) {
    return a + b
}
```

❌ Incorrect:

```plasmascript
Func add(a, b)
{
return a+b}
```

---

## 4️⃣ Print & Expressions

* Always wrap `Print` arguments in square brackets `[...]`.
* Use `+` for string concatenation.

✅ Correct:

```plasmascript
Print ["Hello " + name]
```

❌ Incorrect:

```plasmascript
Print("Hello ", name)
```

---

## 5️⃣ Functions & Returns

* Use **explicit `return`** for clarity.
* Don’t rely on implicit returns (they aren’t supported).

✅ Correct:

```plasmascript
Func add(a, b) {
    return a + b
}
```

---

## 6️⃣ Imports & Exports

* Place all `Import` and `Export` statements at the **top of the file**.
* Group related imports together.

```plasmascript
Import "math"
Import "graphics"

Export Func add(a, b) { return a + b }
Export Func sub(a, b) { return a - b }
```

---

## 7️⃣ Memory Operations

* Only use `malloc`, `store`, `load`, `free` when absolutely necessary.
* For normal programs, prefer lists, dicts, or sets.
* Always `free` what you `malloc`.

✅ Correct:

```plasmascript
let ptr = malloc(16)
store(ptr, 0, 42)
Print [load(ptr, 0)]
free(ptr)
```

---

## 8️⃣ Comprehensions

* Keep comprehensions on a **single line** if short.
* If they’re long, break them with indentation.

✅ Short:

```plasmascript
let squares = [x*x for x in [1,2,3,4,5]]
```

✅ Long:

```plasmascript
let pairs = [
    (x, y)
    for x in [1,2,3]
    for y in [4,5,6]
]
```

---

## 9️⃣ Comments

* Use `;` for inline or standalone comments.
* Keep comments **short and clear**.

```plasmascript
; This function greets the user
Func greetUser(name) {
    Print ["Hello " + name]
}
```

---

## 🔟 Best Practices

1. **Pick one entry/exit form** (`Prog … end` OR `Main … run`) and stick to it.
2. **Keep functions short** — aim for 10–20 lines max.
3. **Avoid magic numbers** — name them as constants.
4. **Prefer collections** (`list`, `dict`, `set`) over manual memory unless you need raw performance.
5. **Always clean up memory** (`free`, `release`, `arena_reset`).
6. **Be explicit** with types when clarity matters (`let x: number = 42`).

---

# ✅ Summary

* PlasmaScript encourages **readability and consistency**.
* You can write formally (`Prog … end`) or conversationally (`Main … run`).
* Style guides avoid hybrids because they mix tones, reducing clarity.
* Follow naming, indentation, and import/export rules to keep projects professional.

---



---

# 📘 PlasmaScript Handbook (Draft)

---

## 🏁 Chapter 1: Introduction

**PlasmaScript** is a minimalist yet powerful programming language designed to balance **expressive readability** with **industrial-grade compilation**.

* **Minimal**: You can write `Prog main() { Print ["hi"] } end` and it works.
* **Expressive**: You can use functions, closures, lambdas, and comprehensions.
* **Powerful**: You can interop with C, OpenGL, Vulkan, DirectX, Unity, Unreal, and WASM.
* **Safe**: Optional memory management (arenas, bump allocators, refcounts).
* **Fast**: AOT-compiled into `.exe`, `.so`, `.dll`, `.dylib` or WASM.

---

## 🟢 Chapter 2: Program Structure

Every PlasmaScript program starts and ends with one of two **canonical forms**:

* **Formal**:

```plasmascript
Prog main() {
    Print ["Hello PlasmaScript!"]
}
end
```

* **Conversational**:

```plasmascript
Main main() {
    Print ["Hello PlasmaScript!"]
}
run
```

> ⚠️ Hybrids (`Prog … run`, `Main … end`) are valid but discouraged for consistency.

---

## ✏️ Chapter 3: Variables & Types

### Declaring variables

```plasmascript
let name = "Shay"
let age: number = 25
```

### Built-in types

| Type     | Example          |
| -------- | ---------------- |
| `text`   | `"hello"`        |
| `number` | `42`             |
| `bool`   | `true`, `false`  |
| `list`   | `[1, 2, 3]`      |
| `dict`   | `{name: "Shay"}` |
| `set`    | `{1, 2, 3}`      |
| `tuple`  | `(1, "a")`       |

---

## 🔄 Chapter 4: Control Flow

### If/Else

```plasmascript
if x > 10 {
    Print ["Big"]
} else {
    Print ["Small"]
}
```

### Loops

```plasmascript
for n in [1,2,3] {
    Print [n]
}
```

### Comprehensions

```plasmascript
let squares = [x*x for x in [1,2,3,4,5]]
let dicts = {x: x*x for x in [1,2,3]}
let sets = {x*x for x in [1,2,3]}
let gens = (x*x for x in [1,2,3])
```

---

## 🧩 Chapter 5: Functions

### Defining functions

```plasmascript
Func add(a, b) {
    return a + b
}
```

### Calling functions

```plasmascript
Print [add(6, 7)]
```

### Anonymous functions (Lambdas)

```plasmascript
let square = Func(x) { return x * x }
Print [square(5)]
```

### Closures

```plasmascript
let makeAdder = Func(x) {
    return Func(y) { return x + y }
}

let add5 = makeAdder(5)
Print [add5(3)] ; prints 8
```

---

## 🧮 Chapter 6: Memory

PlasmaScript gives you **manual + managed memory options**.

### Manual Allocation

```plasmascript
let ptr = malloc(16)
store(ptr, 0, 42)
Print [load(ptr, 0)]
free(ptr)
```

### Arena Allocator

```plasmascript
let arena = arena_init(128)
let p = arena_alloc(arena, 16)
arena_reset(arena)
```

### Refcounted Memory

```plasmascript
let obj = rc_alloc(32)
retain(obj)
release(obj)
```

### Bump Allocator

```plasmascript
let bump = bump_init(64)
let q = bump_alloc(bump, 8)
bump_reset(bump)
```

---

## 🌐 Chapter 7: Interoperability

### Importing libraries

```plasmascript
Import "math"
Import "opengl32"
```

### Extern/Export

```plasmascript
Extern "C" Func glClear(mask: number)
Export Func add(a, b) { return a + b }
```

### Inline Dodecagram

```plasmascript
Inline { dgm(0xDE, 0xAD, 0xBE, 0xEF) }
```

---

## 🛠 Chapter 8: Style Guide

* Pick **one canonical form** (`Prog … end` OR `Main … run`).
* Use **lowercase\_with\_underscores** for variables.
* Use **camelCase** for functions.
* Use **PascalCase** for modules/types.
* Use **ALL\_CAPS** for constants.
* Always free memory you allocate.
* Keep functions under \~20 lines.
* Keep comprehensions readable (single-line if short).

---

## 🚀 Chapter 9: Use Cases

PlasmaScript can be used for:

* Systems programming (manual memory, NASM backend).
* Game development (OpenGL/Vulkan/DirectX/Unity/Unreal interop).
* Scientific computing (fast comprehensions, closures).
* Finance/HPC (compiled `.exe` with predictable performance).
* Creative coding (expressive, poetic syntax).
* Web/cloud (WASM backend).

---

## 🔮 Chapter 10: Future

* JIT support for live coding.
* GPU shaders in native PlasmaScript syntax.
* Auto-vectorization for math.
* Secure enclave compilation.
* PlasmaHub (package manager).

---

# ✅ Summary

The **PlasmaScript Handbook** provides:

* A **beginner-friendly entry point** (`Print ["Hello"]`)
* A **professional standard** (memory, FFI, NASM, LLVM)
* A **stylistic guide** (formal vs conversational dialects)
* A roadmap for **games, HPC, finance, embedded, and creative arts**.

---
Reference Manual can be found at the following link:
https://github.com/JoeySoprano420/PlasmaScript/edit/main/docs/FormingPrograms.md
