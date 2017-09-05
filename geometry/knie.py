import math
from trianglesolver import solve


MA = 54     # 3
AB = 85.85  # 4
FB = 34.6   # 3
MF = 86.0   # 4

# The quadrilateral looks like this, where F is the known angle, and
# FMA is the required angle.
#   M---A
#   |\  |
#   | \ |
#   |  \|
#   F---B
#


def mb_mfb(ang_in_degrees):
    # First solve the bottom triangle:
    #   A
    #   |\
    # c | \ b
    #   |  \
    #   B---C
    #     a
    # B is given and c and a is known
    ang = math.radians(ang_in_degrees)
    a, b, c, A, B, C = solve(c=MF, a=FB, B=ang)

    # Then solve the top triangle
    #     c
    #   A---B
    #    \  |
    #   b \ | a
    #      \|
    #       C
    #  a, b and c is know
    a1, b1, c1, A1, B1, C1 = solve(a=AB, b=b, c=MA)

    return math.degrees(A + A1)



