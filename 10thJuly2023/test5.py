# Add zooming in from the top down and the depth changes and also a proper seabed
import xarray as xr
import numpy as np
from mayavi import mlab
from tvtk.api import tvtk

# Read the NetCDF file using xarray
dataset = xr.open_dataset('../time_series.nc', decode_times=False)

# Extract latitude, longitude, and temperature data
latitude_var = [var for var in dataset.variables if 'lat' in var.lower()][0]
longitude_var = [var for var in dataset.variables if 'lon' in var.lower()][0]
latitude = dataset[latitude_var].values
longitude = dataset[longitude_var].values
temperature = dataset['WATER_TEMP'].values[:, :, :, :]

# Make a seabed
seabed = np.random.rand(len(latitude), len(longitude))
for _ in range(100000):
    peak_row = np.random.randint(0, len(latitude))
    peak_col = np.random.randint(0, len(longitude))
    seabed[peak_row, peak_col] += 0

# Create a meshgrid of latitude and longitude
lon_grid, lat_grid = np.meshgrid(longitude, latitude)
# Create a figure and initial plot
fig = mlab.figure(size=(800, 600), bgcolor=(0, 0, 0))
mesh = mlab.mesh(lon_grid, lat_grid, temperature[0,0,:,:], colormap='jet', scalars=temperature[0,0,:,:])

# Declare the camera
cam = mlab.gcf().scene.camera
color_bar = mlab.colorbar(title='Temperature')

@mlab.animate(delay=100)
def update_depth():
    # The complete animation
    depth_animation_completed = False
    alpha = 1.0 
    while True:
        # mlab.view(azimuth=0, elevation=30, distance='auto')
        if(depth_animation_completed):
            print('animation done')
            break
        for i in range(temperature[0,:,:,:].shape[0]+1):
            # Fade out the current surface
            for fade_step in range(10):
                if(i==temperature[0, :,: , :].shape[0]):
                    # If seabed is there then break
                    break
                # Decrease the alpha value gradually
                z_position = cam.position[2]
                fade_alpha = alpha * (1.0 - fade_step / 10.0)
                mesh.actor.actor.property.opacity = fade_alpha
                mlab.view(azimuth=90, elevation=30, distance=20-fade_step/5.0)
                yield
         
            if(i==temperature[0, :,: , :].shape[0]):
                # If seabed is there then break
                mlab.clf()
                mlab.mesh(lon_grid, lat_grid, seabed, colormap='copper', scalars=seabed)
                color_bar.visible = False
                cam.position = [(longitude.max() + longitude.min()) / 2,
                            (latitude.max() + latitude.min()) / 2,
                            z_position - i]
                mlab.view(azimuth=0, elevation=0, distance=30)
                depth_animation_completed=True
                break
            else:
                mesh.mlab_source.set(z=temperature[0,i,:,:]-i, scalars=temperature[0, i, :, :])
            cam.position = [(longitude.max() + longitude.min()) / 2,
                            (latitude.max() + latitude.min()) / 2,
                            z_position - i]
            # for i in range(10):
            mlab.view(azimuth=90, elevation=30, distance=30)
             # Fade in the new surface
            for fade_step in range(10):
                # Increase the alpha value gradually
                fade_alpha = alpha * (fade_step / 10.0)
                mesh.actor.actor.property.opacity = fade_alpha
                mlab.view(azimuth=90, elevation=30, distance=30-fade_step/5.0)
                yield
            
# @mlab.animate(delay=1000)
# def update_time():
#     while True:
#         for time_step in range(temperature[:, 0, :, :].shape[0]):
#             mesh.mlab_source.set(z=temperature[time_step, 0, :, :], scalars=temperature[time_step, 0, :, :])
#             yield



# Start the animation
anim = update_depth()
# anim_time = update_time()
mlab.show()
