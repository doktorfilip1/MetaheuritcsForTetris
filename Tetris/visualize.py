import matplotlib.pyplot as plt

fitness_values = []
with open('_testovi.txt', 'r') as file:
    for line in file:
        if "Best fitness = " in line:
            fitness = int(line.strip().split('=')[1])
            fitness_values.append(fitness)

# Crtanje grafikona
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(fitness_values) + 1), fitness_values,color = 'r', marker='o')
plt.title('Promena fitness vrednosti kroz generacije')
plt.xlabel('Generacija')
plt.ylabel('Fitness')
plt.grid(True)
plt.show()