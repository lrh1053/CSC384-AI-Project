'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''

from itertools import permutations, product
from cspbase import Variable, Constraint, CSP
from functools import reduce

def binary_ne_grid(kenken_grid):
    n = kenken_grid[0][0]
    variables, constraints = [], []
    for i in range(n):
        variables.append([Variable("%d%d"%(i,j), domain=list(range(1,n+1))) for j in range(n)])

    tuples = [t for t in permutations(list(range(1,n+1)), 2)]
    for i in range(n):
        for j in range(n):
            for k in range(j+1, n):
                cons = Constraint("r%d%d%d"%(i,j,k), [variables[i][j], variables[i][k]])
                cons.add_satisfying_tuples(tuples)
                constraints.append(cons)

                cons = Constraint("c%d%d%d"%(i,j,k), [variables[j][i], variables[k][i]])
                cons.add_satisfying_tuples(tuples)
                constraints.append(cons)

    csp = CSP("binary_ne_grid", [v for row in variables for v in row])
    for cons in constraints:
        csp.add_constraint(cons)
    return csp, variables

def nary_ad_grid(kenken_grid):
    n = kenken_grid[0][0]
    variables, constraints = [], []
    for i in range(n):
        variables.append([Variable("%d%d"%(i,j), domain=list(range(1,n+1))) for j in range(n)])

    tuples = [t for t in permutations(list(range(1,n+1)))]
    for i in range(n):
        cons = Constraint("r%d"%i, variables[i])
        cons.add_satisfying_tuples(tuples)
        constraints.append(cons)

        cons = Constraint("c%d"%i, [variables[j][i] for j in range(n)])
        cons.add_satisfying_tuples(tuples)
        constraints.append(cons)

    csp = CSP("nary_ad_grid", [v for row in variables for v in row])
    for cons in constraints:
        csp.add_constraint(cons)
    return csp, variables

def getij(x):
    return x // 10 - 1, x % 10 - 1

def kenken_csp_model(kenken_grid):
    n = kenken_grid[0][0]
    csp, variables = nary_ad_grid(kenken_grid)
    csp.name = 'kenken_csp_model'
    operations = {
        0: lambda x, y: x + y,
        1: lambda x, y: x - y,
        2: lambda x, y: x // y,
        3: lambda x, y: x * y,
    }
    for raw_constraint in kenken_grid[1:]:
        if len(raw_constraint) == 2:
            i, j = getij(raw_constraint[0])
            cons = Constraint(str(raw_constraint), [variables[i][j]])
            tuples = [[raw_constraint[1]]]
        else:
            vars, tuples = [], []
            for x in raw_constraint[:-2]:
                i, j = getij(x)
                vars.append(variables[i][j])
            cons = Constraint(str(raw_constraint), vars)
            for l in product(list(range(1,n+1)), repeat=len(raw_constraint)-2):
                if reduce(operations[raw_constraint[-1]], l) == raw_constraint[-2]:
                    for per in permutations(l):
                        if per not in tuples:
                            tuples.append(per)
        cons.add_satisfying_tuples(tuples)
        csp.add_constraint(cons)
    return csp, variables
