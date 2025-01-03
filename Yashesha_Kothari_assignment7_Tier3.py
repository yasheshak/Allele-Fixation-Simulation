import argparse  
import numpy as np  

def coalescent_simulation(pop_size, sample_size, replicates):
    """simulate coalescent events to estimate time to the eighth event"""
    times_to_eighth_event = []  # stores times for the eighth event across replicates

    for _ in range(replicates):
        remaining_lineages = sample_size
        coalescent_events = 0
        total_time = 0

        # continue until the eighth coalescent event or only one lineage remains
        while coalescent_events < 8 and remaining_lineages > 1:
            # calculate waiting time for next event using exponential distribution
            rate = remaining_lineages * (remaining_lineages - 1) / (2 * pop_size)
            time_to_next_event = np.random.exponential(1 / rate)
            total_time += time_to_next_event
            
            # update event count and reduce lineages by one for each coalescent event
            coalescent_events += 1
            remaining_lineages -= 1

        # record time if eighth coalescent event occurred
        if coalescent_events == 8:
            times_to_eighth_event.append(total_time)

    # calculate mean and variance for time to the eighth coalescent event
    mean_time = np.mean(times_to_eighth_event)
    variance_time = np.var(times_to_eighth_event)

    return mean_time, variance_time

def main():
    # parse command-line arguments for population size, sample size, and replicates
    parser = argparse.ArgumentParser(description="coalescent simulation for time to eighth event")
    parser.add_argument("--pop_size", type=int, required=True, help="effective population size")
    parser.add_argument("--sample_size", type=int, required=True, help="sample size for simulation")
    parser.add_argument("--replicates", type=int, required=True, help="number of simulation replicates")

    args = parser.parse_args()

    # run simulation and print mean/variance for time to eighth event
    mean_time, variance_time = coalescent_simulation(args.pop_size, args.sample_size, args.replicates)
    print(f"time to eighth coalescent event: {mean_time:.2f}. variance: {variance_time:.2f}")

if __name__ == "__main__":
    main()
