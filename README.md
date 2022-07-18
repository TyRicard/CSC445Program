**student name**: Ty Ricard  \
**student no.**: V00909036

# CSC 445 Programming Assignment
The programming assignment description is separated into several sections; the sections are as followed:
* Running Program
* Software Architecture
* Extra Features

## Running Program
Given the assignment description, the first step in running the program is to decompress the `.tar.bz2` archive.
The command to decompress the `lp.tar.bz2` is the following:

`tar -xf lp.tar.bz2`

After running that command in the terminal, a new directory named `lp` will be present. Entering the directory will bring the user to this `README.md` document, alongside a myriad of source python files required for this assignment. The program was written in Python. Assuming the test files will be provided by the Teaching Team, the next requirement is to run the program. The command to run the program is the following; note, development of the program used the below form of stdin as well.

`python3 main.py < test_file.txt`

In the above case, `test_file.txt` is a placeholder for the test file to be parsed by the program. Note, it is assumed that `test_file.txt` exists in the necessary directory and matches the standard form format discussed in the assignment description. The file's contents are passed through the standard input and the output will be written to standard output. The program is able to handle incorrect LP dimensions and some text input of the incorrect form; this information will be written to standard error. 

Furthermore, the program will print `infeasible` or `unbounded` in those respective cases. When the LP reaches an optimal solution, the program prints `optimal`, the optimal objective value, and the assignments for the optimization variables. The basic format for the optimal case is presented below:

```
optimal
1.25
1 0 1 0
```

As an aside, on a couple files, the assignments for the optimization variables differed from the expected values, but this could be explained as multiple points producing the optimal value.

## Software Architecture
To discuss the Software Architecture, several sections will be used: the sections are (1) Program Source Files, (2) Test Scenarios, and (3) Architecture Summary.

### Program Source Files
As expected, several source files were used throughout the course of this project, and a brief description of each source file is provided below. Note, these are the files used for the basic program, and therefore, the files associated with extra features are ignored.

#### Variable.py
The `Variable.py` file contains the most atomic class: class `Variable`. Class `Variable` is used for both optimization variables and slack variables. Each instance of a variable has the following fields:

* **id**: This field is the `int` identifier for the class.
* **point**: This field is used to determine whether a variable was an optimization variable or a slack variable.
* **row**: This field is used to determine the variable's row in the dictionary. For non-basic variables, the row is set to `-1`.
* **col**: This field is used to determine the variable's column in the dictionary. For basic variables, the column is set to `-1`.
* **value**: This field is used for the assignment of optimization variables.
* **basis**: This field is a `bool` used for determining whether a variable is in the basis.

The methods associated with this file are essentially used for getting and setting the necessary fields. There is also a method called `pivot_variable`, which sets the necessary fields after the variable was either an entering or leaving variable in a pivot.

#### Dictionary.py
The `Dictionary.py` file contains a static `Dictionary` class. This class has several methods that take in a dictionary and provide insight into that dictionary. For example, this class contains the following methods: `is_optimal`, which determines if a dictionary is optimal; `is_infeasible`, which determines if a dictionary is infeasible; and `is_unbounded`, which determines if a dictionary is unbounded by looking for a `None` leaving variable.

Perhaps most crucially, this file can take the input linear program in standard form and produce a dictionary through the method `create_dictionary_form(linear_program)`. After the dictionary is created, the program may call `create_variable(dictionary)` to produce a list of both the optimization and slack variables. The list first inserts the optimization variables, then the slack variables.

#### InputParser.py
The `InputParser.py` file contains a static `InputParser` class. This class reads through the standard form Linear Program provided through standard input. Removing the necessary whitespace, the linear program can be placed into a two-dimensional array for further parsing by the above `Dictionary.py`. The `InputParser.py` file is also responsible for handling flags passed to the program. Since those flags directly relate to the extra features, the flags will be discussed at a later period.

#### OutputHandler.py
The `OutputHandler.py` file contains a static `OutputHandler` class. As expected, this class writes the output to standard out. Note, while several functions are composed of single print statements that could be combined, the class was written to promote clarity in its method names. The `OutputHandler` class is also responsible for converting values from the python class `Fraction` into `Float` numbers, and outputting seven decimal places.

