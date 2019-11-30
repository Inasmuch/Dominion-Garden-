import classes

def calcDistGenetique(ind1, ind2):
	nbGeneTotal = ind1.ADN.compteGene() + ind2.ADN.compteGene()
	nbGeneUnique = nbGeneTotal
	for g in ind1.ADN.seqGene:
		if ind2.ADN.tellSiGene(g.code):
			nbGeneUnique -= 2
	return (nbGeneUnique/nbGeneTotal)*1000

def normale(x):
	if x > 1:
		return 1
	elif x < -1:
		return -1
	else:
		return x

def siCreationBoucle(param, ind, inNode, outNode, caracs):
	mannequin = classes.indiv(param, caracs)
	for g in ind.ADN.seqGene:
		gmanq = classes.gene()
		g.copyTo(gmanq)
		mannequin.ADN.addGene(gmanq)
	
	gmanq = classes.gene()
	gmanq.inNode = inNode
	gmanq.outNode = outNode
	gmanq.active = True
	mannequin.ADN.addGene(gmanq)
	
	boolCreationBoucle = False
	
	for node in range(param['nbOutput']):
		boolCreationBoucle = boolCreationBoucle or\
			recSiBoucle(param, mannequin, node, 1)
	
	for encrNode in range(mannequin.ADN.encOffset, mannequin.maxOutputTotal):
		boolCreationBoucle = boolCreationBoucle or\
			recSiBoucle(param, mannequin, encrNode, 1)
	
	return boolCreationBoucle

def siCreationBoucleChezEnfant(param, enfant, caracs):
	#mannequin = classes.indiv(param, caracs)
	#for g in par1.ADN.seqGene:
	#	gmanq = classes.gene()
	#	g.copyTo(gmanq)
	#	mannequin.ADN.addGene(gmanq)
	
	#for g in par2.ADN.seqGene:
	#	if not mannequin.ADN.tellSiGene(g.code):
	#		gmanq = classes.gene()
	#		g.copyTo(gmanq)
	#		mannequin.ADN.addGene(gmanq)
	
	boolCreationBoucle = False
	
	for node in range(param['nbOutput']):
		boolCreationBoucle = boolCreationBoucle or\
			recSiBoucle(param, enfant, node, 1)

	for encrNode in range(enfant.ADN.encOffset, enfant.maxOutputTotal):
		boolCreationBoucle = boolCreationBoucle or\
			recSiBoucle(param, enfant, encrNode, 1)
	
	return boolCreationBoucle

def recSiBoucle(param, ind, outNode, saut):
	offset = param['nbOutput'] - param['nbInput']
	boolBoucle = False
	
	if saut <= param['maxNodesInt'] + 1:
		for g in ind.ADN.seqGene:
			if g.outNode == outNode and g.active:
				if g.inNode >= param['nbInput']:
					boolBoucle = boolBoucle or \
						recSiBoucle(param, ind, g.inNode + offset, saut + 1)
	else:
		boolBoucle = True
	
	return boolBoucle