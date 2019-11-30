import time

def writeParam(param, siPopFromText, siPopFromCore):
	with open('population.txt', 'w') as txt:
		txt.write('______________________Parameters_____________________\n')
		txt.write('\n')
		for p in param:
			txt.write(str(p) + ': ' + str(param[p]) + '\n')
		txt.write('Load pop from text: ' + str(siPopFromText) + '\n')
		txt.write('Generate pop from core: ' + str(siPopFromCore) + '\n')
		txt.write('\n')
		t = time.localtime()
		txt.write('Debut: ' + str(t.tm_hour).zfill(2) + ':' + \
			str(t.tm_min).zfill(2) + ':' + str(t.tm_sec).zfill(2) + ' ' + \
			str(t.tm_mday).zfill(2) + '/' + str(t.tm_mon).zfill(2) + '/' + \
			str(t.tm_year) + '\n')

def writePop(pop, generation):
	with open('population.txt', 'a') as txt:
		t = time.localtime()
		txt.write('Fin  : ' + str(t.tm_hour).zfill(2) + ':' + \
			str(t.tm_min).zfill(2) + ':' + str(t.tm_sec).zfill(2) + ' ' + \
			str(t.tm_mday).zfill(2) + '/' + str(t.tm_mon).zfill(2) + '/' + \
			str(t.tm_year) + '\n')
		txt.write('\n')
		txt.write('___________________Generation ' + str(generation) + \
			'___________________\n')
		txt.write('\n')
		for ind in pop.indiv:
			txt.write('nom: ' + str(ind.nom)+'; ')
			txt.write('age: ' + str(ind.age)+'; ')
			txt.write('parent1: ' + str(ind.parent1)+'; ')
			txt.write('parent2: ' + str(ind.parent2)+'; ')
			txt.write('espece: ' + str(ind.espece)+'; ')
			txt.write('nbGenes: ' + str(ind.ADN.compteGene())+'; ')
			txt.write('nodeInt: ' + str(ind.ADN.nbNodeInt)+'; ')
			txt.write('score: ' + str(ind.score)+'; ')
			txt.write('classement: ' + str(ind.classement).zfill(3) + '\n')
#			txt.write('ptsMemeEspece: ' + str(ind.ptsMemeEspece)+'\n')
			for g in ind.ADN.seqGene:
				txt.write(str(g.inNode) + '; ')
				txt.write(str(g.outNode) + '; ')
				txt.write(str(g.weight) + '; ')
				txt.write(str(g.active) + '; ')
				txt.write(str(g.code) + '\n')
			txt.write('\n')

def writeSelectedInd(ind):
	with open('population.txt', 'a') as txt:
		txt.write('nom: ' + str(ind.nom)+'; ')
		txt.write('age: ' + str(ind.age)+'; ')
		txt.write('parent1: ' + str(ind.parent1)+'; ')
		txt.write('parent2: ' + str(ind.parent2)+'; ')
		txt.write('espece: ' + str(ind.espece)+'; ')
		txt.write('nbGenes: ' + str(ind.ADN.compteGene())+'; ')
		txt.write('nodeInt: ' + str(ind.ADN.nbNodeInt)+'; ')
		txt.write('score: ' + str(ind.score)+'; ')
		txt.write('classement: ' + str(ind.classement).zfill(3) + '\n')

		for g in ind.ADN.seqGene:
			txt.write(str(g.inNode) + '; ')
			txt.write(str(g.outNode) + '; ')
			txt.write(str(g.weight) + '; ')
			txt.write(str(g.active) + '; ')
			txt.write(str(g.code) + '\n')
		txt.write('\n')

def writeForReplay(ind):
	with open('replay.txt', 'w') as txt:
		txt.write('nom: ' + str(ind.nom)+'; ')
		txt.write('age: ' + str(ind.age)+'; ')
		txt.write('parent1: ' + str(ind.parent1)+'; ')
		txt.write('parent2: ' + str(ind.parent2)+'; ')
		txt.write('espece: ' + str(ind.espece)+'; ')
		txt.write('nbGenes: ' + str(ind.ADN.compteGene())+'; ')
		txt.write('nodeInt: ' + str(ind.ADN.nbNodeInt)+'; ')
		txt.write('score: ' + str(ind.score)+'; ')
		txt.write('classement: ' + str(ind.classement).zfill(3) + '\n')
		for g in ind.ADN.seqGene:
			txt.write(str(g.inNode) + '; ')
			txt.write(str(g.outNode) + '; ')
			txt.write(str(g.weight) + '; ')
			txt.write(str(g.active) + '; ')
			txt.write(str(g.code) + '\n')
		txt.write('\n')

