import pickle

import epiweeks as ew
import numpy as np
import pandas as pd
import xarray as xr


# restrict epiweek to [1, 52]
def dt_to_epiweek(dt):
    epiweek = np.minimum(float(ew.Week.fromdate(dt).week), 52.0)
    return epiweek


# slightly modified from the STARFIT implementation in the MOSART-WM model: https://github.com/IMMM-SFA/mosartwmpy/blob/main/mosartwmpy/reservoirs/istarf.py
def compute_istarf_release(
    epiweek,
    reservoir_id,
    upper_min,
    upper_max,
    upper_alpha,
    upper_beta,
    upper_mu,
    lower_min,
    lower_max,
    lower_alpha,
    lower_beta,
    lower_mu,
    release_min_parameter,
    release_max_parameter,
    release_alpha_one,
    release_alpha_two,
    release_beta_one,
    release_beta_two,
    release_p_one,
    release_p_two,
    release_c,
    capacity_MCM,
    inflow_mean,
    storage_MCM,
    inflow,
):
    storage = storage_MCM * 1.0e6  # input is in MCM, this function needs m^3
    capacity = capacity_MCM * 1.0e6  # input is in MCM, this function needs m^3

    omega = 1.0 / 52.0

    if np.isfinite(reservoir_id):
        max_normal = np.minimum(
            upper_max,
            np.maximum(
                upper_min,
                upper_mu
                + upper_alpha * np.sin(2.0 * np.pi * omega * epiweek)
                + upper_beta * np.cos(2.0 * np.pi * omega * epiweek),
            ),
        )

        min_normal = np.minimum(
            lower_max,
            np.maximum(
                lower_min,
                lower_mu
                + lower_alpha * np.sin(2.0 * np.pi * omega * epiweek)
                + lower_beta * np.cos(2.0 * np.pi * omega * epiweek),
            ),
        )

        # TODO could make a better forecast?
        forecasted_weekly_volume = (
            7.0 * inflow * 24.0 * 60.0 * 60.0
        )  # why not use cumulative volume for the current epiweek, and only extrapolate for the remainder of the week?
        mean_weekly_volume = 7.0 * inflow_mean * 24.0 * 60.0 * 60.0

        standardized_inflow = (
            forecasted_weekly_volume / mean_weekly_volume
        ) - 1.0

        standardized_weekly_release = (
            release_alpha_one * np.sin(2.0 * np.pi * omega * epiweek)
            + release_alpha_two * np.sin(4.0 * np.pi * omega * epiweek)
            + release_beta_one * np.cos(2.0 * np.pi * omega * epiweek)
            + release_beta_two * np.cos(4.0 * np.pi * omega * epiweek)
        )

        release_min = mean_weekly_volume * (1 + release_min_parameter) / 7.0
        release_max = mean_weekly_volume * (1 + release_max_parameter) / 7.0

        availability_status = (100.0 * storage / capacity - min_normal) / (
            max_normal - min_normal
        )

        # above normal
        if availability_status > 1:
            release = (
                storage
                - (capacity * max_normal / 100.0)
                + forecasted_weekly_volume
            ) / 7.0

        # below normal
        elif availability_status < 0:
            release = (
                storage
                - (capacity * min_normal / 100.0)
                + forecasted_weekly_volume
            ) / 7.0  # NK: The first part of this sum will be negative.

        # within normal
        else:
            release = (
                mean_weekly_volume
                * (
                    1
                    + (
                        standardized_weekly_release
                        + release_c
                        + release_p_one * availability_status
                        + release_p_two * standardized_inflow
                    )
                )
            ) / 7.0

        # enforce boundaries on release
        if release < release_min:
            # shouldn't release less than min
            release = release_min
        elif release > release_max:
            # shouldn't release more than max
            release = release_max

        # storage update and boundaries are enforced during the regulation step
        return release, availability_status


# load GRanD data
grand = pd.read_csv("grand_dams.csv", index_col="GRAND_ID")
# export to netcdf
# grand_ds = grand.to_xarray()
# grand_ds.to_netcdf('grand_dams.nc')

# load pre-assembled input data
with open("starfit_inputs.pickle", "rb") as handle:
    list_dict = pickle.load(handle)
dtbeg_list = list_dict["dtbeg_list"]  # start dates of continuous ResOpsUS obs
dtend_list = list_dict["dtend_list"]  # end dates of continuous ResOpsUS obs
I_list = list_dict[
    "I_list"
]  # reservoir inflows (NHM outputs at corresponding stream segments)
I_mean = list_dict["I_mean"]  # mean inflows (from ResOpsUS)
Sobs_list = list_dict["Sobs_list"]  # observed storages (from ResOpsUS)
grand_ids = list_dict[
    "grand_ids"
]  # ids correspoding to other data in this pickle file, from GRanD reservoir db
Ndams = len(grand_ids)

# GrandIds to netcdf file
# grand_ids_ds = xr.DataArray(
#     data=grand_ids,
#     dims=["grand_id"],
#     attrs=dict(description="IDs in GRanD Dams Dataset to model")
# ).rename('grand_id').to_dataset()
# grand_ids_ds.to_netcdf('domain_grand_ids.nc')

# # NHM Inflows to netcdf
# inflow_df = pd.concat([dd for dd in I_list], axis=1, join="outer")
# inflow_df.columns = inflow_df.columns.astype("int64")
# inflow_df = inflow_df.stack()
# inflow_df.index.names = ["time", "grand_id"]
# inflow_ds = inflow_df.to_xarray().rename("lake_inflow").to_dataset()
# inflow_ds.to_netcdf("lake_inflow.nc")

