
def multi_line_input():
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break

    return '\n'.join(lines)
