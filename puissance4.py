
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

# Initialise la grille de jeu

def initTableau() :
	tableau= 6*[0]
	for i in range (len(tableau)) :
		tableau[i]=7*[0]
	return tableau

# Verifier qu une case est libre

def verifCaseLibre( colonne, tableau) :
	verite=True
	if tableau[0][colonne]==0 :
		return True
	else :
		return False

# ajoute un jeton du joueur 1 sur une case		

def placerJetonJoueur1(tab) :
	colonne= int(input("colonne ?"))
	while verifCaseLibre(colonne-1,tab) == False :
		print("erreur, emplacement non disponible")
		colonne=int(input("nouvelle colonne ?"))
	i=5
	while tab[i][colonne-1] !=0 :
		i-=1
	tab[i][colonne-1]=1
	
	# ajoute un jeton du joueur 2 sur une case
	
def placerJetonJoueur2(tab) :
	colonne= int(input("colonne ?"))
	while verifCaseLibre(colonne-1,tab) == False :
		print("erreur, emplacement non disponible")
		colonne=int(input("nouvelle colonne ?"))
	i=5
	while tab[i][colonne-1] !=0 :
		i-=1
	tab[i][colonne-1]=2
	
	# Permet d afficher les jetons des joueurs par un X ou O
	
def affichageJeton(x) :
	if x==1 :
		return ("X")
	elif x==2 :
		return("O")
	else :
		return(" ")

# Permet d afficher la grille du jeu et son etat actuel

def afficheTableau(tab) :
	print("    |  C1  |  C2  |  C3  |  C4  |  C5   |  C6   |  C7 ", end='')
	for i in range(6):
		print("\n________________________________________________________")
		print("L", (i+1), "|", end='')
		for j in range(7) :
			print(" ", affichageJeton(tab[i][j]), "  |", end='')
	print("\n")
	
#Main permettant de lancer le jeu

def main() :
	tab=initTableau()
	compte=0
	while compte <42   :
		afficheTableau(tab)
		if compte%2 ==0 and verifVictoire(tab)==True :
			print("Victoire du joueur 2 !")
			break
		elif compte%2==1 and verifVictoire(tab)==True :
			print("Victoire du joueur 1 !")
			break
		else :
			if compte%2 ==0 :
				print("tour du joueur 1")
				placerJetonJoueur1(tab)
				compte=compte+1
			else :
				print("tour du joueur 2")
				placerJetonJoueur2(tab)
				compte=compte+1
		afficheTableau(tab)
		
main()


	

	
	
	
		
		
		
		
		