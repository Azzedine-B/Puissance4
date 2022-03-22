import puissance4 as p4

def player(state):
	"Definie quel joueur doit jouer dans l'etat (s)"
	number_of_pawns = 0
	for line in range(len(state[0] ) - 1):
		for column in range(len(state[1]) - 1):
			if(state[line][column] == 1 or state[line][column] == 2):
				number_of_pawns += 1

	return 1 if(number_of_pawns % 2 == 0) else 2

def action(state):
	"Retourne l'ensemble des actions possibles dans l'etat (s)"
	actions = []
	for i in range(state.shape[1]):
		if(p4.verifCaseLibre(i, state)):
			actions.append(i + 1)
	return tuple(actions)

def result(state, action):
	"Fonction de transition qui definit quel est le resultat de l'action (a) dans l'etat (state)"
	transitional_board = state.copy()
	p4.placerJeton(action[0], transitional_board, action[1])
	return transitional_board