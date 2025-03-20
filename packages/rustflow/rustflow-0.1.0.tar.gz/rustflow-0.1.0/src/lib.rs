use pyo3::prelude::*;
pub mod reach_routing;

#[pymodule]
fn rustflow(m: &Bound<'_, PyModule>) -> PyResult<()> {
    let reach_module = PyModule::new(m.py(), "reach")?;

    // Expose the contents of `reach_routing/mod.rs` directly here
    reach_routing::init_reach(&reach_module)?;

    m.add_submodule(&reach_module)?;

    Ok(())
}
