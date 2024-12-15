import random

class Individual():
    def __init__(self,cost,costFixed):
        self.cost = cost
        self.costFixed = costFixed
        self.code = [random.uniform(0,1) < 0.25 for _ in range(len(costFixed))]
        self.fix()
        self.fitness = self.calcFit(cost,costFixed)
        
    def __lt__(self,other):
        return self.fitness < other.fitness
    
    def calcFit(self,cost,costFixed):
        totalCost = 0
        
        usedRes = [False for _ in range(len(costFixed))]
        
        for i in range(len(cost)):
            fitest = float('inf')
            fitInd = -1
            for j in range(len(costFixed)):
                if self.code[j] and cost[i][j] < fitest:
                    fitest = cost[i][j]
                    fitInd = j
            totalCost += fitest
            usedRes[fitInd] = True
        
        self.code = usedRes
        
        for j in range(len(usedRes)):
            if usedRes[j]:
                totalCost += costFixed[j]
                
        return 1/totalCost
    
    def fix(self):
        for c in self.code:
            if c:
                return
        randomResource = random.randrange(len(self.code))
        self.code[randomResource] = True

def selection(population):
        TOURNAMENT_SIZE = 5
        bestFitness = float('inf')
        index = -1
        for i in range(TOURNAMENT_SIZE):
            randomIndividual = random.randrange(len(population))
            if population[randomIndividual].fitness > bestFitness:
                bestFitness = population[randomIndividual].fitness
                index = randomIndividual
        return population[index]
    
def crossover(parent1,parent2,child1,child2):
    randInd = random.randrange(len(parent1.code))
    
    child1.code[:randInd] = parent1.code[:randInd]
    child1.code[randInd:] = parent2.code[randInd:]
    
    child2.code[:randInd] = parent2.code[:randInd]
    child2.code[randInd:] = parent1.code[randInd:]

def mutation(single):
    for i in range(len(single.code)):
        if random.uniform(0,1) < 0.03:
            single.code[i] = not single.code[i]

GENS = 20
POPULATION_SIZE = 100
cost = [[1,12,3],[2,7,41],[19,21,7]]
fixedCost = [12,11,13]
population = [Individual(cost,fixedCost) for _ in range(POPULATION_SIZE)]
ELITISM = POPULATION_SIZE // 10


for i in range(GENS):
    population.sort(reverse=True)
    newPopulation = [Individual(cost,fixedCost) for _ in range(POPULATION_SIZE)]
    newPopulation[:ELITISM] = population[:ELITISM]
    for j in range(ELITISM,POPULATION_SIZE,2):
        parent1 = selection(population)
        parent2 = selection(population)
        
        crossover(parent1,parent2,newPopulation[j],newPopulation[j+1])
        
        mutation(newPopulation[j])
        mutation(newPopulation[j+1])
        
        newPopulation[j].fitness = newPopulation[j].calcFit(cost,fixedCost)
        newPopulation[j+1].fitness = newPopulation[j+1].calcFit(cost,fixedCost)
        
        population = newPopulation
best = max(population)
print(best.code)