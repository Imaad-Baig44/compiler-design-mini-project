# LL(1) Parser (Fixed Version)

tokens = [
    'int', 'main', '(', ')', 'begin',
    'int', 'n', ';',
    'do',
    'expr', '=', 'expr', '+', 'expr', ';',
    'n', '=', 'exp', ';',
    'while', '(', 'exp', ')',
    'return', '(', 'n', ')',
    'end', '$'
]

stack = ['$', 'program']

print("STEP\tSTACK\t\tINPUT\t\tACTION")

step = 1

while len(stack) > 0:
    top = stack.pop()
    current = tokens[0]

    print(f"{step}\t{stack}\t{tokens}\t", end="")

    # Match
    if top == current:
        print(f"Match {current}")
        tokens.pop(0)

    # Grammar rules
    elif top == 'program':
        print("Apply program → int main ( ) begin stmt_list end")
        stack.extend(['end', 'stmt_list', 'begin', ')', '(', 'main', 'int'])

    elif top == 'stmt_list':
        if current in ['int', 'n', 'expr', 'do', 'return']:
            print("Apply stmt_list → stmt stmt_list")
            stack.extend(['stmt_list', 'stmt'])
        else:
            print("Apply stmt_list → ε")

    elif top == 'stmt':
        if current == 'int':
            print("Apply stmt → declaration")
            stack.append('declaration')
        elif current in ['n', 'expr']:
            print("Apply stmt → assignment")
            stack.append('assignment')
        elif current == 'do':
            print("Apply stmt → do_while")
            stack.append('do_while')
        elif current == 'return':
            print("Apply stmt → return_stmt")
            stack.append('return_stmt')

    elif top == 'declaration':
        print("Apply declaration → int n ;")
        stack.extend([';', 'n', 'int'])

    elif top == 'assignment':
        print("Apply assignment → id = expr ;")
        stack.extend([';', 'expr', '=', current])

    # 🔥 FIXED PART (VERY IMPORTANT)
    elif top == 'expr':
        if len(tokens) > 1 and tokens[1] == '+':
            print("Apply expr → expr + expr")
            stack.extend(['expr', '+', 'expr'])
        else:
            print("Apply expr → id")
            stack.append(current)

    elif top == 'do_while':
        print("Apply do_while → do stmt_list while ( exp )")
        stack.extend([')', 'exp', '(', 'while', 'stmt_list', 'do'])

    elif top == 'return_stmt':
        print("Apply return → return ( n )")
        stack.extend([')', 'n', '(', 'return'])

    else:
        print("Error")
        break

    step += 1

print("\nParsing Completed!")