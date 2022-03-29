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
			actions.append((player(state), i + 1))
	return tuple(actions) # retour sous forme de tuple

def result(state, action):
	"Fonction de transition qui definit quel est le resultat de l'action (a) dans l'etat (state)"
	transitional_board = state.copy()
	p4.placerJeton(action[0], transitional_board, action[1])
	return transitional_board

def terminal_test(state):
	"Test de terminaison (ou test terminal). Vrai si le jeu est fini dans l'etat (s)"
	return p4.verifVictoire(state)

def utility(state, num_player):
	if(terminal_test(state) and player(state) != num_player):
		return 1
	else:
		return -1

def successors(state):
	"Retourne l'ensemble des actions et des etats qu'elles generent a partir d'un etat (s)"
	actions_state = {}
	actions_set = action(state)
	for a in actions_set:
		actions_state[a] = result(state, a)
	return actions_state




"""
Faire une fonction qui place le jeton adequate en fonction de l'etat de jeu.

Exemple :

Si le jeu commence et que c'est au joueur 1 de commencer : le programme sait qu'il faut placer le jeton du joueur 1
En plein milieu de partie, le programme verifie l'etat de jeu : il sait qu'il faut placer tel jeton  selon cette situation

--> une situation : le bon jeton

Definir une situation
A partir de cette situation, definir un jeton

"""