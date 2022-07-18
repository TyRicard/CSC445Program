# Name: Ty Ricard
# Student no.: V00909036

from fractions import Fraction
from SimplexMethod import SimplexMethod
from Variable import Variable

# For basic printing: 
#   [1] GeeksforGeeks Contributors."Print Lists in Python 4 Different Ways".
#       Available: https://www.geeksforgeeks.org/print-lists-in-python-4-different-ways/
#  
# For Format Printing:
#   [1] Python Guides Contributors. "Python Print 2 Decimal Places."
#       Available: https://pythonguides.com/python-print-2-decimal-places/
class OutputHandler:

    # Prints the status of the Simplex Method
    def print_status(simplex):
        print(simplex.status)
    

    def print_optimal_value(simplex):
        # Need to format the rational to be a float
        float_optimal = float(simplex.optimal)
        print("{0:.7g}".format(float_optimal))


    def print_optimal(simplex):
        OutputHandler.print_status(simplex)
        OutputHandler.print_optimal_value(simplex)
        OutputHandler.print_points(simplex)


    def print_unbounded(simplex):
        OutputHandler.print_status(simplex)
        

    def print_infeasible(simplex):
        OutputHandler.print_status(simplex)


    def print_points(simplex):
        point_list = []
        # Go through the variables looking for optimization variables to be printed
        for var in simplex.variables:
            if var.is_point():
                point_list.append("{0:.7g}".format(float(var.get_value())))
        print(*point_list)






