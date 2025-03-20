import pathlib as pl

import numpy
import pandas as pd
import pynhm

#

grandid_to_segid_file = pl.Path("./grandid_to_segid.csv")
grand_to_seg = pd.read_csv(grandid_to_segid_file)
grand_to_seg = grand_to_seg.rename(
    columns={"GRanD ID": "grand_id", "NHM seg_id": "nhm_seg"}
)

drb_param_file = pl.Path("../../../test_data/drb_2yr/myparam.param")
ucb_param_file = pl.Path("../../../test_data/ucb_2yr/myparam.param")

drb_params = pynhm.PrmsParameters.load(drb_param_file)
ucb_params = pynhm.PrmsParameters.load(ucb_param_file)


drb_segids = drb_params.parameters["nhm_seg"]
ucb_segids = ucb_params.parameters["nhm_seg"]

grand_to_seg_drb = grand_to_seg[grand_to_seg["nhm_seg"].isin(drb_segids)]
grand_to_seg_ucb = grand_to_seg[grand_to_seg["nhm_seg"].isin(ucb_segids)]

drb_ds = grand_to_seg_drb.set_index("grand_id").to_xarray()
ucb_ds = grand_to_seg_ucb.set_index("grand_id").to_xarray()

drb_ds.to_netcdf("grand_seg_ids_drb.nc")
ucb_ds.to_netcdf("grand_seg_ids_ucb.nc")
