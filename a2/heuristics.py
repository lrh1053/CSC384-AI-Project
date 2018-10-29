'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy
from propagators import prop_GAC

def ord_dh(csp):
    '''
    Returns the variable with the largest number of constraints.'''
    var, deg = None, -1
    for v in csp.get_all_unasgn_vars():
        c_deg = len([True for c in csp.get_cons_with_var(v) if c.get_n_unasgn() > 1])
        if var == None or deg < c_deg:
            var, deg = v, c_deg
    return var

def ord_mrv(csp):
    '''
    Returns the next variable to be assigned as per the MRV heuristic.'''
    var, deg = None, -1
    for v in csp.get_all_unasgn_vars():
        if var == None or v.cur_domain_size() < deg:
            var, deg = v, v.cur_domain_size()
    return var

def val_lcv(csp, var):
    domains = var.cur_domain().copy()
    affected = {}
    for d in domains:
        var.assign(d)
        flag, pruned = prop_GAC(csp, var)
        if flag:
            affected[d] = len(pruned)
        for v, d in pruned:
            v.unprune_value(d)
        var.unassign()
    return sorted(affected, key=affected.__getitem__, reverse=True)
