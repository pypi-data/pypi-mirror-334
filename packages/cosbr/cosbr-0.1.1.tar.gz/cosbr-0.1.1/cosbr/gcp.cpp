#include <iostream>
#include <vector>
#include <random>
#include <cmath>
#include <limits>
#include <algorithm>
#include <utility> // for std::pair

// Type definitions for clarity
typedef std::vector<std::vector<double> > Matrix;
typedef std::vector<std::vector<double> > ColorMatrix;

/**
 * Computes the energy function for a given graph coloring.
 * 
 * @param adj_matrix Adjacency matrix of the graph (NxN)
 * @param coloring Coloring matrix (NxC), where C is the number of colors
 * @param A Penalty coefficient
 * @return Energy value of the given coloring
 */
double graph_coloring_energy(const Matrix& adj_matrix, const ColorMatrix& coloring, double A = 1.0) {
    size_t N = coloring.size();      // Number of vertices
    size_t C = coloring[0].size();   // Number of colors
    
    // Term 1: Vertex Constraint - Each vertex should have exactly one color
    double vertex_constraint = 0.0;
    for (size_t i = 0; i < N; ++i) {
        double sum_colors = 0.0;
        for (size_t c = 0; c < C; ++c) {
            sum_colors += coloring[i][c];
        }
        vertex_constraint += std::pow(1.0 - sum_colors, 2);
    }
    
    // Term 2: Edge Constraint - No two adjacent vertices should share the same color
    double edge_constraint = 0.0;
    for (size_t u = 0; u < N; ++u) {
        for (size_t v = 0; v < N; ++v) {
            if (adj_matrix[u][v] == 1.0) {
                for (size_t c = 0; c < C; ++c) {
                    edge_constraint += coloring[u][c] * coloring[v][c];
                }
            }
        }
    }
    
    // Compute total energy
    double energy = A * (vertex_constraint + edge_constraint);
    return energy;
}

/**
 * Compute the local field for DSB algorithm.
 * 
 * @param adj_matrix Adjacency matrix of the graph
 * @param q Current binary state variables
 * @param A Penalty coefficient
 * @return Local field for each variable
 */
ColorMatrix compute_local_field(const Matrix& adj_matrix, const ColorMatrix& q, double A = 1.0) {
    size_t N = q.size();
    size_t C = q[0].size();
    
    // Initialize field
    ColorMatrix h(N, std::vector<double>(C, 0.0));
    
    // Vertex constraint contribution
    for (size_t i = 0; i < N; ++i) {
        double sum_colors = 0.0;
        for (size_t c = 0; c < C; ++c) {
            sum_colors += q[i][c];
        }
        
        for (size_t c = 0; c < C; ++c) {
            h[i][c] += -2.0 * A * (1.0 - sum_colors);
        }
    }
    
    // Edge constraint contribution
    for (size_t u = 0; u < N; ++u) {
        for (size_t v = 0; v < N; ++v) {
            if (adj_matrix[u][v] == 1.0) {
                for (size_t c = 0; c < C; ++c) {
                    h[u][c] += A * q[v][c];
                }
            }
        }
    }
    
    return h;
}

/**
 * Convert q matrix to coloring (0/1 matrix)
 * 
 * @param q_matrix The q matrix to convert
 * @return The coloring matrix
 */
ColorMatrix q_to_coloring(const ColorMatrix& q_matrix) {
    size_t N = q_matrix.size();
    size_t C = q_matrix[0].size();
    
    ColorMatrix coloring(N, std::vector<double>(C, 0.0));
    
    for (size_t i = 0; i < N; ++i) {
        for (size_t c = 0; c < C; ++c) {
            coloring[i][c] = (q_matrix[i][c] > 0) ? 1.0 : 0.0;
        }
    }
    
    return coloring;
}

/**
 * Optimize graph coloring using Discrete Simulated Bifurcation.
 * 
 * @param adj_matrix Adjacency matrix of the graph
 * @param num_colors Number of colors to use
 * @param max_iter Maximum number of iterations
 * @param dt Time step size
 * @param A Penalty coefficient
 * @param alpha_init Initial value of alpha
 * @param alpha_scale Scaling factor for alpha each iteration
 * @return Pair containing optimized coloring and energy history
 */
