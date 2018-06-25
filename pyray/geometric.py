import numpy as np


def jarvis_convex_hull(points):
    """
    Returns points in the order required for a convex hull. A native alternative to scipy.spatial.ConvexHull
    args:
        points: An array of numpy arrays representing the points to be convex hulled in any order.
    """
    start_indx = np.argmax(points[:,0]) #Point with the highest y-coordinate
    res = []
    res.append( (points[start_indx][0], points[start_indx][1]) )
    added_points = set()
    added_points.add(start_indx)
    while True:
        for i in range(len(points)):
            exit = True
            if i != start_indx and i not in added_points:
                signs = 0
                threshold = len(points) - 2
                for j in range(len(points)):
                    if j != i and j != start_indx:
                        m = (points[i][1] - points[start_indx][1] * 1.00001)/(points[i][0] - points[start_indx][0] * 1.00001)
                        check = points[j][1] - points[start_indx][1] - m * (points[j][0] - points[start_indx][0])
                        if abs(check) < 1e-2:
                            if dist(points[start_indx],points[j]) > dist(points[start_indx],points[i]):
                                threshold = threshold + 1
                            else:
                                threshold = threshold - 1
                        elif  check > 0:
                            signs = signs + 1
                        else:
                            signs = signs - 1
                if abs(signs) >= threshold:
                    exit = False
                    res.append( (points[i][0], points[i][1]))
                    added_points.add(i)
                    start_indx = i
                    break
        if exit:
            return res


def dist(pt1,pt2):
    """
    Simple 2d euclidean distances between two points.
    args:
        pt1: The first point.
        pt2: The second point.
    """
    return (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2
