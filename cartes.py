import classes
import IA
import random

def domaine(jeu):
	jeu.carteActive = -1
	return -1

def duche(jeu):
	jeu.carteActive = -1
	return -1

def province(jeu):
	jeu.carteActive = -1
	return -1

def cuivre(jeu):
	jeu.pieces += 1
	jeu.carteActive = -1
	return 0

def argent(jeu):
	jeu.pieces += 2
	jeu.carteActive = -1
	return 0
	
def gold(jeu):
	jeu.pieces += 3
	jeu.carteActive = -1
	return 0

def cave(jeu):
	jeu.actions += 1
	
	nbCartesDefaussees = 0
	arret = False
	while not(arret):
		
		jeu.strategies[jeu.joueurActif].miseAJourInput(jeu)
		c = jeu.strategies[jeu.joueurActif].getDecision()
	
		if (c > -1) and (c < len(jeu.joueurs[jeu.joueurActif].main)):
			nbCartesDefaussees += 1
			jeu.joueurs[jeu.joueurActif].defausse(c)
		else:
			arret = True
	
	jeu.joueurs[jeu.joueurActif].pioche(nbCartesDefaussees)
	
	jeu.carteActive = -1
	return 0

def douves(jeu):
	jeu.joueurs[jeu.joueurActif].pioche(2)
	jeu.carteActive = -1
	return 0

def atelier(jeu):
	jeu.strategies[jeu.joueurActif].miseAJourInput(jeu)
	c = jeu.strategies[jeu.joueurActif].getDecision()
	
	erreur = True
	if (c > -1) and (c < len(jeu.cartes)):
		if (jeu.cartes[c].cout < 5) and (jeu.nbCartes[c] != 0):
			jeu.joueurs[jeu.joueurActif].recoit(jeu, c)
			erreur = False
	
	if erreur:
		cartesEligibles = []
		for i in range(len(jeu.cartes)):
			if (jeu.cartes[i].cout < 5) and (jeu.nbCartes[i] != 0):
				cartesEligibles.append(i)
		if len(cartesEligibles) > 0:
			jeu.joueurs[jeu.joueurActif].recoit(jeu, \
				random.choice(cartesEligibles))
	
	jeu.carteActive = -1
	return 0

def bucheron(jeu):
	jeu.pieces += 2
	jeu.achats +=1
	jeu.carteActive = -1
	return 0

def village(jeu):
	jeu.joueurs[jeu.joueurActif].pioche(1)
	jeu.actions += 2
	jeu.carteActive = -1
	return 0

def forgeron(jeu):
	jeu.joueurs[jeu.joueurActif].pioche(3)
	jeu.carteActive = -1
	return 0

def milice(jeu):
	jeu.pieces += 2
	
	for i in range(len(jeu.joueurs)):
		if i != jeu.joueurActif:
			
			siDouves = False
			for c in jeu.joueurs[i].main:
				if c.nom == "Douves":
					siDouves = True
			
			if not(siDouves):
				while len(jeu.joueurs[i].main) > 3:
					
					jeu.strategies[i].miseAJourInput(jeu)
					c = jeu.strategies[i].getDecision()
					
					if (c > -1) and (c < len(jeu.joueurs[i].main)):
						jeu.joueurs[i].defausse(c)
					else:
						jeu.joueurs[i].defausse( \
							random.randrange(len(jeu.joueurs[i].main)))
					
	jeu.carteActive = -1
	return 0

def renovation(jeu):
	if len(jeu.joueurs[jeu.joueurActif].main) > 0:
		
		jeu.strategies[jeu.joueurActif].miseAJourInput(jeu)
		c = jeu.strategies[jeu.joueurActif].getDecision()
		
		coutCarteEcarte = -1
		if (c > -1) and (c < len(jeu.joueurs[jeu.joueurActif].main)):
			coutCarteEcarte = jeu.joueurs[jeu.joueurActif].main[c].cout
			jeu.joueurs[jeu.joueurActif].ecarte(c)
		else:
			randCarte = random.randrange(len(jeu.joueurs[jeu.joueurActif].main))
			coutCarteEcarte = jeu.joueurs[jeu.joueurActif].main[randCarte].cout
			jeu.joueurs[jeu.joueurActif].ecarte(randCarte)
		
		jeu.strategies[jeu.joueurActif].input.phaseCarte = 1
		jeu.strategies[jeu.joueurActif].input.coutCarteChoisie = coutCarteEcarte
		jeu.strategies[jeu.joueurActif].miseAJourInput(jeu)
		c = jeu.strategies[jeu.joueurActif].getDecision()
			
		erreur = True
		if (c > -1) and (c < len(jeu.cartes)):
			if (jeu.cartes[c].cout < coutCarteEcarte + 3) and (jeu.nbCartes[c] !=0):
				jeu.joueurs[jeu.joueurActif].recoit(jeu, c)
				erreur = False
			
		if erreur:
			cartesEligibles = []
			for i in range(len(jeu.cartes)):
				if (jeu.cartes[i].cout < coutCarteEcarte + 3) and \
					(jeu.nbCartes[i] != 0):
					cartesEligibles.append(i)
			if len(cartesEligibles) > 0:
				jeu.joueurs[jeu.joueurActif].recoit(jeu, \
					random.choice(cartesEligibles))
	
		jeu.strategies[jeu.joueurActif].input.phaseCarte = 0
		jeu.strategies[jeu.joueurActif].input.coutCarteChoisie = -1
	
	jeu.carteActive = -1
	return 0

