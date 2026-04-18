import math

def length(obj): return float(len(obj))
def floor(n): return float(math.floor(n))
def ceil(n): return float(math.ceil(n))
def round_val(n): return float(round(n))
def to_str(obj): return str(obj)
def is_num(obj): return 1.0 if isinstance(obj, (int, float)) else 0.0
def is_str(obj): return 1.0 if isinstance(obj, str) else 0.0
def min_val(a, b): return float(min(a, b))
def max_val(a, b): return float(max(a, b))
def join(lst, sep): return str(sep).join([str(x) for x in lst])

BUILTINS = {
    "length": length,
    "floor": floor,
    "ceil": ceil,
    "round": round_val,
    "to_string": to_str,
    "is_number": is_num,
    "is_string": is_str,
    "min": min_val,
    "max": max_val,
    "join": join
}
