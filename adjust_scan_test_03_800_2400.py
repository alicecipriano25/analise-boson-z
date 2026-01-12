

import numpy as np
import pyhf
import pandas as pd

pyhf.set_backend('numpy')

all_bins = pd.read_csv('all_binning_normalized_with_bkg.csv', index_col=0)

bkg = np.array(all_bins['Background']) #background
observations = list(all_bins['Data'])

all_results = {}

for col in ['mass_zprime_eta0p03_800_data', 'mass_zprime_eta0p03_1000_data', 'mass_zprime_eta0p03_1200_data', 'mass_zprime_eta0p03_1400_data', 'mass_zprime_eta0p03_1600_data', 'mass_zprime_eta0p03_1800_data', 'mass_zprime_eta0p03_2000_data', 'mass_zprime_eta0p03_2200_data', 'mass_zprime_eta0p03_2400_data']:

	single_result = {}

	signal = list(all_bins[col])  #Z'
	bkg_sigma = 0.2*bkg
	
	model = pyhf.simplemodels.uncorrelated_background(
	    signal=signal,  #Z'
	    bkg=bkg, 
	    bkg_uncertainty=bkg_sigma
	)
	
	# Mudando os bounds
	init_pars = model.config.suggested_init()
	bounds = model.config.suggested_bounds()
	bounds[0] = (0, 10)

	data = pyhf.tensorlib.astensor(observations + model.config.auxdata)
	
	scan = np.linspace(0, np.sqrt(2), 40)**2

	obs_limit, exp_limits, (scan, results) = pyhf.infer.intervals.upper_limits.upper_limit(data, model, scan=scan, init_pars=init_pars, par_bounds=bounds, calctype='toybased', ntoys=500, track_progress=False, return_results=True)

	single_result['Observed Limit'] = obs_limit

	for expected_value, n_sigma in zip(exp_limits, np.arange(-2,3)):
		single_result[f'Expected Limits({n_sigma:2d} σ)'] = expected_value

	all_results[col] = single_result
	
	print(single_result)
	
results_df = pd.DataFrame(all_results)
	
results_df.to_csv('stats_results_0p03_800_2400.csv')

