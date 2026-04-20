from .stdlib import BUILTINS
from .diagnostics import UndefinedVariableError, UndefinedFunctionError

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.modules = {}
        self.parent = parent
        
        # Only top-level environment gets builtins
        if parent is None:
            for name, func in BUILTINS.items():
                self.functions[name] = func

    def get_var(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_var(name)
        raise UndefinedVariableError(name)

    def set_var(self, name, value):
        self.variables[name] = value

    def define_function(self, name, func):
        self.functions[name] = func

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        return None
    
    def register_module(self, name, module_data):
        self.modules[name] = module_data

    def get_module(self, name):
        if name in self.modules:
            return self.modules[name]
        if self.parent:
            return self.parent.get_module(name)
        return None
