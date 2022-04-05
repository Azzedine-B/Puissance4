import numpy as np

# Creer la liste de toutes les combinaisons de 4 jetons sur l ensemble des lignes
def verifVictoireLigne(tab) :
	liste=[]
	for i in range(6) :
		for j in range(4) :
			l1=[]
			for h in range (4) :
				l1.append(tab[i][j+h])
			liste.append(l1)
	return liste

# Creer la liste de toutes les combinaisons de 4 jetons sur l ensemble des colonnes 
def verifVictoireColonne(tab) :
	liste=[]
	for i in range(7) :
		for j in range(3) :
			l1=[]
			for h in range(4) :
				l1.append(tab[j+h][i])
			liste.append(l1)
	return liste

# Creer la liste de toutes les combinaisons de 4 jetons sur l ensemble des diagonales
def verifVictoireDiago(tab) :
	liste=[]
	l=[]															
	for i in range(4) :
		l.append(tab[3-i][i])
	liste.append(l)
	l=[]
	for i in range(4) :
		l.append(tab[2+i][i])
	liste.append(l)
	l=[]
	for i in range(4) :
		l.append(tab[i][3+i])
	liste.append(l)
	l=[]
	for i in range(4) :
		l.append(tab[2+i][6-i])
	liste.append(l)
	
	
	
	l=[]
	l1=[]
	for i in range(4) :
		l.append(tab[4-i][i])
		l1.append(tab[3-i][1+i])
	liste.append(l)
	liste.append(l1)
	l=[]
	l1=[]
	for i in range(4) :
		l.append(tab[5-i][2+i])
		l1.append(tab[4-i][3+i])
	liste.append(l)
	liste.append(l1)
	l=[]
	l1=[]
	for i in range(4) :
		l.append(tab[i+1][i])
		l1.append(tab[i+2][1+i])
	liste.append(l)
	liste.append(l1)
	l=[]
	l1=[]
	for i in range(4) :
		l.append(tab[i][i+2])
		l1.append(tab[i+1][i+3])
	liste.append(l)
	liste.append(l1)
	
	
	l=[]
	l1=[]
	l2=[]
	for i in range(4) :
		l.append(tab[5-i][i])
		l1.append(tab[4-i][i+1])
		l2.append(tab[3-i][i+2])
	liste.append(l)
	liste.append(l1)
	liste.append(l2)
	l=[]
	l1=[]
	l2=[]
	for i in range(4) :
		l.append(tab[5-i][1+i])
		l1.append(tab[4-i][i+2])
		l2.append(tab[3-i][i+3])
	liste.append(l)
	liste.append(l1)
	liste.append(l2)
	l=[]
	l1=[]
	l2=[]
	for i in range(4) :
		l.append(tab[i][i])
		l1.append(tab[i+1][i+1])
		l2.append(tab[i+2][i+2])
	liste.append(l)
	liste.append(l1)
	liste.append(l2)
	l=[]
	l1=[]
	l2=[]
	for i in range(4) :
		l.append(tab[i][i+1])
		l1.append(tab[i+1][i+2])
		l2.append(tab[i+2][i+3])
	liste.append(l)
	liste.append(l1)
	liste.append(l2)
	return liste
	

#Verifie que la liste des combinaisons ne contient pas une combinaison gagnante
def verifVictoire(tab) :
	liste = verifVictoireColonne(tab) + verifVictoireLigne(tab) + verifVictoireDiago(tab)
	if [1,1,1,1] in liste or [2,2,2,2] in liste :
		return True
	else :
		return False

def fulled_board(board):
	for i in range(board.shape[0]):
		for j in range(board.shape[1]):
			if(board[i,j] == 0):
				return False
	return True

def number_of_pawns(board):
	number_of_pawns = 0
	for i in range(board.shape[0]):
		for j in range(board.shape[1]):
			if(board[i,j] == 1 or board[i,j] == 2):
				number_of_pawns += 1

	return number_of_pawns

# Initialise la grille de jeu
def initTableau() :
	tableau = np.zeros((6,7))
	return tableau

# Verifier qu une case est libre
def verifCaseLibre(colonne, tableau) :
	verite=True
	if tableau[0][colonne]==0 :
		return True
	else:
		return False

	
# ajoute le jeton du joueur sur une case
def placerJeton(numJoueur, tab, column) :
	if verifCaseLibre(column-1,tab) == False :
		raise ValueError("erreur, emplacement non disponible")
	i=5
	while tab[i][column-1] !=0 :
		i-=1
	tab[i][column-1]= numJoueur
	
	# Permet d afficher les jetons des joueurs par un X ou O
	
def affichageJeton(x, symbol_player1, symbol_player2) :
	if x==1 :
		return symbol_player1
	elif x==2 :
		return symbol_player2
	else :
		return(" ")

# Permet d afficher la grille du jeu et son etat actuel

def afficheTableau(tab, symbol_player1, symbol_player2) :
	print("    |  C1  |  C2  |  C3  |  C4  |  C5   |  C6   |  C7 ", end='')
	for i in range(6):
		print("\n________________________________________________________")
		print("L", (i+1), "|", end='')
		for j in range(7) :
			print(" ", affichageJeton(tab[i][j], symbol_player1, symbol_player2), "  |", end='')
	print("\n")
