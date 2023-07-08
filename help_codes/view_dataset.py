import xarray as xr
import pandas as pd

# Read the NetCDF file using xarray
dataset = xr.open_dataset('../time_series.nc', decode_times=False)

# Iterate over dataset variables and add to the dictionary
for var_name, var_data in dataset.variables.items():
    data = {}
    data[var_name] = var_data.values.flatten()
    df = pd.DataFrame(data)
    df.to_csv(f'{var_name}.csv',index=False)
