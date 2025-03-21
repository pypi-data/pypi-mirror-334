//! Complex number implementation.

use std::{
    ops::{
        Add,
        Sub,
        Mul,
        Div,
    },
};

use pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Copy, PartialEq, Debug)]
pub struct Complex {
    #[pyo3(get)]
    pub real: f64,

    #[pyo3(get)]
    pub imag: f64,
}

#[pymethods]
impl Complex {
    #[new]
    pub fn new(real: f64, imag: f64) -> Self {
        Self {
            real,
            imag,
        }
    }

    #[staticmethod]
    pub fn zero() -> Self {
        Self {
            real: 0.0,
            imag: 0.0,
        }
    }

    pub fn is_zero(&self) -> bool {
        self.real == 0.0 && self.imag == 0.0
    }

    #[pyo3(name = "__abs__")]
    /// Magnitude of this complex number.
    pub fn abs(&self) -> f64 {
        (self.real.powi(2) + self.imag.powi(2)).sqrt()
    }

    /// Argument of this complex number in *degrees*.
    pub fn arg(&self) -> f64 {
        self.imag.atan2(self.real).to_degrees()
    }

    #[pyo3(name = "__str__")]
    pub fn to_string(&self) -> String {
        format!("({:.6} + {:.6}j)", self.real, self.imag)
    }

    #[pyo3(name = "__repr__")]
    pub fn pyrepr(&self) -> String {
        format!("Complex({:.6}, {:.6})", self.real, self.imag)
    }

    #[pyo3(name = "__add__")]
    pub fn add(&self, other: Self) -> Self {
        *self + other
    }
    
    #[pyo3(name = "__sub__")]
    pub fn sub(&self, other: Self) -> Self {
        *self - other
    }

    #[pyo3(name = "__mul__")]
    pub fn mul(&self, other: Self) -> Self {
        *self * other
    }

    #[pyo3(name = "__truediv__")]
    pub fn div(&self, other: Self) -> Self {
        *self / other
    }
}

impl Add<Complex> for Complex {
    type Output = Complex;

    fn add(self, other: Complex) -> Self::Output {
        Self {
            real: self.real + other.real,
            imag: self.imag + other.imag,
        }
    }
}

impl Sub<Complex> for Complex {
    type Output = Complex;

    fn sub(self, other: Complex) -> Self::Output {
        Self {
            real: self.real - other.real,
            imag: self.imag - other.imag,
        }
    }
}

impl Mul<Complex> for Complex {
    type Output = Complex;

    fn mul(self, other: Complex) -> Self::Output {
        Self {
            real: self.real * other.real - self.imag * other.imag,
            imag: self.real * other.imag + self.imag * other.real,
        }
    }
}

impl Div<Complex> for Complex {
    type Output = Complex;

    fn div(self, other: Complex) -> Self::Output {
        Self {
            real: (self.real * other.real + self.imag * other.imag) / (other.real.powi(2) + other.imag.powi(2)),
            imag: (self.imag * other.real - self.real * other.imag) / (other.real.powi(2) + other.imag.powi(2)),
        }
    }
}