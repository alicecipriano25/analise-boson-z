

import numpy as np
import pyhf
import pandas as pd

pyhf.set_backend('numpy')

all_bins = pd.read_csv('all_binning_normalized_with_bkg.csv', index_col=0)

bkg = np.array(all_bins['Background']) #background
observations = list(all_bins['Data'])

all_results = {}

for col in ['mass_zprime_eta0p01_2600_data', 'mass_zprime_eta0p01_2800_data', 'mass_zprime_eta0p01_3000_data', 'mass_zprime_eta0p01_3200_data', 'mass_zprime_eta0p01_3400_data', 'mass_zprime_eta0p01_3600_data', 'mass_zprime_eta0p01_3800_data', 'mass_zprime_eta0p01_4000_data']:

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
	bounds[0] = (0, 85)

	data = pyhf.tensorlib.astensor(observations + model.config.auxdata)
	
	scan = np.linspace(1, np.sqrt(80), 90)**2

	obs_limit, exp_limits, (scan, results) = pyhf.infer.intervals.upper_limits.upper_limit(data, model, scan=scan, init_pars=init_pars, par_bounds=bounds, calctype='toybased', ntoys=500, track_progress=False, return_results=True)

	single_result['Observed Limit'] = obs_limit

	for expected_value, n_sigma in zip(exp_limits, np.arange(-2,3)):
		single_result[f'Expected Limits({n_sigma:2d} σ)'] = expected_value

	all_results[col] = single_result
	
	print(single_result)
	
results_df = pd.DataFrame(all_results)
	
results_df.to_csv('stats_results_0p01_2600_4000.csv')