def printInd(ind):
	print("Nom:", ind.nom, "Espece:", ind.espece, "Age:", \
	   ind.age, "Dscdts:", ind.descendants, "Par1:", ind.parent1, \
	   "Par2:", ind.parent2)
	print("nbGenes:", ind.ADN.compteGene(), "nbNodeInt:", ind.ADN.nbNodeInt, \
	   "nbNodeEncr:", ind.ADN.compteEncrActif(), "Score:", ind.score)
	for g in ind.ADN.seqGene:
		print(g.inNode, g.outNode, g.weight, g.active, g.code)
	print("Nom:", ind.nom, "Espece:", ind.espece, "Age:", \
	   ind.age, "Dscdts:", ind.descendants, "Par1:", ind.parent1, \
	   "Par2:", ind.parent2)
	print("nbGenes:", ind.ADN.compteGene(), "nbNodeInt:", ind.ADN.nbNodeInt, \
	   "nbNodeEncr:", ind.ADN.compteEncrActif(), "Score:", ind.score)

def writeRecursionException(pop, inderr):
	with open('error.txt', 'w') as txt:
		txt.write('___________________Broken Individual___________________\n')
		txt.write('nom: ' + str(inderr.nom)+'; ')
		txt.write('age: ' + str(inderr.age)+'; ')
		txt.write('parent1: ' + str(inderr.parent1)+'; ')
		txt.write('parent2: ' + str(inderr.parent2)+'; ')
		txt.write('espece: ' + str(inderr.espece)+'; ')
		txt.write('nodeInt: ' + str(inderr.ADN.nbNodeInt)+'; ')
		txt.write('score: ' + str(inderr.score)+'; ')
		txt.write('classement: ' + str(inderr.classement).zfill(3) + '\n')
#			txt.write('ptsMemeEspece: ' + str(ind.ptsMemeEspece)+'\n')
		for g in inderr.ADN.seqGene:
			txt.write(str(g.inNode) + '; ')
			txt.write(str(g.outNode) + '; ')
			txt.write(str(g.weight) + '; ')
			txt.write(str(g.active) + '; ')
			txt.write(str(g.code) + '\n')
		txt.write('\n')
		txt.write('___________________Population___________________\n')
		for ind in pop.indiv:
			txt.write('nom: ' + str(ind.nom)+'; ')
			txt.write('age: ' + str(ind.age)+'; ')
			txt.write('parent1: ' + str(ind.parent1)+'; ')
			txt.write('parent2: ' + str(ind.parent2)+'; ')
			txt.write('espece: ' + str(ind.espece)+'; ')
			txt.write('nodeInt: ' + str(ind.ADN.nbNodeInt)+'; ')
			txt.write('score: ' + str(ind.score)+'; ')
			txt.write('classement: ' + str(ind.classement).zfill(3) + '\n')
#			txt.write('ptsMemeEspece: ' + str(ind.ptsMemeEspece)+'\n')
			for g in ind.ADN.seqGene:
				txt.write(str(g.inNode) + '; ')
				txt.write(str(g.outNode) + '; ')
				txt.write(str(g.weight) + '; ')
				txt.write(str(g.active) + '; ')
				txt.write(str(g.code) + '\n')
			txt.write('\n')

def exportForExcelAnalysis(pop):
	with open('analyse.csv', 'w') as txt:
		for ind in pop.indiv:
			for g in ind.ADN.seqGene:
				txt.write(str(ind.nom) + ';' + str(ind.espece) + ';')
				if ind.score < 1:
					txt.write('0,001;')
				else:
					txt.write(str(int(ind.score)) + ';')
				txt.write(str(ind.classement) + ';')
				#txt.write(str(ind.age) + ';')
				#txt.write(str(ind.descendants) + ';')
				txt.write(str(g.inNode) + ';')
				txt.write(str(g.outNode) + ';')
				if g.weight < 0:
					txt.write('-0,' + str(g.weight)[3:] + ';')
				elif g.weight == 1.0:
					txt.write('1;')
				else:
					txt.write('0,' + str(g.weight)[2:] + ';')
				if g.active:
					txt.write('VRAI' + ';')
				else:
					txt.write('FAUX' + ';')
				txt.write(str(g.code) + '\n')