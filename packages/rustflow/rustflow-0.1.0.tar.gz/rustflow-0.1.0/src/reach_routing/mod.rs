use pyo3::prelude::*;

pub mod muskingum;

#[pymodule]
pub fn init_reach(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(muskingum::muskingum_routing, m)?)?;
    Ok(())
}
