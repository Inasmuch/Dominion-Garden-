import init
import classes
import func
import transmit
import simul
import mutation
import suivi
import cartes
import random

siPopFromText = True
siPopFromCore = False

random.seed()
param = init.loadParam()
effets = cartes.creerEffets()
caracs = cartes.creerCaracteristiques()
pop = classes.population(param)
	
if siPopFromText:
	init.loadPopFromText(param, pop, caracs)
elif siPopFromCore:
	init.seedPopFromCore(param, pop, caracs)
else:
	init.creerPopulationAvecCouches(param, pop, caracs)

suivi.writeParam(param, siPopFromText, siPopFromCore)
transmit.speciation(param, pop)
	
randind = list(range(param['nbIndiv']))
groupes = []
nbMaxMatch = int(param['nbSimul']*(param['nbSimul']+1)/2)

for generation in range(param['nbGeneration'] - 1):
	
	print(' ')
	print("*** Generation:", generation, "***")
	init.preparerPopulation(param, pop)
		
	random.shuffle(randind)
	for i in range(int(param['nbIndiv']/(param['nbSimul']+1))):
		groupes.append([])
	for i in range(len(groupes)):
		for j in range((param['nbSimul']+1)):
			groupes[i].append(pop.indiv[randind[i*(param['nbSimul']+1)+j]])
		
	for i in range(len(groupes)):
		#match = 0
		for j in range(len(groupes[i])):
			for k in range(j+1, len(groupes[i])):
				#match += 1
				#print(' ')
				#print ('Gen ' + str(generation + 1).zfill(2) + '/' + \
				#	str(param['nbGeneration']).zfill(2) + ' Group ' +\
				#   str(i + 1).zfill(2) + '/' + str(len(groupes)) + \
				#   ' Match ' + str(match).zfill(2) + '/' + \
				#   str(nbMaxMatch).zfill(2))
				simul.simulation(param, groupes[i][j], groupes[i][k], \
					effets, caracs)
				for g in groupes[i][j].ADN.seqGene:
					g.encr = 0
				for g in groupes[i][k].ADN.seqGene:
					g.encr = 0
				
				simul.simulation(param, groupes[i][k], groupes[i][j], \
					effets, caracs)
				for g in groupes[i][j].ADN.seqGene:
					g.encr = 0
				for g in groupes[i][k].ADN.seqGene:
					g.encr = 0
		print(' ')
		print('Gen: ' + str(generation + 1).zfill(2) + '/' + \
			str(param['nbGeneration']).zfill(2) + ' Group: ' + \
			str(i + 1).zfill(2) + '/' + str(len(groupes)).zfill(2))
		for ind in groupes[i]:
			tag = str(ind.nom).zfill(5) + '.' + str(ind.espece).zfill(3) + \
				' (' + str(ind.age) + ',' + str(ind.descendants) + ')'
			print("{:<12}{:>10}".format(tag, str(ind.score).zfill(2)))

	transmit.succesReproductif(param, pop)
	
	for ind in pop.indiv:
		if ind.classement == 1:
			print(' ')
			print("Champion:")
			suivi.printInd(ind)
	
	transmit.reproduction(param, pop, caracs)
	mutation.mutationArborescente(param, pop, caracs)
	transmit.speciation(param, pop)
	
	del groupes[:]

print(' ')
print("*** Derniere Generation ***")	
init.preparerPopulation(param, pop)

random.shuffle(randind)
for i in range(int(param['nbIndiv']/(param['nbSimul']+1))):
	groupes.append([])
for i in range(len(groupes)):
	for j in range((param['nbSimul']+1)):
		groupes[i].append(pop.indiv[randind[i*(param['nbSimul']+1)+j]])
		
for i in range(len(groupes)):
	#match = 0
	for j in range(len(groupes[i])):
		for k in range(j+1, len(groupes[i])):
			#match += 1
			#print(' ')
			#print ('Derniere generation! Group ' +\
			#	str(i + 1).zfill(2) + '/' + str(len(groupes)) + ' Match ' \
			#	+ str(match).zfill(2) + '/' + str(nbMaxMatch).zfill(2))
			simul.simulation(param, groupes[i][j], groupes[i][k], \
				effets, caracs)
			for g in groupes[i][j].ADN.seqGene:
				g.encr = 0
			for g in groupes[i][k].ADN.seqGene:
				g.encr = 0

			simul.simulation(param, groupes[i][k], groupes[i][j], \
				effets, caracs)
			for g in groupes[i][j].ADN.seqGene:
				g.encr = 0
			for g in groupes[i][k].ADN.seqGene:
				g.encr = 0
	
	print(' ')
	print('Derniere Gen! Group: ' + \
			str(i + 1).zfill(2) + '/' + str(len(groupes)).zfill(2))
	for ind in groupes[i]:
		tag = str(ind.nom).zfill(5) + '.' + str(ind.espece).zfill(3) + \
			' (' + str(ind.age) + ',' + str(ind.descendants) + ')'
		print("{:<12}{:>10}".format(tag, str(ind.score).zfill(2)))

transmit.succesReproductif(param, pop)

for ind in pop.indiv:
	if ind.classement == 1:
		suivi.writeForReplay(ind)
	
suivi.writePop(pop, param['nbGeneration'])
