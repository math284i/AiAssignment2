from sympy.logic.boolalg import to_cnf
from sympy import symbols, And, Or, Not
from sympy.abc import R, P, S


# CNF Tests
# CNF ((¬r ∨ p ∨ s) ∧ (¬p ∨ r ) ∧ (¬s ∨ r ) ∧ ¬r) = ¬p ∧ ¬r ∧ ¬s (i foegle wolfram alpha)


print(to_cnf((~R | P | S) & (~P | R) & (~S | R) & ~R)) # prints which is wrong ~R & (R | ~P) & (R | ~S) & (P | S | ~R)R
assert(to_cnf((~R | P | S) & (~P | R) & (~S | R) & ~R) == (~P & ~R & ~S))