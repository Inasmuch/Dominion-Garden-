import random
import cartes
import IA
import func

class gene:
	
	def __init__(self):
		self.inNode = 0
		self.outNode = 0
		self.weight = 0
		self.encr = 0
		self.active = False
		self.code = 0	
			
	def copyTo(self, g):
		g.inNode = self.inNode
		g.outNode = self.outNode
		g.weight = self.weight
		g.active = self.active
		g.code = self.code

class ADN:
	
	def __init__(self, param):
		self.seqGene = []
		i = param['nbInput']
		o = param['nbOutput']
		t = param['maxNodesInt']
		self.siInLibre = [True for x in range(i)]
		self.siOutLibre = [True for x in range(o)]
		self.siEncrLibre = [True for x in range(o*(i + 1) + t*(i + o + t))]
		self.encOffset = o + t
		self.nbNodeInt = 0

	def addGene(self, g):
		self.seqGene.append(g)

	def compteGene(self):
		return len(self.seqGene)

	def compteMaxGene(self):
		return (self.compteInActif() + self.nbNodeInt)*(self.compteOutActif()\
			+ self.nbNodeInt + self.compteEncrActif()) - self.nbNodeInt 
	
	def addNodeInt(self):
		self.nbNodeInt += 1
		self.siInLibre.append(False)
		self.siOutLibre.append(False)
	
	def setNbNodeInt(self, nbNode):
		for node in range(nbNode):
			self.addNodeInt()

	def compteInLibre(self):
		return self.siInLibre.count(True)
	
	def compteInActif(self):
		return self.siInLibre.count(False)

	def selectInLibre(self):
		randNode = random.randrange(self.compteInLibre())
		for node in range(len(self.siInLibre)):
			if self.siInLibre[node]:
				if randNode == 0:
					return node
				else:
					randNode -= 1

	def selectInActif(self):
		randNode = random.randrange(self.compteInActif())
		for node in range(len(self.siInLibre)):
			if not self.siInLibre[node]:
				if randNode == 0:
					return node
				else:
					randNode -= 1

	def compteOutLibre(self):
		return self.siOutLibre.count(True)

	def compteOutActif(self):
		return self.siOutLibre.count(False)

	def selectOutLibre(self):
		randNode = random.randrange(self.compteOutLibre())
		for node in range(len(self.siOutLibre)):
			if self.siOutLibre[node]:
				if randNode == 0:
					return node
				else:
					randNode -= 1

	def selectOutActif(self):
		randNode = random.randrange(self.compteOutActif() + self.compteEncrActif())
		if randNode < self.compteOutActif():
			for node in range(len(self.siOutLibre)):
				if not self.siOutLibre[node]:
					if randNode == 0:
						return node
					else:
						randNode -= 1
		else:
			randNode -= self.compteOutActif()
			for node in range(len(self.siEncrLibre)):
				if not self.siEncrLibre[node]:
					if randNode == 0:
						return node
					else:
						randNode -= 1

	def compteEncrActif(self):
		return self.siEncrLibre.count(False)
	
	def compteEncrLibre(self):
		return self.siEncrLibre.count(True)

	def selectEncryptionTarget(self):
		randGene = list(range(self.compteGene()))
		random.shuffle(randGene)
		selectedGene = 0

		for i in range(self.compteGene()):
			if self.siEncrLibre[self.seqGene[randGene[i]].code \
				+ self.encOffset]:
				if self.seqGene[randGene[i]].outNode < self.encOffset:
					selectedGene = randGene[i]
		
		return self.seqGene[selectedGene]

	def tellSiGene(self, code):
		for g in self.seqGene:
			if g.code == code:
				return True
		return False

	def findGene(self, code):
		for g in self.seqGene:
			if g.code == code:
				return g

	def reset(self, param):
		del self.seqGene[:]
		i = param['nbInput']
		o = param['nbOutput']
		t = param['maxNodesInt']
		self.siInLibre = [True for x in range(i)]
		self.siOutLibre = [True for x in range(o)]
		self.siEncrLibre = [True for x in range(o*(i + 1) + t*(i + o + t))]
		self.nbNodeInt = 0

