import numpy as np


'''
    Returns a triangular function oscillating between an upper and lower bound (hard coded for now).
'''
def zigzag(x):
    if x < 1:
        return 1 + x
    elif 1 <= x and x < 10:
        return 3 - x
    elif 10 <= x and x <= 22:
        return -17 + x
    else:
        return zigzag(x%22)


def scatter(n = 8, l = 5):
    res = np.ones(l) * int(n/l)
    excess = n - sum(res)
    i = 0
    while excess > 0:
        res[i] += 1
        excess -= 1
        if excess > 0:
            res[len(res)-1-i] += 1
            excess -= 1
        i = i + 1
    return res

def assign(n = 10, level = 3):
    res = np.zeros(n)
    res[n-1] = level-1
    sct = scatter(n-2, level-2)
    k = 1
    l = 0
    for i in sct:
        l = l + 1
        for j in range(int(i)):
            res[k] = l
            k = k + 1
    return res


def move_to_closest(theta, tri, p):
    final = tri[np.argmin((tri-theta)**2)]
    return theta + (final - theta) * p


def move_angle_to_angle(theta1, theta2, p):
    return theta1 + (theta2-theta1) * p

