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




---

# 🟢 Chapter 9: Beginner’s Tutorial Workbook

---

## 9.1 Introduction

Welcome! 🎉 This workbook is your **guided journey** into PlasmaScript.

* No experience needed.
* Each lesson has examples + exercises.
* Start simple → build up to real programs.

By the end, you’ll write a **calculator**, understand **functions**, and even see how PlasmaScript can talk to other languages.

---

## 9.2 Lesson 1: Hello World

Every program starts with `Prog main() { … } end` or `Main main() { … } run`.

```plasmascript
Prog main() {
    Print ["Hello PlasmaScript!"]
}
end
```

When run, it prints:

```
Hello PlasmaScript!
```

✅ **Exercise 1.1**

* Change the message to say your own name.
* Try the alternative style with `Main … run`.

---

## 9.3 Lesson 2: Variables

Variables are like **boxes** where you store information.

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

* Create a variable `city`.
* Print: *"I live in X."*

---

## 9.4 Lesson 3: Decisions

Programs can make choices with `if` and `else`.

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

## 9.5 Lesson 4: Loops

Loops repeat things.

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
* Print each number on its own line.

---

## 9.6 Lesson 5: Functions

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

* Write a function `square(x)` that returns `x * x`.
* Print `square(5)`.

---

## 9.7 Lesson 6: Returning Values

Functions can give back answers with `return`.

```plasmascript
Func add(a, b) {
    return a + b
}

Prog main() {
    Print ["The sum is " + add(6, 7)]
}
end
```

✅ **Exercise 6.1**

* Write a function `subtract(a, b)` that returns `a - b`.
* Print `subtract(10, 3)`.

---

## 9.8 Lesson 7: Lambdas (Anonymous Functions)

Sometimes you just want a quick function without naming it.

```plasmascript
Prog main() {
    let square = Func(x) { return x * x }
    Print [square(4)]
}
end
```

✅ **Exercise 7.1**

* Create a lambda `double(x)` that returns `x * 2`.
* Print `double(7)`.

---

## 9.9 Lesson 8: Collections & Comprehensions

PlasmaScript supports lists, dicts, sets, and tuples.

```plasmascript
Prog main() {
    let squares = [x*x for x in [1,2,3,4,5]]
    Print [squares]
}
end
```

Output:

```
[1, 4, 9, 16, 25]
```

✅ **Exercise 8.1**

* Make a list of names.
* Build `[ "Hello " + n for n in names ]`.
* Print it.

---

## 9.10 Lesson 9: Memory (Advanced Peek)

You can even control memory like C.

```plasmascript
Prog main() {
    let ptr = malloc(16)     ; reserve 16 bytes
    store(ptr, 0, 42)        ; save 42
    Print [load(ptr, 0)]     ; print 42
    free(ptr)                ; release memory
}
end
```

✅ **Exercise 9.1**

* Allocate 8 bytes.
* Store the number `99`.
* Print it.

---

## 9.11 Lesson 10: Interop Basics

PlasmaScript can talk to other languages.

```plasmascript
Extern "C" Func puts(msg: text)

Prog main() {
    puts("Hello from PlasmaScript → C!")
}
end
```

✅ **Exercise 10.1**

* Write an extern for C’s `abs(x)` (absolute value).
* Call it on `-42`.

---

## 9.12 Graduation Project: Calculator

Build a tiny calculator with functions.

```plasmascript
Func add(a, b) { return a + b }
Func sub(a, b) { return a - b }
Func mul(a, b) { return a * b }
Func div(a, b) { return a / b }

Prog main() {
    Print ["2 + 3 = " + add(2, 3)]
    Print ["10 - 4 = " + sub(10, 4)]
    Print ["6 * 7 = " + mul(6, 7)]
    Print ["20 / 5 = " + div(20, 5)]
}
end
```

✅ **Challenge**

* Add `mod(a, b)` for remainder.
* Make the program take user input with `Input()`.

---

## 9.13 Summary

* You now know **variables, loops, decisions, functions, lambdas, collections, memory, and interop**.
* PlasmaScript can be both **fun for beginners** and **powerful for pros**.
* With just these lessons, you can already write **real programs**.

---




---

# 🟢 Chapter 10: Use Cases & Industries (Expanded)

---

## 10.1 Who Uses PlasmaScript?

* **Beginners & Students** → because the syntax is welcoming and intuitive.
* **Systems Programmers** → because they get C-like control without the boilerplate.
* **Game Developers** → because PlasmaScript compiles natively and can directly call graphics APIs.
* **Scientists & Analysts** → because comprehensions and closures make modeling easy, while compiled speed ensures efficiency.
* **Finance & HPC Engineers** → because deterministic, low-latency execution matters.
* **Embedded Developers** → because NASM + `.bin` output allows bare-metal deployment.
* **Artists & Creative Coders** → because the `Main … run` form makes code poetic and expressive.

