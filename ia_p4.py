import math
import puissance4 as p4
import random

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
	# choisir aleatoirement un des resultats max
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
		if(v >= beta): # Si V est pire que beta, MIN va l’eviter --> elaguer la branche
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
		if(v <= alpha): # Si V est pire que alpha, MAX va l’eviter --> elaguer la branche
			return v
		beta = min(beta, v)
	return v



#Main permettant de lancer le jeu
def main() :
	tab= p4.initTableau()
	choice = 0
	token_player1 = ""
	token_player2 = ""
	while(True):
		while(not (choice == 1 or choice == 2)):
			print("Qui commence ?")
			print("1. IA")
			print("2. Humain")
			try:
				choice = int(input("Saisissez votre choix : "))
				if(choice != 1 and choice != 2):
					print("Oops!  Votre choix semble incorrect.  Veuillez essayer a nouveau...")
				else:
					human_turn = 1 if choice == 2 else 2
					break
			except ValueError:
				print("Oops!  Saisie incorrect.  Veuillez essayer a nouveau...")


		if(choice == 1): # faire un tirage aléatoire ici
			print("L'IA a choisi la X, vous aurez donc le O")
			token_player1 = "X"
			token_player2 = "O"
		else:
			token = ""
			while(not (token == "X" or token == "O")):
				print("Veuillez choisir votre symbole (X ou O)")
				token = input()

				if(token != "X" and token != "O"):
					print("Oops!  Votre choix semble incorrect.  Veuillez essayer a nouveau...")
				else:
					token_player1 = token
					token_player2 = "X" if token_player1 == "O" else "O"

		difficulty = 0
		while(not (difficulty == 1 or difficulty == 2 or difficulty == 3)):
			print("Veuillez choisir la difficulté de l'IA")
			print("1. Facile")
			print("2. Moyen")
			print("3. Forte")
			try:
				difficulty = int(input("Saisissez votre choix : "))
				if(difficulty != 1 and difficulty != 2 and difficulty != 3):
					print("Oops!  Votre choix semble incorrect.  Veuillez essayer a nouveau...")
					break
			except ValueError:
				print("Oops!  Saisie incorrect.  Veuillez essayer a nouveau...")

		if(difficulty == 1):
			depth = 2
		elif(difficulty == 2):
			depth = 3
		else:
			depth = 5

		p4.afficheTableau(tab, token_player1, token_player2)
		while True:
			if p4.verifVictoire(tab)==True :
				print("Victoire des " + (token_player1 if player(tab) == 2 else token_player2)) # numero inverse du joueur car il change en fin de boucle
				break
			elif p4.fulled_board(tab) and not p4.verifVictoire(tab):
				print("Match nul")
				break
			else:
				print("Au tour des " + (token_player1 if player(tab)  == 1 else token_player2))
				if(player(tab) == human_turn):
					column = 0
					while(column <= 0 or column > 7):
						print("Entrez la colonne souhaite :")
						try:
							column = int(input())
							if(column < 0 and column > 7):
								print("Oops!  Votre choix semble incorrect.  Veuillez essayer a nouveau...")
							else:
								p4.placerJeton(player(tab), tab, column)
							break
						except ValueError:
							print("Oops!  Saisie incorrect.  Veuillez essayer a nouveau...")
				else:
					action = alpha_beta_decision(tab, depth)
					p4.placerJeton(action[0], tab, action[1])
			p4.afficheTableau(tab, token_player1, token_player2)


main()



"""
Fonction heuristique pour le puissance 4 :
-----------------------------------------

Deux posibilitées pour l'heuristique :
- Considérer un jeton
- Considérer un alignement


Considéré un jeton :
-------------------
- on calcul le taux de cernement d'un pion
Ex : 

 O   O   O 
---|---|----
 X | O | X
---|---|----
 O   O   O
 """


"""
désavantages :
-------------
- Long : on traite chaque pion (donc on parcours tout le plateau), puis son voisinage :
42 * 5 (en moyenne) 210 




Validité de l'heuristique :
--------------------------




L'heuristique bloque litérallement tous les coups mais peine a gagner

Interpretation des résultats :
On rappel que MAX maximise ce que MIN minimise

- Une IA qui bloque tous les coups :
le coup qui bloque est le max qu'il puisse faire par rapport a tous ce que min remonte
--> tres bien, c'est ce qui est attendu d'une bonne IA

- IA qui peine a gagner :
3 alignements deja disponible, c'est au tour de l'IA de jouer, pourtant elle ne choisi pas de gagner
--> un autre coup est plus avantageux 
voyons voir
Selon les resultats observées, elle ne choisi par la possibilité à près 10000 : c'est étrange
La fonction continue d'aller en profondeur meme quand le jeu est terminée
"""

# sys.setrecursionlimit(10**9)


