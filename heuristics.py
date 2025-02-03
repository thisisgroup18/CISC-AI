# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

1. ord_dh (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Degree heuristic

2. ord_mv (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Minimum-Remaining-Value heuristic


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    Variables and constraints of the problem. The assigned Variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return next Variable to be assigned according to the Degree Heuristic '''
    # Gets all unassigned variables
    unassigned = csp.get_all_unasgn_vars()
    
    if not unassigned:
        return None
        
    max_var = unassigned[0]
    max_constraints = 0
    
    for var in unassigned:
        # Gets constraints involving this variable
        constraints = csp.get_cons_with_var(var)
        constraint_count = 0
        
        # Counts constraints with other unassigned variables
        for con in constraints:
            # For each constraint, check if it has other unassigned variables
            # get_n_unasgn returns total number of unassigned vars in constraint
            # If > 1, then there are other unassigned vars besides current var
            if con.get_n_unasgn() > 1:  
                constraint_count += 1
        
        # Updates maximum if we find more constraints
        # Note: >= ensures we take first variable in case of tie
        if constraint_count > max_constraints:
            max_constraints = constraint_count
            max_var = var
            
    return max_var

def ord_mrv(csp):
    ''' return Variable to be assigned according to the Minimum Remaining Values heuristic '''
    # Gets all unassigned variables
    unassigned = csp.get_all_unasgn_vars()
    
    # If no unassigned variables, return None
    if not unassigned:
        return None
    
    # Tracks minimum domain size and corresponding variable
    min_var = unassigned[0]
    min_size = min_var.cur_domain_size()
    
    # Checks each unassigned variable
    for var in unassigned[1:]:
        domain_size = var.cur_domain_size()
        
        if domain_size == 0:  # Handles case where domain is empty
            return var  # Returns immediately as this is a failure case
            
        if domain_size < min_size:
            min_size = domain_size
            min_var = var
            
    return min_var