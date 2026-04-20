"""Hpie - A prose-like programming language."""

__version__ = "1.0.0"

from .lexer import lex
from .parser import Parser
from .interpreter import Interpreter

__all__ = ["lex", "Parser", "Interpreter"]
