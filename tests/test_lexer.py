import pytest
from hpie.lexer import lex, Token

def test_lexer_empty():
    assert lex("") == []

def test_lexer_simple():
    code = 'Say "Hello"'
    tokens = lex(code)
    assert tokens[0].type == "KEYWORD"
    assert tokens[0].value == "Say"
    assert tokens[1].type == "STRING"
    assert tokens[1].value == '"Hello"'

def test_lexer_indentation():
    code = """To define add(a, b):
    Return a + b
"""
    tokens = lex(code)
    # Check if we have INDENT token
    types = [t.type for t in tokens]
    assert "INDENT" in types
    assert "DEDENT" in types

def test_lexer_math():
    code = "1 + 2 * 3"
    tokens = lex(code)
    values = [t.value for t in tokens if t.type not in ["NEWLINE"]]
    assert values == ["1", "+", "2", "*", "3"]