class indiv:
	
	def __init__(self, param, caracs):
		self.ADN = ADN(param)
		
		self.nom = 0
		self.age = 0
		self.parent1 = 0
		self.parent2 = 0
		self.espece = 0
		self.score = 0
		self.classement = 0
		self.ptsMemeEspece = [0 for ind in range(param['nbIndiv'])]
		self.descendants = 0

		i = param['nbInput']
		o = param['nbOutput']
		t = param['maxNodesInt']
		self.nbInput = i
		self.nbOutput = o
		self.maxOutputTotal = o*(i + 1) + t*(i + o + t)
		self.offset = o - i
		self.codeJoueur = 0
		self.maxTour = param['nbSimul']/2

		self.input = inputIA(caracs)
		self.inputNodeVal = [0 for x in range(i)]
		self.inputNodeVal[0] = 1
		self.outputNodeVal = [[0, False] for x in range(self.maxOutputTotal)]
		
	def miseAJourInput(self, jeu):
		for i in range(len(jeu.nbCartes)):
			self.input.nbCartesDispo[i] = jeu.nbCartes[i]/jeu.nbCartesInit[i]
		if jeu.joueurActif == self.codeJoueur:
			self.input.siJoueurActif = 1
		else:
			self.input.siJoueurActif = 0
		
		self.input.nbTours = jeu.joueurs[self.codeJoueur].nbTours/self.maxTour
		self.input.phase = jeu.phase/2
		self.input.actions = jeu.actions/4
		self.input.pieces = jeu.pieces/25
		self.input.achats = jeu.achats/5
		self.input.carteActive = jeu.carteActive/15
		
		self.input.nbCartesMain = \
			len(jeu.joueurs[self.codeJoueur].main)/16
		self.input.nbCartesPaquet = \
			len(jeu.joueurs[self.codeJoueur].paquet)/60
		self.input.nbCartesRecyclage = \
			len(jeu.joueurs[self.codeJoueur].recyclage)/60
		
		del self.input.codesCartesMain[:]
		for c in jeu.joueurs[self.codeJoueur].main:
			self.input.codesCartesMain.append(c.code/15)
	
	def convertInput(self):
		for i in range(len(self.input.nbCartesDispo)):
			self.inputNodeVal[i + 1] = self.input.nbCartesDispo[i] 
		self.inputNodeVal[17] = self.input.siJoueurActif
		self.inputNodeVal[18] = self.input.nbTours
		self.inputNodeVal[19] = self.input.phase
		self.inputNodeVal[20] = self.input.actions
		self.inputNodeVal[21] = self.input.pieces
		self.inputNodeVal[22] = self.input.achats
		self.inputNodeVal[23] = self.input.carteActive
		
		self.inputNodeVal[24] = self.input.nbCartesMain
		self.inputNodeVal[25] = self.input.nbCartesPaquet
		self.inputNodeVal[26] = self.input.nbCartesRecyclage
		
		for i in range(16):
			self.inputNodeVal[27 + i] = -1
		l = len(self.input.codesCartesMain)
		for i in range(min(16, l)):
			self.inputNodeVal[27 + i] = self.input.codesCartesMain[l - 1 - i]
		
	def getDecision(self):
		self.convertInput()
		
		for outNode in range(self.maxOutputTotal):
			self.outputNodeVal[outNode] = [0, False]
			
		for outNode in range(self.nbOutput):
			if not(self.ADN.siOutLibre[outNode]):
				self.recCalcNodeVal(outNode)
		
		for encrNode in range(self.ADN.encOffset, self.maxOutputTotal):
			if not(self.ADN.siEncrLibre[encrNode]):
				self.recCalcNodeVal(encrNode)
		
		for g in self.ADN.seqGene:
			if g.active and not(self.ADN.siEncrLibre[g.code + self.ADN.encOffset]):
				g.encr += self.outputNodeVal[g.code + self.ADN.encOffset][0]
		
		output = -1
		maxOutNode = self.outputNodeVal[0][0]
		for outNode in range(1, self.nbOutput):
			if self.outputNodeVal[outNode][0] > maxOutNode:
				maxOutNode = self.outputNodeVal[outNode][0]
				output = outNode - 1
		
		return output
		
	
	def recCalcNodeVal(self, outNode):
		for g in self.ADN.seqGene:
			if g.outNode == outNode and g.active:
				
				if g.inNode < self.nbInput:
					self.outputNodeVal[outNode][0] += \
						self.inputNodeVal[g.inNode] * (g.weight + g.encr)

				elif self.outputNodeVal[g.inNode + self.offset][1]:
					self.outputNodeVal[outNode][0] += \
						self.outputNodeVal[g.inNode + self.offset][0] * \
							(g.weight + g.encr)
				else:
					self.recCalcNodeVal(g.inNode + self.offset)
					self.outputNodeVal[outNode][0] += \
						self.outputNodeVal[g.inNode + self.offset][0] * \
							(g.weight + g.encr)
		
		if outNode >= self.nbOutput:
			self.outputNodeVal[outNode][0] = \
				func.normale(self.outputNodeVal[outNode][0])
		
		self.outputNodeVal[outNode][1] = True
		
	def reset(self, param):
		self.ADN.reset(param)
		self.nom = 0
		self.age = 0
		self.parent1 = 0
		self.parent2 = 0
		self.espece = 0
		self.score = 0
		self.classement = 0
		self.descendants = 0

