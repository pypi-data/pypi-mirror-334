use pyo3::prelude::*;
use pyo3::types::PyDelta;
use std::time::Duration;

#[pyfunction]
pub fn muskingum_routing(
    py: Python,
    inflow: Vec<f64>,
    k: Py<PyDelta>,
    x: f64,
    time_step: Py<PyDelta>,
    sub_reaches: i64,
    initial_outflow: f64,
) -> PyResult<Vec<f64>> {
    if !(0.0..=0.5).contains(&x) {
        py.import("warnings")?.call_method1(
            "warn",
            ("`x` is outside the recommended range [0.0, 0.5].",),
        )?;
    }
    let time_step_duration: Duration = time_step.extract(py)?;
    let dt_s: f64 = time_step_duration.as_secs_f64();

    let k_duration: Duration = k.extract(py)?;
    let k_s: f64 = k_duration.as_secs_f64() / sub_reaches as f64;

    let mut outflow = muskingum_routing_rs(inflow, dt_s, k_s, x, Some(initial_outflow));
    for _ in 1..sub_reaches {
        outflow = muskingum_routing_rs(outflow, dt_s, k_s, x, None)
    }

    Ok(outflow)
}

fn muskingum_routing_rs(
    q_in: Vec<f64>,
    dt: f64,
    k: f64,
    x: f64,
    initial_outflow: Option<f64>,
) -> Vec<f64> {
    let initial_outflow = initial_outflow.unwrap_or(q_in[0]);
    let den: f64 = 2.0 * k * (1.0 - x) + dt;
    let c0 = (dt - 2.0 * k * x) / den;
    let c1 = (dt + 2.0 * k * x) / den;
    let c2 = (2.0 * k * (1.0 - x) - dt) / den;

    let mut outflow: Vec<f64> = Vec::with_capacity(q_in.len());
    let mut previous_outflow: f64 = initial_outflow;
    let mut previous_inflow: f64 = q_in[0];

    outflow.push(initial_outflow);

    for &current_inflow in q_in.iter().skip(1) {
        let current_outflow = c0 * current_inflow + c1 * previous_inflow + c2 * previous_outflow;
        outflow.push(current_outflow);
        previous_outflow = current_outflow;
        previous_inflow = current_inflow;
    }

    outflow
}
