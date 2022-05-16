import puissance4 as p4
import math
import random
import interface

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

def cutoff_test(initial_state, state, depth):
	"Test de terminaison intermediaire. Vrai si l'etat de jeu correspond a la profondeur souhaitee"
	if(p4.number_of_pawns(state) - p4.number_of_pawns(initial_state) == depth):
		return True
	return False

def utility(state, num_player):
	"Fonction d'utilité : associe une valeur numérique a chaque etat terminal (s) pour un joueur (p)"
	if(p4.verifVictoire(state) and player(state) != num_player):
		return math.inf
	elif(p4.verifVictoire(state) and player(state) == num_player):
		return - math.inf
	else:
		return 0

def alignment_evaluation(state, alignment, num_player):
	"Evalu un alignement donnee"
	if 1 in alignment and 2 in alignment:
		return 0
	elif((1 in alignment and not 2 in alignment) or (2 in alignment and not 1 in alignment)):

		# continuer a réfléchir sur ce problème
		if(num_player in alignment and not 0 in alignment):
			return math.inf
		elif(not num_player in alignment and not 0 in alignment):
			return -math.inf

		evaluation = 1

		for i in range(4):
			if(alignment[i] == 0):
				evaluation *= 1
			else:
				evaluation *= 10

		if((2 if num_player == 1 else 1) in alignment):
			evaluation *= -1

		return evaluation
	else:
		return 0

def evaluation(state, num_player):
	"Permet d’évaluer un jeu à un état donné, pour un joueur donné. "
	liste = p4.verifVictoireColonne(state) + p4.verifVictoireLigne(state) + p4.verifVictoireDiago(state) 
	evaluation = 0
	for l in liste:
		evaluation += alignment_evaluation(state, l, num_player)

	return evaluation


def successors(state):
	"Retourne l'ensemble des actions et des etats qu'elles generent a partir d'un etat (s)"
	actions_state = {}
	for a in action(state):
		actions_state[a] = result(state, a)
	return actions_state


def alpha_beta_decision(state, depth):
	results = {}
	for a in action(state):
		results[a] = min_value(state, result(state, a), -math.inf, math.inf, depth)
	print(results)
	max_val = max(results.values())
	# choisi aleatoirement une valeur maximum s'il y en a plusieurs
	return random.choice([k for (k,v) in results.items() if v == max_val])

def max_value(initial_state, state, alpha, beta, depth):
	"alpha : meilleure valeur (la plus grande) pour MAX trouve jusqu'a present en dehors du chemin actuel"
	"beta : meilleur valeur (la plus petite) pour MIN jusqu’a present"

	if terminal_test(state):
		return utility(state, player(initial_state))

	if cutoff_test(initial_state, state, depth):
		return evaluation(state, player(initial_state))

	v = - math.inf
	for a, s in successors(state).items(): # a : action, s : state
		v = max(v, min_value(initial_state, result(state, a), alpha, beta, depth))
		if(v >= beta): # If v is worse than beta, MIN will avoid it --> prune the branch
			return v
		alpha = max(alpha, v)
	return v

def min_value(initial_state, state, alpha, beta, depth):
	"alpha : meilleure valeur (la plus grande) pour MAX trouve jusqu'a present en dehors du chemin actuel"
	"beta : meilleur valeur (la plus petite) pour MIN jusqu’a present"
	if terminal_test(state):
		return utility(state, player(initial_state))

	if cutoff_test(initial_state, state, depth):
		return evaluation(state, player(initial_state))

	v = math.inf
	for a, s in successors(state).items(): # a : action, s : state
		v = min(v, max_value(initial_state, s, alpha, beta, depth))
		if(v <= alpha): # If v is worse than alpha, MAX will avoid it --> prune the branch
			return v
		beta = min(beta, v)
	return v

def game(): 
	tab= p4.initTableau()
	choice = interface.choose_who_begin()

	human_turn = 1 if choice == 2 else 2

	token_player1, token_player2 = interface.token_distribution(choice)

	difficulty = interface.choose_difficulty()

	depth = interface.determine_depth(difficulty)

	p4.afficheTableau(tab, token_player1, token_player2)
	while True:
		if p4.verifVictoire(tab)==True :
			print("Victoire des " + (token_player1 if player(tab) == 2 else token_player2)) # inverse number of the player because it changes at the end of the loop
			break
		elif p4.fulled_board(tab) and not p4.verifVictoire(tab):
			print("Match nul")
			break
		else:
			print("Au tour des " + (token_player1 if player(tab)  == 1 else token_player2) + (" (IA)" if human_turn != player(tab) else " (Humain)"))
			if(player(tab) == human_turn):
				column = interface.player_turn()
				p4.placerJeton(player(tab), tab, column)
			else:
				if(difficulty != 1):
					action = alpha_beta_decision(tab, depth)
				else:
					action = (player(tab), random.randint(1, 7))
				p4.placerJeton(action[0], tab, action[1])
		p4.afficheTableau(tab, token_player1, token_player2)


#Main permettant de lancer le jeu
def main() :
	choice = 1
	while(choice != 0):
		game()
		print("Voulez-vous recommencer ?")
		print("Entrez 0 pour quitter")
		print("Ou tout autre chiffre pour continuer")
		try:
			choice = int(input())
		except ValueError:
			print("Oops!  Saisie incorrect.  Veuillez essayer a nouveau...")
	


main()
