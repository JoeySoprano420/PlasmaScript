# 📘 PlasmaScript: The Complete Language Manual (Draft)

---

## 📖 Table of Contents (continued)

4. **Syntax Reference**

   * Comments
   * Variables & Types
   * Output (`Print`)
   * Input (`Input`)
   * Control Flow (`if`, `else`, `for`)
   * Functions & Returns
   * Lambdas & Closures
   * Collections (list, dict, set, tuple)
   * Comprehensions (list, dict, set, generator)
   * Modules & Imports
   * Events

5. **Program Structure**

   * Entry keywords (`Prog` vs `Main`)
   * Exit keywords (`end` vs `run`)
   * Canonical vs hybrid forms
   * Example chart (all 4 Hello Worlds)

6. **Memory Management**

   * Manual (`malloc`, `store`, `load`, `free`)
   * Arena Allocators
   * Refcounted Objects
   * Bump Allocators
   * Best Practices

7. **Interoperability**

   * Import/Export
   * C ABI Bindings
   * OpenGL, Vulkan, DirectX, Unity, Unreal
   * Inline Dodecagram
   * WASM Interop

8. **Style Guide**

   * Entry/Exit choice
   * Naming conventions
   * Indentation & braces
   * Print usage
   * Imports/exports
   * Memory safety rules
   * Comments

9. **Beginner’s Tutorial (Workbook)**

   * Lesson 1: Hello World
   * Lesson 2: Variables
   * Lesson 3: Decisions
   * Lesson 4: Loops
   * Lesson 5: Functions
   * Lesson 6: Returning Values
   * Lesson 7: Lambdas
   * Lesson 8: Collections & Comprehensions
   * Lesson 9: Memory (intro)
   * Lesson 10: Interop basics
   * Graduation project: Calculator

10. **Use Cases & Industries**

    * Systems Programming
    * Game Development
    * Scientific Computing
    * Finance & HPC
    * Creative Coding
    * Embedded Systems

11. **Performance & Safety**

    * Startup speed
    * AOT compilation
    * Memory models
    * Safety balance (manual vs managed)

12. **Future Roadmap**

    * JIT/live coding
    * GPU shaders
    * Auto-vectorization
    * Secure enclaves
    * Package ecosystem (PlasmaHub)

13. **Appendices**

    * Full Hello World Suite (all forms)
    * Reserved Keywords
    * Quick Syntax Cheat Sheet

---

## 🟢 Chapter 4: Syntax Reference

### 💬 Comments

Use `;` for comments:

```plasmascript
; This is a comment
let x = 42  ; Inline comment
```

---

### 🧠 Variables & Types

```plasmascript
let name = "Shay"
let age: number = 25
```

**Built-in types:**

| Type     | Example          |
| -------- | ---------------- |
| `text`   | `"hello"`        |
| `number` | `42`             |
| `bool`   | `true`, `false`  |
| `list`   | `[1,2,3]`        |
| `dict`   | `{name: "Shay"}` |
| `set`    | `{1,2,3}`        |
| `tuple`  | `(42, "hi")`     |

---

### 📤 Output

```plasmascript
Print ["Hello PlasmaScript!"]
```

---

### 📥 Input

```plasmascript
let name = Input("What’s your name?")
Print ["Hello " + name]
```

---

### 🔁 Control Flow

**If/Else:**

```plasmascript
if x > 10 {
    Print ["Big"]
} else {
    Print ["Small"]
}
```

**Loops:**

```plasmascript
for n in [1,2,3] {
    Print [n]
}
```

---

### 🧩 Functions

```plasmascript
Func add(a, b) {
    return a + b
}

Prog main() {
    Print [add(6,7)]
}
end
```

---

### 🌀 Lambdas & Closures

```plasmascript
let square = Func(x) { return x * x }
Print [square(5)]

let makeAdder = Func(x) {
    return Func(y) { return x + y }
}
let add5 = makeAdder(5)
Print [add5(3)] ; 8
```

---

### 📦 Collections & Comprehensions

```plasmascript
let squares = [x*x for x in [1,2,3,4,5]]
let dicts = {x: x*x for x in [1,2,3]}
let sets = {x*x for x in [1,2,3]}
let gens = (x*x for x in [1,2,3])
```

---

### 📚 Modules & Imports

```plasmascript
Import "math"
Export Func add(a, b) { return a + b }
```

---

### 🧨 Events

```plasmascript
on start {
    Print ["Program started."]
}
```

---

## 🟢 Chapter 5: Program Structure

### Entry & Exit Keywords

* `Prog … end` = **formal, canonical**
* `Main … run` = **conversational, canonical**
* Hybrids are allowed (`Prog … run`, `Main … end`), but discouraged.

