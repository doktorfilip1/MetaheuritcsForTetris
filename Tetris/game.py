from ga import *

jedinka = Individual(4)
jedinka.code = [0.8608840204413541, 0.5544747214997585, 0.04792394216148155, 0.5905354148753311]
#jedinka.code = [0.9635348759805299, 0.02197870449645889, 0.22959360116973254, 0.20793209342444544]

for i in range(3):
    jedinka.calcFit(simulate_game)
    print(i + 1, "gen, fitness: ", jedinka.fitness)