# # # ResOpsUS data to netcdf
# resops_df = pd.concat([dd for dd in Sobs_list], axis=1, join="outer")
# resops_df.columns = resops_df.columns.astype("int64")
# resops_df = resops_df.stack()
# resops_df.index.names = [
#     "time",
#     "grand_id",
# ]  # make consistent with inflow_df/ds
# resops_ds = resops_df.to_xarray().rename("storage_obs").to_dataset()

# res_vars_dict = {
#     "start_time": dtbeg_list,
#     "end_time": dtend_list,
#     "inflow_mean": I_mean,
# }
# for kk, vv in res_vars_dict.items():
#     if kk == "inflow_mean":
#         assert (vv.index.values.astype("int64") == resops_ds.grand_id).all()
#         val = vv.values
#     else:
#         val = np.array([np.datetime64(ii) for ii in vv])

#     resops_ds[kk] = xr.DataArray(data=val, dims=["grand_id"])

# # storage_obs is only used for initial storage.
# # can just pull that out
# initial_storage = np.zeros(len(resops_ds.grand_id)) * np.nan
# for ii, gi in enumerate(resops_ds.grand_id):
#     initial_storage[ii] = resops_ds.storage_obs.loc[
#         dict(grand_id=gi, time=resops_ds.start_time[ii])
#     ]

# resops_ds["initial_storage"] = xr.DataArray(
#     data=initial_storage, dims=["grand_id"]
# )
# resops_ds.to_netcdf("ResOpsUS.nc")


# load ISTARF-CONUS params
istarf = pd.read_csv("starfit/ISTARF-CONUS.csv", index_col="GRanD_ID")
# export to netcdf
# ds_istarf = istarf.to_xarray()
# ds_istarf.to_netcdf('starfit/ISTARF-CONUS.nc')

param_list = [
    "NORhi_min",
    "NORhi_max",
    "NORhi_alpha",
    "NORhi_beta",
    "NORhi_mu",
    "NORlo_min",
    "NORlo_max",
    "NORlo_alpha",
    "NORlo_beta",
    "NORlo_mu",
    "Release_min",
    "Release_max",
    "Release_alpha1",
    "Release_alpha2",
    "Release_beta1",
    "Release_beta2",
    "Release_p1",
    "Release_p2",
    "Release_c",
    "GRanD_CAP_MCM",
    "Obs_MEANFLOW_CUMECS",
]


# Run daily sim code

Rsim_list = []
SPILLsim_list = []
Ssim_list = []

# loop sites
for irun, (I, Sobs, dtbeg, dtend, grand_id) in enumerate(
    zip(I_list, Sobs_list, dtbeg_list, dtend_list, grand_ids)
):
    istarf_params = istarf.loc[grand_id, param_list]
    cap = istarf_params["GRanD_CAP_MCM"]

    if np.isnan(
        istarf_params["Obs_MEANFLOW_CUMECS"]
    ):  # was nan in cases where storage data were insufficient for storage-based fit (see TUrner et al)
        istarf_params["Obs_MEANFLOW_CUMECS"] = I_mean.iloc[
            irun
        ]  # replace with obs mean for runs (Turner used mean flow value from GRanD in these cases)

    dtend = np.min(
        [dtend, pd.Timestamp("2019-09-30 00:00:00")]
    )  # NHM output ends in WY2019

    print(
        "Simulating reservoir {} (GRanD ID = {}) in {} from {} to {}...".format(
            grand.loc[grand_id, "DAM_NAME"],
            grand_id,
            grand.loc[grand_id, "ADMIN_UNIT"],
            dtbeg.date(),
            dtend.date(),
        )
    )
    print("This is run {} of {}.\n".format(irun + 1, Ndams))

    S = Sobs.loc[dtbeg]  # initial storage value (MCM)

    # loop days
    dtind = pd.date_range(start=dtbeg, end=dtend, freq="D")
    Rsim = pd.Series(np.nan, index=dtind)
    SPILLsim = pd.Series(np.nan, index=dtind)
    Ssim = pd.Series(np.nan, index=dtind)

    for dt in dtind:
        epiweek = dt_to_epiweek(dt.date())
        inflow = I.loc[dt]
        release, availability_status = compute_istarf_release(
            epiweek, grand_id, *istarf_params, S, inflow
        )  # output in m^3/d

        release = release / (24 * 60 * 60)  # convert to m^3/s
        # update storage (dS=I-R)
        dS = (inflow - release) * 24 * 60 * 60 / 1.0e6  # conv to MCM

        # can't release more than storage + inflow. This assumes zero
        # storage = deadpool which may not be accurate, but this situation
        # rarely occurs since STARFIT releases are already designed to keep
        # storage within NOR.
        if S + dS < 0:
            release = max(release + (S + dS) * 1.0e6 / 24 / 60 / 60, 0.0)
            dS = (inflow - release) * 24 * 60 * 60 / 1.0e6

        S = max(S + dS, 0.0)
        if S > cap:  # spill
            spill = (S - cap) * 1.0e6 / 24 / 60 / 60
            # release = release + spill  #uncomment to include spill in release value
            S = cap
            dS = (
                (inflow - release - spill) * 24 * 60 * 60 / 1.0e6
            )  # JLM 5/3/24
        else:
            spill = 0.0
        Rsim.loc[dt] = release
        SPILLsim[dt] = spill
        Ssim.loc[dt] = S

    Rsim_list.append(Rsim)
    SPILLsim_list.append(SPILLsim)
    Ssim_list.append(Ssim)

list_dict = {
    "Rsim_list": Rsim_list,
    "SPILLsim_list": SPILLsim_list,
    "Ssim_list": Ssim_list,
    "grand_ids": grand_ids,
}
with open("starfit_outputs.pickle", "wb") as handle:
    pickle.dump(list_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
