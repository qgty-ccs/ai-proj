from z3 import *

# p, q = Bools('p q')
# demorgan = And(p, q) == Not(Or(Not(p), Not(q)))
# print demorgan

def prove(f, cons):
    s = Solver()
    s.add(cons)
    s.add(Not(f))
    if s.check() == unsat:
        return True
    else:
        return False

# print "Proving demorgan..."
# print prove(demorgan)


def noShip(CELL, BLOCK_LEN, SHIP_LEN):

  Isolated = Function('Isolated', IntSort(), IntSort(), BoolSort())
  NoShip = Function('NoShip', IntSort(), IntSort(), BoolSort())
  # cell - a cell number
  # blk_len - continous isolated block length
  # ship_len - requested ship length

  cell, blk_len, ship_len = Ints('cell blk_len ship_len')

  axioms = [ 
            # 
            # ForAll([cell, blk_len, ship_len], 
            #         Implies(And(Isolated(cell, blk_len), blk_len == 1), NoShip(cell,ship_len))),
            ForAll([cell, blk_len, ship_len], 
                    Implies(And(Isolated(cell, blk_len), blk_len > 0, ship_len > 0, ship_len > blk_len), NoShip(cell,ship_len)))]

  vals = [And(cell == CELL, blk_len == BLOCK_LEN, ship_len == SHIP_LEN, Isolated(cell, blk_len))]
  # solve(vals + axioms)
  return prove(NoShip(1, 3), axioms + vals)


# TODO use inference to find all isolated blocks and their members

# 1. C has two opposite positions visited before (one of them can be N/A)
# 2. C 
C => Isolated(C)

# TODO use inference to find which block should be hit next (and return them)

