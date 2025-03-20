import pathlib as pl
import pickle

import numpy as np
import xarray as xr

data_dir = pl.Path(".")

with open(data_dir / "starfit_outputs.pickle", "rb") as handle:
    ans_dict = pickle.load(handle)

min_year = 1995
max_year = 2001


def sub_time_mean(ser):
    ser_sub = ser[(ser.index.year >= min_year) & (ser.index.year <= max_year)]
    # print(len(ser_sub))
    return ser_sub.mean()


lake_storage = np.array([sub_time_mean(ls) for ls in ans_dict["Ssim_list"]])
# print(len(np.where(np.isnan(lake_storage))[0]))
lake_release = np.array([sub_time_mean(ls) for ls in ans_dict["Rsim_list"]])
lake_spill = np.array([sub_time_mean(ls) for ls in ans_dict["SPILLsim_list"]])
grand_ids = ans_dict["grand_ids"]

assert len(lake_storage) == len(lake_release)
assert len(lake_storage) == len(lake_spill)
assert len(lake_storage) == len(grand_ids)

ds = xr.Dataset(
    data_vars=dict(
        lake_storage_mean=(["grand_id"], lake_storage),
        lake_release_mean=(["grand_id"], lake_release),
        lake_spill_mean=(["grand_id"], lake_spill),
    ),
    coords=dict(
        grand_id=("grand_id", grand_ids),
    ),
    attrs=dict(description="Mean starfit variables over original data"),
)

ds.to_netcdf("./starfit_mean_output.nc")
# must manually copy to pywatershed/test_data/starfit
