import puissance4 as p4

def player(state):
	"Definie quel joueur doit jouer dans l'etat (s)"
	number_of_pawns = 0
	for line in range(state.shape[0]):
		for column in range(state.shape[1]):
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
	if(p4.verifVictoire(state)):
		return True
	if(p4.fulled_board(state)):
		return True
	return False

def utility(state, num_player):
	"Fonction d'utilité : associe une valeur numérique a chaque etat terminal (s) pour un joueur (p)"
	if(p4.verifVictoire(state) and player(state) != num_player):
		return 1
	elif(p4.verifVictoire(state) and player(state) == num_player):
		return -1
	else:
		return 0

def successors(state):
	"Retourne l'ensemble des actions et des etats qu'elles generent a partir d'un etat (s)"
	actions_state = {}
	for a in action(state):
		actions_state[a] = result(state, a)
	return actions_state

def min_value(state):
	"Minimise l'utilite adverse"
	if terminal_test(state):
		return utility(state, 2) 
	v = 1000
	for a, s in successors(state).items(): # a : action, s : state
		v = min(v, max_value(s))
	return v

def max_value(state): 
	"Maximise l'utilite"
	if terminal_test(state):
		return utility(state, 2)
	v = -1000
	for a, s in successors(state).items(): # a : action, s : state
		v = max(v, min_value(s))
	return v

def minimax_descision(state):
	"Retourne l'action qui maximise l'utilite"
	results = {}
	for a in action(state):
		results[a] = min_value(result(state, a))
	max_key = max(results, key= results.get)
	return max_key


board = p4.initTableau()

print(minimax_descision(board))

"""
Trouver le problème du bloquage de minimax_decision 
"""