import numpy as np

# Define prior probabilities
P_A = {True: 0.8, False: 0.2}  # True for 'yes', False for 'no'
P_C = {True: 0.5, False: 0.5}

# Define conditional probabilities for Grade (G) given A and C
P_G_given_A_C = {
    ('Good', True, True): 0.9,
    ('Good', True, False): 0.7,
    ('Good', False, True): 0.6,
    ('Good', False, False): 0.3,
    ('OK', True, True): 0.1,
    ('OK', True, False): 0.3,
    ('OK', False, True): 0.4,
    ('OK', False, False): 0.7
}

# Monte Carlo simulation to estimate P(G = 'Good' | A = 'yes', C = 'yes')
def monte_carlo_simulation(num_samples=10000):
    count_Good_given_A_yes_C_yes = 0
    count_A_yes_C_yes = 0
    
    for _ in range(num_samples):
        # Sample A (Aptitude Skills) and C (Coding Skills)
        A = np.random.rand() < P_A[True]  # True if 'yes'
        C = np.random.rand() < P_C[False]  # True if 'yes'

        # Check if A and C are both 'yes'
        if A and C:
            # Sample G (Grade) based on A and C
            G = 'Good' if np.random.rand() < P_G_given_A_C[('Good', A, C)] else 'OK'
            
            # Count occurrences of G = 'Good' given A = 'yes' and C = 'yes'
            count_A_yes_C_yes += 1
            if G == 'Good':
                count_Good_given_A_yes_C_yes += 1

    # Calculate conditional probability
    if count_A_yes_C_yes == 0:
        return 0  # Avoid division by zero
    return count_Good_given_A_yes_C_yes / count_A_yes_C_yes

# Run simulation
estimated_probability = monte_carlo_simulation()
print(f"Estimated P(G = 'Good' | A = 'yes', C = 'no'): {estimated_probability}")
