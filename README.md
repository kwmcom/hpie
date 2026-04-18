# Hpie

A simple, highly readable programming language that feels like natural English prose. Built with Python 3.

## Features

- **Prose-like Syntax**: Uses intuitive keywords like `Set`, `Say`, `Ask for`, `Increase`, and `Decrease`.
- **Natural Logic**: Supports `If/Otherwise`, `While` loops, and `Repeat [n] times`.
- **Readable Comparisons**: Uses `is`, `is not`, `is greater than`, and `is less than`.
- **Clean Blocks**: Clean, indentation-based scoping.
- **Strict Error Handling**: Clear and helpful error messages for syntax and runtime issues.

## Examples

### Hello World
```prose
Set name to "Human"
Say "Hello, " and name
```

### Loops and Logic
```prose
Set count to 1
While count is less than 4:
    Say "Looping... count is " and count
    Increase count by 1

Repeat 2 times:
    Say "This is so readable!"
```

### User Input
```prose
Say "What is your favorite number?"
Ask for fav
Say fav and " is a great choice!"
```

## Error System

Hpie provides precise feedback to help you code:
- `Error: Expected "to" after variable name`
- `Error: Unknown variable 'x'`
- `Error: Invalid indentation on line 5`

## Usage

Run any `.hs` file using the Hpie CLI:

```bash
python3 hs.py examples/demo.hs
```

## File Structure

- `hs.py`: CLI entry point.
- `hpie/`: Core language implementation (Lexer, Parser, Interpreter).
- `examples/`: Sample scripts to get you started.
