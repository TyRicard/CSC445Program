from fractions import Fraction

class InputParser:

    # Simple conditionals checking for the file_name
    def get_file_name(arguments):
        if len(arguments) < 2:
            print("Not enough arguments were provided")
            exit(1)

        if len(arguments) > 2:
            print("Too many arguments were provided")
            exit(1)
        
        return arguments[1]


    def split_by_whitespace(line):
        if "\t" in line:
            string_row = line.split("\t")
        else:
            string_row = line.split()
        return string_row


    # Parsing the file for the necessary data
    def get_lp(file_name):
        file = open(file_name, 'r')
        lp_string_lines = file.readlines()

        is_first = True
        lp = []

        # For each row of the string, get the coefficients, and append to the LP
        # Note, for the objective function, append a zero for easy conversion to a dictionary
        # For fractions: https://docs.python.org/3/library/fractions.html
        for line in lp_string_lines:
            string_row = []
            lp_row = []

            string_row = InputParser.split_by_whitespace(line)
            for coeff in string_row:
                lp_row.append(Fraction(coeff))
            
            if is_first:
                lp_row.append(Fraction(0, 1))
                is_first = False

            lp.append(lp_row)
        
        return lp





