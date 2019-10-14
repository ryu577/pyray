import numpy as np
from pyray.rotation import planar_rotation


class Line(object):
    def __init__(self,pt1,pt2):
        """
        """
        self.pt1 = pt1
        self.pt2 = pt2
        self.vec_along = (pt2-pt1)
        r = planar_rotation(np.pi/2)
        self.w = np.dot(r,self.vec_along)
        mod_w_sq = np.dot(self.w,self.w)
        self.w = self.w/np.sqrt(mod_w_sq)
        # Eqn of line is assumed to be w^T x+b=0
        self.b = -np.dot(self.w,self.pt1)
        self.closest_pt_from_origin = -self.b*self.w


