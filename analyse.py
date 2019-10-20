import init
import cartes
import classes
import suivi

param = init.loadParam()
caracs = cartes.creerCaracteristiques()
pop = classes.population(param)

init.loadPopForAnalysis(param, pop, caracs)
suivi.exportForExcelAnalysis(pop)