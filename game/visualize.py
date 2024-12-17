import matplotlib.pyplot as plt
import json

def visualize_results(results_file):
    with open(results_file, 'r') as f:
        data = json.load(f)

    generations = data["generations"]
    best_fitness = data["best_fitness"]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, best_fitness, marker='o', linestyle='-', color='b')
    plt.title("Best Fitness Through Generations")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.grid(True)
    plt.savefig("fitness_visualization.png")
    plt.show()


if __name__ == "__main__":
    visualize_results("results.json")
