import math
import random

def length(obj): return float(len(obj))
def floor(n): return float(math.floor(n))
def ceil(n): return float(math.ceil(n))
def round_val(n): return float(round(n))
def to_str(obj): return str(obj)
def is_num(obj): return 1.0 if isinstance(obj, (int, float)) else 0.0
def is_str(obj): return 1.0 if isinstance(obj, str) else 0.0
def min_val(a, b): return float(min(a, b))
def max_val(a, b): return float(max(a, b))
def abs_val(n): return float(abs(n))
def power(base, exp): return float(pow(base, exp))
def sqrt(n): return float(math.sqrt(n))
def sin(n): return float(math.sin(n))
def cos(n): return float(math.cos(n))
def tan(n): return float(math.tan(n))
def join(lst, sep): return str(sep).join([str(x) for x in lst])

# New additions
def rand_int(a, b): return float(random.randint(int(a), int(b)))
def rand_float(): return float(random.random())
def log(n): return float(math.log(n))
def log10(n): return float(math.log10(n))
def exp(n): return float(math.exp(n))
def factorial(n): return float(math.factorial(int(n)))

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
    "abs": abs_val,
    "pow": power,
    "sqrt": sqrt,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "join": join,
    "rand_int": rand_int,
    "rand": rand_float,
    "log": log,
    "log10": log10,
    "exp": exp,
    "factorial": factorial
}
