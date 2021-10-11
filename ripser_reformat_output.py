import re
import sys

def reformat_line(line):
    line = re.sub(r"\[", "", line)
    line = re.sub(r",\ \)", " inf", line)
    line = re.sub(r",", " ", line)
    line = re.sub(r"\)", "", line)
    return line

def reformat(input_file, output_prefix):
    dim = -1
    diagrams = open(input_file)
    for line in diagrams.readlines():

        if re.match(r"^persistence", line):
            dim += 1
            if dim > 0:
                current_file.close()
            current_file = open(output_prefix + "_" + str(dim) + ".txt", 'w')

        elif re.match(r"^\ \[.*\)", line):
            current_file.write(reformat_line(line))
    if dim > -1:
        current_file.close()
    diagrams.close()

def main():
    if len(sys.argv) < 3:
        print("Too few arguments")
    elif len(sys.argv) > 3:
        print("Too many arguments")
    else:
        reformat(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