---

## 10.2 Real-World Applications

### 🖥 Systems Software

* CLI tools, utilities, OS modules.
* Lightweight server daemons and data parsers.
* Example: Writing a custom **file indexer** or **network packet sniffer**.

### 🎮 Game Development

* AI scripting inside Unity or Unreal.
* Procedural content generators using comprehensions.
* Example: **OpenGL shader bootstrap** or **custom physics routine**.

### 🔬 Science & Research

* Numerical models for simulations.
* Data preprocessing for large datasets.
* Example: Running **climate models** or **particle simulations**.

### 💹 Finance & HPC

* Real-time risk assessment models.
* Trading bots needing deterministic execution.
* Example: Compiling **low-latency trading algorithms** directly to `.exe`.

### 🎨 Creative Arts

* Interactive art installations.
* Web-based WASM visuals and music generators.
* Example: A **generative art demo** in PlasmaScript compiled to WASM for galleries.

### 🤖 Embedded & IoT

* Robotics control loops.
* Sensor-driven mini-apps on microcontrollers.
* Example: Running a **bump-allocator-driven firmware routine**.

### 📚 Education

* Coding bootcamps, high school CS courses, intro to programming books.
* Example: Teaching beginners with the **Main … run** dialect while experts use `Prog … end`.

---

## 10.3 Where PlasmaScript Shines

* **As a Teaching Language** → because `Print ["Hello"]` is as simple as it gets, but grows into full memory allocators and extern calls.
* **As a Systems Language** → because it outputs NASM and LLVM IR, giving full AOT-compiled `.exe` performance.
* **In Game Dev** → because you can literally write a `glClear` call in PlasmaScript and it just works.
* **For HPC/Finance** → because of predictable execution speed with no hidden garbage collector pauses.
* **In Web/Cloud** → because WASM export makes PlasmaScript run natively inside browsers and cloud runtimes.
* **In Creative Coding** → because of its poetic, conversational syntax (`Main … run`) that makes art code feel alive.

---

## 10.4 Edge Cases & Special Uses

* **Security Research** → inline Dodecagram assembly lets you craft exact ISA sequences.
* **Shader Languages** → PlasmaScript can be embedded into GPU workflows.
* **Hybrid AI Systems** → closures and functional style combine with FFI to link to ML libraries.
* **Cross-disciplinary Coding** → where beginners and pros must share codebases (education → research pipelines).

---

## 10.5 Industry Adoption Forecast

* **High Early Adoption** →

  * Game dev (indies love expressive syntax + compiled speed).
  * Education (bootcamps and schools love teaching readability).
* **Gradual Adoption** →

  * Finance and HPC (compile pipelines take time to integrate).
  * Embedded (toolchain maturity required).
* **Long-term Adoption** →

  * Large-scale enterprise (needs a stable ecosystem first).

---

## 10.6 Summary

PlasmaScript is:

* **Accessible for beginners** (clear, readable, conversational).
* **Powerful for professionals** (manual memory, NASM, interop).
* **Versatile across domains** — education, games, science, finance, embedded, creative arts.
* **Future-proof** with WASM, OpenGL/Vulkan, and native `.exe` support.

👉 It shines wherever people want **expressive code** that can also compile into **serious executables**.

---




---

# 🟢 Chapter 11: Performance & Safety

---

## 11.1 Startup Speed

PlasmaScript is designed to be **fast to start and predictable in execution**:

* **AOT (Ahead-of-Time) Compilation** → PlasmaScript compiles to `.exe` (or `.so`, `.dll`, `.dylib`, `.wasm`) before execution.
* Programs start **instantly** since there is no interpreter overhead.
* Typical startup: **milliseconds**, competitive with C and Rust.

Example:

```plasmascript
Main main() {
    Print ["PlasmaScript starts instantly!"]
}
run
```

Runs as fast as any compiled binary.

---

## 11.2 AOT vs JIT

* **AOT (default)**

  * Compiles to machine code before execution.
  * Produces `.exe` and `.wasm`.
  * Predictable performance.
  * Ideal for systems, games, finance.

* **JIT (future option)**

  * Enables live coding, interactive scripting.
  * Not default, but supported in future roadmap.
  * Useful for prototyping or hot-reload in game dev.

**Comparison:**

* PlasmaScript → AOT by default, like C and Rust.
* Python, Java, C# → rely on interpreters or JIT.
* Result: PlasmaScript avoids **warm-up time** and hidden slowdowns.

---

