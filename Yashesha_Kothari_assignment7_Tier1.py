import argparse  
import numpy as np  


def simulate_fixation_loss(allele_freq, pop_size, fitness, replicates):
    ''' Simulates the number of generations until an allele reaches fixation (frequency = 1)
        or is lost (frequency = 0) in a Wright-Fisher population model with selection. '''
    
    fixation_times = []  
    loss_times = [] 

    #run multiple independent simulations as specified by 'replicates'
    for _ in range(replicates):
        generations = 0  # track the number of generations for each simulation
        freq = allele_freq  # start with the given initial allele frequency
        
        
        # weighted frequency adjust allele transmission probability based on relative fitness
        while 0 < freq < 1:
            weighted_freq = freq * fitness / (freq * fitness + (1 - freq))# Higher fitness (>1) increases probability of transmission; lower fitness (<1) decreases it
            
            # draw the number of successful allele transmissions from a binomial distribution
            freq = np.random.binomial(pop_size, weighted_freq) / pop_size #result is normalized to conver to allele frequency
            #for genentic drift and realistic frequency for next generation
            
            generations += 1 # increment the generation count after each reproduction event
        
        # record the number of generations until fixation or loss for this replicate
        if freq == 1:
            fixation_times.append(generations)
        elif freq == 0:
            loss_times.append(generations)

    # calculate the mean and variance of the generations-to-fixation and generations-to-loss
    # across all replicates, if either outcome was observed in the simulations
    if fixation_times:
        fixation_mean = np.mean(fixation_times)
        fixation_variance = np.var(fixation_times)
    else:
       fixation_mean, fixation_variance = None, None  # no fixation events observed

    if loss_times:
        loss_mean = np.mean(loss_times)
        loss_variance = np.var(loss_times)
    else:
        loss_mean, loss_variance = None, None  # no loss events observed

    
    return fixation_mean, fixation_variance, loss_mean, loss_variance # return the calculated statistics for both fixation and loss


def main():
    
    parser = argparse.ArgumentParser(description="Wright-Fisher Model Allele Fixation Simulation")
    
    # initial allele frequency, population size, fitness, and replicates
    parser.add_argument("--allele_freq", type=float, required=True, help="Initial frequency of the allele (between 0 and 1)")
    parser.add_argument("--pop_size", type=int, required=True, help="Population size (number of individuals in the haploid model)")
    parser.add_argument("--fitness", type=float, required=True, help="Relative fitness of the allele (e.g., >1 for positive selection)")
    parser.add_argument("--replicates", type=int, required=True, help="Number of Monte Carlo simulation replicates to perform")

    args = parser.parse_args()

    # run the simulation function with provided arguments and capture results
    fixation_mean, fixation_variance, loss_mean, loss_variance = simulate_fixation_loss(
        args.allele_freq, args.pop_size, args.fitness, args.replicates
    )

    #print
    if fixation_mean is not None:
        print(f"Allele was fixed in {fixation_mean:.2f} generations. Variance: {fixation_variance:.2f}")
    if loss_mean is not None:
        print(f"Allele was lost in {loss_mean:.2f} generations. Variance: {loss_variance:.2f}")

if __name__ == "__main__":
    main()
