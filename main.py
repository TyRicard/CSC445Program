import sys
from InputParser import InputParser
from Dictionary import Dictionary
from SimplexMethod import SimplexMethod
from OutputHandler import OutputHandler

def main():
    input_parser = InputParser()
    file_name = InputParser.get_file_name(sys.argv)
    standard_lp = InputParser.get_lp(file_name)

    dictionary = Dictionary.create_dictionary_form(standard_lp)
    variables =  Dictionary.create_variables(dictionary)
    simplex = SimplexMethod(dictionary, variables)
    simplex.run_basic_method()

    OutputHandler.print_output(simplex)



if __name__ == "__main__":
    main()