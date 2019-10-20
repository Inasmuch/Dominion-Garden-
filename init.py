import random
import classes
import mutation

def loadParam():
	with open('parameters.txt', 'r') as txt:
		mots = [line[:-1].split() for line in txt]
	param = dict([(mot[0], int(mot[2])) for mot in mots])
	return param

def creerPopulation(param, pop, caracs):
	for i in range(param['nbIndiv']):
		
		ind = classes.indiv(param, caracs)
		
		for connexion in range(param['connexInit']):
			
			g = classes.gene()
			
			unique = False
			while not unique:
				
				if connexion == 0:
					inNode = 0
				else:
					inNode = random.randrange(param['nbInput'])
				outNode = random.randrange(param['nbOutput'])
				
				if pop.arbreGen[inNode][outNode] == 0:
					unique = True
				elif not ind.ADN.tellSiGene(pop.arbreGen[inNode][outNode]):
					unique = True
			
			g.inNode = inNode
			g.outNode = outNode
			g.weight = random.uniform(-1, 1)
			g.active = True
			
			if pop.arbreGen[inNode][outNode] == 0:
				pop.setGeneCode(inNode, outNode)
			g.code = pop.arbreGen[inNode][outNode]
			
			ind.ADN.addGene(g)
			ind.ADN.siInLibre[inNode] = False
			ind.ADN.siOutLibre[outNode] = False
		
		ind.nom = pop.getProchNom()
		pop.addIndiv(ind)

def creerPopulationAvecCouches(param, pop, caracs):
	for i in range(param['nbIndiv']):
		ind = classes.indiv(param, caracs)
		
		for transverse in range(param['transversesInit']):

			unique = False
			while not unique:
				
				if transverse == 0:
					inNode = 0
				else:
					inNode = random.randrange(param['nbInput'])
				outNode = random.randrange(param['nbOutput'])
				
				if pop.arbreGen[inNode][outNode] == 0:
					unique = True
				elif not ind.ADN.tellSiGene(pop.arbreGen[inNode][outNode]):
					unique = True
			
			for couche in range(param['couchesInit']):
				g = classes.gene()
				g.inNode = inNode
				g.outNode = param['nbOutput'] + ind.ADN.nbNodeInt
				g.weight = random.uniform(-1, 1)
				g.active = True
				
				if pop.arbreGen[g.inNode][g.outNode] == 0:
					pop.setGeneCode(g.inNode, g.outNode)
				g.code = pop.arbreGen[g.inNode][g.outNode]
				
				ind.ADN.addGene(g)
				
				inNode = param['nbInput'] + ind.ADN.nbNodeInt
				ind.ADN.addNodeInt()
			
			g = classes.gene()
			g.inNode = inNode
			g.outNode = outNode
			g.weight = random.uniform(-1, 1)
			g.active = True
			
			if pop.arbreGen[g.inNode][g.outNode] == 0:
				pop.setGeneCode(g.inNode, g.outNode)
			g.code = pop.arbreGen[g.inNode][g.outNode]
			
			ind.ADN.addGene(g)
			
			ind.ADN.siInLibre[inNode] = False
			ind.ADN.siOutLibre[outNode] = False
		
		for nvlInput in range(param['inputSupInit']):
			mutation.creationInput(pop, ind)
			ind.ADN.seqGene[ind.ADN.compteGene() - 1].weight = random.uniform(-1, 1)

		for connexion in range(param['connexInit']):
			mutation.creationConnexion(param, pop, ind, caracs)
			ind.ADN.seqGene[ind.ADN.compteGene() - 1].weight = random.uniform(-1, 1)

		for encryption in range(param['encrInit']):
			mutation.creationEncryption(param, pop, ind, caracs)
			ind.ADN.seqGene[ind.ADN.compteGene() - 1].weight = random.uniform(-1, 1)
		
		for connexion in range(param['connexInit']):
			mutation.creationConnexion(param, pop, ind, caracs)
			ind.ADN.seqGene[ind.ADN.compteGene() - 1].weight = random.uniform(-1, 1)
		
		print (i)
		#for g in ind.ADN.seqGene:
		#	print(str(g.inNode) + '; ' + str(g.outNode) + '; ' + str(g.weight) + '; ' + str(g.active) + '; ' + str(g.code))
		
		ind.nom = pop.getProchNom()
		pop.addIndiv(ind)

def preparerPopulation(param, pop):
	for ind in pop.indiv:
		ind.score = 0
		ind.classement = 0
		ind.ptsMemeEspece = [0 for i in range(param['nbIndiv'])]
		ind.age += 1
	

def replayPopFromText(param, pop, caracs):
	txtpop = []
	with open('replay.txt', 'r') as txt:
		for l in txt:
			txtpop.append(l)
			
	for i in range(len(txtpop)):
		if txtpop[i][:4] == 'nom:':
			
			ind = classes.indiv(param, caracs)
			ind.ADN.setNbNodeInt(int(txtpop[i].split()[13][:-1]))
			
			j = i + 1
			while txtpop[j] != '\n':
				if txtpop[j].split()[3][:-1] == 'True':
					
					g = classes.gene()
					
					g.inNode = int(txtpop[j].split()[0][:-1])
					g.outNode = int(txtpop[j].split()[1][:-1])
					g.weight = float(txtpop[j].split()[2][:-1])
					g.active = True
					g.code = int(txtpop[j].split()[4])
					
					ind.ADN.addGene(g)
					
					
					ind.ADN.siInLibre[g.inNode] = False
					if g.outNode < ind.ADN.encOffset :
						ind.ADN.siOutLibre[g.outNode] = False
					else :
						ind.ADN.siEncrLibre[g.outNode] = False
				j += 1
				
			ind.nom = pop.getProchNom()
			pop.addIndiv(ind)

