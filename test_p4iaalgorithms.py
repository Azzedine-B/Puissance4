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

    def victory_scenario_player1(self):
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 2)
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 2)
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 2)
        p4.placerJeton(1, self.board, 1)

    def victory_scenario_player2(self):
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 2)
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 2)
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 2)
        p4.placerJeton(1, self.board, 3)
        p4.placerJeton(1, self.board, 2)

    def draw_scenario(self):
        switch = True
        for i in range(1, 7):
            for j in range(1, 8, 2):
                if(switch):
                    p4.placerJeton(1, self.board, j)
                    switch = False
                else:
                    p4.placerJeton(2, self.board, j)
                    switch = True
            for j in range(2, 8, 2):
                if(switch):
                    p4.placerJeton(1, self.board, j)
                    switch = False
                else:
                    p4.placerJeton(2, self.board, j)
                    switch = True

        print(self.board)



    def filled_column(self):
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 1)
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 1)
        p4.placerJeton(1, self.board, 1)
        p4.placerJeton(2, self.board, 1)


    def test_player(self):
        # le plateau est vide, c'est au joueur 1 de jouer
        self.assertEqual(ia_p4.player(self.board), 1)
        # le joueur 1 joue
        p4.placerJeton(1, self.board, 1)
        # c'est au joueur 2 de jouer
        self.assertEqual(ia_p4.player(self.board), 2)


    def test_action(self):
        # lorsque le plateau est vide, toute les colonnes sont disponibles dans les actions pour le joueur 1
        self.assertEqual(ia_p4.action(self.board), ((1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7)))
        # on rempli un colonne de jetons
        self.filled_column()
        # la colonne n'est plus disponible dans les actions pour le joueur 1
        self.assertEqual(ia_p4.action(self.board), ((1,2), (1,3), (1,4), (1,5), (1,6), (1,7)))

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
        self.victory_scenario_player1()
        self.assertTrue(ia_p4.terminal_test(self.board))


    def test_utility(self):
        # -1 pour le joueur 1 et 2 lorsque le plateau est vide
        self.assertEqual(ia_p4.utility(self.board, 1), -1)
        self.assertEqual(ia_p4.utility(self.board, 2), -1)


        # le joueur 1 a gagne 
        self.victory_scenario_player1()

        # 1 pour le joueur 1 et -1 pour le joueur 2
        self.assertEqual(ia_p4.utility(self.board, 1), 1)
        self.assertEqual(ia_p4.utility(self.board, 2), -1)


    def test_utility_draw(self):
        # 0 pour les deux joueur lors d'un match nul
        self.assertEqual(ia_p4.utility(self.board, 1), 0)
        self.assertEqual(ia_p4.utility(self.board, 2), 0)

    def test_successors(self):
        # actions possible lorsque le plateau est vide : toutes les colonnes peuvent acceuillir les jetons dans leur derniere ligne
        actions_set = {}

        for i in range(1, 8):
            plateau = p4.initTableau()
            p4.placerJeton(1, plateau, i) # on place les jetons du joueur 1 pour generer actions_set necessaire au test
            actions_set[(1,i)] = plateau

        self.assertTrue(ia_p4.successors(self.board), actions_set)

    def test_min_value(self):

        # - 1 d'utilite pour le joueur 2 lorsque la partie commence
        self.assertEqual(ia_p4.min_value(self.board, 2), -1)

        print(self.draw_scenario())

"""
        # 1 d'utilite pour le joueur 1 lorsqu'il a gagne
        self.victory_scenario_player1()
        self.assertEqual(ia_p4.min_value(self.board, 1), 1)
"""


if __name__ == '__main__':
    unittest.main()