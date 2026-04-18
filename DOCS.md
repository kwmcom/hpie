# Hpie Language Reference

Hpie is a prose-like programming language built for readability.

## Basic Syntax
```prose
Set count to 10
Say "Result: " and count
```

## Control Flow
```prose
If count is greater than 5 then:
    Say "High"
Otherwise:
    Say "Low"

While count is less than 20:
    Increase count by 1
```

## Functions
```prose
To define add(a, b):
    Return a + b

Set x to Call add(5, 5)
```

## Diagnostics
Errors are clearly marked with location and context:
```text
SyntaxError: Expected indented block
Line 5:    If 1 is 1 then
               ^
```