---

### All 4 Hello World Forms

```plasmascript
; Canonical
Prog main() { Print ["Hello"] } end

; Canonical
Main main() { Print ["Hello"] } run

; Hybrid (valid but discouraged)
Prog main() { Print ["Hello"] } run

; Hybrid (valid but discouraged)
Main main() { Print ["Hello"] } end
```

---



---

# 🟢 Chapter 6: Memory Management

---

## 6.1 Overview

PlasmaScript supports **two models of memory**:

1. **High-level, safe collections** → lists, dicts, sets, tuples.

   * No cleanup needed.
   * Ideal for most code.

2. **Low-level, manual or semi-managed allocation** → `malloc`, `free`, arenas, bump allocators, refcounts.

   * Gives you control over performance.
   * Used for high-performance systems, game engines, and embedded code.

---

## 6.2 Manual Allocation

You can allocate raw memory using **`malloc`**, store values with **`store`**, read them with **`load`**, and release them with **`free`**.

```plasmascript
Prog main() {
    let ptr = malloc(16)     ; reserve 16 bytes
    store(ptr, 0, 42)        ; save 42 at position 0
    let x = load(ptr, 0)     ; read it back
    Print [x]
    free(ptr)                ; release the memory
}
end
```

### Notes

* Memory is **indexed by bytes**.
* Forgetting `free(ptr)` will cause a **memory leak**.
* This model is similar to C.

---

## 6.3 Arena Allocators

An **arena** lets you allocate many things quickly, then reset all at once.
This is efficient when you create lots of temporary objects.

```plasmascript
Prog main() {
    let arena = arena_init(128)       ; make a 128-byte arena
    let p1 = arena_alloc(arena, 16)   ; allocate 16 bytes
    let p2 = arena_alloc(arena, 32)   ; allocate 32 bytes

    store(p1, 0, 7)
    Print [load(p1, 0)]

    arena_reset(arena)                ; frees ALL allocations at once
}
end
```

### Notes

* Faster than malloc/free for bulk allocations.
* Best for short-lived objects in loops or functions.
* Everything inside the arena dies together.

---

## 6.4 Refcounted Memory

Some objects can be **reference-counted**.
When the count goes to zero, the object is freed automatically.

```plasmascript
Prog main() {
    let obj = rc_alloc(32)    ; allocate with refcount
    retain(obj)               ; increment
    release(obj)              ; decrement
    release(obj)              ; count hits 0 → frees
}
end
```

### Notes

* Similar to smart pointers in C++ or ARC in Swift.
* Safer than manual `malloc/free`.
* You still must `release` what you `retain`.

---

## 6.5 Bump Allocators

A **bump allocator** is like an arena, but it just “bumps” a pointer forward.
It’s the fastest way to allocate memory linearly.

```plasmascript
Prog main() {
    let bump = bump_init(64)           ; make a 64-byte bump allocator
    let q1 = bump_alloc(bump, 8)       ; allocate 8 bytes
    let q2 = bump_alloc(bump, 16)      ; allocate 16 bytes

    store(q1, 0, 99)
    Print [load(q1, 0)]

    bump_reset(bump)                   ; wipe everything
}
end
```

### Notes

* Extremely fast.
* Works best for stack-like or linear lifetimes.
* Reset wipes everything at once.

---

## 6.6 Safety Rules

1. **Always free what you allocate** (unless using arenas/bump).
2. **Do not double-free** → freeing the same pointer twice is an error.
3. **Do not use freed memory** → accessing after `free` causes crashes.
4. **Prefer high-level collections** unless you need raw performance.
5. **For short-term lifetimes**, use arenas or bumps.
6. **For shared objects**, use refcounting.

---

## 6.7 When to Use What

| Model                  | When to Use                                       |
| ---------------------- | ------------------------------------------------- |
| **Lists, Dicts, Sets** | Everyday programming, safe defaults.              |
| **malloc/free**        | Systems programming, fine-grained control.        |
| **Arena**              | Many temporary objects, clear all at once.        |
| **Refcount**           | Shared objects, automatic freeing.                |
| **Bump**               | High-performance, stack-like allocation patterns. |

---

## 6.8 Example: Mixed Memory Styles

```plasmascript
Prog main() {
    ; High-level safe collections
    let names = ["Ana", "Ben", "Clara"]
    for n in names { Print [n] }

    ; Arena for short-term objects
    let arena = arena_init(64)
    let tmp = arena_alloc(arena, 8)
    store(tmp, 0, 123)
    Print [load(tmp, 0)]
    arena_reset(arena)

    ; Refcount for shared data
    let obj = rc_alloc(16)
    retain(obj)
    release(obj)
    release(obj) ; frees
}
end
```