#### SimplexMethod.py
The `SimplexMethod.py` file contains the class `SimplexMethod`, which is used to execute the Simplex Method. The class contains several fields necessary to complete the Simplex Method; the fields are described below:

* **dictionary**: This field contains a two-dimensional list representing the dictionary undergoing the Simplex Method. The elements of the dictionary are of type `Fraction`. The number of rows and number of columns match the number of constraints (plus the objective function) and the number of optimization variables (plus a constant) respectively. 

* **variables**: This field contains a list of the variables for the dictionary. Note, the optimization variables are provided before the slack variables.

* **pivot_rule**: This field is either set to `"Largest Increase"` or `"Largest Coefficient"`. In other words, this field directly relates to the extra `Largest Increase` feature and would be set by the command line. Without the necessary flag being provided in the command line, the default `"Largest Coefficient"` will be used. Note, this `pivot_rule` field will be ignored in favor of Bland's rule when the dictionary starts demonstrating cycling.

* **entering**: This field is set to the variable to be used as the entering variable in a Simplex pivot. The `entering` field will be determined according to the pivot rule, whether the rule is largest increase, largest coefficient, or Bland's rule.

* **leaving**: This field is set to the variable to be used as the leaving variable in a Simplex pivot. If the field is set to `None` after running a method like `set_pivot_variables()`, then the Linear Program would be unbounded. In other words, the method `set_pivot_variables()` will set the `leaving` field unless the possible leaving variables are unbounded.

* **optimal**: This field is set to the optimal objective value after completing a feasible, bounded Linear Program. This is essentially used for output purposes.

* **degeneracy_counter**: This field is integral to preventing cycling in the system. After a degenerate pivot, the `degeneracy_counter` increments, and if the `degeneracy_counter` achieves a count of three or higher, then the Simplex Method starts using Bland's Rule, which was determined to prevent cycling. Once a non-degenerate pivot has occurred, the `degeneracy_counter` is reset, and the rule determined by `pivot_rule` will be used instead.

* **status**: This field, initialized to `"incomplete"`, can be set to `"optimal"`, `"infeasible"` or `"unbounded"` depending on the state of the dictionary. Note, this status field is only assigned after the Simplex method had reached some conclusion.

Because this report is only to be used to provide a high-level description of the architecture, it does not feel appropriate to describe the individual methods of this class. However, the methods can be separated into broad categories.

1. **Helper Methods**: These methods are used for helping the Simplex Method and are inclusive of methods such as `get_variable_by_col(col)`, which is used for getting a certain variable based on the column in the dictionary, and `create_subconstraint()`, which re-orders a constraint so the entering variable enters the basis.

2. **Pivot Rule Methods**: These methods implement several pivots rules. For the largest coefficient rule, the methods `largest_coeff_entering()` and `basic_leaving()` are used. For the largest increase rule, the method `largest_increase_entering_and_leaving()` is used for both the entering and leaving variable. For Bland's rule, the methods `blands_rule_entering()` and `basic_leaving()` are used.

3. **Simplex Methods**: These methods are directly related to the Simplex Method. In other words, this category includes the methods `run_simplex()` and `pivot()`. 

#### AuxiliaryMethod.py
The `AuxiliaryMethod.py` file contains the class `AuxiliaryMethod`, which is used to handle the Auxiliary problem, and inherits from the `SimplexMethod` class. The `AuxiliaryMethod` class has an additional field called `original_function`, which is used to return to the original objective function after the Auxiliary Method had been run. This file has several methods, but the more complex methods either have to do with adding/removing the variable `omega` or recreating the objective function.

#### main.py
The `main.py` file contains the method `main()`, which calls methods from the above files. In other words, `main()` contains a lot of logic regarding dictionary feasibility and execution of the Simplex Methods.

### Test Scenarios
There are three basic scenarios to be described in this section: Average Linear Program, Initially-Infeasible Linear Program, and Degenerate Linear Program. These scenarios will provide the basic flow but will not go into depth regarding each function.

#### Average Linear Program
This scenario would occur when the Linear Program is initially feasible, and there are no degenerate constraints. In `main.py`, the dictionary and variables will be produced. Since the dictionary is initially feasible, the program would create an instance of the Simplex Method and call the method `run_simplex()`. The method `run_simplex()` provides a good synopsis of this workflow. While the dictionary is not in a completed state, the method does the following:

