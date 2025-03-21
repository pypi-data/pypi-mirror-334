# AutoControl

from autoctrl import Complex, System, ControllerSpec

# Define open-loop poles
s1 = Complex(0, 2)
s2 = Complex(0, -2)

# Define target pole
target = Complex(-4, 2)

# Create system
g = System(
    1,          # Scalar multiplier
    [],         # No zeros
    [s1, s2],   # Two poles
)

# Controller specification
spec = ControllerSpec(target)

# Design a PD controller
g.pd_control(spec)
