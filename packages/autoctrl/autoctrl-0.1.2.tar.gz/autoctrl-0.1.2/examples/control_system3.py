# AutoControl

from autoctrl import Complex, System, ControllerSpec

# Define open-loop poles
s1 = Complex(1, 0)
s2 = Complex(-2, 0)
s3 = Complex(-20, 0)

# Define target pole
target = Complex(-2.998, 4.001)

# Create system
g = System(
    5,                  # Scalar multiplier
    [],                 # No zeros
    [s1, s2, s3],       # Three poles
)

# Controller specification
spec = ControllerSpec(target)

# Design a PD controller
g.pd_control(spec)
