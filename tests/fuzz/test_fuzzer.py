from hpie.parser import Parser
from hpie.lexer import lex
from hpie.diagnostics import SyntaxError
from hypothesis import given, strategies as st
import pytest

# Simple strategy for generating random strings that might look like HPIE code
code_strategy = st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n():=+-*/[]\"'.,<>", min_size=1)

@given(code_strategy)
def test_fuzzer_parser(code):
    try:
        tokens = lex(code)
        parser = Parser(tokens, code)
        parser.parse()
    except (SyntaxError, Exception):
        # We expect potential exceptions here, which is fine as long as they are handled
        pass

if __name__ == "__main__":
    # If running directly, pytest can run it
    import pytest
    pytest.main([__file__])
