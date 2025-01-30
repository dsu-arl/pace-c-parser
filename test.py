from parser import *

c_file = 'example.c'

file_contents = get_file_contents(c_file)
main_func = format_func_declar('int main()')
function_contents = get_function_contents_v2(file_contents, main_func)

print('Function contents:', function_contents)
statements = split_c_code(function_contents)

print('Statements:')
for statement in statements:
    print('   ', statement)

formatted_statements = parse_c_statements(statements)
print('Formatted statements:')
for statement in formatted_statements:
    print('   ', statement)

# Can declare correct variables like this for verification
correct_var = Variable(data_type='int', name='b', value='3')

# Current example:
'''
#include <stdio.h>

int main() {
    int a = 5;
    int b = 3;

    if (a > b) {
        printf("%d is bigger than %d\n", a, b);
        if (10 < 14) {
            int x = 15;
            printf("This is a second print statement\n");
        }
    }
    else if (a == b) {
        printf("%d is equal to %d\n", a, b);
    }
    else {
        printf("%d is greater than %d\n", b, a);
    }
}
'''