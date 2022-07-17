# Name: Ty Ricard
# Student no.: V00909036

import sys
from InputParser import InputParser
from Dictionary import Dictionary
from SimplexMethod import SimplexMethod
from AuxiliaryMethod import AuxiliaryMethod
from DualMethod import DualMethod
from OutputHandler import OutputHandler

def main():
    (pivot_rule, initialization_approach) = InputParser.get_pivot_rule(sys.argv)
    standard_lp = InputParser.get_lp()

    dictionary = Dictionary.create_dictionary_form(standard_lp)
    variables =  Dictionary.create_variables(dictionary)

    if Dictionary.is_infeasible(dictionary):
        if initialization_approach == "Auxiliary":
            aux_simplex = AuxiliaryMethod(dictionary, variables, pivot_rule)
            aux_simplex.run_auxiliary()

            if aux_simplex.status == "infeasible":
                OutputHandler.print_infeasible(aux_simplex)
                exit(0)

            dictionary = aux_simplex.dictionary
            variables = aux_simplex.variables
        
        # If it is not Dual Feasible, use dual initialization to get a Feasible Primal Dictionary
        # that would be run using the regular simplex method
        # Otherwise, run the Dual Simplex Method until an optimal value has been achieved
        # An already Optimal Dictionary will be passed to the Simplex Method
        else:
            dual_simplex = DualMethod(dictionary, variables, pivot_rule)
        
            if Dictionary.is_infeasible(dual_simplex.dictionary) or Dictionary.is_completely_degenerate(dual_simplex.dictionary):
                dual_simplex.run_initialization()
            else:
                dual_simplex.run_dual_simplex()
    
            if dual_simplex.status == "infeasible":
                OutputHandler.print_infeasible(dual_simplex)
                exit(0)

            dictionary = dual_simplex.dictionary
            variables = dual_simplex.variables


    simplex = SimplexMethod(dictionary, variables, pivot_rule)

    simplex.run_simplex()

    if simplex.status == "optimal":
        OutputHandler.print_optimal(simplex)

    elif simplex.status == "unbounded":
        OutputHandler.print_unbounded(simplex)

if __name__ == "__main__":
    main()