## 11.3 Execution Performance

PlasmaScript performance is:

* Comparable to **C** when compiled to NASM.
* Within \~5–10% of **Rust** for most workloads.
* Far faster than **Python** (10×–100× depending on workload).

Why?

* LLVM optimizations (constant folding, loop unrolling).
* NASM backend with direct x64 instructions.
* No garbage collector — memory is manual or predictable (arena/bump/refcount).

---

## 11.4 Memory Safety

PlasmaScript offers **tiered safety**:

* **High-level mode** → lists, dicts, sets, comprehensions → no leaks.
* **Refcounted objects** → safe shared memory.
* **Arena/Bump allocators** → safe, reset-based deallocation.
* **Manual malloc/free** → raw control, but your responsibility.

Rules:

1. PlasmaScript won’t free memory automatically unless you use refcounts.
2. You can mix safe + unsafe memory handling in the same program.
3. Dodecagram inline assembly bypasses safety — intended for experts.

---

## 11.5 Security Guarantees

PlasmaScript balances flexibility with guardrails:

* **No hidden GC** → no unpredictable pauses.
* **Strong type checks** → runtime verifies lists, dicts, sets, tuples.
* **Safe-by-default I/O** → Input/Output wrapped in checked calls.
* **FFI Safety** → Extern functions require explicit signatures.
* **Sandboxable** → PlasmaScript → WASM is fully sandboxed for the web.

---

## 11.6 Comparison with Other Languages

| Feature            | PlasmaScript            | C              | Rust                | Python             |
| ------------------ | ----------------------- | -------------- | ------------------- | ------------------ |
| **Startup Speed**  | Instant (AOT `.exe`)    | Instant        | Instant             | Slow (interpreter) |
| **Performance**    | Near C/Rust speed       | Fast           | Fast                | Slow               |
| **Memory Control** | Manual + managed tiers  | Manual only    | Safe borrow checker | GC only            |
| **Safety**         | Medium (opt-in)         | Low            | High                | Medium             |
| **Interop**        | C ABI, WASM, APIs       | Direct ABI     | C ABI + safe FFI    | C ABI (slower)     |
| **Ease of Use**    | Beginner → Pro friendly | Steep learning | Steep learning      | Very easy          |
| **Use Cases**      | Games, HPC, Systems, Ed | Systems only   | Systems, HPC        | Scripting, AI      |

---

## 11.7 Where PlasmaScript Excels

* **Instant startup** → great for CLI tools.
* **Predictable runtime** → great for finance & HPC.
* **Cross-domain readability** → teachers + professionals can share code.
* **Interop breadth** → OpenGL, Vulkan, Unity, Unreal, WASM.
* **Memory choice** → safe high-level OR raw malloc/free.

---

## 11.8 Summary

* PlasmaScript is **as fast to start as C**, with **predictable AOT execution**.
* Performance is **close to C and Rust**, dramatically ahead of Python.
* Safety is **tiered**, giving you **choice** instead of forcing one model.
* Interop is **first-class**, making it at home in both **games** and **finance**.




---

# 🟢 Chapter 12: Future Roadmap

---

## 12.1 Overview

PlasmaScript today is already:

* **Readable for beginners.**
* **Powerful for professionals.**
* **Compiled to `.exe` and WASM.**
* **Interop-ready with graphics/game engines.**

But the roadmap aims to take it from **great niche language** → **mainstream powerhouse**.

---

## 12.2 JIT (Just-in-Time) Compilation

* Current model: **AOT (Ahead-of-Time)** by default.
* Future model: **optional JIT mode** for:

  * Live coding in game engines.
  * Rapid prototyping.
  * Hot-reload workflows (edit → run instantly).
* Implementation: Lightweight LLVM-based JIT, toggled with `--jit` flag.

👉 This makes PlasmaScript attractive to **creative coders** and **game developers** who value iteration speed.

---

## 12.3 GPU Shaders in Native Syntax

PlasmaScript will gain **direct shader support**:

```plasmascript
Shader simple {
    input vec3 position
    output vec4 color

    Main() {
        color = vec4(position, 1.0)
    }
}
```

* Compiles to **GLSL/HLSL/SPIR-V** under the hood.
* Allows writing **graphics code directly in PlasmaScript style**.
* Bridges scripting and shader programming seamlessly.

👉 This makes it a strong candidate for **indie game dev, graphics research, and creative art installations**.

---

## 12.4 PlasmaHub (Package Manager & Ecosystem)

* Central hub for PlasmaScript packages:

  * Math libraries.
  * Game dev utilities.
  * Scientific & finance toolkits.
  * Community-driven extensions.
* Command-line tool:

