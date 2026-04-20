# Hpie

A readable, prose-like programming language built in Python.

## Quick Example
```hpie
To define square(n):
    Return n * n

Set result to Call square(4)
Say "Square of 4 is " and result
```

## Features
- **Prose-like syntax** (Keywords: `Set`, `Say`, `If/Otherwise`, `While`)
- **Indentation-based blocks**
- **Dynamic module support** (`import("os" as os)`)
- **Robust diagnostics** and custom error handling

## Usage
```bash
python3 hs.py examples/main.hpy
```
