import numpy as np
from pyray.rotation2.rotn_4d import four_vec_gram_schmidt


def get_rotation_plane(f1, f2):
    """
    Gets the plane about which rotations should
    occur for two connected faces of a Tesseract
    or other four dimensional solid. The f1 and f2
    are faces.
    """
    [pt1, pt2] = get_common_verts(f1, f2)
    v1 = pt1 - pt2
    v2 = pt2 - f1.face_center
    v3 = pt1 - f2.face_center
    v4 = np.random.uniform(size=4)
    # Check if resulting matrix is full-rank as expected.
    # Taken from: https://stackoverflow.com/a/13252541/1826912
    a = np.array([v1, v2, v3, v4])
    if np.linalg.cond(a) > 1e5:
        print("The vectors aren't independent\
                as we were expecting!")
        breakpoint()
    e = four_vec_gram_schmidt(v1, v2, v3, v4)
    u4 = e[3]
    pt3 = pt1 + u4
    return pt1, pt2, pt3


def get_common_verts(f1, f2):
    """
    Gets the common vertices of two connected faces.
    Note: This can be made more efficient by storing
    the vertices in a certain order, etc. But we just
    have four vertices for each face, so we don't bother.
    """
    pts = []
    for i in range(4):
        for j in range(4):
            if sum((f1.vertices[i] - f2.vertices[j])**2) < 0.1:
                pts.append(f1.vertices[i])
    if len(pts) != 2:
        print("Two faces should only have two end\
               points intersecting.")
        breakpoint()
    return np.array(pts)


if __name__== "__main__":
    print("0")
