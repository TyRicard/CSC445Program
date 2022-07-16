# Name: Ty Ricard
# Student no.: V00909036

from fractions import Fraction
from Variable import Variable
from SimplexMethod import SimplexMethod

# For Basic Inheritance Format: https://www.w3schools.com/python/python_inheritance.asp
class AuxiliaryMethod(SimplexMethod):

    def __init__(self, dictionary, variables):
        super().__init__(dictionary, variables)
        self.original_function = dictionary[0].copy()


    def zero_objective_function(self):
        for col in range(0, len(self.dictionary[0])):
            self.dictionary[0][col] = Fraction(0)


    def add_omega(self):
        omega_dictionary = []
        # First, create Omega Variable
        omega_col = len(self.dictionary[0])
        self.variables.append(Variable(omega_col, False, -1, omega_col))

        # Second, append omega to objective function
        omega_objective = self.dictionary[0].copy()
        omega_objective.append(Fraction(-1))
        omega_dictionary.append(omega_objective)

        # Third, append omega to basis
        for row in range(1, len(self.dictionary)):
            temp_row = self.dictionary[row]
            temp_row.append(Fraction(1))
            omega_dictionary.append(temp_row)

        # Fourth, re-assign dictionary for use in Simplex Method and assign as entering
        self.dictionary = omega_dictionary
        self.entering = self.get_variable_by_col(omega_col)


    def remove_omega(self):
        dictionary = []

        # In case degeneracy makes Omega remain in the basis, perform an additional pivot
        if (self.variables[len(self.variables)-1].is_in_basis()):

            # Determine the value to be switched with Omega
            entering_variable_col = None
            for col in range(1, len(self.dictionary[0])):
                if self.dictionary[0][col] != Fraction(0):
                    leaving_variable_col = col
                    
            self.entering = self.get_variable_by_col(leaving_variable_col)
            self.leaving = self.variables[len(self.variables) - 1]
            self.pivot()

        # First, remove Omega Variable and fix index issues
        omega = self.variables.pop(len(self.variables) - 1)
        for i in range(omega.get_col() + 1, len(self.dictionary[0])):
            temp_var = self.get_variable_by_col(i)
            temp_var.set_col(i - 1)

        # Second, remove omega from objective function
        objective = self.dictionary[0].copy()
        objective.pop(omega.get_col())
        dictionary.append(objective)

        # Third, remove omega from basis
        for row in range(1, len(self.dictionary)):
            temp_row = self.dictionary[row]
            temp_row.pop(omega.get_col())
            dictionary.append(temp_row)

        # Fourth, re-assign dictionary for use in Simplex Method
        self.dictionary = dictionary


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
                temp_function[var.get_col()] = temp_function[var.get_col()] + self.original_function[var.get_id()]
            
            # If basic, multiple every value in its row by the original coefficient
            else:
                original_coeff = self.original_function[var.get_id()]

                for col in range(0, len(self.dictionary[0])):
                    new_coeff = original_coeff * self.dictionary[var.get_row()][col]
                    temp_function[col] = temp_function[col] + new_coeff
        
        self.dictionary[0] = temp_function

    
    def find_most_infeasible_for_leaving(self):
        # One row must be negative, and therefore, change values of infeasible_row / infeasible_constant
        infeasible_row = 0
        infeasible_constant = 0

        for row in range(1, len(self.dictionary)):
            if self.dictionary[row][0] < infeasible_constant:
                infeasible_constant = self.dictionary[row][0]
                infeasible_row = row
        
        self.leaving = self.get_variable_by_row(infeasible_row)

        
    def setup(self):
        self.zero_objective_function()
        self.add_omega()
        # Do the first pivot manually to handle infeasibility
        self.find_most_infeasible_for_leaving()
        self.pivot()


    def closedown(self):
        self.remove_omega()
        self.recreate_objective_function()


    def auxiliary_is_infeasible(self):
        return (self.status == "unbounded") or (self.dictionary[0][0] != Fraction(0))

    
    def handle_auxiliary_infeasible(self):
        self.status = "infeasible"
        return

    
    def run_auxiliary(self):
        self.setup()
        self.run_simplex()

        if self.auxiliary_is_infeasible():
            self.handle_auxiliary_infeasible()
            return

        self.closedown()





        

        


