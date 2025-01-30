import matplotlib.pyplot as plt
<<<<<<< Updated upstream
import json

def visualize_results(results_file):
    with open(results_file, 'r') as f:
        data = json.load(f)

    generations = data["generations"]
    best_fitness = data["best_fitness"]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, best_fitness, marker='o', linestyle='-', color='r')
    plt.title("Best Fitness Through Generations")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.grid(True)
    plt.savefig("fitness_visualization.png")
    plt.show()


if __name__ == "__main__":
    visualize_results("results.json")
=======
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
>>>>>>> Stashed changes
