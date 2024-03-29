import sys, getopt
import parser, tokenizer
import re


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('main.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    preprocessed_data = tokenizer.preprocess(inputfile)
    output = parser.parse(preprocessed_data)

    with open("out/" + outputfile, "w") as output_file:
        output_file.write(output)


if __name__ == "__main__":
    main(sys.argv[1:])