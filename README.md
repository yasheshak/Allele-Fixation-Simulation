"""
# **Population Genetics Simulation Tool**

## **Overview**
This comprehensive toolset provides simulations for population genetics using Wright-Fisher and coalescent models. It consists of three tiers, simulating allele fixation/loss, variable population dynamics, and coalescent events to study genetic drift and evolution.

---

## **Features**

### **Tier 1: Wright-Fisher Model with Selection**
1. Simulates the number of generations until an allele reaches fixation (frequency = 1) or loss (frequency = 0).
2. Incorporates selection through weighted allele frequencies based on relative fitness.
3. Outputs:
   - Mean and variance of generations to fixation or loss.

### **Tier 2: Wright-Fisher Model with Variable Population Sizes**
1. Extends the Tier 1 model to include variable population sizes over generations.
2. Reads population size changes from a TSV file and adjusts dynamics accordingly.
3. Outputs:
   - Mean and variance of generations to fixation or loss under varying population sizes.

### **Tier 3: Coalescent Simulation for Time to Eighth Event**
1. Simulates coalescent events to estimate the time to the eighth coalescent event in a sample.
2. Uses an exponential waiting time model based on population size and the number of lineages.
3. Outputs:
   - Mean and variance of time to the eighth coalescent event.

---

## **Dependencies**
- **Python 3.x**
- **NumPy** (`pip install numpy`)

---

## **Input Arguments**

### **Tier 1**:
1. `--allele_freq`: Initial allele frequency (0-1).
2. `--pop_size`: Population size.
3. `--fitness`: Relative fitness of the allele.
4. `--replicates`: Number of simulation replicates.

### **Tier 2**:
1. `--allele_freq`: Initial allele frequency (0-1).
2. `--pop_size_file`: Path to a TSV file containing population size changes per generation.
3. `--fitness`: Relative fitness of the allele.
4. `--replicates`: Number of simulation replicates.

### **Tier 3**:
1. `--pop_size`: Effective population size.
2. `--sample_size`: Sample size for simulation.
3. `--replicates`: Number of simulation replicates.

---

## **Usage**

### **Tier 1**:
```bash
python tier1_simulation.py --allele_freq 0.1 --pop_size 100 --fitness 1.2 --replicates 1000
