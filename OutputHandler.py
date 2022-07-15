from fractions import Fraction
from SimplexMethod import SimplexMethod
from Variable import Variable

# For basic printing: https://www.geeksforgeeks.org/print-lists-in-python-4-different-ways/
class OutputHandler:

    def print_status(simplex):
        print(simplex.status)
    

    def print_optimal(simplex):
        print(simplex.optimal)


    def print_points(simplex):
        point_list = []
        for var in simplex.variables:
            if var.is_point():
                point_list.append(var.get_value())
        print(*point_list)


    def print_output(simplex):
        OutputHandler.print_status(simplex)
        if (simplex.status == "optimal"):
            OutputHandler.print_optimal(simplex)
            OutputHandler.print_points(simplex)