```bash
plasmahub install graphics-tools
plasmahub publish mylibrary
```

* Similar to Python’s `pip` or Rust’s `cargo`, but tuned for **cross-domain use**.

👉 This will unlock a true **developer ecosystem**, beyond just core language.

---

## 12.5 Secure Enclave Compilation

PlasmaScript will support **compiling into secure enclaves**:

* Encrypted memory regions.
* Runtime protection against injection and tampering.
* Ideal for:

  * Finance (trading bots, risk models).
  * Healthcare (data-sensitive apps).
  * Government/security systems.

👉 This makes PlasmaScript stand out as both **expressive** and **trustworthy**.

---

## 12.6 WASM Evolution

Today: PlasmaScript exports to **WebAssembly**.
Future:

* Full **WASI support** (filesystem, networking, async I/O).
* Deploy to **cloud runtimes** seamlessly.
* PlasmaScript as a **universal scripting layer** across desktop + browser + cloud.

---

## 12.7 Long-Term Vision

PlasmaScript will grow into:

* A **beginner’s language** (education, tutorials).
* A **professional systems language** (HPC, finance, embedded).
* A **creative engine** (games, shaders, art).
* A **secure execution layer** (enclaves, WASM, finance).

**Tagline for the future:**

> *“Readable enough for your first day.
> Powerful enough for your last project.”*

---

## 12.8 Summary

* **JIT support** → live coding, instant prototyping.
* **GPU shaders** → direct PlasmaScript-to-GLSL/HLSL/SPIR-V.
* **PlasmaHub** → package manager and ecosystem.
* **Secure enclaves** → hardened execution for finance/security.
* **Evolving WASM** → making PlasmaScript a universal runtime citizen.

---




---

# 🟢 Chapter 13: Appendices

---

## 13.1 Reserved Keywords

These words are **reserved** in PlasmaScript and cannot be used as variable or function names:

```
Prog, Main, end, run
let, Func, return, Export, Extern, Import, Inline, on
if, else, for, in
text, number, bool, list, dict, set, tuple
true, false
malloc, free, store, load
arena_init, arena_alloc, arena_reset
rc_alloc, retain, release
bump_init, bump_alloc, bump_reset
```

> ⚠️ Reserved keywords may expand in future versions (especially with PlasmaHub and shader features).

---

## 13.2 Hello World Forms

PlasmaScript allows **four variations** of Hello World.
Two are **canonical**, two are **hybrids**.

### Canonical Forms

```plasmascript
Prog main() {
    Print ["Hello PlasmaScript!"]
}
end
```

```plasmascript
Main main() {
    Print ["Hello PlasmaScript!"]
}
run
```

### Hybrid Forms (Valid but discouraged)

```plasmascript
Prog main() {
    Print ["Hello PlasmaScript!"]
}
run
```

```plasmascript
Main main() {
    Print ["Hello PlasmaScript!"]
}
end
```

---

## 13.3 Quick Syntax Cheat Sheet

### Comments

```plasmascript
; This is a comment
```

### Variables

```plasmascript
let name = "Shay"
let age: number = 25
```

### Printing

```plasmascript
Print ["Hello " + name]
```

### Input

```plasmascript
let name = Input("What’s your name?")
```

### Functions

```plasmascript
Func add(a, b) {
    return a + b
}
```

### If/Else

```plasmascript
if age >= 18 {
    Print ["Adult"]
} else {
    Print ["Child"]
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
[x*x for x in [1,2,3]]
{x: x*x for x in [1,2,3]}
{x*x for x in [1,2,3]}
(x*x for x in [1,2,3])
```

### Lambdas

```plasmascript
let square = Func(x) { return x * x }
```

### Memory (manual)

```plasmascript
let ptr = malloc(16)
store(ptr, 0, 42)
Print [load(ptr, 0)]
free(ptr)
```

### Imports/Exports

```plasmascript
Import "math"
Extern "C" Func puts(msg: text)
Export Func add(a, b) { return a + b }
```

### Inline Assembly (Dodecagram)

```plasmascript
Inline { dgm(0xA1, 0xB2, 0xC3) }
```

---

## 13.4 Example: Full Mini Program

```plasmascript
Import "math"

Func square(x) {
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

Output:

```
Square: 1
Square: 4
Square: 9
Square: 16
Square: 25
```

---

# ✅ End of Manual

You now have:

* **Ch. 1–4** → Syntax & Core Language.
* **Ch. 5–6** → Program structure & memory.
* **Ch. 7–8** → Interop & style guide.
* **Ch. 9** → Beginner’s workbook.
* **Ch. 10–12** → Use cases, performance, future roadmap.
* **Ch. 13** → Appendices for quick reference.

---


