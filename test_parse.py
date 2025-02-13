from .parser import check_variable, check_conditional, split_c_code, parse_c_statements, parse_function
import pytest
from .test_cases import *


@pytest.mark.parametrize('statement, expected', variables_test_cases)
def test_variable_parse(statement, expected):
    assert check_variable(statement) == expected


@pytest.mark.parametrize('statement, expected', conditionals_test_cases)
def test_condition_parse(statement, expected):
    conditional, body = check_conditional(statement)
    body_statements = split_c_code(body)
    body_statements = parse_c_statements(body_statements)
    conditional.body = body_statements
    assert conditional == expected


@pytest.mark.parametrize('statement, expected', function_test_cases)
def test_function_parse(statement, expected):
    function = parse_function(statement)
    assert function == expected