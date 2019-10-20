import init
import classes
import func
import simul
import cartes
import random
#import test

niveau = 1

random.seed()

param = init.loadParam()
	
effets = cartes.creerEffets()
caracs = cartes.creerCaracteristiques()
iaTest = classes.ia(caracs, niveau)
	
pop = classes.population(param)
init.replayPopFromText(param, pop, caracs)

init.preparerPopulation(param, pop)
		
partie = classes.jeu(pop.indiv[0], iaTest)
partie.miseEnPlace(caracs)
	
while (partie.nbCartes.count(0) < 3) and (partie.nbCartes[2] > 0):
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

vainqueur = partie.trouveVainqueur()
	
for j in partie.joueurs:
	print ("Joueur", j.code,	"Points :", j.points, \
		"Nombre de Tours :", j.nbTours)
	for c in partie.cartes:
		qte = j.main.count(c) + j.recyclage.count(c) + j.paquet.count(c)
		if qte > 0:	
			print (c.nom, ":", qte)

print ("Vainqueur : Joueur", vainqueur, \
	"Points :",  partie.joueurs[vainqueur].points, \
	"Nombre de tours :", partie.joueurs[vainqueur].nbTours)