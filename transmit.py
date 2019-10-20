import random
import func
import classes
import mutation

def speciation(param, pop):
	for ind1 in pop.indiv:
		#print (ind1.nom)
		if ind1.age == 0:
			memeEspece = False
			for ind2 in pop.indiv:
				if ind2.espece != 0:
					if func.calcDistGenetique(ind1, ind2) <= \
						param['seuilEspece']:
						memeEspece = True
				if memeEspece:
					ind1.espece = ind2.espece
					break
			if not memeEspece:
				ind1.espece = pop.getProchEspece()

def succesReproductif(param, pop):
	randInd = list(range(param['nbIndiv']))
	random.shuffle(randInd)
	
	for ind in pop.indiv:
		if ind.score == 0:
			ind.score = 0.001
	
	for clsmt in range(1, param['nbIndiv'] + 1):
		i = 0
		while pop.indiv[randInd[i]].classement != 0:
			i += 1
		candidat = randInd[i]
		score = pop.indiv[candidat].score
		
		for i in range(param['nbIndiv']):
			if pop.indiv[randInd[i]].classement == 0 and \
				pop.indiv[randInd[i]].score > score:
				candidat = randInd[i]
				score = pop.indiv[candidat].score
		
		pop.indiv[candidat].classement = clsmt
	
	for ind in pop.indiv:
		if ind.classement <= param['nbSurv']:
			for i in range(param['nbIndiv']):
				if ind.espece == pop.indiv[i].espece:
					if pop.indiv[i].classement <= param['nbSurv']:
						ind.ptsMemeEspece[i] = pop.indiv[i].score

def reproduction(param, pop, caracs):
	for ind in pop.indiv:
		if ind.classement > param['nbSurv']:
			ind.reset(param)
	
	for parent1 in pop.indiv:
		if parent1.classement != 0:
			parent2 = random.choices(pop.indiv, parent1.ptsMemeEspece)[0]
			
			for enfant in pop.indiv:
				if enfant.nom == 0:
					break
			enfant.nom = pop.getProchNom()
			enfant.parent1 = parent1.nom
			enfant.parent2 = parent2.nom
			
			for g in parent1.ADN.seqGene:
				genf = classes.gene()
				
				if parent2.ADN.tellSiGene(g.code):
					if random.randrange(2):
						g.copyTo(genf)
					else:
						parent2.ADN.findGene(g.code).copyTo(genf)
				else:
					g.copyTo(genf)
				
				enfant.ADN.addGene(genf)
			
			for g in parent2.ADN.seqGene:
				if not enfant.ADN.tellSiGene(g.code):
					genf = classes.gene()
					g.copyTo(genf)
					enfant.ADN.addGene(genf)
			
			enfant.ADN.setNbNodeInt(parent1.ADN.nbNodeInt)	
			for g in enfant.ADN.seqGene:
				enfant.ADN.siInLibre[g.inNode] = False
				if g.outNode < enfant.ADN.encOffset :
					enfant.ADN.siOutLibre[g.outNode] = False
				else :
					enfant.ADN.siEncrLibre[g.outNode] = False

	for regen in pop.indiv:
		if regen.nom == 0:
			regen.nom = pop.getProchNom()
		
			for transverse in range(param['transversesInit']):
				unique = False
				while not unique:
					if transverse == 0:
						inNode = 0
					else:
						inNode = random.randrange(param['nbInput'])
					outNode = random.randrange(param['nbOutput'])
				
					if not ind.ADN.tellSiGene(pop.arbreGen[inNode][outNode]):
						unique = True
			
				for couche in range(param['couchesInit']):
					g = classes.gene()
					g.inNode = inNode
					g.outNode = param['nbOutput'] + regen.ADN.nbNodeInt
					g.weight = random.uniform(-1, 1)
					g.active = True
				
					if pop.arbreGen[g.inNode][g.outNode] == 0:
						pop.setGeneCode(g.inNode, g.outNode)
					g.code = pop.arbreGen[g.inNode][g.outNode]
				
					regen.ADN.addGene(g)
					inNode = param['nbInput'] + regen.ADN.nbNodeInt
					regen.ADN.addNodeInt()
			
				g = classes.gene()
				g.inNode = inNode
				g.outNode = outNode
				g.weight = random.uniform(-1, 1)
				g.active = True
			
				if pop.arbreGen[g.inNode][g.outNode] == 0:
					pop.setGeneCode(g.inNode, g.outNode)
				g.code = pop.arbreGen[g.inNode][g.outNode]
			
				regen.ADN.addGene(g)
				regen.ADN.siInLibre[inNode] = False
				regen.ADN.siOutLibre[outNode] = False
			
			for nvlInput in range(param['inputSupInit']):
				mutation.creationInput(pop, regen)
				regen.ADN.seqGene[regen.ADN.compteGene() - 1].weight = random.uniform(-1, 1)

			for connexion in range(param['connexInit']):
				mutation.creationConnexion(param, pop, regen, caracs)
				regen.ADN.seqGene[regen.ADN.compteGene() - 1].weight = random.uniform(-1, 1)

			for encryption in range(param['encrInit']):
				mutation.creationEncryption(param, pop, regen, caracs)
				regen.ADN.seqGene[regen.ADN.compteGene() - 1].weight = random.uniform(-1, 1)
		
			for connexion in range(param['connexInit']):
				mutation.creationConnexion(param, pop, regen, caracs)
				regen.ADN.seqGene[regen.ADN.compteGene() - 1].weight = random.uniform(-1, 1)
		