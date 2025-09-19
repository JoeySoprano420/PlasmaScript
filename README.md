# PlasmaScript

---

# 🌟 PlasmaScript Specification

### Overview

PlasmaScript is a minimalist, expressive scripting language designed for clarity, poetic readability, and conversational coding. It borrows simplicity from BASIC, flexibility from Python, and structure from modern scripting languages. Its philosophy: **“Possible — therefore Try.”**

---

## 1. Program Structure

Minimal Hello World:

```plasmascript
; comment Prog () greeting {hello user} Print ["hello Shay!"] run
```

Alternative form:

```plasmascript
; comment Main () greeting {hello user} Print ["hello Shay!"] end
```

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

