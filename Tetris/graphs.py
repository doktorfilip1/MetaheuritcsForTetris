import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

GENS = 20
data=[]

with open("tests.json", "w") as f:
    json.dump(data, f, indent=4)

# Učitavanje podataka za crtanje grafika
generations = list(range(1, GENS + 1))
best_fitness = [entry["best_fitness"] for entry in data]
worst_fitness = [entry["worst_fitness"] for entry in data]
avg_fitness = [entry["avg_fitness"] for entry in data]

# Crtanje pojedinačnih grafika
plt.figure(figsize=(12, 6))
plt.plot(generations, best_fitness, label="Best Fitness", color='green')
plt.plot(generations, worst_fitness, label="Worst Fitness", color='red')
plt.plot(generations, avg_fitness, label="Average Fitness", color='blue')
plt.xlabel("Generations")
plt.ylabel("Fitness")
plt.title("Fitness Evolution Through Generations")
plt.legend()
plt.grid()
plt.show()

# Heatmap za genome
genomes = np.array([entry["genom"] for entry in data])
plt.figure(figsize=(10, 6))
sns.heatmap(genomes, annot=True, cmap="coolwarm", xticklabels=["Param 1", "Param 2", "Param 3", "Param 4"], yticklabels=generations)
plt.xlabel("Genome Parameters")
plt.ylabel("Generation")
plt.title("Heatmap of Best Genome per Generation")
plt.show()