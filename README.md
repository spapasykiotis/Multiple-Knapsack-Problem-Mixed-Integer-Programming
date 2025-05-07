# Multiple Knapsacks Optimization Problem

## Overview

This project implements a solution to the **Multiple Knapsack Problem (MKP)** using Mixed Integer Programming (MIP) via the **Google OR-Tools** library and the **SCIP** solver. The objective is to maximize the total value of items packed into a given number of knapsacks (bins), each with a limited capacity, subject to the constraint that each item can be placed in at most one bin.

## Problem Description

Given:
- A set of items, each with an associated weight and value.
- A set of knapsacks (bins), each with a specified capacity.

Goal:
- Select a subset of items and assign each item to at most one bin, such that the total value of packed items is maximized, and the total weight in each bin does not exceed its capacity.

## Mathematical Formulation

Let:
- \( x_{i,j} \in \{0,1\} \): 1 if item \( i \) is placed in bin \( j \), 0 otherwise.
- \( w_i \): weight of item \( i \)
- \( v_i \): value of item \( i \)
- \( c_j \): capacity of bin \( j \)

### Objective Function:
Maximize:
\[
\sum_{i \in \text{items}} \sum_{j \in \text{bins}} v_i \cdot x_{i,j}
\]

### Constraints:
- Each item can be assigned to at most one bin:
\[
\sum_{j \in \text{bins}} x_{i,j} \leq 1 \quad \forall i
\]
- The total weight in each bin must not exceed its capacity:
\[
\sum_{i \in \text{items}} w_i \cdot x_{i,j} \leq c_j \quad \forall j
\]

## Implementation Details

- Language: Python
- Solver: Google OR-Tools with SCIP backend
- Input: CSV files for item data (`items_dataset.csv`) and bin capacities (`bins_dataset.csv`)
- Output: Printed solution summary and optional visual representation using `plot_bin_packing.py`

## File Structure

```
.
├── multiple_knapsacks.py           # Main solver script
├── datasets/
│   ├── items_dataset.csv           # Item data (weight, value)
│   └── bins_dataset.csv            # Bin data (capacity)
├── plot_bin_packing.py             # (Optional) Visualization script
├── problem_description_greek.pptx  # Ploblem and solution description PowerPoint file (Greek Language)
└── README.md                       # Project description and usage

```

## How to Run

1. Ensure the following dependencies are installed:
   ```bash
   pip install ortools matplotlib
   ```

2. Prepare your input CSV files:
   - `items_dataset.csv` with headers: `weight`, `value`
   - `bins_dataset.csv` with header: `capacity`

3. Execute the script:
   ```bash
   python multiple_knapsacks.py
   ```

4. When prompted, enter the number of bins to use from the dataset.

## Visualization

If the `plot_bin_packing.py` script is present, the packed bins and items will be visualized after solving the problem.

## Example

Given 5 items and 4 bins with capacities, the solver will explore placements using branch-and-bound and constraint propagation to efficiently reach an optimal or feasible solution.

## References

- [Google OR-Tools Documentation](https://developers.google.com/optimization/introduction/python)
- [SCIP Optimization Suite](https://scipopt.org/)
