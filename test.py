from parser import *

c_file = 'example.c'

file_contents = get_file_contents(c_file)
main_func = format_func_declar('int main()')
contents = get_function_contents(file_contents, main_func)

'''
test C code
#include <stdio.h>

int main() {
    int a = 5;
    int b = 3;

    if (a > b) {
        printf("%d is bigger than %d\n", a, b);
        printf("This is a second print statement\n");
    }
    else {
        printf("%d is greater than %d\n", b, a);
    }
}
'''