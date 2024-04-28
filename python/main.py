from sympy.logic.boolalg import to_cnf
from sympy.logic.inference import satisfiable
from sympy import symbols, And, Or, Not, Implies
from sympy.abc import A, B, D, R, P, S

############## The belief revision agent ##############

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
    return resolution(clauses)

def resolution(clauses):
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
                        return resolution(clauses + [new_clause])
    return False

def contraction(belief_base_cnf, proposition):
    bb_clauses = make_clauses(belief_base_cnf)
    prop_clauses = make_clauses(to_cnf(proposition))
    clauses_new = bb_clauses.copy()
    for prop_clause in prop_clauses:
        for bb_clause in bb_clauses:
            if prop_clause == bb_clause:
                clauses_new.remove(bb_clause)
    return from_clause_to_belief_base(clauses_new)

def from_clause_to_belief_base(clauses):
    result = [] 
    for clause in clauses:
        if len(clause) > 1:
            result.append(Or(*clause))
        else:
            result.append(And(*clause))
    belief_base_cnf = to_cnf(And(*result))
    return belief_base_cnf

def expansion(belief_base_cnf, proposition):
    return to_cnf(belief_base_cnf & proposition)

def revision(belief_base_cnf, proposition):
    #Levi identity
    return expansion(contraction(belief_base_cnf, Not(proposition)), proposition)

############## BELOW ARE AGM POSTULATES ##############

def success(belief_base_cnf, proposition):
    revised_belief = revision(belief_base_cnf,proposition)

    prop_cnf = make_clauses(to_cnf(proposition))
    revised_belief = make_clauses(revised_belief)

    for element in prop_cnf:
        if not element in revised_belief:
            return False
    return True

def inclusion(belief_base_cnf, proposition):
    revised_belief = revision(belief_base_cnf, proposition)
    expanded_belief = expansion(belief_base_cnf, proposition)

    revised_belief = make_clauses(revised_belief)
    expanded_belief = make_clauses(expanded_belief)
    
    for element in revised_belief:
        if element not in expanded_belief:
            return False
    return True

def vacuity(belief_base_cnf, proposition):
    if contraction(belief_base_cnf, Not(proposition)) == belief_base_cnf:
        return revision(belief_base_cnf, proposition) == expansion(belief_base_cnf, proposition)
    return f"negated proposition: {Not(proposition)} was a part of belief_base_cnf: {belief_base_cnf}"


def consistency(belief_base_cnf, proposition):
    #The sympy function satisfiable is a check for whether a belief is consistent
    if satisfiable(to_cnf(proposition)):
        return satisfiable(revision(belief_base_cnf,proposition))
    else:
        return True


def extensionality(belief_base_cnf, proposition1, proposition2):
    p1_cnf = to_cnf(proposition1)
    p2_cnf = to_cnf(proposition2)
    if p1_cnf == p2_cnf:
        return revision(belief_base_cnf, p1_cnf) == revision(belief_base_cnf, p2_cnf)
    return f"proposition 1: {p1_cnf} and proposition 2: {p2_cnf} are not logically equivalent"


############## AGM POSTULATES END ##############

def make_belief_base():
    A, B, D = symbols('A B D')
    belief_base = (Implies(~B , D) & (~A | B)) & ~D & (~R | P | S)
    belief_base_cnf = to_cnf(belief_base)
    return belief_base_cnf

def main():
    belief_base_cnf = make_belief_base()
    proposition = ~D
    print(f"{belief_base_cnf} entails {proposition}")
    print(entails(belief_base_cnf, proposition))

    print(f"before contraction/expansion  {belief_base_cnf}")
    belief_base_cnf = contraction(belief_base_cnf, proposition)
    print(f"contraction                   {belief_base_cnf}")
    belief_base_cnf = expansion(belief_base_cnf, proposition)
    print(f"expansion                     {belief_base_cnf}")

    print("AGM now")
    print(vacuity(belief_base_cnf, proposition))
    proposition2 = B | A
    print(extensionality(belief_base_cnf, proposition, proposition2))

main()

# & = AND
# | = OR
# ~ = NOT
# >> = IMPLIES1