def loadPopFromText(param, pop, caracs):
	txtpop = []
	with open('population.txt', 'r') as txt:
		for l in txt:
			txtpop.append(l)
			
	for i in range(len(txtpop)):
		if txtpop[i][:4] == 'nom:':
			
			ind = classes.indiv(param, caracs)
			ind.ADN.setNbNodeInt(int(txtpop[i].split()[13][:-1]))

			j = i + 1
			while txtpop[j] != '\n':
				#if txtpop[j].split()[3][:-1] == 'True':
					
				g = classes.gene()
					
				g.inNode = int(txtpop[j].split()[0][:-1])
				g.outNode = int(txtpop[j].split()[1][:-1])
				g.weight = float(txtpop[j].split()[2][:-1])
				g.active = bool(txtpop[j].split()[3][:-1])
				g.code = int(txtpop[j].split()[4])
				
				if pop.arbreGen[g.inNode][g.outNode] == 0:
					pop.arbreGen[g.inNode][g.outNode] = g.code
					if g.code > pop.prochCode:
						pop.prochCode = g.code
					
				ind.ADN.addGene(g)
					
				ind.ADN.siInLibre[g.inNode] = False
				if g.outNode < ind.ADN.encOffset :
					ind.ADN.siOutLibre[g.outNode] = False
				else :
					ind.ADN.siEncrLibre[g.outNode] = False	
					
				j += 1
				
			ind.nom = pop.getProchNom()
			pop.addIndiv(ind)


def loadPopForAnalysis(param, pop, caracs):
	txtpop = []
	with open('population.txt', 'r') as txt:
		for l in txt:
			txtpop.append(l)
			
	for i in range(len(txtpop)):
		if txtpop[i][:4] == 'nom:':
			
			ind = classes.indiv(param, caracs)
			ind.nom = int(txtpop[i].split()[1][:-1])
			ind.espece = int(txtpop[i].split()[9][:-1])
			ind.score = float(txtpop[i].split()[15][:-1])
			ind.classement = int(txtpop[i].split()[17])
			
			j = i + 1
			while txtpop[j] != '\n':
					
				g = classes.gene()
					
				g.inNode = int(txtpop[j].split()[0][:-1])
				g.outNode = int(txtpop[j].split()[1][:-1])
				g.weight = float(txtpop[j].split()[2][:-1])
				g.active = bool(txtpop[j].split()[3][:-1])
				g.code = int(txtpop[j].split()[4])
					
				ind.ADN.addGene(g)
					
				j += 1
				
			pop.addIndiv(ind)

def seedPopFromCore(param, pop, caracs):
	txtpop = []
	with open('core.txt', 'r') as txt:
		for l in txt:
			txtpop.append(l)
			
	for i in range(len(txtpop)):
		if txtpop[i][:4] == 'nom:':
			
			ind = classes.indiv(param, caracs)
			ind.ADN.setNbNodeInt(int(txtpop[i].split()[13][:-1]))

			j = i + 1
			while txtpop[j] != '\n':
					
				g = classes.gene()
					
				g.inNode = int(txtpop[j].split()[0][:-1])
				g.outNode = int(txtpop[j].split()[1][:-1])
				g.weight = float(txtpop[j].split()[2][:-1])
				g.active = bool(txtpop[j].split()[3][:-1])
				g.code = int(txtpop[j].split()[4])
				
				if pop.arbreGen[g.inNode][g.outNode] == 0:
					pop.arbreGen[g.inNode][g.outNode] = g.code
					if g.code > pop.prochCode:
						pop.prochCode = g.code
					
				ind.ADN.addGene(g)
					
				ind.ADN.siInLibre[g.inNode] = False
				if g.outNode < ind.ADN.encOffset :
					ind.ADN.siOutLibre[g.outNode] = False
				else :
					ind.ADN.siEncrLibre[g.outNode] = False	
					
				j += 1
				
			ind.nom = pop.getProchNom()
			pop.addIndiv(ind)

	for i in range(param['nbIndiv'] - 1):
			
		clone = classes.indiv(param, caracs)
		clone.ADN.setNbNodeInt(ind.ADN.nbNodeInt)

		for g0 in ind.ADN.seqGene:
					
			g = classes.gene()
			g0.copyTo(g)
			clone.ADN.addGene(g)
					
			clone.ADN.siInLibre[g.inNode] = False
			if g.outNode < clone.ADN.encOffset :
				clone.ADN.siOutLibre[g.outNode] = False
			else :
				clone.ADN.siEncrLibre[g.outNode] = False	
			
		for nvlInput in range(param['inputSupInit']):
				mutation.creationInput(pop, clone)
		for nvlOutput in range(param['outputSupInit']):
			mutation.creationOutput(param, pop, clone, caracs)
		for connexion in range(param['connexInit']):
			mutation.creationConnexion(param, pop, clone, caracs)
		for encryption in range(param['encrInit']):
			mutation.creationEncryption(param, pop, clone, caracs)
		for chgtPoids in range(param['chgtPoidsInit']):
			mutation.changementPoids(clone)

		clone.nom = pop.getProchNom()
		pop.addIndiv(clone)
		print(clone.nom)