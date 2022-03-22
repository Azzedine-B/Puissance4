import unittest
import puissance4 as p4
import ia_p4

class p4IaAlgorithms(unittest.TestCase):
# A testcase is created by subclassing unittest.Tescase
# T
# Tests are defined with methods whose names start with letters "test"
# assertEquals() : to check for an expected result
# assertTrue(), assertFalse() : to verify a condition
# assertRaises() to verify that a specific exception gets raised
# setUp() and tearDown(): allow to define instructions that will be executed before and after each test method

    def setUp(self):
        self.board = p4.initTableau()

    def victory_scenario(self):
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 2)
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 2)
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 2)
        p4.placerJeton(2, self.board, 2)

    def filled_column(self):
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 1)
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 1)
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 1)


    def test_player(self):
        # le plateau est vide, cr'est au joueur 1 de jouer
        self.assertEqual(ia_p4.player(self.board), 1)
        # le joueur 1 joue
        p4.placerJeton(1, self.board, 1)
        # c'est au joueur 2 de jouer
        self.assertEqual(ia_p4.player(self.board), 2)


    def test_action(self):
        # lorsque le plateau est vide, toute les colonnes sont disponibles dans les actions
        self.assertEqual(ia_p4.action(self.board), (1, 2, 3, 4, 5, 6, 7))
        # on rempli un colonne de jetons
        self.filled_column()
        # la colonne n'est plus disponible dans les actions
        self.assertEqual(ia_p4.action(self.board), (2, 3, 4, 5, 6, 7))

    def test_result(self):
        # le plateau vide est égal au plateau vide
        initial_state = self.board.copy()
        self.assertEqual(self.board.all(), initial_state.all())
        # on rempli la 1ere colonne
        p4.placerJeton(1, self.board, 1)
        # le plateau est dans le meme etat en effectuant l'action
        self.assertEqual(ia_p4.result(self.board, (1,1)).all() , self.board.all())

        # on rempli la 3eme colonne
        p4.placerJeton(2, self.board, 3)
        # le plateau est dans le meme etat en effectuant l'action
        self.assertEqual(ia_p4.result(self.board, (2,3)).all(), self.board.all())

    def test_terminal_test(self):
        # faux lorsque le plateau est vide
        self.assertFalse(ia_p4.terminal_test(self.board))

        # vrai après une victoire du joueur 1
        self.victory_scenario()
        self.assertTrue(ia_p4.terminal_test(self.board))








if __name__ == '__main__':
    unittest.main()