class population:
	
	def __init__(self, param):
		self.indiv = []
		i = param['nbInput']
		o = param['nbOutput']
		t = param['maxNodesInt']
		self.arbreGen = [[0 for output in range(o*(i + 1) + t*(i + o + t))]\
			for input in range(i + t)]
		self.prochCode = 0
		self.prochNom = 0
		self.prochEspece = 0
	
	def addIndiv(self, ind):
		self.indiv.append(ind)
	
	def getProchNom(self):
		self.prochNom += 1
		return self.prochNom
	
	def getProchEspece(self):
		self.prochEspece += 1
		return self.prochEspece
	
	def setGeneCode(self, input, output):
		self.prochCode += 1
		self.arbreGen[input][output] = self.prochCode

class ia: 
	
	def __init__(self, caracs, type):
		self.input = inputIA(caracs)
		self.codeJoueur = 1
		self.type = type
		
	def miseAJourInput(self, jeu):
		for i in range(len(jeu.nbCartes)):
			self.input.nbCartesDispo[i] = jeu.nbCartes[i]
		if jeu.joueurActif == self.codeJoueur:
			self.input.siJoueurActif = 1
		else:
			self.input.siJoueurActif = 0
		
		self.input.nbTours = jeu.joueurs[self.codeJoueur].nbTours
		self.input.phase = jeu.phase
		self.input.actions = jeu.actions
		self.input.pieces = jeu.pieces
		self.input.achats = jeu.achats
		self.input.carteActive = jeu.carteActive
		
		self.input.nbCartesMain = len(jeu.joueurs[self.codeJoueur].main)
		self.input.nbCartesPaquet = len(jeu.joueurs[self.codeJoueur].paquet)
		self.input.nbCartesRecyclage = len(jeu.joueurs[self.codeJoueur].recyclage)
		
		del self.input.codesCartesMain[:]
		for c in jeu.joueurs[self.codeJoueur].main:
			self.input.codesCartesMain.append(c.code)
	
	def getDecision(self):
		dictIAs = {0: IA.randDecision, 1: IA.IAbasique, 2: IA.IAmoyenne, 3: IA.joueurHumain}
		return dictIAs.get(self.type)(self.input)
			
