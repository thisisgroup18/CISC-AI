# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
import itertools
from cspbase import *
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *

def binary_ne_grid(cagey_grid):
    n = cagey_grid[0]  # Grid size
    dom = list(range(1, n+1))  # Domain is 1 to n
    
    # Creates variables array
    var_array = []
    for i in range(n):
        for j in range(n):
            # Variable name is Cell(i+1,j+1) because grid is 1-based
            var = Variable(f'Cell({i+1},{j+1})', dom)
            var_array.append(var)
            
    # Creates CSP
    csp = CSP(f"binary_ne_grid_{n}", var_array)
    
    # Adds row constraints
    for i in range(n):
        for j in range(n):
            for k in range(j+1, n):
                # Gets variables for cells in same row
                var1 = var_array[i*n + j]
                var2 = var_array[i*n + k]
                
                # Creates constraint
                con = Constraint(f'R{i+1}_{j+1}!={k+1}', [var1, var2])
                
                # Adds satisfying tuples where values are not equal
                sat_tuples = [(x,y) for x in dom for y in dom if x != y]
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)
    
    # Adds column constraints
    for j in range(n):
        for i in range(n):
            for k in range(i+1, n):
                # Gets variables for cells in same column
                var1 = var_array[i*n + j]
                var2 = var_array[k*n + j]
                
                # Creates constraint
                con = Constraint(f'C{j+1}_{i+1}!={k+1}', [var1, var2])
                
                # Adds satisfying tuples where values are not equal
                sat_tuples = [(x,y) for x in dom for y in dom if x != y]
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)
                
    return csp, var_array


def nary_ad_grid(cagey_grid):
    n = cagey_grid[0]  # Grid size
    dom = list(range(1, n+1))  # Domain is 1 to n
    
    # Creates variables array
    var_array = []
    for i in range(n):
        for j in range(n):
            # Variable name is Cell(i+1,j+1) because grid is 1-based
            var = Variable(f'Cell({i+1},{j+1})', dom)
            var_array.append(var)
            
    # Creates CSP
    csp = CSP(f"nary_ad_grid_{n}", var_array)
    
    # Adds row constraints
    for i in range(n):
        # Gets all variables in current row
        row_vars = [var_array[i*n + j] for j in range(n)]
        
        # Creates constraint
        con = Constraint(f'Row{i+1}_AllDiff', row_vars)
        
        # Generates all permutations of 1..n as satisfying tuples
        import itertools
        sat_tuples = list(itertools.permutations(dom))
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)
    
    # Adds column constraints
    for j in range(n):
        # Gets all variables in current column
        col_vars = [var_array[i*n + j] for i in range(n)]
        
        # Creates constraint
        con = Constraint(f'Col{j+1}_AllDiff', col_vars)
        
        # Generates all permutations of 1..n as satisfying tuples
        sat_tuples = list(itertools.permutations(dom))
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)
        
    return csp, var_array

def cagey_csp_model(cagey_grid):
    """Returns a CSP object representing a Cagey Grid CSP."""
    n, cages = cagey_grid
    
    # Creates variables array for grid
    var_array = []
    for i in range(n):
        for j in range(n):
            var = Variable(f'Cell({i+1},{j+1})', list(range(1, n+1)))
            var_array.append(var)

    # Creates CSP
    csp = CSP(f"Cagey_{n}", var_array)
    
    # Adds row and column constraints (using binary not equal)
    for i in range(n):
        for j in range(n):
            for k in range(j+1, n):
                # Row constraints
                var1 = var_array[i*n + j]
                var2 = var_array[i*n + k]
                con = Constraint(f'R{i+1}_{j+1}!={k+1}', [var1, var2])
                sat_tuples = [(x,y) for x in range(1,n+1) for y in range(1,n+1) if x != y]
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)

                # Column constraints
                var1 = var_array[j*n + i]
                var2 = var_array[k*n + i]
                con = Constraint(f'C{i+1}_{j+1}!={k+1}', [var1, var2])
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)

    # Processes each cage
    for cage in cages:
        target, cell_list, op = cage
        
        # Gets variables for cells in the cage
        cage_vars = []
        for (row, col) in cell_list:
            cage_vars.append(var_array[(row-1)*n + (col-1)])
            
        # Creates operation variable for the cage
        op_var_name = f'Cage_op({target}:{op}:{cage_vars})'
        if op == '?':
            op_var = Variable(op_var_name, ['+', '-', '*', '/'])
        else:
            op_var = Variable(op_var_name, [op])
        var_array.append(op_var)
        csp.add_var(op_var)
        
        # Creates the cage constraint
        con = Constraint(f'Cage_{target}_{op}_{cell_list}', cage_vars + [op_var])
        
        # Generates satisfying tuples
        sat_tuples = []
        domains = [list(range(1, n+1)) for _ in range(len(cage_vars))]
        op_domain = op_var.domain()
        
        for values in itertools.product(*domains):
            for operation in op_domain:
                # Checks if values satisfy the operation and target
                if operation == '+' and sum(values) == target:
                    sat_tuples.append(values + (operation,))
                elif operation == '*' and all(v != 0 for v in values):
                    product = 1
                    for v in values:
                        product *= v
                    if product == target:
                        sat_tuples.append(values + (operation,))
                elif operation == '-' and len(values) == 2:
                    if abs(values[0] - values[1]) == target:
                        sat_tuples.append(values + (operation,))
                elif operation == '/' and len(values) == 2 and values[1] != 0:
                    if values[0] / values[1] == target or values[1] / values[0] == target:
                        sat_tuples.append(values + (operation,))
                        
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)

    return csp, var_array