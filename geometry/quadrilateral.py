import math
from trianglesolver import solve

import pandas as pd
import matplotlib.pyplot as plt

# The quadrilateral looks like this, where F is the known angle, and
# FMA is the required angle.
# M is where the motor is connected
# A is the motor lever anchor point
# F is fixed lever point of the driven lever
# B is the moving end of the driven lever
#
#   M---A
#   |\  |
#   | \ |
#   |  \|
#   F---B
#


def mb_mfb(ang_in_degrees, joint_string):

    KNIE = {
        'MA': 54,       # 3
        'AB': 85.85,    # 4
        'FB': 34.6,     # 3
        'MF': 86.0      # 4
    }

    ENKEL = {
        'MA': 36.5,     # 3
        'AB': 89.4,     # 4
        'FB': 14.5,     # 3
        'MF': 117       # 4
    }

    if joint_string.lower() == 'enkel':
        joint = ENKEL
    elif joint_string.lower() == 'knie':
        joint = KNIE
    else:
        raise Exception('%s is not a known joint' % joint_string)

    # First solve the bottom triangle:
    #   A
    #   |\
    # c | \ b
    #   |  \
    #   B---C
    #     a
    # B is given and c and a is known
    MA = joint.get('MA')
    AB = joint.get('AB')
    FB = joint.get('FB')
    MF = joint.get('MF')

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

    # Lock
    # a2, b2, c2, A2, B2, C2 = solve(a=AB+FB, b=MF, c=MA)

    return math.degrees(A + A1)


def graph(joint_string, min=0, max=181):
    ser = []
    for i in range(min, max):
        try:
            res = mb_mfb(i, joint_string)
        except AssertionError:
            res = None
        ser.append([i, res])
    df = pd.DataFrame(ser, columns=[joint_string, 'motor'])

    fig = df.plot()
    fig.set(xlabel='grade', ylabel='grade')
    plt.title('Motor posisie vs %s posisie' % joint_string)
    # plt.show()
    plt.savefig('/home/gumm/Documents/luds/%s.png' % joint_string)