std::pair<ColorMatrix, std::vector<double> > discrete_simulated_bifurcation(
    const Matrix& adj_matrix, 
    size_t num_colors, 
    size_t max_iter = 1000, 
    double dt = 0.1, 
    double A = 1.0, 
    double alpha_init = 0.5, 
    double alpha_scale = 0.998
) {
    size_t N = adj_matrix.size();  // Number of vertices
    
    // Random number generation
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, 1);
    
    // Initialize binary variables and their velocities
    ColorMatrix q(N, std::vector<double>(num_colors));
    ColorMatrix p(N, std::vector<double>(num_colors, 0.0));
    
    // Initialize q with random values (-1 or 1)
    for (size_t i = 0; i < N; ++i) {
        for (size_t c = 0; c < num_colors; ++c) {
            q[i][c] = (dist(gen) == 0) ? -1.0 : 1.0;
        }
    }
    
    // Initialize alpha (bifurcation parameter)
    double alpha = alpha_init;
    
    // Initialize energy history
    std::vector<double> energy_history;
    energy_history.reserve(max_iter);
    
    // Main loop
    for (size_t iteration = 0; iteration < max_iter; ++iteration) {
        // Convert q to coloring format for energy calculation
        ColorMatrix coloring = q_to_coloring(q);
        
        // Calculate current energy
        double energy = graph_coloring_energy(adj_matrix, coloring, A);
        energy_history.push_back(energy);
        
        // Calculate local field
        ColorMatrix h = compute_local_field(adj_matrix, coloring, A);
        
        // Update momentum (p)
        for (size_t i = 0; i < N; ++i) {
            for (size_t c = 0; c < num_colors; ++c) {
                p[i][c] = p[i][c] - dt * h[i][c];
            }
        }
        
        // Update position (q)
        for (size_t i = 0; i < N; ++i) {
            for (size_t c = 0; c < num_colors; ++c) {
                // Update using discrete simulated bifurcation equations
                if (p[i][c] > 0) {
                    q[i][c] = 1.0;
                } else if (p[i][c] < 0) {
                    q[i][c] = -1.0;
                }
                // If p[i][c] is exactly 0, q[i][c] remains unchanged
            }
        }
        
        // Decrease alpha (annealing)
        alpha *= alpha_scale;
        
        // Check if solution is valid (termination condition)
        if (energy == 0) {
            break;
        }
    }
    
    // Return the best coloring found
    ColorMatrix final_coloring = q_to_coloring(q);
    return std::make_pair(final_coloring, energy_history);
}

/**
 * Run DSB multiple times and return the best result.
 * 
 * @param adj_matrix Adjacency matrix of the graph
 * @param num_colors Number of colors to use
 * @param R Number of runs
 * @param max_iter Maximum number of iterations per run
 * @param dt Time step size
 * @param A Penalty coefficient
 * @param alpha_init Initial value of alpha
 * @param alpha_scale Scaling factor for alpha each iteration
 * @return Pair containing best coloring and its energy history
 */
std::pair<ColorMatrix, std::vector<double> > gcp_solver(
    const Matrix& adj_matrix, 
    size_t num_colors, 
    size_t R = 100, 
    size_t max_iter = 20000, 
    double dt = 0.05, 
    double A = 1.0, 
    double alpha_init = 0.5, 
    double alpha_scale = 0.999
) {
    ColorMatrix best_coloring;
    std::vector<double> best_energy_history;
    double lowest_final_energy = std::numeric_limits<double>::infinity();
    
    for (size_t r = 0; r < R; ++r) {
        std::pair<ColorMatrix, std::vector<double> > result = discrete_simulated_bifurcation(
            adj_matrix, 
            num_colors, 
            max_iter, 
            dt, 
            A, 
            alpha_init,
            alpha_scale
        );
        
        ColorMatrix coloring = result.first;
        std::vector<double> energy_history = result.second;
        
        if (energy_history.back() < lowest_final_energy) {
            lowest_final_energy = energy_history.back();
            best_coloring = coloring;
            best_energy_history = energy_history;
        }
    }
    
    return std::make_pair(best_coloring, best_energy_history);
}

/**
 * Print the coloring matrix to console.
 * 
 * @param coloring The coloring matrix to print
 */
void print_coloring(const ColorMatrix& coloring) {
    size_t N = coloring.size();
    size_t C = coloring[0].size();
    
    std::cout << "Vertex coloring:\n";
    for (size_t i = 0; i < N; ++i) {
        std::cout << "Vertex " << i << ": ";
        for (size_t c = 0; c < C; ++c) {
            if (coloring[i][c] > 0) {
                std::cout << "Color " << c << "\n";
                break;
            }
        }
    }
}

int main() {
    // Example adjacency matrix
    Matrix adj_matrix;
    adj_matrix.resize(5);
    for (size_t i = 0; i < 5; ++i) {
        adj_matrix[i].resize(5, 0.0);
    }
    
    // Initialize with the example values
    adj_matrix[0][1] = 1.0; adj_matrix[0][3] = 1.0;
    adj_matrix[1][0] = 1.0; adj_matrix[1][4] = 1.0;
    adj_matrix[2][3] = 1.0;
    adj_matrix[3][0] = 1.0; adj_matrix[3][2] = 1.0;
    adj_matrix[4][1] = 1.0;
    
    size_t num_colors = 2;
    
    std::cout << "Running DSB for graph coloring with " << num_colors << " colors...\n";
    
    std::pair<ColorMatrix, std::vector<double> > result = gcp_solver(
        adj_matrix, 
        num_colors, 
        100,   // R = 100 runs
        20000, // max_iter = 20000
        0.05,  // dt = 0.05
        1.0,   // A = 1.0
        0.5,   // alpha_init = 0.5
        0.999  // alpha_scale = 0.999
    );
    
    ColorMatrix best_coloring = result.first;
    std::vector<double> energy_history = result.second;
    
    // Print final energy
    double final_energy = energy_history.back();
    std::cout << "Final energy: " << final_energy << "\n";
    
    // Print the coloring
    print_coloring(best_coloring);
    
    // Check if solution is valid
    if (final_energy == 0) {
        std::cout << "Found valid coloring!\n";
    } else {
        std::cout << "Could not find valid coloring.\n";
    }
    
    return 0;
}