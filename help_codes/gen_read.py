# Generalized form to read the latitude and longitude in all the datasets 
# so that no need to change the values 
import xarray as xr

# Read the NetCDF file using xarray
dataset = xr.open_dataset('../indian_ocean.nc', decode_times=False)

# Extract latitude, longitude, and temperature data
latitude_var = [var for var in dataset.variables if 'lat' in var.lower()][0]
longitude_var = [var for var in dataset.variables if 'lon' in var.lower()][0]
latitude = dataset[latitude_var].values
longitude = dataset[longitude_var].values


