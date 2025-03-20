from collections import Counter
from pprint import pprint

import xarray as xr

import pywatershed as pws

pws_root = pws.constants.__pywatershed_root__
domain_dir = pws_root / ("../test_data/drb_2yr")

sep_param_files = sorted(domain_dir.glob("parameter*PRMS*.nc"))

vars = []
for ff in sep_param_files:
    ds = xr.open_dataset(ff)
    vars += list(ds.data_vars)

pprint(
    {key: val for key, val in Counter(vars).items() if val > 1},
    sort_dicts=False,
)

# Counter({'hru_area': 6,  # !
#          'cov_type': 3,  # ??
#          'hru_type': 3,  # !
#          'hru_aspect': 2, # !
#          'hru_lat': 2,    # !
#          'hru_slope': 2,  # !
#          'radj_sppt': 2,
#          'radj_wppt': 2,
#          'tmax_allsnow': 2,
#          'covden_sum': 2,
#          'covden_win': 2,
#          'potet_sublim': 2,
#          'dprst_frac': 2,
#          'hru_percent_imperv': 2,
#          'soil_moist_max': 2,
#          'adjmix_rain': 1,
#          'dday_intcp': 1,
#          'dday_slope': 1,
#          'jh_coef': 1,
#          'jh_coef_hru': 1,
#          'ppt_rad_adj': 1,
#          'radadj_intcp': 1,
#          'radadj_slope': 1,
#          'radmax': 1,
#          'rain_cbh_adj': 1,
#          'snow_cbh_adj': 1,
#          'temp_units': 1,
#          'tmax_allrain_offset': 1,
#          'tmax_cbh_adj': 1,
#          'tmax_index': 1,
#          'tmin_cbh_adj': 1,
#          'transp_beg': 1,
#          'transp_end': 1,
#          'transp_tmax': 1,
#          'snow_intcp': 1,
#          'srain_intcp': 1,
#          'wrain_intcp': 1,
#          'hru_segment': 1,
#          'mann_n': 1,
#          'obsin_segment': 1,
#          'obsout_segment': 1,
#          'seg_depth': 1,
#          'seg_length': 1,
#          'seg_slope': 1,
#          'segment_flow_init': 1,
#          'segment_type': 1,
#          'tosegment': 1,
#          'tosegment_nhm': 1,
#          'x_coef': 1,
#          'gwflow_coef': 1,
#          'gwsink_coef': 1,
#          'gwstor_init': 1,
#          'gwstor_min': 1,
#          'carea_max': 1,
#          'dprst_depth_avg': 1,
#          'dprst_et_coef': 1,
#          'dprst_flow_coef': 1,
#          'dprst_frac_init': 1,
#          'dprst_frac_open': 1,
#          'dprst_seep_rate_clos': 1,
#          'dprst_seep_rate_open': 1,
#          'imperv_stor_max': 1,
#          'op_flow_thres': 1,
#          'smidx_coef': 1,
#          'smidx_exp': 1,
#          'snowinfil_max': 1,
#          'sro_to_dprst_imperv': 1,
#          'sro_to_dprst_perv': 1,
#          'va_clos_exp': 1,
#          'va_open_exp': 1,
#          'albset_rna': 1,
#          'albset_rnm': 1,
#          'albset_sna': 1,
#          'albset_snm': 1,
#          'cecn_coef': 1,
#          'den_init': 1,
#          'den_max': 1,
#          'emis_noppt': 1,
#          'freeh2o_cap': 1,
#          'hru_deplcrv': 1,
#          'melt_force': 1,
#          'melt_look': 1,
#          'rad_trncf': 1,
#          'settle_const': 1,
#          'snarea_curve': 1,
#          'snarea_thresh': 1,
#          'snowpack_init': 1,
#          'tstorm_mo': 1,
#          'fastcoef_lin': 1,
#          'fastcoef_sq': 1,
#          'pref_flow_den': 1,
#          'sat_threshold': 1,
#          'slowcoef_lin': 1,
#          'slowcoef_sq': 1,
#          'soil2gw_max': 1,
#          'soil_moist_init_frac': 1,
#          'soil_rechr_init_frac': 1,
#          'soil_rechr_max_frac': 1,
#          'soil_type': 1,
#          'ssr2gw_exp': 1,
#          'ssr2gw_rate': 1,
#          'ssstor_init_frac': 1})
