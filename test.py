'''
Example code:
#include <stdio.h>
#include <stdlib.h>

int subtract(int x, int y);

int sum(int a, int b) {
    int sum = a + b;
    return sum;
}

int main() {
    int x = 10;
    printf("Hello, World!\n");
    return 0;
}

int subtract(int x, int y) {
    int diff = x - y;
    return diff;
}

Should output:
[
    '#include <stdio.h>',
    '#include <stdlib.h>',
    Function(
        return_type='int',
        function_name='subtract',
        parameters=[
            Variable(data_type='int', name='x', value=None),
            Variable(data_type='int', name='y', value=None)
        ]
    )
    FunctionDefinition(
        return_type='int',
        function_name='sum',
        parameters=[
            Variable(data_type='int', name='a', value=None),
            Variable(data_type='int', name='b', value=None)
        ],
        body=[
            Variable(data_type='int', name='sum', value='a + b'),
            'return sum;'
        ]
    ),
    FunctionDefinition(
        return_type='int',
        function_name='main',
        parameters=[],
        body=[
            Variable(data_type='int', name='x', value=10),
            'printf("Hello, World!\n");
            'return 0;'
        ]
    ),
    FunctionDefinition(
        return_type='int',
        function_name='subtract',
        parameters=[
            Variable(data_type='int', name='x', value=None),
            Variable(data_type='int', name='y', value=None)
        ],
        body=[
            Variable(data_type='int', name='diff', value='x - y'),
            'return subtract;'
        ]
    )
]
'''

from parser import *


filename = 'example.c'
get_file_contents_v2(filename)
