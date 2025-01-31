from .data_classes import Variable, If, ElseIf, Else


#################### VARIABLE TEST CASES ####################
variables_test_cases = [
    ('int x = 5;', Variable(data_type='int', name='x', value='5')), # int declaration and initialization
    ('int age;', Variable(data_type='int', name='age', value=None)), # int declaration
    # ('age = 26;', Variable(data_type=None, name='age', value='26')) # int assignment TODO: Fails unit test
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
                Variable(data_type='int', name='b', value='10'),
                'printf("a is equal to 5\n");'
            ]
        )
    )
]