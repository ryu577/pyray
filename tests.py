import unittest
from rotation.rotation import *


class TestRotationMethods(unittest.TestCase):
	def test_upper(self):
		# Rotating by 260 degrees should preserve the vector.
        r = rotation(3, np.pi*2)
        vec = np.random.uniform(size=3)
        vec_rot = np.dot(r, vec)
        self.assertTrue(sum(abs(vec-vec_rot)/vec)<1e-5)


if __name__ == '__main__':
    unittest.main()