1. It checks if the dictionary is optimal, and if it is, handle the optimal case using `handle_optimal()`.
2. If it is not optimal, set pivot variables for the given iteration of the Simplex Method. Note, the variables are selected according to the pivot rule.
3. If the dictionary is unbounded (no `leaving` variable found), handle the unbounded case using `handle_unbounded()`.
4. Because the dictionary does not have degeneracy, the `degeneracy_counter` can be overlooked.
5. Pivot the dictionary and repeat from Step 1 until the dictionary is either optimal or unbounded. Infeasiblility would not occur in this scenario.

Concluding `run_simplex()`, the necessary information is outputted.

#### Initially-Infeasible Linear Program
This scenario would occur when the Linear Program is initially infeasible, and there are no degenerate constraints. In `main.py`, the initially-infeasible dictionary would cause the Auxiliary Method to be run (ignoring the extra feature). The Auxiliary Method workflow is best shown through the method `run_auxiliary()` in `AuxiliaryMethod.py`. The method does the following:

1.  Setup the Auxiliary Dictionary by doing the following:
    1. Making the Objective Function be composed of zeroes
    2. Add the Omega variable to the dictionary and variable list
    3. Find the most infeasible constraint and pivot with Omega
2.  Run the Simplex Method
3.  Close the Auxiliary Dictionary by doing the following:
    1. Remove the Omega Variable
    2. Re-construct the objective function

Note, if the optimal objective value of the Auxiliary Dictionary does not equal zero, then the dictionary is declared `"infeasible"`.

#### Degenerate Linear Program
This scenario differs from the average linear program because there are degenerate constraints. With degenerate constraints, there is the possibility of cycling, and therefore, this scenario attempts to show how the program handles cycling. After a degenerate pivot has occurred, the `degeneracy_counter` of the `SimplexMethod` class is updated using the subsequent code:

```
if self.dictionary_has_degenerate_pivot():
    self.degeneracy_counter = self.degeneracy_counter + 1
else:
    self.degeneracy_counter = 0
```

Looking at the method `set_pivot_variables()`, if the `degeneracy_counter` exceeds two, then the method `blands_rule_entering()` is called. The method determines the entering variable based on Bland's rule. Bland's rule will continue to run until a pivot is not degenerate. From lecture, it is known that cycling will not occur with Bland's rule, and therefore, switching to that rule after several degenerate pivots would prevent cycling from occurring in the program. 

### Architecture Summary
While most of the architecture was touched on, it may be beneficial to include a summary of important architectural decisions:

* The code was written in Python.
* Dictionaries are represented as two-dimensional lists composed of Fractions. Rational Representation is used.
* The Auxiliary Dictionary is used in the case of an initially-infeasible Linear Program
* The Largest Coefficient Rule was used as the default pivot rule unless several degenerate pivots had occurred, in which case the pivot rule is Bland's rule.
* Bland's rule can be adopted to prevent cycling.

## Extra Features
The extra features used for this program were (1) Largest-Increase Rule, and (2) Primal-Dual Methods.

### Largest-Increase Rule
The Largest-Increase Rule will be described through its execution and through its implementation.

#### Execution
To use the Largest-Increase Rule instead of the Largest-Coefficient Rule, the `-inc` flag must be included on the command line. An example command using the Largest-Increase Rule is provided below:

`python3 main.py -inc < test_file.txt`

Please note, the Largest-Increase Rule was not set to the default because the computation of the largest increase may be more extensive than just taking the largest coefficient. To show that this feature works, run a similar test suite as the Largest-Coefficient Rule. Note, it is hard to show that this method is running unless providing additional output, which is not allowed.

#### Implementation
The implementation of the Largest-Increase Rule is shown in the method `largest_increase_entering_and_leaving()` found in the `SimplexMethod.py` file. Note, there are additional components to this feature, such as handling the input flag, but the method `largest_increase_entering_and_leaving()` appeared to be the most crucial. The method follows the subsequent procedure:

1. Create `largest_increase` and `largest_increase_indices` variables
2. While iterating through the columns of the objective function
    1. If the column's coefficient is negative, iterate to the next column
    2. Set the entering variable to be the column
    3. Using `basic_leaving()` to determine the leaving variable. If the leaving variable is `None`, the dictionary is unbounded and return.
    4. Determine the possible increase associated with the entering and leaving variables
    5. If the increase is greater than the `largest_increase`, update the `largest_increase` and set the `largest_increase_indices` to be a tuple of the leaving variable's row and entering variable's column.
    5. Assign the entering and leaving variables to be `None` for the next iteration.
