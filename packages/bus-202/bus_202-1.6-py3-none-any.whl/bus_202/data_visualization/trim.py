import numpy as np

def trim(series, percentile_keep=100):
  
  # Calculate cut percentage on each end
  cut = (100 - percentile_keep) / 2
  
  # Calculate bounds
  lower_bound = np.percentile(series, cut)
  upper_bound = np.percentile(series, 100 - cut)
  
  # Return filtered series
  return series[(series >= lower_bound) & (series <= upper_bound)]
