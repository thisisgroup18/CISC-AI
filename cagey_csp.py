# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#
import itertools
import math

#Look for #IMPLEMENT tags in this file.
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
    '''A model of a Cagey grid (without cage constraints) built using only binary not-equal constraints.'''
    
    n, cages = cagey_grid
    vars = []
    
    # Create variables for each cell in the grid
    for i in range(1, n+1):
        for j in range(1, n+1):
            var_name = f"Cell({i},{j})"
            var = Variable(var_name, list(range(1, n+1)))
            vars.append(var)
    
    csp = CSP("Binary_NE_Grid", vars)
    
    # Add binary not-equal constraints for rows and columns
    for i in range(n):
        for j in range(n):
            for k in range(j+1, n):
                # Row constraints
                var1 = vars[i*n + j]
                var2 = vars[i*n + k]
                con = Constraint(f"Row_{i+1}_{j+1}_{k+1}", [var1, var2])
                sat_tuples = [(x, y) for x in range(1, n+1) for y in range(1, n+1) if x != y]
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)
                
                # Column constraints
                var1 = vars[j*n + i]
                var2 = vars[k*n + i]
                con = Constraint(f"Col_{i+1}_{j+1}_{k+1}", [var1, var2])
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)
    
    return csp, vars  # Ensure this is inside the function


def nary_ad_grid(cagey_grid):
    '''A model of a Cagey grid (without cage constraints) built using only n-ary all-different constraints.'''
    
    n, cages = cagey_grid
    vars = []
    
    # Create variables for each cell in the grid
    for i in range(1, n+1):
        for j in range(1, n+1):
            var_name = f"Cell({i},{j})"
            var = Variable(var_name, list(range(1, n+1)))
            vars.append(var)
    
    csp = CSP("Nary_AD_Grid", vars)
    
    # Add n-ary all-different constraints for rows and columns
    for i in range(n):
        # Row constraints
        row_vars = vars[i*n : (i+1)*n]
        con = Constraint(f"Row_{i+1}", row_vars)
        sat_tuples = list(itertools.permutations(range(1, n+1), n))
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)
        
        # Column constraints
        col_vars = vars[i::n]
        con = Constraint(f"Col_{i+1}", col_vars)
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)
    
    return csp, vars

def cagey_csp_model(cagey_grid):
    '''A model of a Cagey grid built using your choice of binary not-equal or n-ary all-different constraints, 
       together with Cagey cage constraints.'''
    
    n, cages = cagey_grid
    csp, vars = nary_ad_grid(cagey_grid)  # Use n-ary all-different constraints for the grid
    
    # Add cage constraints
    for cage in cages:
        value, cells, op = cage
        cage_vars = [vars[(cell[0]-1)*n + (cell[1]-1)] for cell in cells]  # Get variables for the cells in the cage
        cage_name = f"Cage_{value}_{op}_{cells}"
        con = Constraint(cage_name, cage_vars)
        
        # Generate satisfying tuples based on the cage operation
        sat_tuples = []
        for assignment in itertools.product(*[var.domain() for var in cage_vars]):
            if op == '+' and sum(assignment) == value:
                sat_tuples.append(assignment)
            elif op == '-' and len(assignment) == 2 and abs(assignment[0] - assignment[1]) == value:
                sat_tuples.append(assignment)
            elif op == '*' and math.prod(assignment) == value:
                sat_tuples.append(assignment)
            elif op == '/' and len(assignment) == 2 and (
                assignment[0] / assignment[1] == value or assignment[1] / assignment[0] == value
            ):
                sat_tuples.append(assignment)
            elif op == '?':
                sat_tuples.append(assignment)  # Accept all assignments if operation is unknown
        
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)
    
    return csp, vars