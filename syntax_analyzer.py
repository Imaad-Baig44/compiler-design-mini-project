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

output = []

def log(line):
    print(line)
    output.append(line)

log("STEP\tSTACK\tINPUT\tACTION")

step = 1

while len(stack) > 0:
    top = stack.pop()
    current = tokens[0]

    line = f"{step}\t{stack}\t{tokens}\t"
    
    # ✅ MATCH
    if top == current:
        line += f"Match {current}"
        tokens.pop(0)

    # ✅ PROGRAM
    elif top == 'program':
        line += "program -> int main ( ) begin stmt_list end"
        stack.extend(['end', 'stmt_list', 'begin', ')', '(', 'main', 'int'])

    # ✅ STMT LIST
    elif top == 'stmt_list':
        if current in ['int', 'n', 'expr', 'do', 'return']:
            line += "stmt_list -> stmt stmt_list"
            stack.extend(['stmt_list', 'stmt'])
        else:
            line += "stmt_list -> epsilon"

    # ✅ STMT
    elif top == 'stmt':
        if current == 'int':
            line += "stmt -> declaration"
            stack.append('declaration')
        elif current in ['n', 'expr']:
            line += "stmt -> assignment"
            stack.append('assignment')
        elif current == 'do':
            line += "stmt -> do_while"
            stack.append('do_while')
        elif current == 'return':
            line += "stmt -> return_stmt"
            stack.append('return_stmt')

    # ✅ DECLARATION
    elif top == 'declaration':
        line += "declaration -> int n ;"
        stack.extend([';', 'n', 'int'])

    # ✅ ASSIGNMENT
    elif top == 'assignment':
        line += "assignment -> id = expr ;"
        stack.extend([';', 'expr', '=', current])

    # ✅ FIXED EXPR (IMPORTANT)
    elif top == 'expr':
        if current == 'expr':
            if len(tokens) > 1 and tokens[1] == '+':
                line += "expr -> expr + expr"
                stack.extend(['expr', '+', 'expr'])
            else:
                line += "expr -> id"
                stack.append('expr')
        elif current == 'exp':
            line += "expr -> id"
            stack.append('exp')
        else:
            line += "expr -> id"
            stack.append(current)

    # ✅ DO WHILE
    elif top == 'do_while':
        line += "do_while -> do stmt_list while ( exp )"
        stack.extend([')', 'exp', '(', 'while', 'stmt_list', 'do'])

    # ✅ RETURN
    elif top == 'return_stmt':
        line += "return -> return ( n )"
        stack.extend([')', 'n', '(', 'return'])

    else:
        line += "Error"
        log(line)
        break

    log(line)
    step += 1

log("\nParsing Completed!")

# ✅ SAVE OUTPUT (FIXED ENCODING)
with open("parser_output.txt", "w", encoding="utf-8") as f:
    for line in output:
        f.write(line + "\n")

print("\nParser output saved to parser_output.txt")

# ✅ SAVE GRAMMAR (NO → SYMBOL)
with open("grammar.txt", "w", encoding="utf-8") as f:
    f.write("GRAMMAR:\n")
    f.write("program -> int main ( ) begin stmt_list end\n")
    f.write("stmt_list -> stmt stmt_list | epsilon\n")
    f.write("stmt -> declaration | assignment | do_while | return\n")
    f.write("expr -> expr + expr | id\n")

print("Grammar saved to grammar.txt")