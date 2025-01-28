import matplotlib.pyplot as plt

# Read the data from the file
generations = []
fitnesses = []
with open("/home/vookmeer/Documents/GitHub/MetaheuritcsForTetris/proba/data.txt", 'r') as file:
    for line in file:
        parts = line.split(': ')
        if len(parts) == 2:
            generation = int(parts[0].split()[1])
            fitness = float(parts[1].split('=')[1])
            generations.append(generation)
            fitnesses.append(fitness)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(generations, fitnesses, marker='o')

# Labeling the axes
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title('Best Fitness Over Generations')

# Display the plot
plt.grid(True)
plt.show()