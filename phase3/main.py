import getopt
import sys
from cgenerator import generate_code


def main(argv):
    input_file_name = ''
    output_file_name = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('main.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file_name = arg
        elif opt in ("-o", "--ofile"):
            output_file_name = arg

    with open("tests/" + input_file_name, "r") as input_file:
        code = generate_code(input_file.read())

    with open("out/" + output_file_name, "w") as output_file:
        output_file.write(code)

if __name__ == "__main__":
    main(sys.argv[1:])
