from .data_classes import *


#################### VARIABLE TEST CASES ####################
variables_test_cases = [
    ('int x = 5;', Variable(data_type='int', name='x', value=5)), # int declaration and initialization
    ('int age;', Variable(data_type='int', name='age', value=None)), # int declaration
    ('age = 26;', Variable(data_type=None, name='age', value=26)), # int assignment
    ("char test = 'c';", Variable(data_type='char', name='test', value="'c'")),
    ("char letter;", Variable(data_type='char', name='letter', value=None)),
    ("test = 'c';", Variable(data_type=None, name='test', value="'c'"))
]


#################### CONDITIONAL TEST CASES ####################
conditionals_test_cases = [
    # if statement
    (
        '''
        if (a > b) {
            printf("a is greater than b\n");
        }
        ''',
        If(condition='a > b', body=['printf("a is greater than b\n");'])
    ),
    # else if statement
    (
        '''
        else if (a == b) {
            printf("a is equal to b\n");
        }
        ''',
        ElseIf(condition='a == b', body=['printf("a is equal to b\n");'])
    ),
    # else statement
    (
        '''
        else {
            print("a is less than b\n");
        }
        ''',
        Else(body=['print("a is less than b\n");'])
    ),
    # if statement with multiple body statements
    (
        '''
        if (a == 5) {
            int b = 10;
            printf("a is equal to 5\n");
        }
        ''',
        If(
            condition='a == 5',
            body=[
                Variable(data_type='int', name='b', value=10),
                'printf("a is equal to 5\n");'
            ]
        )
    )
]


######################### FOR LOOP TEST CASES #########################


######################### WHILE LOOP TEST CASES #########################


######################### FUNCTION TEST CASES #########################
function_test_cases = [
    (
        'int sum(int a, int b);',
        Function(
            return_type='int',
            function_name='sum',
            parameters=[
                Variable(data_type='int', name='a', value=None),
                Variable(data_type='int', name='b', value=None)
            ]
        )
    ),
    (
        '''
        int subtract(int x, int y) {
            int diff = x - y;
            return diff;
        }
        ''',
        FunctionDefinition(
            return_type='int',
            function_name='subtract',
            parameters=[
                Variable(data_type='int', name='x', value=None),
                Variable(data_type='int', name='y', value=None)
            ],
            body=[
                Variable(data_type='int', name='diff', value='x - y'),
                'return diff;'
            ]
        )
    )
]