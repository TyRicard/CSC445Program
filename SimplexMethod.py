# Name: Ty Ricard
# Student no.: V00909036

from fractions import Fraction
from Variable import Variable
from Dictionary import Dictionary

class SimplexMethod:

    def __init__(self, dictionary, variables, pivot_rule):
        self.dictionary = dictionary
        self.variables = variables
        self.pivot_rule = pivot_rule
        self.entering = None
        self.leaving = None
        self.optimal = None
        self.degeneracy_counter = 0
        self.status = "incomplete"


    def get_variable_by_col(self, col):
        for variable in self.variables:
            if variable.get_col() == col:
                return variable
        return None


    def get_variable_by_row(self, row):
        for variable in self.variables:
            if variable.get_row() == row:
                return variable
        return None


    def dictionary_has_degenerate_pivot(self):
        leaving_row = self.leaving.get_row()
        if self.dictionary[leaving_row][0] == Fraction(0):
            return True
        else:
            return False


    def set_pivot_variables(self):
        # Use Bland's Rule if degenerate for several pivots

        if self.degeneracy_counter >= 3:
            self.blands_rule_entering()
            self.basic_leaving()

        # The largest increase pivot rule can be run using the same method
        elif self.pivot_rule == "Largest Increase":
            self.largest_increase_entering_and_leaving()
        
        # Default using largest coefficient
        else:
            self.largest_coeff_entering()
            self.basic_leaving()


    def largest_coeff_entering(self):
        # There must be at least one coefficient that is positive; otherwise, it is optimal
        largest_coefficient = -1
        for i in range(1, len(self.dictionary[0])):
            
            if self.dictionary[0][i] <= Fraction(0):
                continue

            elif self.dictionary[0][i] > largest_coefficient:
                largest_coefficient = self.dictionary[0][i]
                self.entering = self.get_variable_by_col(i)

            # Use lowest variable if equal
            elif self.dictionary[0][i] == largest_coefficient:
                if (self.get_variable_by_col(i).get_id() < self.entering.get_id()):
                    self.entering = self.get_variable_by_col(i)


    def largest_increase_entering_and_leaving(self):
        # Iterate through the objective function coefficients looking for positives
        largest_increase = None
        largest_increase_indices = (None, None)

        for i in range(1, len(self.dictionary[0])):

            if self.dictionary[0][i] <= Fraction(0):
                continue

            # Assign entering and leaving before checking for difference
            self.entering = self.get_variable_by_col(i)
            self.basic_leaving()

            # Handle Unbounded Case
            if Dictionary.is_unbounded(self.leaving):
                return

            # Calculate the temporary increase (note, temp_val cannot be negative as unboundedness would have been caught)
            temp_val = (self.dictionary[self.leaving.get_row()][0] /  self.dictionary[self.leaving.get_row()][self.entering.get_col()]) * Fraction(-1)
            temp_increase = self.dictionary[0][self.entering.get_col()] * temp_val

            # Update if necessary
            if (largest_increase is None) or (temp_increase > largest_increase):
                largest_increase = temp_increase
                largest_increase_indices = (self.leaving.get_row(), self.entering.get_col())

            # Use lowest variable if equal
            elif temp_increase == largest_increase:
                if (self.entering.get_id() < self.get_variable_by_col(largest_increase_indices[1]).get_id()):
                    largest_increase_indices = (self.leaving.get_row(), self.entering.get_col())
            
            # Make the entering and leaving be None for next iteration
            self.entering = None
            self.leaving  = None

        # Lastly, assign entering and leaving using determined indices
        self.entering = self.get_variable_by_col(largest_increase_indices[1])
        self.leaving  = self.get_variable_by_row(largest_increase_indices[0])


    def blands_rule_entering(self):
        # Go through variables looking for the smallest non-basic
        for var in self.variables:
            if not var.is_in_basis() and self.dictionary[0][var.get_col()] > 0:
                self.entering = var
                break


    def basic_leaving(self):
        is_unbounded = False
        # Note, if the largest increase < 0, then the LP is unbounded
        increase = None
        for i in range(1, len(self.dictionary)):

            # Check for a coefficient of zero or unbounded
            if (self.dictionary[i][self.entering.get_col()] >= Fraction(0)):
                continue
                        
            # Note, the entering_variable_coefficient should never be zero (would be optimal)
            temp_val = (self.dictionary[i][0] /  self.dictionary[i][self.entering.get_col()]) * Fraction(-1)

            if temp_val < 0:
                continue
            
            # Assign if increase is smaller than previous or nonexistent
            if (increase is None) or (temp_val < increase):
                increase = temp_val
                self.leaving = self.get_variable_by_row(i)
            
            # Check for smallest id if tie
            elif temp_val == increase:
                if (self.get_variable_by_row(i).get_id() < self.leaving.get_id()):
                    self.leaving = self.get_variable_by_row(i)


    # This method re-orders a given constraint of the dictionary such that the entering
    # variable enters the basis
    def create_sub_constraint(self):
        entering_col = self.entering.get_col()
        leaving_row = self.leaving.get_row()
        constraint = self.dictionary[leaving_row]
       
        divisor = constraint[entering_col] * Fraction(-1)
        constraint[entering_col] = -1
        for i in range(0, len(constraint)):
            constraint[i] = constraint[i] /  divisor
        
        return constraint


    def restructure_constraint(self, sub_constraint, row):
        entering_col = self.entering.get_col()
       
        # First, multiply the substitution constraint by the necessary coefficient
        for i in range(0, len(sub_constraint)):
            sub_constraint[i] = self.dictionary[row][entering_col] * sub_constraint[i]

        # Second, add the coefficients with the new coefficients to get the coefficients values
        for j in range(0, len(sub_constraint)):
            if (j == entering_col):
                self.dictionary[row][entering_col] = sub_constraint[entering_col]
            else:
                self.dictionary[row][j] = self.dictionary[row][j] + sub_constraint[j]
        return 


    def pivot(self):
        sub_constraint = self.create_sub_constraint()

        for i in range(0, len(self.dictionary)):
            sub_constraint_copy = sub_constraint.copy()
            if i == self.leaving.get_row():
                self.dictionary[i] = sub_constraint_copy
            else:
                self.restructure_constraint(sub_constraint_copy, i)

        self.handle_pivot_info()
        

    def handle_pivot_info(self):
        entering_col = self.entering.get_col()
        leaving_row = self.leaving.get_row()

        self.entering.pivot_variable(leaving_row, -1)
        self.leaving.pivot_variable(-1, entering_col)
        self.entering = None
        self.leaving = None


    # This method handles the optimal case, and includes assigning the 
    # optimization variables their expected values
    def handle_optimal(self):
        self.status = "optimal"
        self.optimal = self.dictionary[0][0]
        
        for var in self.variables:
            if var.is_point():
                if var.is_in_basis():
                    var.set_value(self.dictionary[var.get_row()][0])
                else:
                    var.set_value(Fraction(0))
        return
        
        
    def handle_unbounded(self):
        self.status = "unbounded"
        return


    def run_simplex(self):

        while(True):
            # Check for Optimal
            if Dictionary.is_optimal(self.dictionary):
                self.handle_optimal()
                return
            
            # Set the entering and leaving variable depending on criteria
            self.set_pivot_variables()

            # Check for unboundedness
            if Dictionary.is_unbounded(self.leaving):
                self.handle_unbounded()
                return

            # Update degeneracy counter where required
            # The degeneracy_counter increments whenever a degenerate_pivot occurs
            # and it zeroes whenever the pivot is not degenerate
            if self.dictionary_has_degenerate_pivot():
                self.degeneracy_counter = self.degeneracy_counter + 1
            else:
                self.degeneracy_counter = 0
        
            # Pivot
            self.pivot()

        

