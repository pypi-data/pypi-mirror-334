//! Main library for the AutoControl controller design utility.

mod complex;
mod lead_lag;
mod pd;

use pyo3::prelude::*;

use complex::Complex;

/// Phase condition tolerance (degrees).
pub const TOLERANCE: f64 = 1.0E-3;

#[pyclass]
#[derive(Clone)]
pub struct System {
    #[pyo3(get, set)]
    /// Gain multiplier.
    pub gain: f64,

    #[pyo3(get, set)]
    /// Open-loop zeros.
    pub zeros: Vec<Complex>,

    #[pyo3(get, set)]
    /// Open-loop poles.
    pub poles: Vec<Complex>,
}

#[pymethods]
impl System {
    #[new]
    pub fn new(gain: f64, zeros: Vec<Complex>, poles: Vec<Complex>) -> Self {
        Self {
            gain,
            zeros,
            poles,
        }
    }

    pub fn add_zero(&mut self, zero: Complex) {
        self.zeros.push(zero);
    }

    pub fn add_pole(&mut self, pole: Complex) {
        self.poles.push(pole);
    }

    pub fn add_free_integrator(&mut self) {
        self.poles.push(Complex::zero());
    }

    /// Evaluate the transfer function at a given `s`.
    pub fn eval(&self, s: Complex) -> Complex {
        // Initialize result
        let mut result = Complex::new(self.gain, 0.0);

        // Multiply for each zero
        for zero in &self.zeros {
            result = result * (s - *zero);
        }

        // Divide for each pole
        for pole in &self.poles {
            result = result / (s - *pole);
        }

        result
    }

    #[getter]
    /// Evaluate system type.
    pub fn get_system_type(&self) -> usize {
        let mut result = 0;

        for pole in &self.poles {
            if pole.is_zero() {
                result += 1;
            }
        }

        result
    }

    #[getter]
    /// Evaluate system constant.
    pub fn get_system_constant(&self) -> f64 {
        // Initialize result
        let mut result = Complex::new(self.gain, 0.0);

        // Multiply each zero
        for zero in &self.zeros {
            result = result * *zero;
        }

        // Divide each pole
        for pole in &self.poles {
            if !pole.is_zero() {
                result = result / *pole;
            }
        }

        result.real
    }

    /// Compute the transfer function magnitude at a given `s`.
    pub fn magnitude(&self, s: Complex) -> f64 {
        self.eval(s).abs()
    }

    /// Compute the transfer function phase at a given `s`.
    /// 
    /// Note that this returns a phase in *degrees*.
    pub fn phase(&self, s: Complex) -> f64 {
        self.eval(s).arg()
    }

    /// Compose two systems into a new system.
    pub fn compose(&self, other: &Self) -> Self {
        let mut poles = self.poles.clone();
        let mut zeros = self.zeros.clone();

        poles.extend(&other.poles);
        zeros.extend(&other.zeros);

        Self {
            gain: self.gain * other.gain,
            poles,
            zeros,
        }
    }

    /// Design a PD controller for this system, given a specification.
    pub fn pd_control(&self, spec: ControllerSpec) -> Self {
        pd::design_pd_controller(self, spec)
    }

    /// Design a lead/lag controller for this system, given a specification.
    pub fn lead_lag_control(&self, spec: ControllerSpec) -> Self {
        lead_lag::design_lead_lag_controller(self, spec)
    }
}

#[pyclass]
#[derive(Clone, Copy)]
/// Controller design specification.
pub struct ControllerSpec {
    #[pyo3(get, set)]
    /// Desired system type.
    pub system_type: Option<usize>,

    #[pyo3(get, set)]
    /// Desired tracking error (based on system type).
    pub tracking_error: Option<f64>,

    #[pyo3(get, set)]
    /// Target pole.
    pub target: Complex,

    #[pyo3(get, set)]
    /// Pole/zero ratio in lead controller design.
    pub pz_ratio: f64,

    #[pyo3(get, set)]
    /// Zero/target ratio in lag controller design.
    pub zt_ratio: f64,

    #[pyo3(get, set)]
    /// Must this controller have a matched number of poles and zeros?
    pub balanced: bool,
}

#[pymethods]
impl ControllerSpec {
    #[new]
    /// Construct a new, empty controller specification.
    pub fn new(target: Complex) -> Self {
        Self {
            system_type: None,
            tracking_error: None,
            target,
            pz_ratio: 10.0,
            zt_ratio: 10.0,
            balanced: false,
        }
    }

    #[getter]
    /// Get the target system constant.
    pub fn get_system_constant(&self) -> Option<f64> {
        if let Some (e) = self.tracking_error {
            if let Some (t) = self.system_type {
                match t {
                    0 => Some(1.0 / e - 1.0),
                    _ => Some(1.0 / e),
                }
            } else {
                None
            }
        } else {
            None
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn autoctrl(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<System>()?;
    m.add_class::<Complex>()?;
    m.add_class::<ControllerSpec>()?;

    Ok(())
}