---

## 6.9 Summary

* PlasmaScript gives you **the full spectrum**:

  * From **high-level safe lists** → to **manual system allocators**.
* You choose the model depending on your project:

  * Everyday scripts → lists/dicts.
  * High-performance systems → arenas/bump allocators.
  * Shared lifetimes → refcounting.
* This makes PlasmaScript suitable for both **beginners** and **low-level systems engineers**.

---




---

# 🟢 Chapter 7: Interoperability

---

## 7.1 Overview

One of PlasmaScript’s biggest strengths is that it **doesn’t live in a bubble**.

It was designed to:

* Call **C functions** directly.
* Import **graphics APIs** like OpenGL, Vulkan, DirectX.
* Bind with **Unity** and **Unreal Engine**.
* Export to **WebAssembly (WASM)** for the web/cloud.
* Inline **Dodecagram (base-12) assembly** for ultimate low-level control.

This makes PlasmaScript a bridge between **expressive scripting** and **systems-grade interop**.

---

## 7.2 Importing Libraries

Use `Import` to bring in external libraries or standard modules.

```plasmascript
Import "math"
Import "opengl32"
```

* On Windows → `"opengl32"` maps to `opengl32.dll`.
* On Linux → `"GL"` maps to `libGL.so`.
* On macOS → `"OpenGL"` maps to system frameworks.

---

## 7.3 Extern & Export

### Declaring External Functions

```plasmascript
Extern "C" Func puts(msg: text)
```

This declares the C function `puts`, which prints a string.

### Example

```plasmascript
Extern "C" Func puts(msg: text)

Prog main() {
    puts("Hello from PlasmaScript → C!")
}
end
```

Output:

```
Hello from PlasmaScript → C!
```

---

### Exporting PlasmaScript Functions

```plasmascript
Export Func add(a: number, b: number) {
    return a + b
}
```

This makes the PlasmaScript function visible to **other languages** (C, Rust, etc.).

---

## 7.4 OpenGL Example

```plasmascript
Import "opengl32"

Extern "C" Func glClear(mask: number)
Extern "C" Func glClearColor(r: number, g: number, b: number, a: number)

Prog main() {
    Print ["Clearing screen..."]
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(0x00004000) ; GL_COLOR_BUFFER_BIT
}
end
```

👉 PlasmaScript code here looks as clean as a script, but compiles to **native OpenGL calls**.

---

## 7.5 Vulkan / DirectX Example

```plasmascript
Import "vulkan"
Import "d3d12"

Extern "C" Func vkCreateInstance(info, alloc, instance)
Extern "C" Func D3D12CreateDevice(adapter, level, riid, device)
```

These bindings allow you to directly construct Vulkan or DirectX contexts.

---

## 7.6 Unity / Unreal Integration

PlasmaScript can act as a **scripting layer** for Unity and Unreal:

### Unity Example (C# Bridge)

```plasmascript
Extern "C" Func UnityPrint(msg: text)

Prog main() {
    UnityPrint("PlasmaScript speaking inside Unity!")
}
end
```

### Unreal Example (C++ Bridge)

```plasmascript
Extern "C" Func UE_Log(msg: text)

Prog main() {
    UE_Log("PlasmaScript powering Unreal scripting")
}
end
```

---

## 7.7 Inline Dodecagram Assembly

For extreme low-level control, you can embed **Dodecagram (base-12) assembly instructions** directly.

```plasmascript
Inline { dgm(0xA1, 0xB2, 0xC3) }
```

* **`Inline {}`** → raw block.
* **`dgm(...)`** → base-12 encoded instruction sequence.
* Compiles into **direct x64 machine instructions**.

This is useful for:

* Cryptography
* Custom allocators
* CPU instruction tuning
* Hobbyist systems hacking

---

## 7.8 WebAssembly (WASM)

PlasmaScript can compile to **WebAssembly** modules, making it web-ready.

```plasmascript
Export Func add(a: number, b: number) { return a + b }
```

When compiled to WASM, this becomes callable from JavaScript:

```javascript
const wasm = await WebAssembly.instantiateStreaming(fetch("prog.wasm"));
console.log(wasm.instance.exports.add(2, 3)); // → 5
```

---

## 7.9 Interop Safety

PlasmaScript balances interop **power** with **clarity**:

1. All externs must declare a **calling convention** (`Extern "C"`).
2. Types must be explicit when crossing ABI boundaries.
3. Inline Dodecagram is raw power — use carefully.
4. WASM exports/imports follow strict type signatures.

---

## 7.10 Summary

