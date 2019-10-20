import random
import classes
import func

def mutationArborescente(param, pop, caracs):
	mutations = ['nvlInput', 'nvlOutput', 'nvlConnex', 'nvlNodeInt',\
		'nvlEncr', 'chgActiv', 'chgPoids']
	pctMutation = [param['pctNvlInput'], param['pctNvlOutput'],\
		param['pctNvlConnex'], param['pctNvlNodeInt'],\
		param['pctEncryption'] , param['pctChangmtActiv'], \
		1000 - (param['pctNvlInput'] + \
		param['pctNvlOutput'] + param['pctNvlConnex'] + \
		param['pctNvlNodeInt'] + param['pctEncryption'] + \
		param['pctChangmtActiv'])] 
	
	for ind in pop.indiv:
		if ind.age == 0:
			if (ind.parent1 != 0 and ind.parent1 == ind.parent2) or \
				random.randrange(1, 101) <= param['pctMutation']:
				
				mut = random.choices(mutations, pctMutation)[0]
				#print str(ind.nom) + ': ' + mut)
				
				if mut == 'nvlInput':
					
					if ind.ADN.compteInLibre() > 0:
						creationInput(pop, ind)
					elif ind.ADN.compteOutLibre() > 0:
						creationOutput(param, pop, ind, caracs)
					elif ind.ADN.nbNodeInt < param['maxNodesInt']:
						creationNodeInt(param, pop, ind)
					elif ind.ADN.compteGene() < ind.ADN.compteMaxGene():
						creationConnexion(param, pop, ind, caracs)
					elif ind.ADN.compteEncrActif() < param['maxNodesEncr']:
						creationEncryption(param, pop, ind, caracs)
					else:
						changementPoids(ind)
					
				elif mut == 'nvlOutput':
					
					if ind.ADN.compteOutLibre() > 0:
						creationOutput(param, pop, ind, caracs)
					elif ind.ADN.compteInLibre() > 0:
						creationInput(pop, ind)
					elif ind.ADN.nbNodeInt < param['maxNodesInt']:
						creationNodeInt(param, pop, ind)
					elif ind.ADN.compteGene() < ind.ADN.compteMaxGene():
						creationConnexion(param, pop, ind, caracs)
					elif ind.ADN.compteEncrActif() < param['maxNodesEncr']:
						creationEncryption(param, pop, ind, caracs)
					else:
						changementPoids(ind)
					
				elif mut == 'nvlConnex':
					
					if ind.ADN.compteGene() < ind.ADN.compteMaxGene():
						creationConnexion(param, pop, ind, caracs)
					elif ind.ADN.compteInLibre() > 0:
						creationInput(pop, ind)
					elif ind.ADN.compteOutLibre() > 0:
						creationOutput(param, pop, ind, caracs)
					elif ind.ADN.nbNodeInt < param['maxNodesInt']:
						creationNodeInt(param, pop, ind)
					elif ind.ADN.compteEncrActif() < param['maxNodesEncr']:
						creationEncryption(param, pop, ind, caracs)
					else:
						changementPoids(ind)
				
				elif mut == 'nvlNodeInt':
					
					if ind.ADN.nbNodeInt < param['maxNodesInt']:
						creationNodeInt(param, pop, ind)
					elif ind.ADN.compteGene() < ind.ADN.compteMaxGene():
						creationConnexion(param, pop, ind, caracs)
					elif ind.ADN.compteEncrActif() < param['maxNodesEncr']:
						creationEncryption(param, pop, ind, caracs)
					elif ind.ADN.compteInLibre() > 0:
						creationInput(pop, ind)
					elif ind.ADN.compteOutLibre() > 0:
						creationOutput(param, pop, ind, caracs)
					else:
						changementPoids(ind)

				elif mut == 'nvlEncr':
					
					if ind.ADN.compteEncrActif() < param['maxNodesEncr']:
						creationEncryption(param, pop, ind, caracs)
					elif ind.ADN.nbNodeInt < param['maxNodesInt']:
						creationNodeInt(param, pop, ind)
					elif ind.ADN.compteGene() < ind.ADN.compteMaxGene():
						creationConnexion(param, pop, ind, caracs)
					elif ind.ADN.compteInLibre() > 0:
						creationInput(pop, ind)
					elif ind.ADN.compteOutLibre() > 0:
						creationOutput(param, pop, ind, caracs)
				
				elif mut == 'chgActiv':
					
					changementActivation(param, ind, caracs)
				
				elif mut == 'chgPoids':
					
					changementPoids(ind)
				
				else:
					print ('uh oh')

def changementPoids(ind):
	random.choices(ind.ADN.seqGene)[0].weight = random.uniform(-1, 1)
	
def changementActivation(param, ind, caracs):
	rndGene = random.choices(ind.ADN.seqGene)[0]
	
	if rndGene.inNode >= param['nbInput'] and not rndGene.active:
#		and rndGene.outNode >= param['nbOutput']  
		
		if func.siCreationBoucle(param, ind, rndGene.inNode, rndGene.outNode, caracs):
			changementPoids(ind)
		else:
			rndGene.active = True
	else:
		rndGene.active = not rndGene.active
	
