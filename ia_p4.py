def player(state):
	"Definie quel joueur doit jouer dans l'etat (s)"
	number_of_pawns = 0
	for line in range(len(state[0] ) - 1):
		for column in range(len(state[1]) - 1):
			if(state[line][column] == 1):
				number_of_pawns += 1

	return 1 if(number_of_pawns % 2 == 0) else 2