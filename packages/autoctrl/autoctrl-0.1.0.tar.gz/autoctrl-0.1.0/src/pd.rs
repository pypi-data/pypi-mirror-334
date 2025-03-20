//! PD controller design routine.

use crate::{
    Complex,
    ControllerSpec,
    System,
    TOLERANCE,
};

pub fn design_pd_controller(plant: &System, spec: ControllerSpec) -> System {
    // Print headers
    println!("AutoControl\n===========\n");

    println!("PD CONTROLLER DESIGN\n");

    ///////////////////////////////////
    // STEP 1: CHECK PHASE CONDITION //
    ///////////////////////////////////

    println!("PHASE CONDITION ANALYSIS\n");

    // Resultant controller
    let mut pd_controller = System::new(1.0, Vec::new(), Vec::new());

    let current_phase = plant.phase(spec.target);

    println!("\tPhase of target pole is {:.6} degrees\n", current_phase);

    let added_phase = 180.0 - current_phase;

    if added_phase.abs() > TOLERANCE {
        // Place PD zero
        let z = -spec.target.real + spec.target.imag / added_phase.to_radians().tan();

        println!("\tADDING ZERO to increase phase by {:.6} degrees\n", added_phase);

        // Add zero to controller
        let zero = Complex::new(-z, 0.0);
        pd_controller.add_zero(zero);

        if z < 0.0 {
            println!("\tPhase condition requires zero placement at location {} but zero cannot be in RHP\n", zero.to_string());
            println!("\tPD control NOT POSSIBLE for this system, QUITTING\n");
            return System::new(1.0, Vec::new(), Vec::new());
        }

        println!("\t\tSelecting PD CONTROLLER ZERO LOCATION of {}\n", zero.to_string());

        let current_phase = plant.compose(&pd_controller)
            .phase(spec.target);

        println!("\tPhase condition satisfied at {:.6} degrees, moving on\n", current_phase);
    } else {
        println!("\tPhase condition satisfied, moving on\n");
    }

    /////////////////////////////////
    // STEP 2: SELECT CONTROL GAIN //
    /////////////////////////////////

    println!("CONTROL GAIN SELECTION\n");

    // Select control gain
    let ctrl_gain = (Complex::new(-1.0, 0.0) / plant.compose(&pd_controller).eval(spec.target)).real;

    println!("\tSELECTED CONTROL GAIN of {:.6}\n", ctrl_gain);

    pd_controller.gain = ctrl_gain;

    println!("Control design routine complete!\n");

    // Provide summary to user
    println!("Summary\n-------\n");
    println!("Gain : {:.6}", pd_controller.gain);
    println!("Poles: {}", pd_controller.poles.iter().map(|p| p.to_string()).collect::<Vec<String>>().join(", "));
    println!("Zeros: {}", pd_controller.zeros.iter().map(|z| z.to_string()).collect::<Vec<String>>().join(", "));

    pd_controller
}