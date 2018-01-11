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

'''
'''
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

'''

'''
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

'''
Move an angle, theta towards the target it is closest to in an array of angles. The extent of movement is dedicated by p.
args:
	theta: Angles that is to be moved.
	tri: Array of angles. The closest one is chosen and theta moves towards it.
	p: The extent to which the movement happens. 1 means full movement to the element of tri.
'''
def move_to_closest(theta, tri, p):
    final = tri[np.argmin((tri-theta)**2)]
    return theta + (final - theta) * p

'''
Move a number towards another number (here, the numbers were angles).
args:
	theta1: The first number
	theta2: The second number
	p: The extent of movement. 1 means full movement.
'''
def move_angle_to_angle(theta1, theta2, p):
    return theta1 + (theta2-theta1) * p



'''
Given two points, gives us the coefficients for a parabola.
args:
	pt1: The first point.
	pt2: The second point.
'''
def two_pt_parabola(pt1,pt2):
    [x1, y1] = pt1 * 1.0
    [x2, y2] = pt2 * 1.0
    a = (y2-y1)/(x2-x1)**2
    c = y1 + a*x1*x1
    b = -2*a*x1
    return [a,b,c]


'''
Represents a number, n in number system with base b.
'''
def GeneralBase(n, b):
    res = np.zeros(3)
    indx = 0
    while(n > 0):
        res[indx] = (n % b)
        indx = indx + 1
        n = n / b
    return res