def marche(jeu):
	jeu.joueurs[jeu.joueurActif].pioche(1)
	jeu.actions += 1
	jeu.pieces +=1
	jeu.achats += 1
	jeu.carteActive = -1
	return 0

def mine(jeu):
	if len(jeu.joueurs[jeu.joueurActif].main) > 0:
		
		jeu.strategies[jeu.joueurActif].miseAJourInput(jeu)
		c = jeu.strategies[jeu.joueurActif].getDecision()
		
		coutCarteEcarte = -1
		erreur = True
		if (c > -1) and (c < len(jeu.joueurs[jeu.joueurActif].main)):
			if jeu.joueurs[jeu.joueurActif].main[c].type == 1:
				coutCarteEcarte = jeu.joueurs[jeu.joueurActif].main[c].cout
				jeu.joueurs[jeu.joueurActif].ecarte(c)
				erreur = False
		
		if erreur:
			cartesEligibles = []
			for i in range(len(jeu.joueurs[jeu.joueurActif].main)):
				if jeu.joueurs[jeu.joueurActif].main[i].type == 1:
					cartesEligibles.append(i)
			if len(cartesEligibles) > 0:
				randCarte = random.choice(cartesEligibles)
				coutCarteEcarte = jeu.joueurs[jeu.joueurActif].main[randCarte].cout
				jeu.joueurs[jeu.joueurActif].ecarte(randCarte)
		
		if coutCarteEcarte != -1:
			jeu.strategies[jeu.joueurActif].input.phaseCarte = 1
			jeu.strategies[jeu.joueurActif].input.coutCarteChoisie = coutCarteEcarte
			jeu.strategies[jeu.joueurActif].miseAJourInput(jeu)
			c = jeu.strategies[jeu.joueurActif].getDecision()
				
			erreur = True
			if (c > -1) and (c < len(jeu.cartes)):
				if (jeu.cartes[c].cout < coutCarteEcarte + 4) \
					and  jeu.cartes[c].type == 1 \
					and (jeu.nbCartes[c] !=0):
					
					jeu.joueurs[jeu.joueurActif].acquiert(jeu, c)
					erreur = False
				
			if erreur:
				cartesEligibles = []
				for i in range(len(jeu.cartes)):
					if (jeu.cartes[i].cout < coutCarteEcarte + 4) \
						and  jeu.cartes[i].type == 1 \
						and (jeu.nbCartes[i] != 0):
						cartesEligibles.append(i)
				if len(cartesEligibles) > 0:
					jeu.joueurs[jeu.joueurActif].acquiert(jeu, \
						random.choice(cartesEligibles))
	
			jeu.strategies[jeu.joueurActif].input.phaseCarte = 0
			jeu.strategies[jeu.joueurActif].input.coutCarteChoisie = -1	
	
	jeu.carteActive = -1
	return 0

def creerEffets():
	dictFonctions = {0: domaine, 1: duche, 2: province, 3: cuivre, \
		4: argent, 5: gold, 6: cave, 7: douves, 8: atelier, 9: bucheron, \
		10: village, 11: forgeron, 12: milice, 13: renovation, 14: marche, \
		15: mine}
	return dictFonctions
	
def creerCaracteristiques():
	dictCarac = {0: ["* Domaine", 0, 2, 1], 1: ["** Duche", 0, 5, 3], \
		2: ["*** Province", 0, 8, 6], 3: ["$ Cuivre", 1, 0, 0], \
		4: ["$$ Argent", 1, 3, 0], 5: ["$$$ Or", 1, 6, 0], 6: ["Cave", 2, 2, 0], \
		7: ["Douves", 2, 2, 0], 8: ["Atelier", 2, 3, 0], \
		9: ["Bucheron", 2, 3, 0], 10: ["Village", 2, 3, 0], \
		11: ["Forgeron", 2, 4, 0], 12: ["Milice", 2, 4, 0], \
		13: ["Renovation", 2, 4, 0], 14: ["Marche", 2, 5, 0], \
		15: ["Mine", 2, 5, 0]}
	return dictCarac
