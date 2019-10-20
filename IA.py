import classes
import random

def randDecision(ip):
	return random.randrange(-1, 16)

def IAbasique(ip):
	if ip.carteActive == -1:
		if ip.phase == 1:
			if ip.pieces < 3: 
				return -1
			else:
				if ip.pieces < 6:
					return 4
				else:
					if ip.pieces < 8:
						return 5
					else:
						return 2
		else:
			return -1
	else:
		return 0

def IAmoyenne(ip):	
	if ip.carteActive == -1:
		if ip.phase == 0:
			forgeron = -1
			for i in range(ip.nbCartesMain):
				if ip.codesCartesMain[i] == 11:
					forgeron = i
			return forgeron
		else:
			if ip.phase == 1:
				if ip.pieces < 3: 
					return -1
				else:
					if (ip.nbTours < 2) and (ip.pieces > 3):
						return 11
					else:
						if ip.pieces < 6:
							return 4
						else:
							if ip.pieces < 8:
								return 5
							else:
								return 2
	else:
		if ip.carteActive == 12:
			defausse = -1
			for i in range(ip.nbCartesMain):
				if (ip.caracs[ip.codesCartesMain[i]][1] == 0):
					defausse = i
			if defausse == -1:
				for i in range(ip.nbCartesMain):
					if (ip.codesCartesMain[i] == 3):
						defausse = i
				if defausse == -1:
					for i in range(ip.nbCartesMain):
						if (ip.codesCartesMain[i] == 4):
							defausse = i
					if defausse == -1:
						for i in range(ip.nbCartesMain):
							if (ip.codesCartesMain[i] == 11):
								defausse = i
			return defausse
		else:
			return -1

def joueurHumain(ip):	
	if ip.carteActive == -1:
		if ip.phase == 0:
			print ("Actions :", ip.actions, "Pieces :", ip.pieces,\
				"Achats :", ip.achats)
			print ("Cartes en main")
			for i in range(ip.nbCartesMain):
				print (i, ":", ip.caracs[ip.codesCartesMain[i]][0])
			return int(input("Quelle carte poser? (-1 = aucune) : "))
		else:
			if ip.phase == 1:
				print ("Quantites cartes du marche :", ip.nbCartesDispo)
				print ("Cartes disponibles :")
				for i in range(len(ip.nbCartesDispo)):
					if (ip.nbCartesDispo[i] > 0) and (ip.caracs[i][2] <= ip.pieces):
						print (i , ":", ip.caracs[i][0], "$", ip.caracs[i][2])
				print ("Pieces :", ip.pieces, "Achats :", ip.achats)
				return int(input("Quelle carte acheter? (-1 = aucune) : "))
	else:
		if ip.carteActive == 8:
			print ("Quantites cartes du marche :", ip.nbCartesDispo)
			print ("Cartes disponibles :")
			for i in range(len(ip.nbCartesDispo)):
				if (ip.nbCartesDispo[i] > 0) and (ip.caracs[i][2] < 5):
						print (i , ":", ip.caracs[i][0], "$", ip.caracs[i][2])
			return int(input("Recevez une carte coutant 4 au plus : "))
		else:
			if ip.carteActive == 13:
				if ip.phaseCarte == 0:
					print ("Cartes en main")
					for i in range(ip.nbCartesMain):
						print (i, ":", ip.caracs[ip.codesCartesMain[i]][0])
					print ("1/2 : Ecartez une carte de votre main.")
					return int(input("Carte a ecarter : "))
				else:	
					print ("Quantites cartes du marche :", ip.nbCartesDispo)
					print ("Cartes disponibles :")
					for i in range(len(ip.nbCartesDispo)):
						if (ip.nbCartesDispo[i] > 0) and (ip.caracs[i][2] < ip.coutCarteChoisie + 3):
							print (i , ":", ip.caracs[i][0], "$", ip.caracs[i][2])
					print ("2/2 : Recevez une carte coutant", ip.coutCarteChoisie + 2, "au plus.")
					return int(input("Carte a recevoir : "))
			else:
				if ip.carteActive == 15:
					if ip.phaseCarte == 0:
						print ("Cartes en main")
						for i in range(ip.nbCartesMain):
							print (i, ":", ip.caracs[ip.codesCartesMain[i]][0])
						print ("1/2 : Ecartez une carte Tresor de votre main.")
						return int(input("Carte a ecarter : "))
					else:	
						print ("Quantites cartes du marche :", ip.nbCartesDispo)
						print ("Cartes disponibles :")
						for i in range(len(ip.nbCartesDispo)):
							if (ip.caracs[i][1] == 1) and (ip.caracs[i][2] < ip.coutCarteChoisie + 4) and (ip.nbCartesDispo[i] > 0):
								print (i , ":", ip.caracs[i][0], "$", ip.caracs[i][2])
						print ("2/2 : Recevez dans votre main une carte Tresor coutant", ip.coutCarteChoisie + 3, "au plus : ")
						return int(input("Carte a recevoir : "))
				else:
					if ip.carteActive == 6:
						print ("Cartes en main")
						for i in range(ip.nbCartesMain):
							print (i, ":", ip.caracs[ip.codesCartesMain[i]][0])
						return int(input("Defaussez des cartes pour en piocher autant (-1 = arret) : "))
					else:
						if ip.carteActive == 12:
							print ("Cartes en main")
							for i in range(ip.nbCartesMain):
								print (i, ":", ip.caracs[ip.codesCartesMain[i]][0])
							return int(input("Defaussez des cartes jusqu'à en n'avoir que trois : "))
						else:
							return -1
