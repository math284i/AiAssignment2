from sympy.logic.boolalg import to_cnf, eliminate_implications
from sympy import symbols, And, Or, Not, Implies
from sympy.abc import A, B, D, R, P, S
from itertools import product



class Symbol:
    def __init__(self, name : str, value : bool) -> None:
        self.name : str = name
        self.value : bool = value

def make_belief_base():
    A, B, D = symbols('A B D')
    belief_base = (Implies(~B , D) & (~A | B)) & ~D
    belief_base_cnf = to_cnf(belief_base)
    return belief_base_cnf

def make_clauses(belief_base_cnf):
    listed_beliefs_clauses = []
    if isinstance(belief_base_cnf, And):
        listed_beliefs_clauses = list(belief_base_cnf.args)
    else:
        new_set = set()
        new_set.add(belief_base_cnf)
        listed_beliefs_clauses = list(new_set)
    clauses = []
    for clause in listed_beliefs_clauses:
        if isinstance(clause, Or):
            clauses.append(set(clause.args))              
        else:
            new_set = set()
            new_set.add(clause)   
            clauses.append(new_set)
    return clauses

def entails(belief_base_cnf, proposition) -> list[set]:
    clauses = make_clauses(expansion(belief_base_cnf, Not(proposition)))
    print("CLAUSES FINAL: " + str(clauses))
    # Code above makes belief_base into list of lists representing clauses  [{~D}, {B, D}, {B, ~A}, {~B}]
    # Example 
    #                         Belief base                           |                 Proposition
    # Original  |    B & (Implies(~B , D) & (~A | B)) & ~D          |                Implies(B, ~A)
    # CNF       |    B & ~D & (B | D) & (B | ~A)                    |                    A | B
    # Clausal   |    [[B], [~D], [B, D], [B, ~A],                   |                   [A, B]]           
    return resolution2(clauses)

def resolution(clauses):
    resolution_clauses = []
    for clause1 in clauses:
        current_clauses = []
        for symbol in clause1:
            add = True
            for clause2 in clauses:
                if Not(symbol) in clause2:
                    clause2.remove(Not(symbol))
                    add = False
            if add:
                current_clauses.append(symbol)
        resolution_clauses.append(current_clauses)
    # Code above compares the clauses and removes symbols if they intertwine. 
    # Code below checks if an empty claus is present implying 
    # that the belief base entails the proposition.
    return [] in resolution_clauses

def resolution2(clauses):       #[{B}, {~D}, {D, B}, {~A, B}, {~A}, {~D}]
    for clause1 in clauses:
        for element in clause1:
            for clause2 in clauses:
                if Not(element) in clause2:
                    copy1 = clause1.copy()      
                    copy1.remove(element)           
                    copy2 = clause2.copy()       
                    copy2.remove(Not(element))
                    new_clause = copy1.union(copy2)
                    if len(new_clause) == 0:
                        return True
                    elif new_clause not in clauses:
                        return resolution2(clauses + [new_clause])
    return False

def contraction(belief_base_cnf, proposition):
    return to_cnf(belief_base_cnf & Not(proposition))

def expansion(belief_base_cnf, proposition):
    return to_cnf(belief_base_cnf & proposition)


belief_base_cnf = make_belief_base()
proposition = B
print(f"{belief_base_cnf} entails {proposition}")
print(entails(belief_base_cnf, proposition))

print(f"before contraction/expansion  {belief_base_cnf}")

belief_base_cnf = contraction(belief_base_cnf, proposition)
print(f"contraction                   {belief_base_cnf}")
belief_base_cnf = expansion(belief_base_cnf, proposition)
print(f"expansion                     {belief_base_cnf}")


# & = AND
# | = OR
# ~ = NOT
# >> = IMPLIES1


# 1. design and implementation of belief base; W

# 2. design and implementation of a method for checking logical entailment (e.g., resolution-
# based), you should implement it yourself, without using any existing packages; W

# 3. implementation of contraction of belief base (based on a priority order on formulas in the
# belief base);

# 4. implementation of expansion of belief base. W

# The output should be the resulting/new belief base.


