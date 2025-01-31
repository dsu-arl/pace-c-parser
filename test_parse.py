from .parser import check_variable, check_conditional, split_c_code, parse_c_statements
import pytest
from .test_cases import variables_test_cases, conditionals_test_cases


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