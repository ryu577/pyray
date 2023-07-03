import numpy as np
from copy import deepcopy


def get_common_verts(verts1, verts2, thresh=0.1):
    """
    Gets the common vertices of two connected faces.
    Note: This can be made more efficient by storing
    the vertices in a certain order, etc. But we just
    have four vertices for each face, so we don't bother.
    """
    pts = []
    for i in range(len(verts1)):
        for j in range(len(verts2)):
            if sum((verts1[i] - verts2[j])**2) < thresh:
                pts.append(verts1[i])
    if len(pts) != 2:
        print("Two faces should only have two end\
               points intersecting.")
    return np.array(pts)


def rotate_points_about_plane2(face, ax1, ax2, ax3,
							  theta, ref_face=None,
							  rand_vec=np.array([.187,.226,.745,.401]),):
	"""
	Keeps the faces connected as rotation is happening.
	"""
	pts = face.vertices
	v4 = rand_vec
	pts4 = rotate_points_about_plane_helper(pts, ax1,
										   ax2, ax3,v4,
							  			   theta)
	if ref_face is not None:
		pts4_prime = rotate_points_about_plane_helper(pts, ax1, 
										   ax2, ax3,v4,
							  			   -theta)
		commons = get_common_verts(pts4, ref_face.vertices)
		if len(commons) < 2:
			return pts4_prime
	return pts4


def rotate_points_about_plane(pts, ax1, ax2, ax3,
							  theta, ref_pt=None,
							  rand_vec=np.array([.187,.226,.745,.401]),
							  take_farther=False):
	v4 = rand_vec
	pts4 = rotate_points_about_plane_helper(pts, ax1,
										   ax2, ax3,v4,
							  			   theta)
	if ref_pt is not None:
		pts4_prime = rotate_points_about_plane_helper(pts, ax1, 
										   ax2, ax3,v4,
							  			   -theta)
		pt4 = np.mean(pts4, axis=0)
		pt4_prime = np.mean(pts4_prime, axis=0)
		if np.sum((ref_pt-pt4_prime)**2)\
			 	 > np.sum((pt4-ref_pt)**2)\
									and take_farther:
			return pts4_prime, -1
		elif np.sum((ref_pt-pt4_prime)**2)\
			 	 < np.sum((pt4-ref_pt)**2)\
									and not take_farther:
			return pts4, 1
	return pts4, +1


def rotate_points_about_plane_helper(pts, ax1, ax2, ax3, v4,
							  		theta):
    v1 = ax1 - ax2
    v2 = ax2 - ax3
    v3 = np.mean(pts, axis=0) - ax1
    #v3 = np.random.norma(size=4)
    a = np.array([v1, v2, v3, v4])
    if np.linalg.cond(a) > 1e5:
        # print("The vectors aren't independent\
        #         as we were expecting. \
		# 		This is often because the points\
		# 		lie on the very plane of rotation.\
		# 		Hence, returning the points without rotating.")
        return pts
    e = four_vec_gram_schmidt(v1, v2, v3, v4)
    if np.linalg.det(e) < 0:
        v4 = -v4
        e = four_vec_gram_schmidt(v1, v2, v3, v4)
	# Make ax1 the origin.
    pts1 = pts - ax1
	# Express the point in the new basis.
    pts2 = np.dot(pts1, np.transpose(e))
	# Next, do the rotation.
	# e1 and e2 were aligned with the plane.
	# Now, the rotation should keep points on the plane fixed.
	# this is the reason only z-w parts of matrix have the rotation.
    rot = np.array([[1,0,0,0],
					[0,1,0,0],
					[0,0,np.cos(theta), np.sin(theta)], 
					[0,0,-np.sin(theta), np.cos(theta)]])
    pts2 = np.dot(pts2, rot)
	# Next, undo the change of basis.
    pts3 = np.dot(pts2, e)
	# Undo move of origin.
    pts4 = pts3 + ax1
    return pts4