def creationInput(pop, ind):
	g = classes.gene()
	
	g.inNode = ind.ADN.selectInLibre()
	g.outNode = ind.ADN.selectOutActif()
	g.weight = 0
	g.active = True
	if pop.arbreGen[g.inNode][g.outNode] == 0:
		pop.setGeneCode(g.inNode, g.outNode)
	g.code = pop.arbreGen[g.inNode][g.outNode]
	
	ind.ADN.addGene(g)
	ind.ADN.siInLibre[g.inNode] = False

def creationOutput(param, pop, ind, caracs):
	inNode = ind.ADN.selectInActif()
	outNode = ind.ADN.selectOutLibre()
	
	if func.siCreationBoucle(param, ind, inNode, outNode, caracs):
		changementPoids(ind)
	else:
		g = classes.gene()
		
		g.inNode = inNode
		g.outNode = outNode
		g.weight = 0
		g.active = True
		if pop.arbreGen[g.inNode][g.outNode] == 0:
			pop.setGeneCode(g.inNode, g.outNode)
		g.code = pop.arbreGen[g.inNode][g.outNode]
		
		ind.ADN.addGene(g)
		ind.ADN.siOutLibre[g.outNode] = False

def creationEncryption(param, pop, ind, caracs):
	
	inNode = ind.ADN.selectInActif()
	outNode = ind.ADN.selectEncryptionTarget().code + ind.ADN.encOffset
	
	if func.siCreationBoucle(param, ind, inNode, outNode, caracs):
		changementPoids(ind)
	else:
		g = classes.gene()
		
		g.inNode = inNode
		g.outNode = outNode
		g.weight = 0
		g.active = True
		if pop.arbreGen[g.inNode][g.outNode] == 0:
			pop.setGeneCode(g.inNode, g.outNode)
		g.code = pop.arbreGen[g.inNode][g.outNode]
		
		ind.ADN.addGene(g)
		ind.ADN.siEncrLibre[g.outNode] = False	

def creationNodeInt(param, pop, ind):
	
	nbConnexEligible = ind.ADN.compteGene()
	connexEligible = []
	for g in ind.ADN.seqGene:
		if g.weight == 0 or not g.active:
			nbConnexEligible -= 1
			connexEligible.append(0)
		else:
			connexEligible.append(1)
	
	if nbConnexEligible == 0:
		changementPoids(ind)
	else:
		rndGene = random.choices(ind.ADN.seqGene, connexEligible)[0]
		rndGene.active = False
		
		g1 = classes.gene()
		g1.inNode = rndGene.inNode
		g1.outNode = param['nbOutput'] + ind.ADN.nbNodeInt
		g1.weight = 1
		g1.active = True
		if pop.arbreGen[g1.inNode][g1.outNode] == 0:
			pop.setGeneCode(g1.inNode, g1.outNode)
		g1.code = pop.arbreGen[g1.inNode][g1.outNode]		
		
		g2 = classes.gene()
		g2.inNode = param['nbInput'] + ind.ADN.nbNodeInt
		g2.outNode = rndGene.outNode
		g2.weight = rndGene.weight
		g2.active = True
		if pop.arbreGen[g2.inNode][g2.outNode] == 0:
			pop.setGeneCode(g2.inNode, g2.outNode)
		g2.code = pop.arbreGen[g2.inNode][g2.outNode]
		
		ind.ADN.addGene(g1)
		ind.ADN.addGene(g2)
		ind.ADN.addNodeInt()

		oldEncr = rndGene.code + ind.ADN.encOffset
		if not ind.ADN.siEncrLibre[oldEncr]:
			newEncr = g2.code + ind.ADN.encOffset
			for g in ind.ADN.seqGene:
				if g.outNode == oldEncr:
					g.outNode = newEncr
			ind.ADN.siEncrLibre[oldEncr] = True
			ind.ADN.siEncrLibre[newEncr] = False

def creationConnexion(param, pop, ind, caracs):
	
	while True:
		inNode = ind.ADN.selectInActif()
		while True:
			outNode = ind.ADN.selectOutActif()
			if inNode < param['nbInput'] or outNode < param['nbOutput']\
				or inNode - param['nbInput'] != outNode - param['nbOutput']:
				break
		if not ind.ADN.tellSiGene(pop.arbreGen[inNode][outNode]):
			break
#prevents self-connexions and redundant genes
	
#	if inNode >= param['nbInput'] and outNode >= param['nbOutput']:
	if inNode >= param['nbInput']:
		if func.siCreationBoucle(param, ind, inNode, outNode, caracs):
			changementPoids(ind)
		else:
			g = classes.gene()
			
			g.inNode = inNode
			g.outNode = outNode
			g.weight = 0
			g.active = True
			if pop.arbreGen[g.inNode][g.outNode] == 0:
				pop.setGeneCode(g.inNode, g.outNode)
			g.code = pop.arbreGen[g.inNode][g.outNode]
			
			ind.ADN.addGene(g)
	else:
		g = classes.gene()
		
		g.inNode = inNode
		g.outNode = outNode
		g.weight = 0
		g.active = True
		if pop.arbreGen[g.inNode][g.outNode] == 0:
			pop.setGeneCode(g.inNode, g.outNode)
		g.code = pop.arbreGen[g.inNode][g.outNode]
			
		ind.ADN.addGene(g)