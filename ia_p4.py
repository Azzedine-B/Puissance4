import sys
import math
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

"""
On remplace terminal_test par cutoff_test
"""
def cutoff_test(initial_state, state, depth):
	if(terminal_test(state)):
		return True
	if(p4.number_of_pawns(state) - p4.number_of_pawns(initial_state) == depth):
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

"""
Alignement possibles a partir du jeton considere :
- jeton en 1er position (on progresse positivement)
- jeton en 2eme position (on progresse du negatif au positif)
- jeton en 3eme position (identique a 2eme mais en partant du positif vers les negatif)
- jeton en dernière position (identique a 1ere mais en partant dans les negatifs)

Pour chaque jeton, on calcul une utilite dans les 8 directions cardinal et pour les deux configurations.


"""

def alignment_evaluation(state, alignment, num_player):
	if 1 in alignment and 2 in alignment:
		return 0
	elif((1 in alignment and not 2 in alignment) or (2 in alignment and not 1 in alignment)):

		# continuer a réfléchir sur ce problème
		if(num_player in alignment and not 0 in alignment):
			return 10000
		elif(not num_player in alignment and not 0 in alignment):
			return -10000

		evaluation = 1

		for i in range(4):
			if(alignment[i] == 0):
				evaluation *= 1
			else:
				evaluation *= 10

		if(not num_player in alignment):
			evaluation *= -1

		return evaluation
	else:
		return 0


def evaluation(state, num_player):
	liste = p4.verifVictoireColonne(state) + p4.verifVictoireLigne(state) + p4.verifVictoireDiago(state) 
	evaluation = 0
	for l in liste:
		evaluation += alignment_evaluation(state, l, num_player)

	return evaluation



"""
On remplace utility(state, num_player) par evaluation(state, num_player)

Principe :
----------
On parcours tout le plateau
Seul les alignements de 4 pions ou les alignement ou il les configurations ou il encore possible
d'obtenir un alignement de 4 pions sont consideres.
Leurs resultats sont positif (en faveur du joueur qui calcul l'utilite) ou negatif (en sa defaveur)
On calcul l'utilite de chaque pion dans toutes les directions cardinales possibles : Nord, Sud, Est, Ouest, Nord-Est, Nord-Ouest, Sud-Est, Sud-Ouest
L'utilite d'un pion est la somme de ses utilites dans les directions citees precedement
L'utilite total du plateau est la somme de toutes les utilites de chaque pions 

Calcul :
--------
On commence avec une utilite de :
- 1 si le pion considere est celui du joueur
- -1 si le pion est celui du joueur adverse

On parcours le plateau dans les toutes les directions, en prenant une direction a chaque fois :
- si dans la case adjacente il y a un pion appartenant au joueur on multiplie par 10
- si la case adjacente est vide on multiplie par 5
- si dans la case adjacente il y a un pion appartenant au joueur adverse on multiplie par 0
"""
def successors(state):
	"Retourne l'ensemble des actions et des etats qu'elles generent a partir d'un etat (s)"
	actions_state = {}
	for a in action(state):
		actions_state[a] = result(state, a)
	return actions_state


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
		return evaluation(state, 1 if player(state) == 2 else 2) 
	v = math.inf
	for a, s in successors(state).items(): # a : action, s : state
		v = min(v, max_value(initial_state ,s, depth))
	return v

def max_value(initial_state, state, depth): # cutoff_test and evaluation
	"Maximise l'utilite"
	if cutoff_test(initial_state, state, depth):
		return evaluation(state, player(state))
	v = - math.inf
	for a, s in successors(state).items(): # a : action, s : state
		v = max(v, min_value(initial_state, s, depth))
	return v



#Main permettant de lancer le jeu

def main() :
	tab= p4.initTableau()
	while(True):
		print("Qui commence ? (IA ou Humain)")
		response = input()
		if(response == "IA"):
			human_turn = 2
		elif(response == "Humain"):
			human_turn = 1
		else:
			print("Je n'ai pas compris votre choix, merci de bien vouloir recommencer")

		print(response, " Veuillez choisir votre jeton (X ou O)")

		token = input()
		token_player1 = token
		if(token == "X"):
			token_player2 = "O"
			break
		elif(token == "O"):
			token_player2 = "X"
			break
		else:
			print("Caractere incorrect veuillez recommencer")

	# num_player = 1
	p4.afficheTableau(tab, token_player1, token_player2)
	while True:
		if p4.verifVictoire(tab)==True :
			print("Victoire des " + (token_player1 if player(tab) == 2 else token_player2)) # numero inverse du joueur car il change en fin de boucle
			break
		elif p4.fulled_board(tab) and not p4.verifVictoire(tab):
			print("Match nul")
			break
		else :
			print("Au tour des " + (token_player1 if player(tab)  == 1 else token_player2))
			if(player(tab) == human_turn):
				print("Entrez la colonne souhaite :")
				column = int(input())
				p4.placerJeton(player(tab), tab, column)
			else:
				action = minimax_descision(tab, 4)
				p4.placerJeton(action[0], tab, action[1])
			# compte=compte+1
			# num_player = 1 if num_player == 2 else 2
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
- 

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
def max_value(state, alpha, beta): # alpha-beta
	if(terminal_test(state)):
		return utility(state, 2)

	v = -1000
	for a, s in successors(state).items(): # a : action, s : state
		print(alpha, beta)
		v = max(v, min_value(state, alpha, beta))
		if(v >= beta):
			return v
		alpha = max(alpha, v)

	return v


def min_value(state, alpha, beta): # alhpa-beta
	if(terminal_test(state)):
		return utility(state, 2)

	v = 1000
	for a, s in successors(state).items(): # a : action, s : state
		print(alpha, beta)
		v = min(v, max_value(state, alpha, beta))
		if(v <= alpha):
			return v
		beta = min(beta, v)
	return v
"""
