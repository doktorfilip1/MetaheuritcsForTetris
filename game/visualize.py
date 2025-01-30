import matplotlib.pyplot as plt
import pickle

def plot_fitness():
    with open("fitness_data.pkl", "rb") as f:
        generations, fitness_values = pickle.load(f)

    plt.figure(figsize=(10, 5))
    plt.plot(generations, fitness_values, marker='o', linestyle='-', color='b', label='Best Fitness')
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title("Fitness Change Over Generations")
    plt.legend()
    plt.grid()
    plt.show()