class jeu:
	
	def __init__(self, ind0, ind1):
		self.nbCartes = [14, 8, 8, 60, 40, 30, 10, 10, 10, 10, 10,\
			10, 10, 10, 10, 10]
		self.nbCartesInit = [8, 8, 8, 46, 40, 30, 10, 10, 10, 10, 10,\
			10, 10, 10, 10, 10]	
		self.strategies = [ind0, ind1]
		self.cartes = []
		#self.rebut = []
		self.joueurs = []

		self.joueurActif = random.randrange(2)
		self.actions = 1
		self.pieces = 0
		self.achats = 1
		self.phase = 0
		self.carteActive = -1
		
	def miseEnPlace(self, caracs):
		#print("Distribution des cartes")
		for i in range(16):
			c = carte(caracs, i)
			self.cartes.append(c)
		
		for i in range(2):
			j = joueur(caracs)
			j.code = i
			for k in range(3):
				j.recoit(self, 0)
			for k in range(7):
				j.recoit(self, 3)
			j.pioche(5)
			self.joueurs.append(j)
			
		#print ("Premier joueur :", self.joueurActif)
	
	def reinitTour(self):
		self.joueurs[self.joueurActif].nbTours += 1
		self.joueurActif = (self.joueurActif + 1) % len(self.joueurs)
		self.actions = 1
		self.pieces = 0
		self.achats = 1
		self.phase = 0
		#print ("")
		#print ("Tour du joueur :", self.joueurActif)
	
	def trouveVainqueur(self):
		for j in self.joueurs:
			j.comptePoints()
		
		randJoueur = list(range(len(self.joueurs)))
		random.shuffle(randJoueur)
		
		vainqueur = randJoueur[0]
		maxPoints = self.joueurs[vainqueur].points
		for i in range(len(self.joueurs)):
			if self.joueurs[randJoueur[i]].points > maxPoints:
				vainqueur = randJoueur[i]
				maxPoints = self.joueurs[randJoueur[i]].points
	
		exAequo = [vainqueur]
		for i in range(len(self.joueurs)):
			if (randJoueur[i] != vainqueur) and \
				(self.joueurs[randJoueur[i]].points == maxPoints):
				exAequo.append(randJoueur[i])
		
		if len(exAequo) > 1:
			minTours = self.joueurs[vainqueur].nbTours
			for i in range(1, len(exAequo)):
				if self.joueurs[exAequo[i]].nbTours < minTours:
					vainqueur = exAequo[i]
					minTours = self.joueurs[vainqueur].nbTours
		
		return vainqueur
			
class carte:
	
	def __init__(self, caracs, code):
		self.code = code
		self.nom = caracs.get(code)[0]
		self.type = caracs.get(code)[1]
		self.cout = caracs.get(code)[2]
		self.points = caracs.get(code)[3]
		
	def joue(self, jeu, effets):
		return effets.get(self.code)(jeu)
		
class inputIA:
	
	def __init__(self, caracs):
		self.nbCartesDispo = [14, 8, 8, 60, 40, 30, 10, 10, 10, 10, 10,\
			10, 10, 10, 10, 10]
		
		self.caracs = []
		for i in range(16):
			self.caracs.append(caracs.get(i))
		
		self.nbTours = 0
		self.siJoueurActif = 0
		self.phase = 0
		self.actions = 0
		self.pieces = 0
		self.achats = 0
		
		self.carteActive = -1
		self.phaseCarte = 0
		self.coutCarteChoisie = -1
		
		self.nbCartesMain = 0
		self.nbCartesPaquet = 0
		self.nbCartesRecyclage = 0
		
		self.codesCartesMain = []		

