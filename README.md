# CSC 445 Programming Assignment
The programming assignment description is separated into several sections; the sections are as followed:
* Running Program
* Software Architecture
* Extra Features

## Running Program
Given the assignment description, the first step in running the program is to uncompress the `.tar.bz2` archive.
The command to uncompress the `lp.tar.bz2` is the following:

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

As an aside, on a couple files, the assignmts for the optimization variables differed from the expected values, but this could be explained as multiple points producing the optimal value.

## Software Architecture
To discuss the Software Architecture, several sections will be used: the sections are (1) Program Source Files, (2) Test Scenarios, and (3) Additional Information.

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
The `OutputHandler.py` file constains a static `OutputHandler` class. As expected, this class writes the output to standard out. Note, while several functions are composed of single print statements that could be combined, the class was written to promote clarity in its method names. The `OutputHandler` class is also responsible for converting values from the python class `Fraction` into `Float` numbers, and outputting seven decimal places.

#### SimplexMethod.py
The `SimplexMethod.py` file contains the class `SimplexMethod`, which is used to execute the Simplex Method. The class contains several fields necessary to complete the Simplex Method; the fields are described below:

* **dictionary**: This field contains a two-dimensional list representing the dictionary undergoing the Simplex Method. The elements of the dictionary are of type `Fraction`. The number of rows and number of cols match the number of constraints (plus the objective function) and the number of optimization variables (plus a constant) respectively. 

* **variables**: This field contains a list of the variables for the dictionary. Note, the optimization variables are provided before the slack variables.

* **pivot_rule**: This field is either set to `"Largest Increase"` or `"Largest Coefficient"`. In other words, this field directly relates to the extra `Largest Increase` feature, and would be set by the command line. Without the necessary flag being provided in the command line, the default `"Largest Coefficient"` will be used. Note, this `pivot_rule` field will be ignored in favor of Bland's rule when the dictionary starts demonstrating cycling.

* **entering**: This field is set to the variable to be used as the entering variable in a Simplex pivot. The `entering` field will be determined according to the pivot rule, whether the rule is largest increase, largest coefficient or Bland's rule.

* **leaving**: This field is set to the variable to be used as the leaving variable in a Simplex pivot. If the field is set to `None` after running a method like `set_pivot_variables()`, then the Linear Program would be unbounded. In other words, the method `set_pivot_variables()` will set the `leaving` field unless the possible leaving variables are unbounded.

* **optimal**: This field is set to the optimal objective value after completing a feasible, bounded Linear Program. This is essentially used for output purposes.

* **degeneracy_counter**: This field is integral to preventing cycling in the system. After a degenerate pivot, the `degeneracy_counter` increments, and if the `degeneracy_counter` achieves a count of three or higher, then the Simplex Method starts using Bland's Rule, which was determined to prevent cycling. Once a non-degenerate pivot has occurred, the `degeneracy_counter` is reset and the rule determined by `pivot_rule` will be used instead.

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
There are three basic scenarios to be described in this section: Average Linear Program, Initially-Infeasible Linear Program, and Degenerate Linear Program. These scenarios will provide the basic flow, but will not go into depth regarding each function.

#### Average Linear Program
This scenario would occur when the Linear Program is initially feasible, and there are no degenerate constraints. In `main.py`, the dictionary form and variables will produced. Since the dictionary is initially feasible, the program would create an instance of the Simplex Method and call the method `run_simplex()`. The method `run_simplex()` provides a good synopsis of this workflow. While the dictionary is not in a completed state, the method does the following:

1. It checks if the dictionary is optimal, and if it is, handle the optimal case using `handle_optimal()`.
2. If it is not optimal, set pivot variables for the given iteration of the Simplex Method. Note, the variables are selected according to the pivot rule.
3. If the dictionary is unbounded (no `leaving` variable found), handle the unbounded case using `handle_unbounded()`.
4. Because the dictionary does not have degeneracy, the `degeneracy_counter` can be overlooked.
5. Pivot the dictionary, and repeat from Step 1 until the dictionary is either optimal or unbounded. Infeasiblility would not occur in this scenario.

Concluding `run_simplex()`, the necessary information is outputted.

#### Initially-Infeasible Linear Program
This scenario would occur when the Linear Program is initially infeasible, and there are no degenerate constraints. In `main.py`, the initially-infeasible dictionary would cause the Auxiliary Method to be run (ignoring the extra feature). The Auxiliary Method workflow is best shown through the method `run_auxiliary()` in `AuxiliaryMethod.py`. The method does the following:

1.  


