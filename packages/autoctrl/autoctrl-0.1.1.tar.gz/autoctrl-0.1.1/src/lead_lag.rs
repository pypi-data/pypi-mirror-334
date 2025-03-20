//! Lead-lag controller design routine.

use crate::{
    Complex,
    ControllerSpec,
    System,
    TOLERANCE,
};

/// Maximum phase added per lead controller (degrees).
pub const LEAD_PHASE: f64 = 75.0;

pub fn design_lead_lag_controller(plant: &System, spec: ControllerSpec) -> System {
    // Print headers
    println!("AutoControl\n===========\n");

    println!("LEAD/LAG CONTROLLER DESIGN\n");

    ////////////////////////////////
    // STEP 1: DESIGN SYSTEM TYPE //
    ////////////////////////////////

    println!("SYSTEM TYPE ANALYSIS\n");

    // Resultant controller
    let mut free_integrator_controller = System::new(1.0, Vec::new(), Vec::new());

    println!("\tOpen-loop system is Type {}\n", plant.get_system_type());

    // Is this system deficient in free integrators?
    let type_diff = if let Some (t) = spec.system_type {
        t - plant.get_system_type()
    } else {
        println!("\tDesired system type not specified, moving on\n");

        0
    };

    // Add zero(s) with free integrator(s), if specified
    let zero = Complex::new(spec.target.real, 0.0);

    // Add free integrator(s), if necessary
    if type_diff > 0 {
        println!("\t\tADDING {} FREE INTEGRATOR(S)\n", type_diff);

        if spec.balanced {
            println!("\t\tBalancing controller by ADDING {} ZERO(S) AT LOCATION {}\n", type_diff, zero.to_string());
        }

        for _ in 0..type_diff {
            free_integrator_controller.add_free_integrator();

            if spec.balanced {
                free_integrator_controller.add_zero(zero);
            }
        }
    }
    
    println!("\tSystem is of desired type, moving on\n");

    ///////////////////////////////////
    // STEP 2: CHECK PHASE CONDITION //
    ///////////////////////////////////

    println!("PHASE CONDITION ANALYSIS\n");

    // Resultant controller
    let mut original_lead_controller = System::new(1.0, Vec::new(), Vec::new());

    let current_phase = plant.compose(&free_integrator_controller).phase(spec.target);

    println!("\tPhase of target pole is {:.6} degrees\n", current_phase);

    let added_phase = 180.0 - current_phase;

    if added_phase.abs() > TOLERANCE {
        // Decide on number of lead controllers
        let n_lead = (added_phase / LEAD_PHASE).ceil() as usize;

        // Phase per controller
        let lead_ctrl_phase = added_phase / (n_lead as f64);

        println!("\tADDING {} LEAD CONTROLLER(S) to increase phase by {:.6} degrees per controller\n", n_lead, lead_ctrl_phase);

        // Quadratic coefficients
        let a = spec.pz_ratio * lead_ctrl_phase.to_radians().tan();
        let b = -(spec.pz_ratio + 1.0) * (-spec.target.real) * lead_ctrl_phase.to_radians().tan() - (spec.pz_ratio - 1.0) * spec.target.imag;
        let c = spec.target.abs().powi(2) * lead_ctrl_phase.to_radians().tan();

        // Place lead zero
        let z = -b/2.0/a + (b.powi(2) - 4.0*a*c).sqrt()/2.0/a;

        // Add zero and pole to controller
        let zero = Complex::new(-z, 0.0);
        let pole = Complex::new(-spec.pz_ratio*z, 0.0);
        
        for _ in 0..n_lead {
            original_lead_controller.add_zero(zero);
            original_lead_controller.add_pole(pole);
        }

        println!("\t\tSelecting LEAD CONTROLLER ZERO LOCATION of {}\n", zero.to_string());

        println!("\t\tSelecting LEAD CONTROLLER POLE LOCATION of {}\n", pole.to_string());

        let current_phase = plant.compose(&free_integrator_controller)
            .compose(&original_lead_controller)
            .phase(spec.target);

        println!("\tPhase condition satisfied at {:.6} degrees, moving on\n", current_phase);
    } else {
        println!("\tPhase condition satisfied, moving on\n");
    }

    //////////////////////////////////////////
    // STEP 3: IMPROVE TRACKING PERFORMANCE //
    //////////////////////////////////////////

    println!("TRACKING PERFORMANCE ANALYSIS\n");

    // Resultant controller
    let mut lag_controller = System::new(1.0, Vec::new(), Vec::new());
    let mut lag_control = false;

    if let Some (target_k) = spec.get_system_constant() {
        // Get the system constant
        let current_k = plant.compose(&free_integrator_controller)
            .compose(&original_lead_controller)
            .get_system_constant();

        println!("\tCurrent system constant is {:.4}\n", current_k);

        // Check tracking performance
        if current_k > target_k {
            println!("\tTracking performance is satisfactory, moving on\n");
        } else {
            println!("\tTracking performance needs improvement, ADDING LAG CONTROLLER\n");

            // Place zero based on system dynamics
            let z = spec.target.real / spec.zt_ratio;

            // Place pole based on needed system constant
            let p = current_k * z / target_k;

            // Add pole and zero to controller
            let zero = Complex::new(-z, 0.0);
            let pole = Complex::new(-p, 0.0);
            lag_controller.add_zero(zero);
            lag_controller.add_pole(pole);

            println!("\t\tSelecting LAG CONTROLLER ZERO LOCATION of {}\n", zero.to_string());

            println!("\t\tSelecting LAG CONTROLLER POLE LOCATION of {}\n", pole.to_string());
        }

        lag_control = true;
    } else {
        println!("\tNo tracking performance specified, moving on\n");
    };

    ////////////////////////////////////
    // STEP 4: REPAIR PHASE CONDITION //
    ////////////////////////////////////

    println!("PHASE CONDITION REPAIR\n");

    // Resultant controller
    let mut new_lead_controller = System::new(1.0, Vec::new(), Vec::new());

    let current_phase = plant.compose(&free_integrator_controller)
        .compose(&lag_controller)
        .phase(spec.target);

    println!("\tPhase of target pole (excluding lead control) is {:.6} degrees\n", current_phase);

    let added_phase = 180.0 - current_phase;

    if lag_control && added_phase.abs() > TOLERANCE {
        // Decide on number of lead controllers
        let n_lead = (added_phase / LEAD_PHASE).ceil() as usize;

        // Phase per controller
        let lead_ctrl_phase = added_phase / (n_lead as f64);

        println!("\tADDING {} NEW LEAD CONTROLLER(S) to increase phase by {:.6} degrees per controller\n", n_lead, lead_ctrl_phase);

        // Quadratic coefficients
        let a = spec.pz_ratio * lead_ctrl_phase.to_radians().tan();
        let b = -(spec.pz_ratio + 1.0) * (-spec.target.real) * lead_ctrl_phase.to_radians().tan() - (spec.pz_ratio - 1.0) * spec.target.imag;
        let c = spec.target.abs().powi(2) * lead_ctrl_phase.to_radians().tan();

        // Place lead zero
        let z = -b/2.0/a + (b.powi(2) - 4.0*a*c).sqrt()/2.0/a;

        // Add zero and pole to controller
        let zero = Complex::new(-z, 0.0);
        let pole = Complex::new(-spec.pz_ratio*z, 0.0);
        
        for _ in 0..n_lead {
            new_lead_controller.add_zero(zero);
            new_lead_controller.add_pole(pole);
        }

        println!("\t\tSelecting NEW LEAD CONTROLLER ZERO LOCATION of {}\n", zero.to_string());

        println!("\t\tSelecting NEW LEAD CONTROLLER POLE LOCATION of {}\n", pole.to_string());

        let current_phase = plant.compose(&free_integrator_controller)
            .compose(&lag_controller)
            .compose(&new_lead_controller)
            .phase(spec.target);

        println!("\tPhase condition repaired at {:.6} degrees, moving on\n", current_phase);
    } else {
        println!("\tPhase condition repair not required, moving on\n");
    }

    /////////////////////////////////
    // STEP 5: SELECT CONTROL GAIN //
    /////////////////////////////////

    println!("CONTROL GAIN SELECTION\n");

    let mut controller = if lag_control {
        free_integrator_controller.compose(&lag_controller).compose(&new_lead_controller)
    } else {
        free_integrator_controller.compose(&original_lead_controller)
    };

    // Select control gain
    let ctrl_gain = (Complex::new(-1.0, 0.0) / plant.compose(&controller).eval(spec.target)).real;

    println!("\tSELECTED CONTROL GAIN of {:.6}\n", ctrl_gain);

    controller.gain = ctrl_gain;

    println!("Control design routine complete!\n");

    // Provide summary to user
    println!("Summary\n-------\n");
    println!("Gain : {:.6}", controller.gain);
    println!("Poles: {}", controller.poles.iter().map(|p| p.to_string()).collect::<Vec<String>>().join(", "));
    println!("Zeros: {}", controller.zeros.iter().map(|z| z.to_string()).collect::<Vec<String>>().join(", "));

    controller
}