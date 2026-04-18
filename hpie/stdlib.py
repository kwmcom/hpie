import time
import math
import random
import datetime

# Basic
def length(obj): return float(len(obj))
def to_str(obj): return str(obj)
def is_num(obj): return 1.0 if isinstance(obj, (int, float)) else 0.0
def is_str(obj): return 1.0 if isinstance(obj, str) else 0.0

# Math
def floor(n): return float(math.floor(n))
def ceil(n): return float(math.ceil(n))
def round_val(n): return float(round(n))
def abs_val(n): return float(abs(n))
def power(base, exp): return float(pow(base, exp))
def sqrt(n): return float(math.sqrt(n))
def min_val(a, b): return float(min(a, b))
def max_val(a, b): return float(max(a, b))
def log(n): return float(math.log(n))
def log10(n): return float(math.log10(n))
def exp(n): return float(math.exp(n))
def factorial(n): return float(math.factorial(int(n)))
def sin(n): return float(math.sin(n))
def cos(n): return float(math.cos(n))
def tan(n): return float(math.tan(n))
def pi(): return float(math.pi)
def e(): return float(math.e)

# Random
def rand_int(a, b): return float(random.randint(int(a), int(b)))
def rand_float(): return float(random.random())

# String / List
def join(lst, sep): return str(sep).join([str(x) for x in lst])
def split(s, sep): return list(str(s).split(str(sep)))

# Time
def get_time(): return float(time.time())
def get_date(): return str(datetime.date.today())

BUILTINS = {
    "length": length,
    "to_string": to_str,
    "is_number": is_num,
    "is_string": is_str,
    "floor": floor,
    "ceil": ceil,
    "round": round_val,
    "abs": abs_val,
    "pow": power,
    "sqrt": sqrt,
    "min": min_val,
    "max": max_val,
    "log": log,
    "log10": log10,
    "exp": exp,
    "factorial": factorial,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "pi": pi,
    "e": e,
    "join": join,
    "split": split,
    "rand_int": rand_int,
    "rand": rand_float,
    "time": get_time,
    "date": get_date
}