class joueur:

	def __init__(self, caracs):
		self.paquet = []
		self.main = []
		self.table = []
		self.recyclage = []
		self.points = 0
		self.nbTours = 0
		self.code = -1	
			
	def recoit(self, jeu, code):
		if jeu.nbCartes[code] == 0:
			return -1
		else:
			jeu.nbCartes[code] -= 1
			self.recyclage.append(jeu.cartes[code])
			#print ("J", self.code, "recoit :", jeu.cartes[code].nom)
			return 0
	
	def achete(self, jeu, code):
		if (code != -1) and (code < len(jeu.cartes)):
			if (jeu.pieces >= jeu.cartes[code].cout) and \
				(jeu.achats > 0) and (jeu.nbCartes[code] > 0):
				
				jeu.pieces -= jeu.cartes[code].cout
				jeu.nbCartes[code] -= 1
				jeu.achats -= 1
				self.recyclage.append(jeu.cartes[code])
				#print ("J", self.code, "achete :", jeu.cartes[code].nom)
				return 0
			else:
				return -1
		else:
			return -1
	
	def acquiert(self, jeu, code):
		if jeu.nbCartes[code] == 0:
			return -1
		else:
			jeu.nbCartes[code] -= 1
			self.main.append(jeu.cartes[code])
			#print ("J", self.code, "acquiert :", jeu.cartes[code].nom)
			return 0
		
	def pioche(self, nb):
		for i in range(nb):
			if len(self.paquet) > 0:
				self.main.append(self.paquet.pop())
			else:
				random.shuffle(self.recyclage)
				for c in range(len(self.recyclage)):
					self.paquet.append(self.recyclage.pop())
				if len(self.paquet) > 0:
					self.main.append(self.paquet.pop())
		#if nb < 2:
			#print ("J", self.code, "pioche", nb, "carte")
		#else:
			#print ("J", self.code, "pioche", nb, "cartes")
		#if (len(self.paquet) == 0) and (len(self.recyclage) == 0):
			#print ("DOMINION!!!")
	
	def defausse(self, positionCarte):
		if positionCarte < len(self.main):
			self.recyclage.append(self.main[positionCarte])
			nom = self.main[positionCarte].nom
			del self.main[positionCarte]
			#print ("J", self.code, "defausse :", nom)
			return 0
		else:
			return -1
	
	def ecarte(self, positionCarte):
		if positionCarte < len(self.main):
			nom = self.main[positionCarte].nom
			del self.main[positionCarte]
			#print ("J", self.code, "ecarte :", nom)
			return 0
		else:
			return -1
	
	def pose(self, jeu, effets, positionCarte):
		if (positionCarte != -1) and (positionCarte < len(self.main)):
			if self.main[positionCarte].type != 0:
				if self.main[positionCarte].type == 2:
					if (jeu.phase == 0) and (jeu.actions > 0):
						jeu.actions -=1
						self.table.append(self.main[positionCarte])
						jeu.carteActive = self.main[positionCarte].code
						nom = self.main[positionCarte].nom
						del self.main[positionCarte]
						#print ("J", self.code, "joue :", nom)
						return self.table[len(self.table) - 1].joue(jeu, effets)
					else:
						return -1
				else:
					if (jeu.phase == 1):
						self.table.append(self.main[positionCarte])
						jeu.carteActive = self.main[positionCarte].code
						nom = self.main[positionCarte].nom
						del self.main[positionCarte]
						#print ("J", self.code, "pose :", nom)
						return self.table[len(self.table) - 1].joue(jeu, effets)
					else:
						return -1
			else:
				return -1
		else:
			return -1
	
	def posePieces(self, jeu, effets):
		if jeu.phase == 1:
			l = len(self.main)
			for i in range(l):
				self.pose(jeu, effets, l - 1 - i)
			return 0
		else:
			return -1

	def finitTour(self):
		l = len(self.main)
		for i in range(l):
			self.defausse(l - 1 - i)
		for i in range(len(self.table)):
			self.recyclage.append(self.table.pop())
		self.pioche(5)
	
	def comptePoints(self):
		for c in self.main:
			self.points += c.points
		for c in self.paquet:
			self.points += c.points
		for c in self.recyclage:
			self.points += c.points
		
			
			
			
			
			
			
			
			
			
			
			
			