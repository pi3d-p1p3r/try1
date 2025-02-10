import xarray as xr 
import matplotlib.pyplot as plt 
import numpy as np 

place = 'Rajshahi'
# Load dataset 
ds = xr.open_dataset('temp_soilmoist.nc')  # Update path 

# Convert temperature to Celsius if needed 
if ds.t2m.units == 'K': 
    ds['t2m'] = ds.t2m - 273.15 
    ds.t2m.attrs['units'] = '°C' 

# Select 2010-2012 period 
ti = '2010-01-01'
tf = '2012-12-31'
period_ds = ds.sel(valid_time=slice(ti, tf)) 

# Select specific coordinates (using nearest neighbor)
target_lat = 26.4940
target_lon = 88.3568

# Get data for specific location
temp_ts = period_ds.t2m.sel(
    latitude=target_lat, 
    longitude=target_lon,
    method='nearest'
)
sm1_ts = period_ds.swvl1.sel(
    latitude=target_lat,
    longitude=target_lon,
    method='nearest'
)
sm2_ts = period_ds.swvl2.sel(
    latitude=target_lat,
    longitude=target_lon,
    method='nearest'
)

# Create figure with two subplots 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6)) 
plt.subplots_adjust(wspace=0.3) 

# Plot Soil Moisture Level 1 vs Temperature
sc1 = ax1.scatter(sm1_ts, temp_ts, c=np.arange(len(sm1_ts)),  
                cmap='viridis', alpha=0.7) 
ax1.set_title(f'Soil Moisture Level 1 vs Temperature\n{place} [{ti} to {tf}] ({target_lat}°N, {target_lon}°E)', fontsize=12) 
ax1.set_ylabel('2m Temperature (°C)', fontsize=10) 
ax1.set_xlabel('Soil Moisture (m³/m³)', fontsize=10) 
ax1.grid(alpha=0.3) 
cbar1 = plt.colorbar(sc1, ax=ax1) 
cbar1.set_label('Time Progression', fontsize=9) 

# Plot Soil Moisture Level 2 vs Temperature
sc2 = ax2.scatter(sm2_ts, temp_ts, c=np.arange(len(sm2_ts)),  
                cmap='plasma', alpha=0.7) 
ax2.set_title(f'Soil Moisture Level 2 vs Temperature\n{place} [{ti} to {tf}] ({target_lat}°N, {target_lon}°E)', fontsize=12) 
ax2.set_ylabel('2m Temperature (°C)', fontsize=10) 
ax2.set_xlabel('Soil Moisture (m³/m³)', fontsize=10) 
ax2.grid(alpha=0.3) 
cbar2 = plt.colorbar(sc2, ax=ax2) 
cbar2.set_label('Time Progression', fontsize=9) 

# Add trend lines 
for ax, sm_data in zip([ax1, ax2], [sm1_ts, sm2_ts]): 
    z = np.polyfit(sm_data, temp_ts, 1) 
    p = np.poly1d(z) 
    ax.plot(sm_data, p(sm_data), "r--", linewidth=1.5) 
    ax.text(0.05, 0.95, f'y = {z[0]:.4f}x + {z[1]:.4f}', 
            transform=ax.transAxes, ha='left', va='top', 
            bbox=dict(facecolor='white', alpha=0.8)) 

plt.suptitle(f'Temperature vs Soil Moisture Relationship at ({target_lat}°N, {target_lon}°E) (2010-2012)', 
             y=1.05, fontsize=14) 
plt.show()