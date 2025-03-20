from datetime import timedelta

import pandas
from rustflow.reach import muskingum_routing as mkr

if __name__ == "__main__":
    df = pandas.read_csv("./data/gage_flow_data.csv", index_col=0, parse_dates=True)
    inflow = df["Flow (cfs)"]
    dt = timedelta(minutes=15)
    # inflow = inflow.reindex(pandas.date_range(inflow.index[0], inflow.index[-1], freq=dt)).interpolate()
    outflow = mkr(
        inflow=inflow,
        k=timedelta(hours=1),
        x=0.25,
        time_step=dt,
        sub_reaches=12,
    )
    o_df = pandas.DataFrame({"flow": outflow}, index=inflow.index)
    # o_df = o_df.loc[df.index]
    o_df.to_csv("./data/outflow.csv")
