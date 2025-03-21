"""
splinaltap - Keyframe interpolation and expression evaluation that goes to eleven!
"""

from .knot import Knot
from .spline import Spline
from .spline_group import SplineGroup
from .solver import SplineSolver, KeyframeSolver
from .expression import ExpressionEvaluator
from .visualization import plot_interpolation_comparison, plot_single_interpolation

# For backward compatibility
Channel = Spline
Keyframe = Knot

__version__ = "1.0.0"
__all__ = [
    "SplineSolver",
    "KeyframeSolver",  # For backward compatibility
    "SplineGroup",
    "Spline", 
    "Knot",
    "Channel",  # For backward compatibility 
    "Keyframe",  # For backward compatibility
    "ExpressionEvaluator",
    "plot_interpolation_comparison", 
    "plot_single_interpolation",
]