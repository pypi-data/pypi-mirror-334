#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  // For automatic conversion of STL containers
#include <pybind11/numpy.h>
#include <vector>
#include <utility>

// Include the gcp.cpp file
// We'll include it as a header to avoid rewriting the functions
#include "gcp.cpp"

namespace py = pybind11;

PYBIND11_MODULE(gcp_module, m) {
    m.doc() = "Graph coloring problem solver using Discrete Simulated Bifurcation";
    
    // Expose the main functions
    m.def("graph_coloring_energy", &graph_coloring_energy, 
          py::arg("adj_matrix"), py::arg("coloring"), py::arg("A") = 1.0,
          "Computes the energy function for a given graph coloring");
          
    m.def("discrete_simulated_bifurcation", &discrete_simulated_bifurcation,
          py::arg("adj_matrix"), py::arg("num_colors"), 
          py::arg("max_iter") = 1000, py::arg("dt") = 0.1,
          py::arg("A") = 1.0, py::arg("alpha_init") = 0.5, 
          py::arg("alpha_scale") = 0.998,
          "Optimize graph coloring using Discrete Simulated Bifurcation");
          
    m.def("gcp_solver", &gcp_solver,
          py::arg("adj_matrix"), py::arg("num_colors"), 
          py::arg("R") = 100, py::arg("max_iter") = 20000, 
          py::arg("dt") = 0.05, py::arg("A") = 1.0, 
          py::arg("alpha_init") = 0.5, py::arg("alpha_scale") = 0.999,
          "Run DSB multiple times and return the best result");
          
    // Helper functions
    m.def("q_to_coloring", &q_to_coloring, 
          py::arg("q_matrix"), 
          "Convert q matrix to coloring (0/1 matrix)");
          
    // Add a Python-friendly version of the main function
    m.def("solve_graph_coloring", [](const Matrix& adj_matrix, size_t num_colors) {
        std::cout << "Running DSB for graph coloring with " << num_colors << " colors...\n";
        
        auto result = gcp_solver(
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
        
        // Return coloring, energy history, and final energy
        return py::make_tuple(best_coloring, energy_history, final_energy);
    }, py::arg("adj_matrix"), py::arg("num_colors"),
       "Solves the graph coloring problem and returns the results");
}