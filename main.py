import sys
from InputParser import InputParser
from Dictionary import Dictionary
from SimplexMethod import SimplexMethod
from AuxiliaryMethod import AuxiliaryMethod
from OutputHandler import OutputHandler

def main():
    input_parser = InputParser()
    file_name = InputParser.get_file_name(sys.argv)
    standard_lp = InputParser.get_lp(file_name)

    dictionary = Dictionary.create_dictionary_form(standard_lp)
    variables =  Dictionary.create_variables(dictionary)

    if Dictionary.is_infeasible(dictionary):
        aux_simplex = AuxiliaryMethod(dictionary, variables)
        aux_simplex.run_auxiliary()

        if aux_simplex.status == "infeasible":
            OutputHandler.print_infeasible(aux_simplex)
            exit(0)

        dictionary = aux_simplex.dictionary
        variables = aux_simplex.variables

    simplex = SimplexMethod(dictionary, variables)

    simplex.run_simplex()

    if simplex.status == "optimal":
        OutputHandler.print_optimal(simplex)

    elif simplex.status == "unbounded":
        OutputHandler.print_unbounded(simplex)



if __name__ == "__main__":
    main()