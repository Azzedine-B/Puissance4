import random

def display_who_begin():
	print("Qui commence ?")
	print("1. IA")
	print("2. Humain")

def display_difficulty():
	print("Veuillez choisir la difficulté de l'IA")
	print("1. Facile")
	print("2. Moyen")
	print("3. Forte")



def choose_who_begin():
	choice = 0
	display_who_begin()
	while(choice != 1 or choice != 2):
		try:
			choice = int(input("Saisissez votre choix : "))
			if(choice != 1 and choice != 2):
				print("Oops!  Votre choix semble incorrect.  Veuillez essayer a nouveau...")
			else:
				return choice
		except ValueError:
			print("Oops!  Saisie incorrect.  Veuillez essayer a nouveau...")

def choose_random_token():
	"""choose a random token for the AI"""
	return random.choice(["X", "O"])

def choose_remaining_token(choosen_token):
	"""choose the remaining token for the user"""
	return "X" if choosen_token == "O" else "O"

def choose_human_token():
	token = ""
	print("Veuillez choisir votre symbole (X ou O)")
	while(not (token == "X" or token == "O")):
		token = input()

		if(token != "X" and token != "O"):
			print("Oops!  Votre choix semble incorrect.  Veuillez essayer a nouveau...")
		else:
			return token

def choose_difficulty():
	difficulty = 0
	while(difficulty != 1 and difficulty != 2 and difficulty != 3):
		try:
			display_difficulty()
			difficulty = int(input("Saisissez votre choix : "))
			if(difficulty != 1 and difficulty != 2 and difficulty != 3):
				print("Oops!  Votre choix semble incorrect.  Veuillez essayer a nouveau...")
			else:
				return difficulty
		except ValueError:
			print("Oops!  Saisie incorrect.  Veuillez essayer a nouveau...")

def token_distribution(choice):
	if(choice == 1): # if the AI starts, chooses a token randomly and assigns the remaining token to the player
		token_player1 = choose_random_token()
		token_player2 = choose_remaining_token(token_player1)
		print("L'IA a choisi les {}, vous aurez donc les {}".format(token_player1, token_player2))
	else: # 
		token_player1 = choose_human_token()
		token_player2 = choose_remaining_token(token_player1)
		print("Vous avez choisi les {}, l'IA aura donc les {}".format(token_player1, token_player2))

	return token_player1, token_player2

def determine_depth(difficulty):
	"""chooses the depth according to the difficulty"""
	if(difficulty == 1):
		return 2
	elif(difficulty == 2):
		return 4
	else:
		return 5

def player_turn():
	column = 0
	while(column <= 0 or column > 7):
		print("Entrez la colonne souhaite :")
		try:
			column = int(input())
			if(column < 0 and column > 7):
				print("Oops!  Votre choix semble incorrect.  Veuillez essayer a nouveau...")
			else:
				return column
		except ValueError:
			print("Oops!  Saisie incorrect.  Veuillez essayer a nouveau...")