3. Assign the entering and leaving variable using the `largest_increase_indices`

### Primal-Dual Method
The Primal-Dual Method will be described through its execution and through its implementation.

#### Execution
To use the Primal-Dual Method instead of the Auxiliary Method, the `-dual` flag must be included on the command line. An example command using the Primal-Dual Method is provided below:

`python3 main.py -dual < test_file.txt`

Please note, the Primal-Dual Method was not set to the default because the Primal-Dual Method can have more complicated logic than the Auxiliary Problem. To show that this method works, use files that have either infeasible LPs or are initially infeasible.

#### Implementation
The major component of the implementation was the introduction of the file `DualMethod.py`, which includes the `DualMethod` class. Moreover, the `DualMethod` class inherits from the `SimplexMethod` class, but includes some additional fields and methods. The additional fields are the following:

* **primal_function**: This field is a list containing the coefficients associated with the objective function of the primal dictionary.
* **primal_variables**: This field is a list containing the variables associated with the primal dictionary. The variables can be mapped to the variables of the dual dictionary.

The methods introduced in the `DualMethod` class are the following:

* **convert_dictionary()**: This method is called during the initialization of a `DualMethod` instance and at the completion of either `run_dual_simplex()` or `run_initialization()`. The method takes a primal dictionary, and calculates the dual dictionary or vice versa. In other words, it takes a dictionary and does the negative transpose on that dictionary to get another dictionary.

* **map_dual_variable_to_primal()**: This method is called near the completion of either `run_dual_simplex()` or `run_initialization()`. Essentially, the program iterates through the variables associated with the dual dictionary and maps those variables to the primal variables. By producing this mapping, the primal variables' rows and columns can be updated after the dual has completed pivoting. Updates made to the optimization and slack variables differ greatly.

* **recreate_objective_function()**: This method is called near the completion of `run_initialization()`. Since the dual initialization process produces an invalid objective function, a new objective function must be created. This method goes through the primal optimization variables (updated after pivoting on the dual) and checks to see if the variables are still not in the basis. If the variable is non-basic, then the coefficient associated with that variable is equal to its coefficient in the original `primal_function`. If the variable is basic, the variable's row is multipled by the coefficient in the original `primal_function`, and the objective function adds the product to its elements. Note, this method was taken from the `AuxiliaryMethod` class. 

* **run_dual_simplex()**: This method is executed when the dual dictionary for an infeasible primal dictionary is feasible. In essence, the simplex method is executed, and the dual dictionary is converted back to the primal dictionary. Note, the conversion back to the primal method would produce an optimal dictionary, and therefore, when the Simplex method is later called on the dictionary, it should quickly choose the optimal status. Lastly, if the dual dictionary produces an unbounded value, the primal dictionary is infeasible.

* **run_initialization()**: This method is like the method `run_dual_simplex()`, but the duals' constants are made to be 1. The method mimics the dual initialization from lecture, wherein the primal objective function was zeroed, making the dual dictionary feasible. However, constants of 1 made operations easier, and it seemed easier to just update the dual dictionary instead of editing the primal dictionary. Next, the Simplex Method is run. Lastly, the dual dictionary is converted back to a primal dictionary. If the dual dictionary produces an unbounded dictionary, the primal dictionary is infeasible.

To conclude discussion of the dual method, it is worth noting the conditions required to execute `run_dual_simplex()` or `run_initialization()`. Firstly, the flag `-dual` must be used, resulting in the dual method being used over the auxiliary problem. If the dual dictionary is feasible, `run_dual_simplex()` is run, and an optimal/infeasible primal dictionary is reached. If this updated primal dictionary is optimal, the dictionary will be quickly passed through the Simplex method and `"optimal"` will be printed. If the dual dictionary is infeasible, `run_initialization()` is run, and if possible, a new primal dictionary will be produced. Note, this dictionary most likely will not be optimal, and therefore, executing the regular Simplex Method is still required. Lastly, the method `is_completely_degenerate(dictionary)` was added because the Dual Simplex Method struggled with a constant objective value. In this case, the zeroes were set to ones.