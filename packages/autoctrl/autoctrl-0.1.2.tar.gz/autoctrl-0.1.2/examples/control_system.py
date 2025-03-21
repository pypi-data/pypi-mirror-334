# AutoControl

from autoctrl import Complex, System, ControllerSpec

# Define open-loop poles
s1 = Complex(-2, 0)
s2 = Complex(-4, 0)

# Define target pole
target = Complex(-5.6, 5.713)

# Create system
g = System(
    8,          # Scalar multiplier
    [],         # No zeros
    [s1, s2],   # Two poles
)

# Controller specification
spec = ControllerSpec(target)
spec.system_type = 1
spec.balanced = True

# Design a lead/lag controller
g.lead_lag_control(spec)