def rotate_abt_plane(pts, ax1, ax2, ax3,
							  		theta):
    v1 = ax1 - ax2
    v2 = ax2 - ax3
    v3 = np.random.normal(size=4)
    v4 = np.random.normal(size=4)
    e = four_vec_gram_schmidt(v1, v2, v3, v4)
    if np.linalg.det(e) < 0:
        v4 = -v4
        e = four_vec_gram_schmidt(v1, v2, v3, v4)
    # Make ax1 the origin.
    pts1 = pts - ax1
	# Express the point in the new basis.
    pts2 = np.dot(pts1, np.transpose(e))
	# Next, do the rotation.
	# e1 and e2 were aligned with the plane.
	# Now, the rotation should keep points on the plane fixed.
	# this is the reason only z-w parts of matrix have the rotation.
    rot = np.array([[1,0,0,0],
					[0,1,0,0],
					[0,0,np.cos(theta), np.sin(theta)], 
					[0,0,-np.sin(theta), np.cos(theta)]])
    pts2 = np.dot(pts2, rot)
	# Next, undo the change of basis.
    pts3 = np.dot(pts2, e)
	# Undo move of origin.
    pts4 = pts3 + ax1
    return pts4


def two_vec_gram_schmidt(v1, v2):
	u1 = v1
	e1 = normalize(u1)
	u2 = v2 - project(u1, v2)
	e2 = normalize(u2)
	return e1, e2


def four_vec_gram_schmidt(v1, v2, v3, v4):
	if sum(v4==0) == len(v4):
		breakpoint()
	if sum(v3 == 0) == len(v3):
		breakpoint()
	if sum(v2 == 0) == len(v2):
		breakpoint()
	if sum(v1 == 0) == len(v1):
		breakpoint()
	u1 = v1
	e1 = normalize(u1)
	u2 = v2 - project(u1, v2)
	e2 = normalize(u2)
	u3 = v3 - project(u1, v3) - project(u2, v3)
	e3 = normalize(u3)
	if sum(u3 == 0.0) == len(u3):
		print("Inuput vectors weren't linearly independent.")
	u4 = v4 - project(u1, v4) - project(u2, v4)\
			- project(u3, v4)
	e4 = normalize(u4)
	return np.array([e1, e2, e3, e4])


def normalize(a):
	a = np.array(a)
	a = a.astype(float)
	sum1 = 0
	for e in a:
		sum1 += e**2
	a1 = deepcopy(a)
	sum1 = np.sqrt(sum1)
	for i in range(len(a)):
		a1[i] = float(a1[i]/sum1)
	return a1


def project(u, v):
	"""Project on u the vector v"""
	const = np.dot(v, u)/np.dot(u, u)
	return const*np.array(u)


def rotn_1(i=0):
    """
	Particularly nice rotation matrices in 4-d space.
	Close to maximize the shadow in 2-d space. The i revolves
	the object around.
	"""
    r1 = np.eye(4)
    r1[1:3,1:3] = \
            np.array([[np.cos(np.pi/4), np.sin(np.pi/4)],
                    [-np.sin(np.pi/4),np.cos(np.pi/4)]])
    r2 = np.eye(4)
    r2[0:2,0:2] = \
            np.array([[np.cos(np.pi/4), np.sin(np.pi/4)],
                    [-np.sin(np.pi/4),np.cos(np.pi/4)]])
    r = np.dot(r1, r2)
    r3 = np.eye(4)
    r3[np.ix_([0,3],[0,3])] = \
            np.array([[np.cos(np.pi/8*i/13), np.sin(np.pi/8*i/13)],
                    [-np.sin(np.pi/8*i/13),np.cos(np.pi/8*i/13)]])
    r = np.dot(r1, r2)
    r = np.dot(r, r3)
    return r


if __name__ == "__main__":
	a1 = np.array([1,1,1,1])
	a2 = np.array([0,0,0,1])
	a3 = np.array([1,1,0,1])
	a4 = np.array([1,2,3,4])
	aa = np.array([a1, a2, a3, a4])
	e = four_vec_gram_schmidt(a1, a2, a3, a4)
	aa1 = np.array([a1, a2, a3])
	np.dot(aa1, e)
