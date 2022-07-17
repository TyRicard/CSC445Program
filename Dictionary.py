# Name: Ty Ricard
# Student no.: V00909036

from fractions import Fraction
from Variable import Variable

class Dictionary:

    def create_dictionary_form(linear_program):
        dictionary = []
        is_objective_function = True

        for row in linear_program:
            lp_row = []
            lp_row.append(row[len(row) - 1])

            if is_objective_function:
                for i in range(0, len(row) - 1):
                    lp_row.append(row[i])
                is_objective_function = False
            else:
                for i in range(0, len(row) - 1):
                    lp_row.append(row[i] * -1)
            dictionary.append(lp_row)
        
        return dictionary


    def create_variables(dictionary):
        num_variables = 1
        variables = []
        for col in range(1, len(dictionary[0])):
            variables.append(Variable(num_variables, True, -1, col))
            num_variables = num_variables + 1

        for row in range(1, len(dictionary)):
            variables.append(Variable(num_variables, False, row, -1))
            num_variables = num_variables + 1
        
        return variables

    
    def is_unbounded(leaving_variable):
        return leaving_variable is None


    def is_optimal(dictionary):
        for i in range(1, len(dictionary[0])):
            if dictionary[0][i] > Fraction(0):
                return False
        return True


    def is_infeasible(dictionary):
        for i in range(1, len(dictionary)):
            if dictionary[i][0] < Fraction(0):
                return True
        return False


    def is_completely_degenerate(dictionary):
        for i in range(1, len(dictionary)):
            if dictionary[i][0] != Fraction(0):
                return False
        return True
        

        


