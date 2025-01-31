# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# propagators.py
# desc:


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

    1. prop_FC (worth 0.5/3 marks)
        - a propagator function that propagates according to the FC algorithm that 
          check constraints that have exactly one Variable in their scope that has 
          not assigned with a value, and prune appropriately

    2. prop_GAC (worth 0.5/3 marks)
        - a propagator function that propagates according to the GAC algorithm, as 
          covered in lecture

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned Variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned Variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any Variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of Variable values pairs are all of the values
      the propagator pruned (using the Variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a Variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining Variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one Variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a Variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned Variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated Variable. Remember to keep
       track of all pruned Variable,value pairs and return '''
    pruned = []
    
    if newVar is None:
        # If no variable is newly assigned, return True and an empty list
        return True, []
    
    # Get all constraints involving the newly assigned variable
    constraints = csp.get_cons_with_var(newVar)
    
    for constraint in constraints:
        # Check constraints with exactly one unassigned variable
        if constraint.get_n_unasgn() == 1:
            unassigned_var = constraint.get_unasgn_vars()[0]
            for value in unassigned_var.cur_domain():
                # Check if assigning this value violates the constraint
                if not constraint.check_var_val(unassigned_var, value):
                    # Prune the value if it violates the constraint
                    unassigned_var.prune_value(value)
                    pruned.append((unassigned_var, value))
            
            # If the domain of the unassigned variable is empty, return False (deadend)
            if unassigned_var.cur_domain_size() == 0:
                return False, pruned
    
    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    pruned = []  # List to store pruned (Variable, value) pairs

    # Initialize the GAC queue with all constraints if newVar is None
    if newVar is None:
        gac_queue = csp.get_all_cons()
    else:
        # Otherwise, initialize the queue with constraints involving newVar
        gac_queue = csp.get_cons_with_var(newVar)
    
    while gac_queue:
        constraint = gac_queue.pop(0)
        for var in constraint.get_scope():
            for value in var.cur_domain():
                # Check if the value is still supported by the constraint
                if not constraint.check_var_val(var, value):
                    # Prune the value if it is not supported
                    var.prune_value(value)
                    pruned.append((var, value))
                    
                    # If the domain of the variable is empty, return False (deadend)
                    if var.cur_domain_size() == 0:
                        return False, pruned
                    
                    # Add all constraints involving this variable back to the queue
                    for con in csp.get_cons_with_var(var):
                        if con not in gac_queue:
                            gac_queue.append(con)
    
    return True, pruned