* PlasmaScript can **import libraries** (`Import "math"`, `Import "opengl32"`).
* **Extern** declares outside functions.
* **Export** makes PlasmaScript functions visible.
* Supports full **graphics APIs** (OpenGL, Vulkan, DirectX).
* Works with **Unity and Unreal** as a scripting language.
* **Inline Dodecagram** provides raw instruction control.
* **WASM** makes it web- and cloud-compatible.

PlasmaScript is one of the few languages that is **as comfortable talking to C as it is rendering a 3D scene in Unity, or running inside a browser as WASM.**

---




---

# 🟢 Chapter 8: Style Guide

---

## 8.1 Entry & Exit Forms

PlasmaScript allows multiple program entry/exit pairs, but **only two are canonical**:

* ✅ **Formal**:

  ```plasmascript
  Prog main() {
      Print ["Hello"]
  }
  end
  ```

* ✅ **Conversational**:

  ```plasmascript
  Main main() {
      Print ["Hello"]
  }
  run
  ```

⚠️ Hybrids (`Prog … run`, `Main … end`) are **valid but discouraged** for style consistency.

> **Rule:** Pick one canonical form for your project and use it consistently.

---

## 8.2 Naming Conventions

| Item          | Convention                   | Example                      |
| ------------- | ---------------------------- | ---------------------------- |
| Variables     | `lowercase_with_underscores` | `user_name`, `total_score`   |
| Functions     | `camelCase`                  | `greetUser`, `addTwoNumbers` |
| Types/Modules | `PascalCase`                 | `Window`, `MathLib`          |
| Constants     | `ALL_CAPS`                   | `PI`, `MAX_USERS`            |

---

## 8.3 Indentation & Braces

* Use **4 spaces** (no tabs).
* Opening `{` goes on the **same line**.
* Closing `}` goes on its **own line**.

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

## 8.4 Print & Expressions

Always wrap `Print` arguments in `[...]`.

✅ Correct:

```plasmascript
Print ["Hello " + name]
```

❌ Incorrect:

```plasmascript
Print("Hello ", name)
```

---

## 8.5 Functions & Returns

* Always use **explicit `return`**.
* Don’t rely on implicit return (not supported).

✅ Correct:

```plasmascript
Func multiply(a, b) {
    return a * b
}
```

---

## 8.6 Imports & Exports

* Place all imports at the **top** of the file.
* Group related imports.
* Export functions explicitly if meant for reuse.

```plasmascript
Import "math"
Import "graphics"

Export Func add(a, b) { return a + b }
Export Func sub(a, b) { return a - b }
```

---

## 8.7 Memory Safety

* Only use `malloc`/`free` if necessary.
* Prefer collections (`list`, `dict`, `set`) when possible.
* Always `free` what you `malloc`.
* Avoid double-free or use-after-free.
* Use arenas/bump allocators for temporary data.
* Use refcounting for shared lifetimes.

---

## 8.8 Comprehensions

* Keep one-liners short.

```plasmascript
let squares = [x*x for x in [1,2,3,4,5]]
```

* Break long comprehensions across lines:

```plasmascript
let pairs = [
    (x, y)
    for x in [1,2,3]
    for y in [4,5,6]
]
```

---

## 8.9 Comments

* Use `;` for single-line comments.
* Keep comments **short and meaningful**.

```plasmascript
; Greet the user by name
Func greetUser(name) {
    Print ["Hello " + name]
}
```

---

## 8.10 Best Practices

1. **Choose one canonical entry/exit pair** and stay consistent.
2. **Keep functions small** (10–20 lines max).
3. **Avoid “magic numbers”** — define them as constants.
4. **Use descriptive names** for variables and functions.
5. **Use comprehensions for clarity**, not for code golf.
6. **Prefer high-level collections**, unless you need raw memory.
7. **Organize imports/exports at the top** for visibility.
8. **Clean up memory** (`free`, `release`, `arena_reset`) when managing manually.
9. **Follow naming conventions** to make code universally readable.
10. **Comment wisely** — enough to clarify intent, but not to clutter.

---

## 8.11 Example of Styled Code

```plasmascript
Import "math"

; Calculate squares of numbers and print them
Func square(x: number) {
    return x * x
}

Prog main() {
    let nums = [1,2,3,4,5]
    let results = [square(n) for n in nums]

    for r in results {
        Print ["Square: " + r]
    }
}
end
```

---

## 8.12 Summary

* PlasmaScript’s style guide prioritizes **clarity and consistency**.
* Use **formal (`Prog … end`)** or **conversational (`Main … run`)** — not hybrids.
* Follow **naming conventions**, **indentation**, and **import/export rules**.
* Always be explicit with **returns** and **memory safety**.
* Code should **read like a story, but compile like a machine**.

---


