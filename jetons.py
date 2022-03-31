def peut_diviser(pile, indice , nb_jetons_pile1, nb_jetons_pile2):
	"Permet de déterminer si la division de la pile est possible"
	if(nb_jetons_pile1 == nb_jetons_pile2):
		return False
	if(nb_jetons_pile1 + nb_jetons_pile2 > sum(pile)):
		return False
	if(nb_jetons_pile1 + nb_jetons_pile2 != pile[indice]):
		return False
	else:
		return True


def diviser_pile(pile, indice, nb_jetons_pile1, nb_jetons_pile2):
	"Divise la pile si cela est possible"
	if(peut_diviser(pile, indice, nb_jetons_pile1, nb_jetons_pile2)):
		sub_pile = [nb_jetons_pile1, nb_jetons_pile2]
		new_pile = []
		for i, val in enumerate(pile):
			if(i != indice):
				new_pile.append(val)
		new_pile = new_pile + sub_pile
		new_pile.sort()
		return new_pile
	else:
		raise ValueError("Il n'est pas possible de diviser la pile de cette maniere")


def afficher_pile(pile):
	"Affiche la pile"
	string = ""
	for jeton in pile:
		string += str(jeton) + " "
	return string

def a_perdu(pile):
	"Détermine si le joueur a perdu"
	for val in pile:
		if(val != 1 and val != 2):
			return False
	return True


"""
Algorithmes relatifs a l'IA
"""

"""
Formalisme d'une action:

(indice, nb_jetons_pile1, nb_jetons_pile2) 

Formalise d'un etat:

la pile

"""

def player(state):
	"Definie quel joueur doit jouer dans l'etat s"
	if(len(state) % 2 == 0):
		return 2
	else:
		return 1


def action(state):
	"Retourne l'ensemble des actions possibles dans l'etat (s)"
	actions = []
	for i, val in enumerate(state):
		for j in range(1, val):
			# si la division de la pile ne cree pas de pile vide ou deux piles de valeurs identiques
			# et que le tuple n'est pas deja enregistre dans les actions, alors on l'ajoute
			if(val - j != j and val - j != 0 and (not actions.count((i, j, val - j)) and not actions.count((i, val - j, j)))):
				actions.append((i, j, val - j))
	return actions


def result(state, a):
	"Fonction de transition qui definit quel est le resultat de l'action dans (a) dans l'etat (s)"
	transitional_pile = state.copy()
	result_pile = diviser_pile(transitional_pile, a[0], a[1], a[2])
	return result_pile

def terminal_test(state):
	"Test de terminaison (ou test terminal). Vrai si le jeu est fini dans l'etat (s)"
	for val in state:
		if(val != 1 and val != 2):
			return False
	return True

def utility(state, nb_player):
	"Fonction d'utilité : associe une valeur numérique a chaque etat terminal (s) pour un joueur (p)"
	if(terminal_test(state) and player(state) == nb_player):
		return -1
	else:
		return 1

def successors(state): 
	"Retourne l'ensemble des actions et des etats qu'elles generent a partir d'un etat (s)"
	action_state = {}
	actions_set = action(state)
	for a in actions_set:
		action_state[a] = result(state, a)
	return action_state

def min_value(state):
	"Minimise l'utilite adverse"
	if terminal_test(state):
		return utility(state, 1) # s'il s'agit du tour du joueur 1 alors renvoi -1 sinon 1
	v = 1000
	results = []
	for a, s in successors(state).items():
		v = min(v, max_value(s))
	return v

def max_value(state):
	"Maximise l'utilite"
	if terminal_test(state):
		return utility(state, 1) # s'il s'agit du tour du joueur 1 alors renvoi -1 sinon 1 : donc on peux
	v = -1000
	results = []
	for a, s in successors(state).items(): # a : action, s : state
		v = max(v, min_value(s))
	return v

def minimax_descision(state):
	"Retourne l'action qui maximise l'utilite"
	results = {}
	for a in action(state):
		results[a] = min_value(result(state, a))
	max_key = max(results, key= results.get)
	print(results)
	return max_key


def main():
	"Boucle de jeu"
	nb_jetons = 10

	pile = [nb_jetons]
	while(not terminal_test(pile)):
		print(pile)
		if(player(pile) == 2):
			print(f"Au joueur n°{player(pile)} de joueur")
			action = input().split() #recupere les entrees du joueur
			action = list(map(int, action)) # converti les chaines entrees en entiers
		if(player(pile) == 1):
			print("Coup de l'IA")
			action = minimax_descision(pile)
		try:
			pile = diviser_pile(pile, action[0], action[1], action[2])
		except IndexError as ie:
			print("Saisie incorrect")
		except ValueError as ve:
			print(ve)

	print(pile)
	if(player(pile) == 1):
		print("L'IA a perdu")
	else:
		print("L'IA a gagné")


main()



