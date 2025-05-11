from ortools.linear_solver import pywraplp
from plot_bin_packing import plot_solution
import csv

plot_results = True
items_dataset = "datasets/items_dataset.csv"
bins_dataset = "datasets/bins_dataset.csv"

def print_solution(data, x, objective):
    total_weight = 0
    for j in data['bins']:
        bin_weight = 0
        bin_value = 0
        print('Bin ', j, '\n')
        for i in data['items']:
            if x[i, j].solution_value() > 0:
                print('Item', i, '- weight:', data['weights'][i], ' value:',
                      data['values'][i])
                bin_weight += data['weights'][i]
                bin_value += data['values'][i]
        print('Packed bin weight:', bin_weight)
        print('Packed bin value:', bin_value)
        print()
        total_weight += bin_weight
    print('Total packed weight:', total_weight)

def load_items_from_csv(items_dataset):
    weights = []
    values = []
    with open(items_dataset, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            weights.append(int(row['weight']))
            values.append(int(row['value']))
    return weights, values

def load_bin_capacities_from_csv(bins_dataset):
    bin_capacities = []
    with open(bins_dataset, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bin_capacities.append(int(row['capacity']))
    return bin_capacities

# Load items and bin capacity list first
bin_capacities_all = load_bin_capacities_from_csv(bins_dataset)
weights, values = load_items_from_csv(items_dataset)

# Ask user to input the number of bins
while True:
    try:
        num_bins_to_use = int(input(f"Enter the number of bins to use (1 to {len(bin_capacities_all)}): "))
        if 1 <= num_bins_to_use <= len(bin_capacities_all):
            break
        else:
            print(f"Please enter a number between 1 and {len(bin_capacities_all)}.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

def create_data_model(weights, values, bin_capacities_all):  
    bin_capacities = bin_capacities_all[:num_bins_to_use]

    data = {}
    data['weights'] = weights
    data['values'] = values
    data['items'] = list(range(len(weights)))
    data['num_items'] = len(weights)
    num_bins = len(bin_capacities)
    data['bins'] = list(range(num_bins))
    data['bin_capacities'] = bin_capacities
    return data

data = create_data_model(weights, values, bin_capacities_all)

# Create the MIP solver
solver = pywraplp.Solver.CreateSolver('SCIP')
# solver.EnableOutput()

# Variables
# x[i, j] = 1 if item i is packed in bin j.
x = {}
for i in data['items']:
    for j in data['bins']:
        x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

# Constraints
# Each item can be in at most one bin.
for i in data['items']:
    solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
# The amount packed in each bin cannot exceed its capacity.
for j in data['bins']:
    solver.Add(
        sum(x[(i, j)] * data['weights'][i]
            for i in data['items']) <= data['bin_capacities'][j])

# Objective
objective = solver.Objective()

for i in data['items']:
    for j in data['bins']:
        objective.SetCoefficient(x[(i, j)], data['values'][i])
objective.SetMaximization()

# Call solver
status = solver.Solve()

# Check for the solution status
if status == pywraplp.Solver.OPTIMAL:
    print('Total packed value:', objective.Value())
    print_solution(data, x, objective)

elif status == pywraplp.Solver.FEASIBLE:
    print("A feasible but suboptimal solution was found.")
    print_solution(data, x, objective)

elif status == pywraplp.Solver.INFEASIBLE:
    print('The problem is infeasible, no solution exists that satisfies the constraints.')
    plot_results = False
else:
    print('The problem does not have a feasible or optimal solution.')
    plot_results = False

# Additional line after status check
DV = solver.variables()
print('Number of total decision variables:', len(DV))

# Visualize results
if plot_results:
    plot_solution(data, x)