"""
p4.placerJeton(1, board, 1)
p4.placerJeton(2, board, 2)
p4.placerJeton(1, board, 3)
p4.placerJeton(1, board, 4)
p4.placerJeton(1, board, 5)
p4.placerJeton(2, board, 6)
p4.placerJeton(1, board, 7)
p4.placerJeton(2, board, 1)
p4.placerJeton(2, board, 2)
p4.placerJeton(1, board, 3)
p4.placerJeton(1, board, 4)
p4.placerJeton(2, board, 5)
p4.placerJeton(1, board, 6)
p4.placerJeton(2, board, 7)
p4.placerJeton(2, board, 1)
p4.placerJeton(2, board, 2)
p4.placerJeton(1, board, 4)
p4.placerJeton(2, board, 5)
p4.placerJeton(2, board, 6)
p4.placerJeton(1, board, 1)
p4.placerJeton(2, board, 5)
p4.placerJeton(1, board, 6)
"""


"""

def minimax_descision(state, depth): # cutoff_test and evaluation
	"Retourne l'action qui maximise l'utilite"
	results = {}
	for a in action(state):
		results[a] = min_value(state, result(state, a), depth)
	print(results)
	max_key = max(results, key= results.get)
	return max_key

def min_value(initial_state, state, depth): # cutoff_test and evaluation
	"Minimise l'utilite adverse"
	if cutoff_test(initial_state, state, depth):
		# return token_evaluation(state, 1 if player(state) == 2 else 2)
		return evaluation(state, 1 if player(state) == 2 else 2) 
	v = math.inf
	for a, s in successors(state).items(): # a : action, s : state
		v = min(v, max_value(initial_state ,s, depth))
	return v

def max_value(initial_state, state, depth): # cutoff_test and evaluation
	"Maximise l'utilite"
	if cutoff_test(initial_state, state, depth):
		#return token_evaluation(state, player(state))
		return evaluation(state, player(state))
	v = - math.inf
	for a, s in successors(state).items(): # a : action, s : state
		v = max(v, min_value(initial_state, s, depth))
	return v



def alpha_beta_decision(state, depth):
	results = {}
	for a in action(state):
		# print("*************** Tour, Alpha:", alpha , "Beta:", beta)
		results[a] = minimax(state, result(state, a), depth, False, -math.inf, math.inf)
	print(results)
	max_key = max(results, key= results.get)
	return max_key


def minimax(initial_state, state, depth, is_maximizing_player, alpha, beta):
	if terminal_test(state):
		return utility(state, player(initial_state))

	if cutoff_test(initial_state, state, depth):
		return evaluation(state, player(initial_state))
    
	if is_maximizing_player:
		best_val = (-math.inf) 
		for a, s in successors(state).items(): # a : action, s : state
			value = minimax(initial_state, s, depth, False, alpha, beta)
			best_val = max(best_val, value) 
			alpha = max(alpha, best_val)
			# print("Alpha:",best_val)
			if beta <= alpha:
				break
		return best_val

	else :
		best_val = math.inf
		for a, s in successors(state).items(): # a : action, s : state
			value = minimax(initial_state, s, depth, True, alpha, beta)
			best_val = min(best_val, value) 
			beta = min(beta, best_val)
			# print("Beta:", beta)
			if beta <= alpha:
				break
		return best_val

def token_evaluation(state, num_player):
	evaluation = 0
	for i in range(state.shape[0]):
		for j in range(state.shape[1]):
	 		token_evaluation = 1 if state[i,j] == num_player else -1
	 		for i2 in range(i-1, i+1):
	 			if(i2 < 0 or i2 >= state.shape[0]):
	 				continue
	 			for j2 in range(j-1, j+1):
	 				if(j2 < 0 or j2 >= state.shape[1] or (i2 == i and j2== j)):
	 					continue
	 				if(state[i2,j2] == num_player):
	 					token_evaluation *= 100
	 				elif(state[i2,j2] != num_player):
	 					token_evaluation -= 1000
	 				else:
	 					token_evaluation += 0
	 		evaluation += token_evaluation

	return token_evaluation


def alignment_evaluation2(state, alignment, num_player):
	if 1 in alignment and 2 in alignment:
		return 0
	elif((1 in alignment and not 2 in alignment) or (2 in alignment and not 1 in alignment)):

		# continuer a réfléchir sur ce problème
		if(num_player in alignment and not 0 in alignment):
			return math.inf
		elif(not num_player in alignment and not 0 in alignment):
			return -math.inf
		elif(not num_player in alignment):
			cpt = 0
			for token in alignment: 
				if(token != 0):
					cpt += 1
			if(cpt > 2):
				return - 100000
			else:
				return -1000
		elif(num_player in alignment):
			cpt = 0
			for token in alignment:
				if(token != 0):
					cpt += 1
			if(cpt == 2):
				return 100000
			elif(cpt == 3):
				return 1000000
			else:
				return 10000
	else:
		return 0

Le but du puissance 4 :
- bloquer le joueur pour l'empecher de gagner
- aligner le plus de pion possible

Lorsque l'ennemi a moins de 3 pions aligne, opter pour l'option aligner le plus de pion possible
Lorsque l'ennemi a 3 pions aligner le bloquer 

"""