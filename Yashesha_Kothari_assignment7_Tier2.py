import argparse  
import numpy as np  

def load_population_sizes(pop_size_file):
    """loads population sizes from a tsv file, returning a list of (generation, size) tuples"""
    population_changes = []
    with open(pop_size_file, 'r') as file:
        for line in file:
            generation, size = map(int, line.strip().split())
            population_changes.append((generation, size))  # add each generation and size pair
    return population_changes

def get_population_size(generation, population_changes):
    """returns population size for a given generation based on specified changes"""
    for i in range(len(population_changes) - 1):
        # use the population size for the current range of generations
        if population_changes[i][0] <= generation < population_changes[i + 1][0]:
            return population_changes[i][1]
    return population_changes[-1][1]  # if past all specified changes, use last population size

def simulate_fixation_loss(allele_freq, pop_size_file, fitness, replicates):
    # load population change points from file
    population_changes = load_population_sizes(pop_size_file)
    
    fixation_times = []
    loss_times = []

    for _ in range(replicates):
        generations = 0
        freq = allele_freq
        
        while 0 < freq < 1:
            # get population size for the current generation
            current_pop_size = get_population_size(generations, population_changes)
            
            # calculate next generation's allele frequency with selection
            weighted_freq = freq * fitness / (freq * fitness + (1 - freq))
            freq = np.random.binomial(current_pop_size, weighted_freq) / current_pop_size
            generations += 1

        # record generations until fixation or loss
        if freq == 1:
            fixation_times.append(generations)
        elif freq == 0:
            loss_times.append(generations)

    # compute mean and variance for fixation and loss times
    fixation_mean, fixation_variance = (np.mean(fixation_times), np.var(fixation_times)) if fixation_times else (None, None)
    loss_mean, loss_variance = (np.mean(loss_times), np.var(loss_times)) if loss_times else (None, None)

    return fixation_mean, fixation_variance, loss_mean, loss_variance

def main():
    parser = argparse.ArgumentParser(description="Wright-Fisher model with variable population sizes")
    parser.add_argument("--allele_freq", type=float, required=True, help="initial allele frequency (0-1)")
    parser.add_argument("--pop_size_file", type=str, required=True, help="path to tsv file with population sizes")
    parser.add_argument("--fitness", type=float, required=True, help="relative fitness of the allele")
    parser.add_argument("--replicates", type=int, required=True, help="number of simulation replicates")

    args = parser.parse_args()

    # run simulation and get fixation and loss stats
    fixation_mean, fixation_variance, loss_mean, loss_variance = simulate_fixation_loss(
        args.allele_freq, args.pop_size_file, args.fitness, args.replicates
    )

    # print results
    if fixation_mean is not None:
        print(f"allele was fixed in {fixation_mean:.2f} generations. variance: {fixation_variance:.2f}")
    if loss_mean is not None:
        print(f"allele was lost in {loss_mean:.2f} generations. variance: {loss_variance:.2f}")

if __name__ == "__main__":
    main()
