from datetime import timedelta
from typing import Optional

from ..rustflow import reach


# Expose Rust functions
def muskingum_routing(
    inflow: list[float],
    k: timedelta,
    x: float,
    time_step: timedelta,
    sub_reaches: Optional[int] = 1,
    initial_outflow: Optional[float] = None,
):
    """
    Performs Muskingum routing on a given inflow hydrograph.

    The Muskingum method is a hydrological routing technique used to predict
    the downstream hydrograph given an upstream hydrograph. It is based on
    the principles of conservation of mass and a simplified representation of
    storage within the channel reach.

    Args:
        inflow (list[float]): A list of inflow discharges (e.g., in cfs or cms)
            at the upstream end of the reach. The list should represent a
            time series of flow values.
        k (timedelta): The storage time constant of the reach (e.g., in hours).
            This parameter represents the travel time through the reach.
        x (float): The weighting factor for the inflow and outflow, typically
            between 0.0 and 0.5. `x=0` corresponds to reservoir routing
            while `x=0.5` would be kinematic routing. Values closer to 0
            indicate more prism storage, and values closer  to 0.5 indicate
            more wedge storage.
        time_step (timedelta): The time step used for the inflow hydrograph
            (e.g., in minutes or hours). This determines the time interval
            between consecutive inflow values.
        sub_reaches (Optional[int], optional): The number of sub-reaches to
            divide the reach into. Dividing the reach increases accuracy at the cost of computation time. Defaults to 1.
        initial_outflow (Optional[float], optional): The initial outflow
            discharge at the start of the simulation. If not provided, it
            defaults to the first inflow value.

    Returns:
        list[float]: A list of outflow discharges (in the same units as the
            inflow) at the downstream end of the reach, representing the routed
            hydrograph.

    Raises:
        TypeError: If `inflow` is not a list or a compatible iterable.
        TypeError: if `k`, `time_step` is not a timedelta

    Example:
        ```python
        from datetime import timedelta
        from rustflow.reach import muskingum_routing

        inflow = [10.0, 15.0, 25.0, 40.0, 30.0, 20.0, 15.0, 10.0]  # cfs
        k = timedelta(hours=2)
        x = 0.2
        time_step = timedelta(minutes=15)
        sub_reaches = 4
        outflow = muskingum_routing(inflow, k, x, time_step, sub_reaches)
        print(outflow)
        ```
    """

    if not isinstance(inflow, list):
        inflow = list(inflow)

    if initial_outflow is None:
        initial_outflow = inflow[0]

    return reach.muskingum_routing(
        inflow, k, x, time_step, sub_reaches, initial_outflow
    )
