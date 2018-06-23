import unittest
from rotation.rotation import *
from shapes.cube import *
from utils.color import *
from utils.misc import *

class TestMethods(unittest.TestCase):
    def test_rotation_360(self):
        """
        Rotating by 360 degrees should preserve the vector.
        """
        r = rotation(3, np.pi*2)
        vec = np.random.uniform(size=3)
        vec_rot = np.dot(r, vec)
        self.assertTrue(sum(abs(vec-vec_rot)/vec)<1e-5)

    def test_binary_vec(self):
        """
        Check that the conversion of cube vertice to binary form works.
        """
        v = Vertice(i=3, n=4)
        binary = v.to_binary()
        binary_str = bin(3)[::-1]
        b = True
        if int(binary_str[0]) != int(binary[0]):
            b = False
        if int(binary_str[1]) != int(binary[1]):
            b = False
        self.assertTrue(b)

    def test_heat_map(self):
        """
        Tests that the heat map when set at its maximum value, returns red.
        """
        self.assertTrue(heat_rgb(0,1,1)[0]==255)

    def test_move_to_closest(self):
        """
        Test moving a number to the closest one in an array.
        """
        self.assertTrue(move_to_closest(1.1,np.array([0,1,2]),0.9)==1.01)



if __name__ == '__main__':
    unittest.main()

