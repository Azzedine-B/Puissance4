import unittest
import puissance4 as p4
import ia_p4

class p4IaAlgorithms(unittest.TestCase):
# A testcase is created by subclassing unittest.Tescase
# The three individual tests are defined with methods whose names start with letters test
# assertEquals() : to check for an expected result
# assertTrue(), assertFalse() : to verify a condition
# assertRaises() to verify that a specific exception gets raised
# setUp() and tearDown(): allow to define instructions that will be executed before and after each test method

    def setUp(self):
        self.board = p4.initTableau()

 
    def test_player(self):
        self.assertEqual(ia_p4.player(self.board), 1)
        p4.placerJetonJoueur1(self.board, 1)
        self.assertEqual(ia_p4.player(self.board), 2)

if __name__ == '__main__':
    unittest.main()