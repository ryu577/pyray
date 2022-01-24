import numpy as np


def jarvis_convex_hull(points):
    """
    Returns points in the order required for a convex hull.
    A native alternative to scipy.spatial.ConvexHull
    args:
        points: An array of numpy arrays representing
        the points to be convex hulled in any order.
    """
    start_index = np.argmax(points[:, 0])  # Point with the highest y-coordinate
    start_point = points[start_index]
    # result = [start_index[:]]
    result = [start_index]
    added_points = {start_index}
    while True:
        for ref_index, ref_point in enumerate(points):
            exit_ = True
            if ref_index == start_index or ref_index in added_points:
                continue

            signs = 0
            threshold = len(points) - 2
            for compare_index, compare_point in enumerate(points):
                if compare_index == ref_index or compare_index == start_index:
                    continue
                check = compare(start_point, ref_point, compare_point)
                if abs(check) < 1e-2:
                    dist_start_ref = distance(start_point, ref_point)
                    dist_start_compare = distance(start_point, compare_point)
                    if dist_start_compare > dist_start_ref:
                        threshold = threshold + 1
                    else:
                        threshold = threshold - 1
                    continue
                signs = signs + 1 if check > 0 else signs - 1

            if abs(signs) < threshold:
                continue

            exit_ = False
            result.append(ref_index[:])
            added_points.add(ref_index)
            start_index = ref_index
            break

        if exit_:
            return result


def distance(pt1, pt2):
    """
    Simple 2d euclidean distances between two points.
    args:
        pt1: The first point.
        pt2: The second point.
    """
    return (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2


def compare(first_point, ref_point, compare_point):
    """
    I don't know exaclty what does this formula... anybody can explain ?
    """
    x2, y2 = first_point
    x1, y1 = ref_point
    x3, y3 = compare_point
    m = (y2 - (y1 * 1.00001)) / (x2 - (x1 * 1.00001))
    return y3 - y1 - m * (x3 - x1)
