from dataclasses import dataclass
from typing import List, Union


@dataclass
class Variable:
    data_type: str
    name: str
    value: Union[str, int, 'Function'] # using '' for forward reference

# FunctionDeclaration
@dataclass
class Function:
    return_type: str
    function_name: str
    parameters: List['Variable'] # using '' for forward reference


@dataclass
class If:
    condition: str
    body: str

@dataclass
class ElseIf:
    condition: str
    body: str

@dataclass
class Else:
    body: str


@dataclass
class FunctionDefinition(Function):
    body: List[Union[Variable, If, ElseIf, Else, str]]