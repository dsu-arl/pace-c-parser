from pathlib import Path
import re
import subprocess
from data_classes import Variable, Function, If, ElseIf, Else


RED_TEXT_CODE = '\033[31m'
GREEN_TEXT_CODE = '\033[32m'
RESET_TEXT_CODE = '\033[0m'


# define function call as Variable = Function
# for example: int total = sum(5, 10);
# Variable(data_type='int', name='total', value=Function(return_type='int', ))

######################### GET FILE CONTENTS #########################
def get_file_contents(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f'Error: File {filename} not found')
        return None


######################### COMPILE PROGRAM #########################
def compile_program(c_file, output_file='a.out'):
    compile_process = subprocess.run(
        ['gcc', c_file, '-o', output_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if compile_process.returncode != 0:
        print('Program failed to compile')
        print(compile_process.stderr.decode())
        return False

    return True


######################### RUN PROGRAM #########################
def run_program(c_file, output_file='a.out'):
    if not compile_program(c_file, output_file):
        print('Program failed to compile')
        return None

    run_process = subprocess.run(
        [f'./{output_file}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if run_process.returncode != 0:
        print('Runtime error:')
        print(run_process.stderr.decode())
        return None
    
    return run_process.stdout.decode()


######################### EXTRACT LINES #########################
def extract_lines(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        lines = []
    
    lines = [line.replace('\n', '') for line in lines]
    
    imports = []
    for line in lines:
        if '#include' in imports:
            imports.append(line)


######################### EXTRACT FUNCTION PARAMETERS #########################
def extract_function_parameters(parameters):
    if parameters == '':
        return []

    parameters = parameters.split(',')
    parameters = [param.strip() for param in parameters]
    clean_params = []
    for param in parameters:
        data_type, param_name = param.split(' ')
        if param_name[0] == '*':
            data_type += '*'
            param_name = param_name[1:]
        parameter = Variable(data_type=data_type, name=param_name, value=None)
        clean_params.append(parameter)
    
    return clean_params


######################### FORMAT FUNCTION DECLARATION #########################
def format_func_declar(func_str):
    pattern = r"^(\S+(?:\s+\S+)*)\s+(\w+)\s*\(([^)]*)\)$"
    match = re.match(pattern, func_str)
    
    if not match:
        print('Function declaration not found')
        return None
    
    return_type, function_name, parameters = match.groups()
    
    # Deal with pointer return types for functions as well (int* sum() vs int *sum())
    if function_name[0] == '*':
        return_type += '*'
        function_name = function_name[1:]

    # Extract function parameters
    clean_parameters = extract_function_parameters(parameters)
    function = Function(return_type, function_name, clean_parameters)
    return function


######################### FIND FUNCTIONS #########################
def find_functions(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f'Error: File {filename} not found')
        return None

    function_regex = re.compile(
        r"""
        ^\s*                          # Start of the line, optional leading whitespace
        ([a-zA-Z_][\w\s\*]+)\s+       # Return type (e.g., int, void, char*)
        ([a-zA-Z_]\w*)\s*             # Function name (C identifier)
        \(\s*                         # Opening parenthesis for parameters
        ([^)]*)\s*                    # Parameter list (non-greedy match)
        \)\s*                         # Closing parenthesis
        (?:;|{)                       # End with a semicolon (prototype) or opening brace (definition)
        """,
        re.VERBOSE | re.MULTILINE
    )

    # Find all function declarations
    matches = function_regex.findall(content)
    print('Matches:', matches)

    functions = []
    for match in matches:
        return_type, function_name, parameters = match
        function_str = f'{return_type} {function_name}({parameters})'
        clean_func_declar = format_func_declar(function_str)
        functions.append(clean_func_declar)

    return functions


######################### GET FUNCTION CONTENTS #########################
def get_function_contents(content, function):
    # Normalize spaces: replace multiple spaces with a single space
    content = re.sub(r'\s+', ' ', content.strip())

    # Extract details from the dictionary
    return_type = function.return_type
    func_name = function.function_name
    params = function.parameters

    # Build the parameter string
    param_str = ', '.join(f"{param.data_type} {param.name}" for param in params)
    
    # Construct the function signature regex dynamically
    func_pattern = re.compile(rf'\s*{return_type}\s+{func_name}\s*\({param_str}\)\s*(\{{|\s*\{{)')

    found_function = False
    inside_function = False
    brace_count = 0
    function_body = ''

    # Search for the function match within the entire content
    match = func_pattern.search(content)
    
    if match:
        found_function = True
        inside_function = True
        brace_count = 1  # We've found the opening brace

        # Now process the content after the function signature
        for i in range(match.end(), len(content)):
            char = content[i]

            # Track braces to find the body of the function
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1

            if inside_function and brace_count > 0:
                function_body += char

            # If we've closed all braces, we've captured the full function
            if brace_count == 0:
                inside_function = False
                break

    if not found_function:
        return None

    # Extract statements
    pattern = re.compile(r'[^;]+;')
    function_body = function_body.strip()
    statements = pattern.findall(function_body)

    return [statement.strip() for statement in statements]


######################### EXTRACT FUNCTION VARIABLES #########################
def extract_function_variables(function_contents):
    pattern = r'^\s*(int|float|char|double|long|short|unsigned|signed|void)\s+([\w*]+)(\s*=\s*([^;]+))?\s*;'
    # pattern = r'^\s*(int|float|char|double|long|short|unsigned|signed|void)\s+([\w*]+)(\s*=\s*(.*))?\s*\(.*\)\s*;'

    variables = []
    for line in function_contents:
        match = re.match(pattern, line)
        if match:
            print('Match:', match)
            data_type = match.group(1)
            var_name = match.group(2)
            if match.group(3):
                # Value will be in the format ' = 10' so this removes the = and spaces
                var_value = match.group(3).split('=')[-1].strip()
                # check if var_value is a function call
                func_pattern = r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*'
                match = re.match(func_pattern, var_value)
                if match:
                    print(match.group(1))
                    print(match.group(2))
            else:
                var_value = None
            print(Variable(data_type=data_type, name=var_name, value=var_value))
            variables.append(Variable(data_type=data_type, name=var_name, value=var_value))

    return variables


######################### VERIFY INITIAL CHECKS #########################
def verify_initial_checks(filename):
    # Check file extension
    path = Path(filename)
    if path.suffix.lower() != '.c':
        print('Provided file is not C file')
        return False

    # Attempt to compile program before looking through C file
    # If it doesn't compile then don't open C file since something isn't working
    if not compile_program(filename):
        return False

    # Retrieve contents of C file
    contents = get_file_contents(filename)

    # Has 'return 0;' as the last line in main()
    # Compilation will fail if main function doesn't exist
    main_function = format_func_declar('int main()')
    function_contents = get_function_contents(contents, main_function)
    if function_contents is not None:
        # Check if 'return 0;' is last line in main()
        if 'return 0;' != function_contents[-1]:
            print("Missing 'return 0;' statement at end of main()")
            return False

    return True


#################### SPLIT C CODE ####################
def split_c_code(code):
    statements = []
    current_statement = ''
    brace_count = 0

    for i in range(len(code)):
        char = code[i]
        current_statement += char

        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        
        # Check if end of if statement or else statement
        if (char == '}' and brace_count == 0) or (char == ';' and brace_count == 0):
            statements.append(current_statement.strip())
            current_statement = ''

    return statements


#################### CHECK VARIABLE ####################
def check_variable(statement):
    '''
    Identifies if the given statement is a variable declaration and parses it if so.

    Args:
        - statement (str): C code statement
    
    Returns:
        Variable or None: If a match is found, returns Variable. Otherwise, returns None.
    '''
    pattern = r'^\s*(int|float|char|double|long|short|unsigned|signed|void)\s+([\w*]+)(\s*=\s*([^;]+))?\s*;'
    match = re.match(pattern, statement)
    if match:
        data_type = match.group(1)
        var_name = match.group(2)
        if match.group(3):
            # Value will be in the format ' = 10' so this removes the = and spaces
            var_value = match.group(3).split('=')[-1].strip()
        else:
            var_value = None
        return Variable(data_type=data_type, name=var_name, value=var_value)

    return None


#################### CHECK CONDITIONAL ####################
def check_conditional(statement):
    conditional_regex = re.compile(
        r"\b(if|else\s+if|else)\s*(?:\(([^)]*)\))?\s*\{([^}]*)\}",
        re.DOTALL
    )
    match = conditional_regex.search(statement)
    if match:
        conditional_type = match[1]
        condition = match[2] if match[2] else None
        
        # body will be everything between { and }
        open_brace_idx = statement.find('{')
        close_brace_idx = statement.rfind('}')
        body = statement[open_brace_idx+1:close_brace_idx].strip()

        # figure out how to handle conditionals that don't have curly braces (for if, else if, and else)
        # for example:
        '''
        if (10 < 14)
            printf("10 is bigger than 14\n");
        '''

        if conditional_type == 'if':
            return If(condition, body=[]), body
        if conditional_type == 'else if':
            return ElseIf(condition, body=[]), body
        if conditional_type == 'else':
            return Else(body=[]), body
        
    # Throws an error if you try to return either a tuple or None
    return '', ''


#################### PARSE C STATEMENTS ####################
def parse_c_statements(c_statements):
    parsed_statements = []

    for statement in c_statements:
        # Check if statement is a variable
        variable = check_variable(statement)
        # if variable, then value will not be None
        if variable:
            parsed_statements.append(variable)
            continue

        # Check if statement is a condition
        conditional, body = check_conditional(statement)
        if conditional != '':
            body_statements = split_c_code(body)
            body_statements = parse_c_statements(body_statements)
            conditional.body = body_statements
            parsed_statements.append(conditional)
            continue

        # If not variable or conditional, then function call (treat just as string for now)
        parsed_statements.append(statement)

    return parsed_statements


######################### GET FUNCTION CONTENTS V2 #########################
def get_function_contents_v2(content, function):
    # Normalize spaces: replace multiple spaces with a single space
    content = re.sub(r'\s+', ' ', content.strip())

    # Extract details from the dictionary
    return_type = function.return_type
    func_name = function.function_name
    params = function.parameters

    # Build the parameter string
    param_str = ', '.join(f"{param.data_type} {param.name}" for param in params)
    
    # Construct the function signature regex dynamically
    func_pattern = re.compile(rf'\s*{return_type}\s+{func_name}\s*\({param_str}\)\s*(\{{|\s*\{{)')

    found_function = False
    inside_function = False
    brace_count = 0
    function_body = ''

    # Search for the function match within the entire content
    match = func_pattern.search(content)
    
    if match:
        found_function = True
        inside_function = True
        brace_count = 1  # We've found the opening brace

        # Now process the content after the function signature
        for i in range(match.end(), len(content)):
            char = content[i]

            # Track braces to find the body of the function
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1

            if inside_function and brace_count > 0:
                function_body += char

            # If we've closed all braces, we've captured the full function
            if brace_count == 0:
                inside_function = False
                break

    if not found_function:
        return None

    split_statements = split_c_code(function_body)
    statements = parse_c_statements(split_statements)

    return statements