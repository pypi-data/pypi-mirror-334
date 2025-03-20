# Rustflow: High-Performance Hydrological Routing in Rust

Rustflow is a hydrological routing library designed for **speed and efficiency**. It leverages the power of the Rust programming language to provide fast and reliable computations for modeling water flow through river reaches. The core functionality is implemented in Rust, with a Python interface for easy integration into existing hydrological workflows.

## Key Features

- **High Performance:** Rust's performance characteristics (speed, memory safety, concurrency) provide significant advantages for computationally intensive hydrological simulations.
- **Python Interface:** A user-friendly Python API simplifies integration with popular scientific computing libraries like NumPy and Pandas.
- **Well-Documented:** Comprehensive docstrings and examples in both Rust and Python make it easy to use and extend.

## Installation

### Python Package

Install the `rustflow` Python package using pip:

```bash
# TODO
pip install rustflow 
```

### Building from Source

1.  **Rust:** Ensure you have Rust and Cargo installed. If not, follow the instructions at https://www.rust-lang.org/tools/install.
2.  **Clone:** Clone this repository:

    ```bash
    git clone https://github.com/darshanbaral/rustflow.git
    cd rustflow
    ```

3.  **Build:** Build the Rust library and the Python bindings using `maturin`

    ```bash
     # Install maturin if you dont already have it.
    pip install maturin
    maturin develop
    ```

    This will build the rust code, and install the python package.
