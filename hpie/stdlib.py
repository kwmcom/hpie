def length(obj):
    return float(len(obj))

def floor(n):
    return float(int(n))

# Registry of built-in functions
BUILTINS = {
    "length": length,
    "floor": floor
}
