# Name: Ty Ricard
# Student no.: V00909036

from fractions import Fraction
from Variable import Variable
from SimplexMethod import SimplexMethod
from Dictionary import Dictionary

# For Basic Inheritance Format: 
#   [1] w3schools Contributors. "Python Inheritance."
#       Available: https://www.w3schools.com/python/python_inheritance.asp
class DualMethod(SimplexMethod):

    def __init__(self, dictionary, variables, pivot_rule):
        super().__init__(dictionary, variables, pivot_rule)

        # For this subclass, the dual dictionary is the main dictionary
        self.convert_dictionary()
        self.variables = Dictionary.create_variables(self.dictionary)

        # Need to store additional information about the primal dictionary
        self.primal_function = dictionary[0]
        self.primal_variables = variables


    def convert_dictionary(self):
        # This essentially does the negative transpose calculation
        temp_dictionary = []
        temp_row = []

        for col in range(0, len(self.dictionary[0])):
            for row in range(0, len(self.dictionary)):
                temp_row.append(self.dictionary[row][col] * Fraction(-1))

            temp_dictionary.append(temp_row)
            temp_row = []
        
        self.dictionary = temp_dictionary


    def map_dual_variable_to_primal(self):
        num_variables = len(self.variables)
        # Subtract by one to account for constant
        num_points = len(self.primal_function) - 1
        num_slack = num_variables - num_points
        diff_points_slack = num_points - num_slack

        for var_index in range(0, len(self.variables)):
            primal_variable = self.primal_variables[var_index]
    
            # For points
            if var_index < num_points:

                # The difference is required for unequal dimensions
                # For example, 10x7, the first basis variable would be at 10 + 0 - 3 = 7.
                dual_variable = self.variables[num_points + var_index - diff_points_slack]
            
                # If it is in the basis, just update the column
                if dual_variable.is_in_basis():
                    primal_variable.set_col(dual_variable.get_row())

                # Otherwise, have to make massive change to the primal variable
                else:
                    primal_variable.toggle_basis_status()
                    primal_variable.set_row(dual_variable.get_col())
                    primal_variable.set_col(-1)

            # For slack variables
            else:
                dual_variable = self.variables[var_index - num_points]
                # If it is in the basis, have to make massive change to the primal variable
                if dual_variable.is_in_basis():
                    primal_variable.toggle_basis_status()
                    primal_variable.set_row(-1)
                    primal_variable.set_col(dual_variable.get_row())
                
                # Otherwise, just update the row
                else:
                    primal_variable.set_row(dual_variable.get_col())

            self.primal_variables[var_index] = primal_variable

        self.variables = self.primal_variables


    # Copy of Auxiliary code
    def recreate_objective_function(self):
        temp_function = []

        # Create an list with all zeroes
        for col in range(0, len(self.dictionary[0])):
            temp_function.append(Fraction(0))

        # Go through variable indices
        for var_index in range(0, len(self.dictionary[0]) - 1):
            var = self.variables[var_index]

            # If nonbasic, add coefficient of original objective function to coefficient in new
            if not var.is_in_basis():
                temp_function[var.get_col()] = temp_function[var.get_col()] + self.primal_function[var.get_id()]
            
            # If basic, multiple every value in its row by the original coefficient
            else:
                primal_coeff = self.primal_function[var.get_id()]

                for col in range(0, len(self.dictionary[0])):
                    new_coeff = primal_coeff * self.dictionary[var.get_row()][col]
                    temp_function[col] = temp_function[col] + new_coeff
        
        self.dictionary[0] = temp_function


    def handle_infeasible(self):
        self.status = "infeasible"
        return


    def run_initialization(self):
        # First, assign the constants to be one
        for row_index in range(1, len(self.dictionary)):
            self.dictionary[row_index][0] = 1

        # Second, run the Simplex Method
        self.run_simplex()

        # If the status of the Dual is unbounded, then the Primal will be infeasible
        if self.status == "unbounded":
            self.handle_infeasible()
            return

        self.convert_dictionary()
        self.map_dual_variable_to_primal()
        self.recreate_objective_function()

    
    def run_dual_simplex(self):
        # First, run the Simplex Method
        self.run_simplex()

        # If the status of the Dual is unbounded, then the Primal will be infeasible
        if self.status == "unbounded":
            self.handle_infeasible()
            return

        self.convert_dictionary()
        self.map_dual_variable_to_primal()
        

            


        







        

        


