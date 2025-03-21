# COSBr

**C**ombinatorial **O**ptimization **S**olver using discrete simulated **B**ifurcation in C++ with Python bindings.

## Description

COSBr is a Python package that provides fast C++ implementations of Discrete Simulated Bifurcation (DSB) algorithms for solving combinatorial optimization problems.

## Installation

```bash
pip install cosbr
```

## Usage

### Basic Usage

```python
import numpy as np
from cosbr import gcp_solver

# Create adjacency matrix
adj_matrix = np.zeros((5, 5))
adj_matrix[0, 1] = adj_matrix[1, 0] = 1.0
adj_matrix[0, 3] = adj_matrix[3, 0] = 1.0
adj_matrix[1, 4] = adj_matrix[4, 1] = 1.0
adj_matrix[2, 3] = adj_matrix[3, 2] = 1.0

# Convert to list of lists format (required for the C++ function)
adj_matrix_list = adj_matrix.tolist()

# Solve the graph coloring problem with 2 colors
best_coloring, energy_history = gcp_solver(
    adj_matrix_list,  # adj_matrix
    2,                # num_colors
    100,              # R = 100 runs
    20000,            # max_iter = 20000
    0.05,             # dt = 0.05
    1.0,              # A = 1.0
    0.5,              # alpha_init = 0.5
    0.999             # alpha_scale = 0.999
)

# Print final energy
print(f"Final energy: {energy_history[-1]}")

# Convert the coloring to a more usable format
vertex_colors = []
for i, colors in enumerate(best_coloring):
    for c, is_colored in enumerate(colors):
        if is_colored > 0:
            vertex_colors.append(c)
            break

print(f"Vertex colors: {vertex_colors}")
```

### Advanced Usage

```python
from cosbr import solve_graph_coloring

# This is a convenience function that returns additional information
best_coloring, energy_history, final_energy = solve_graph_coloring(
    adj_matrix_list,  # adj_matrix
    2                 # num_colors
)

print(f"Final energy: {final_energy}")
```

## Features

* Fast C++ implementation of Discrete Simulated Bifurcation algorithm
* Python bindings with numpy support
* Multiple runs with different initializations to find the best solution
* Support for different parameters to tune the optimization process

## License

MIT License