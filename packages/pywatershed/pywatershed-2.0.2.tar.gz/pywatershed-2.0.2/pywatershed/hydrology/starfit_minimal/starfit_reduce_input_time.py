import numpy as np
import xarray as xr

inflows = xr.open_dataset("./lake_inflow.nc")

inflows1 = inflows.where(
    (
        (inflows.time >= np.datetime64("1995-01-01"))
        & (inflows.time <= np.datetime64("2001-12-31"))
    ),
    drop=True,
)

inflows1.to_netcdf("../../../test_data/starfit/lake_inflow.nc")
