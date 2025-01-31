from parser import *

c_file = 'solution.c'

file_contents = get_file_contents(c_file)
main_func = format_func_declar('int main()')
function_contents = get_function_contents(file_contents, main_func)

print('Function contents:', function_contents)

# print('Function contents:', function_contents)
# statements = split_c_code(function_contents)

# print('Statements:')
# for statement in statements:
#     print('   ', statement)

# formatted_statements = parse_c_statements(statements)
# print('Formatted statements:')
# for statement in formatted_statements:
#     print('   ', statement)

# correct = False
# for statement in formatted_statements:
#     if isinstance(statement, Variable):
#         if statement.data_type == 'int' and statement.name == 'age':
#             print('Variable is correct')
#             correct = True

# if not correct:
#     print('Unable to find variable')