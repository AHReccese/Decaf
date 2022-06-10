
def multi_line_input():
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break

    return '\n'.join(lines)

def read_input_file(fileName):
    input_lines = []
    with open(fileName, "r") as input_file:
        for line in input_file:
            l = line.strip()
            if l != "":
                input_lines.append(line.strip())
    return '\n'.join(input_lines)

def write_results(fileName,text):
    with open(fileName,"w") as file:
        file.write(text)