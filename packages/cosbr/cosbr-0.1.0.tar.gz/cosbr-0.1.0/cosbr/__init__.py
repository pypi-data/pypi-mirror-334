"""
COSBr: Combinatorial Optimization Solver using Bifurcation
==================================================

This package provides a graph coloring problem solver using 
Discrete Simulated Bifurcation algorithm.
"""

from .gcp_module import (
    graph_coloring_energy,
    discrete_simulated_bifurcation,
    gcp_solver,
    q_to_coloring,
    solve_graph_coloring
)

__version__ = '0.1.0'
__all__ = [
    'graph_coloring_energy',
    'discrete_simulated_bifurcation',
    'gcp_solver',
    'q_to_coloring',
    'solve_graph_coloring'
]