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
	"""
	terminal test si : 
		- victoire
		- match nul

	victoire : p4.verifVictoire(state)
	match nul : ???
	"""
	return p4.verifVictoire(state)

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
	actions_set = action(state)
	for a in actions_set:
		actions_state[a] = result(state, a)
	return actions_state

def min_value(state): # opposing_player_number correspond au numero du joueur adverse
	"Minimise l'utilite adverse"
	if terminal_test(state):
		# print("je suis passe par terminal test de max_value")
		return utility(state, 1) 
	v = 1000
	results = []
	for a, s in successors(state).items():
		print(s)
		v = min(v, max_value(s))
	return v

def max_value(state): # opposing_player_number correspond au numero du joueur adverse
	"Maximise l'utilite"
	if terminal_test(state):
		# print("je suis passe par terminal test de min_value")
		return utility(state, 1)
	v = -1000
	results = []
	for a, s in successors(state).items(): # a : action, s : state
		print(s)
		v = max(v, min_value(s))
	return v

def minimax_descision(state):
	"Retourne l'action qui maximise l'utilite"
	results = {}
	for a in action(state):
		results[a] = min_value(result(state, a))
	max_key = max(results, key= results.get)
	return max_key

"""
Minimax_decision doit obligatoirement prendre en parametre le numero du joueur ??

elle utilise min_value et max_value qui utilisent elles-mêmes utility(s,p) 
"""