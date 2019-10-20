import func
import suivi
import sys

import classes
import cartes
import IA
import random

def simulation(param, ind0, ind1, effets, caracs):
	partie = classes.jeu(ind0, ind1)
	partie.miseEnPlace(caracs)
	nbTours = 0
	
	while (nbTours < param['maxTours']) and (partie.nbCartes.count(0) < 3) and (partie.nbCartes[2] > 0):
		#print ("Phase Action")
		arret = False
		while (partie.actions > 0) and (not(arret)):
			partie.strategies[partie.joueurActif].miseAJourInput(partie)
			succes = partie.joueurs[partie.joueurActif].pose(partie, effets, \
				partie.strategies[partie.joueurActif].getDecision())
			if succes == -1:
				arret = True
		
		partie.phase = 1
		#print ("Phase Achat")
		partie.joueurs[partie.joueurActif].posePieces(partie, effets)
		arret = False
		while (partie.achats > 0) and (not(arret)):
			partie.strategies[partie.joueurActif].miseAJourInput(partie)
			succes = partie.joueurs[partie.joueurActif].achete(partie, \
				partie.strategies[partie.joueurActif].getDecision())
			if succes == -1:
				arret = True
		
		partie.phase = 2
		#print ("Phase Ajustement")
		partie.joueurs[partie.joueurActif].finitTour()
		partie.reinitTour()
		nbTours += 1
	
	ind = [ind0, ind1]
	
	if (nbTours < param['maxTours']) or (partie.nbCartes.count(0) >= 3) or (partie.nbCartes[2] == 0):
		vainqueur = partie.trouveVainqueur()
		v = partie.joueurs[vainqueur]
		ind[vainqueur].score += 51 - v.nbTours

		perdant = (vainqueur + 1) % 2
		p = partie.joueurs[perdant]

		print(' ')
		print ('    Vainqueur ' + str(ind[vainqueur].nom) + '.' + str(ind[vainqueur].espece) + ' tr ' + str(v.nbTours) +\
			' pt ' + str(v.points))
		for c in partie.cartes:
			qte = v.main.count(c) + v.recyclage.count(c) + v.paquet.count(c)
			if qte > 0:
				print("   ", c.nom, ":", qte)
		
		print(' ')
		print ('Perdant ' + str(ind[perdant].nom) + '.' + str(ind[perdant].espece) + ' tr ' + str(p.nbTours) +\
			' pt ' + str(p.points))
		for c in partie.cartes:
			qte = p.main.count(c) + p.recyclage.count(c) + p.paquet.count(c)
			if qte > 0:	
				print(c.nom, ":", qte)
	
	else:
		fauxVainqueur = partie.trouveVainqueur()
		for j in partie.joueurs:
			print(' ')
			print ('ID ' + str(ind[j.code].nom) + '.' + str(ind[j.code].espece) + ' tr ' + str(j.nbTours) +\
			' pt ' + str(j.points))
			for c in partie.cartes:
				qte = j.main.count(c) + j.recyclage.count(c) + j.paquet.count(c)
				if qte > 0:	
					print (c.nom, ":", qte)
