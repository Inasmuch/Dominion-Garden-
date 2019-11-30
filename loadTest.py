
import init
import classes
import func
import simul
import cartes
import random
#import test

param = init.loadParam()	
caracs = cartes.creerCaracteristiques()
pop = classes.population(param)
#init.replayPopFromText(param, pop, caracs)

#for g in pop.indiv[0].ADN.seqGene:
	#print(g.inNode, g.outNode, g.weight, g.active, g.code)

init.loadPopFromText(param, pop, caracs)
par1 = pop.indiv[0]
par2 = pop.indiv[1]
print(par1.nom)
print(par2.nom)
print(max(par1.nom, par2.nom))
par2 = par1
print(par2.nom)
print(pop.indiv[1].nom)
print(max(par1.nom, par2.nom))