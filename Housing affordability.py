#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the data
file_path = '/mnt/data/Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv'
data = pd.read_csv(file_path)

# Select relevant columns: RegionName, StateName, and the latest date (e.g., 2024-12-31)
latest_date = '2024-12-31'
selected_data = data[['RegionName', 'StateName', latest_date]].dropna()

# Load US states shapefile from Geopandas
us_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
us_map = us_map[us_map['continent'] == 'North America']

# Rename columns to match shapefile for merging
selected_data.rename(columns={'StateName': 'name', latest_date: 'IncomeNeeded'}, inplace=True)

# Group by state to calculate mean income needed per state (if required)
state_income = selected_data.groupby('name')['IncomeNeeded'].mean().reset_index()

# Merge state-level data with the US map
us_map = us_map.merge(state_income, on='name', how='left')

# Plot the map
plt.figure(figsize=(15, 10))
us_map.boundary.plot(color='black', linewidth=0.5, ax=plt.gca())
us_map.plot(column='IncomeNeeded', cmap='OrRd', legend=True, legend_kwds={'label': "Income Needed ($)"}, ax=plt.gca())

plt.title('Housing Affordability: Income Needed by State (2024-12)', fontsize=16)
plt.axis('off')
plt.show()


# In[2]:


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Select relevant columns: RegionName, StateName, and the latest date (e.g., 2024-12-31)
latest_date = '2024-12-31'
selected_data = data[['RegionName', 'StateName', latest_date]].dropna()

# Load US states shapefile from Geopandas
us_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
us_map = us_map[us_map['continent'] == 'North America']

# Rename columns to match shapefile for merging
selected_data.rename(columns={'StateName': 'name', latest_date: 'IncomeNeeded'}, inplace=True)

# Group by state to calculate mean income needed per state (if required)
state_income = selected_data.groupby('name')['IncomeNeeded'].mean().reset_index()

# Merge state-level data with the US map
us_map = us_map.merge(state_income, on='name', how='left')

# Plot the map
plt.figure(figsize=(15, 10))
us_map.boundary.plot(color='black', linewidth=0.5, ax=plt.gca())
us_map.plot(column='IncomeNeeded', cmap='OrRd', legend=True, legend_kwds={'label': "Income Needed ($)"}, ax=plt.gca())

plt.title('Housing Affordability: Income Needed by State (2024-12)', fontsize=16)
plt.axis('off')
plt.show()


# In[3]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Load the shapefile of U.S. states
gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
gdf = gdf[gdf['continent'] == 'North America']  # Keep only North America
gdf = gdf.rename(columns={'name': 'StateName'})

# Prepare the data for merging
data_long = pd.melt(data, id_vars=['RegionName', 'StateName'], var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'])  # Convert dates to datetime
merged = gdf.merge(data_long, on='StateName', how='left')

# Filter the GeoDataFrame to include only contiguous U.S. states
contiguous_states = gdf[~gdf['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# Set up the base map
fig, ax = plt.subplots(figsize=(18, 12))

# Create a placeholder for the colorbar
vmin = data_long['IncomeNeeded'].min()
vmax = data_long['IncomeNeeded'].max()
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.036, pad=0.04)
cbar.set_label('Income Needed for Housing Affordability ($)', fontsize=15)

def update(date):
    # Clear the previous data but keep static elements like colorbar and map boundaries
    ax.cla()

    # Re-plot the base map with boundaries
    contiguous_states.plot(ax=ax, color='white', edgecolor='black')

    # Update the title for the current date
    ax.set_title(f'Housing Affordability in the U.S. on {date.strftime("%Y-%m-%d")}', fontsize=18)

    # Set appropriate limits for better visualization
    ax.set_xlim(-130, -65)
    ax.set_ylim(24, 50)
    ax.set_axis_off()

    # Filter data for the specific date and plot the corresponding values
    temp = merged[merged['Date'] == date]
    temp = temp[~temp['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
    if not temp.empty:
        temp.plot(ax=ax, column='IncomeNeeded', cmap='viridis', legend=False)

# Generate dates for animation
dates = sorted(data_long['Date'].dropna().unique())
dates = dates[::3]  # Reduce frames for smoother animation

# Calculate FPS to fit the animation into approximately 15 seconds
total_duration = 15  # seconds
fps = len(dates) / total_duration

# Create the animation
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a .gif file
output_path = r'C:\Users\Nimith Narapareddy\Documents\Python Scripts\Income_Affordability_Animation.gif'
ani.save(output_path, writer='pillow', fps=fps)

plt.show()
print(f"Animation saved to {output_path}")


# In[4]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Identify columns that represent dates
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

# Prepare the data for merging
data_long = pd.melt(data, id_vars=['RegionName', 'StateName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Handle invalid date formats

# Drop rows where Date conversion failed
data_long = data_long.dropna(subset=['Date'])

# Load the shapefile of U.S. states
gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
gdf = gdf[gdf['continent'] == 'North America']  # Keep only North America
gdf = gdf.rename(columns={'name': 'StateName'})

# Merge with GeoDataFrame
merged = gdf.merge(data_long, on='StateName', how='left')

# Filter the GeoDataFrame to include only contiguous U.S. states
contiguous_states = gdf[~gdf['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# Set up the base map
fig, ax = plt.subplots(figsize=(18, 12))

# Create a placeholder for the colorbar
vmin = data_long['IncomeNeeded'].min()
vmax = data_long['IncomeNeeded'].max()
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.036, pad=0.04)
cbar.set_label('Income Needed for Housing Affordability ($)', fontsize=15)

def update(date):
    # Clear the previous data but keep static elements like colorbar and map boundaries
    ax.cla()

    # Re-plot the base map with boundaries
    contiguous_states.plot(ax=ax, color='white', edgecolor='black')

    # Update the title for the current date
    ax.set_title(f'Housing Affordability in the U.S. on {date.strftime("%Y-%m-%d")}', fontsize=18)

    # Set appropriate limits for better visualization
    ax.set_xlim(-130, -65)
    ax.set_ylim(24, 50)
    ax.set_axis_off()

    # Filter data for the specific date and plot the corresponding values
    temp = merged[merged['Date'] == date]
    temp = temp[~temp['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
    if not temp.empty:
        temp.plot(ax=ax, column='IncomeNeeded', cmap='viridis', legend=False)

# Generate dates for animation
dates = sorted(data_long['Date'].dropna().unique())
dates = dates[::3]  # Reduce frames for smoother animation

# Calculate FPS to fit the animation into approximately 15 seconds
total_duration = 15  # seconds
fps = len(dates) / total_duration

# Create the animation
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a .gif file
output_path = r'C:\Users\Nimith Narapareddy\Documents\Python Scripts\Income_Affordability_Animation.gif'
ani.save(output_path, writer='pillow', fps=fps)

plt.show()
print(f"Animation saved to {output_path}")


# In[5]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Identify columns that represent dates
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

# Prepare the data for merging
data_long = pd.melt(data, id_vars=['RegionName', 'StateName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Handle invalid date formats

# Drop rows where Date conversion failed
data_long = data_long.dropna(subset=['Date'])

# Path to the downloaded shapefile (update this path as per your system)
shapefile_path = r"C:\Users\Nimith Narapareddy\Documents\shapefiles\ne_110m_admin_0_countries.shp"

# Load the shapefile of U.S. states
gdf = gpd.read_file(shapefile_path)
gdf = gdf[gdf['CONTINENT'] == 'North America']  # Filter for North America
gdf = gdf.rename(columns={'NAME': 'StateName'})  # Adjust column name for merging

# Merge with GeoDataFrame
merged = gdf.merge(data_long, on='StateName', how='left')

# Filter the GeoDataFrame to include only contiguous U.S. states
contiguous_states = gdf[~gdf['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# Set up the base map
fig, ax = plt.subplots(figsize=(18, 12))

# Create a placeholder for the colorbar
vmin = data_long['IncomeNeeded'].min()
vmax = data_long['IncomeNeeded'].max()
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.036, pad=0.04)
cbar.set_label('Income Needed for Housing Affordability ($)', fontsize=15)

def update(date):
    # Clear the previous data but keep static elements like colorbar and map boundaries
    ax.cla()

    # Re-plot the base map with boundaries
    contiguous_states.plot(ax=ax, color='white', edgecolor='black')

    # Update the title for the current date
    ax.set_title(f'Housing Affordability in the U.S. on {date.strftime("%Y-%m-%d")}', fontsize=18)

    # Set appropriate limits for better visualization
    ax.set_xlim(-130, -65)
    ax.set_ylim(24, 50)
    ax.set_axis_off()

    # Filter data for the specific date and plot the corresponding values
    temp = merged[merged['Date'] == date]
    temp = temp[~temp['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
    if not temp.empty:
        temp.plot(ax=ax, column='IncomeNeeded', cmap='viridis', legend=False)

# Generate dates for animation
dates = sorted(data_long['Date'].dropna().unique())
dates = dates[::3]  # Reduce frames for smoother animation

# Calculate FPS to fit the animation into approximately 15 seconds
total_duration = 15  # seconds
fps = len(dates) / total_duration

# Create the animation
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a .gif file
output_path = r'C:\Users\Nimith Narapareddy\Documents\Python Scripts\Income_Affordability_Animation.gif'
ani.save(output_path, writer='pillow', fps=fps)

plt.show()
print(f"Animation saved to {output_path}")


# In[6]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Identify columns that represent dates
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

# Prepare the data for merging
data_long = pd.melt(data, id_vars=['RegionName', 'StateName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Handle invalid date formats

# Drop rows where Date conversion failed
data_long = data_long.dropna(subset=['Date'])

# Path to the shapefile
shapefile_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\ne_110m_admin_0_countries.shp"

# Load the shapefile of U.S. states
gdf = gpd.read_file(shapefile_path)
gdf = gdf[gdf['CONTINENT'] == 'North America']  # Filter for North America
gdf = gdf.rename(columns={'NAME': 'StateName'})  # Adjust column name for merging

# Merge with GeoDataFrame
merged = gdf.merge(data_long, on='StateName', how='left')

# Filter the GeoDataFrame to include only contiguous U.S. states
contiguous_states = gdf[~gdf['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# Set up the base map
fig, ax = plt.subplots(figsize=(18, 12))

# Create a placeholder for the colorbar
vmin = data_long['IncomeNeeded'].min()
vmax = data_long['IncomeNeeded'].max()
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.036, pad=0.04)
cbar.set_label('Income Needed for Housing Affordability ($)', fontsize=15)

def update(date):
    # Clear the previous data but keep static elements like colorbar and map boundaries
    ax.cla()

    # Re-plot the base map with boundaries
    contiguous_states.plot(ax=ax, color='white', edgecolor='black')

    # Update the title for the current date
    ax.set_title(f'Housing Affordability in the U.S. on {date.strftime("%Y-%m-%d")}', fontsize=18)

    # Set appropriate limits for better visualization
    ax.set_xlim(-130, -65)
    ax.set_ylim(24, 50)
    ax.set_axis_off()

    # Filter data for the specific date and plot the corresponding values
    temp = merged[merged['Date'] == date]
    temp = temp[~temp['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
    if not temp.empty:
        temp.plot(ax=ax, column='IncomeNeeded', cmap='viridis', legend=False)

# Generate dates for animation
dates = sorted(data_long['Date'].dropna().unique())
dates = dates[::3]  # Reduce frames for smoother animation

# Calculate FPS to fit the animation into approximately 15 seconds
total_duration = 15  # seconds
fps = len(dates) / total_duration

# Create the animation
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a .gif file
output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Income_Affordability_Animation.gif"
ani.save(output_path, writer='pillow', fps=fps)

plt.show()
print(f"Animation saved to {output_path}")


# In[7]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Identify columns that represent dates
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

# Prepare the data for merging
data_long = pd.melt(data, id_vars=['RegionName', 'StateName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Handle invalid date formats

# Drop rows where Date conversion failed
data_long = data_long.dropna(subset=['Date'])

# Path to the shapefile
shapefile_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\ne_110m_admin_0_countries.shp"

# Load the shapefile of U.S. states
gdf = gpd.read_file(shapefile_path)
gdf = gdf[gdf['CONTINENT'] == 'North America']  # Filter for North America
gdf = gdf.rename(columns={'NAME': 'StateName'})  # Adjust column name for merging

# Merge the GeoDataFrame with the data
merged = gdf.merge(data_long, on='StateName', how='left')

# Filter the GeoDataFrame to include only contiguous U.S. states
contiguous_states = merged[~merged['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# Set up the base map
fig, ax = plt.subplots(figsize=(18, 12))

# Create a placeholder for the colorbar
vmin = data_long['IncomeNeeded'].min()
vmax = data_long['IncomeNeeded'].max()
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.036, pad=0.04)
cbar.set_label('Income Needed for Housing Affordability ($)', fontsize=15)

def update(date):
    # Clear the previous data but keep static elements like colorbar and map boundaries
    ax.cla()

    # Re-plot the base map with boundaries
    contiguous_states.boundary.plot(ax=ax, color='black')

    # Update the title for the current date
    ax.set_title(f'Housing Affordability in the U.S. on {date.strftime("%Y-%m-%d")}', fontsize=18)

    # Set appropriate limits for better visualization
    ax.set_xlim(-130, -65)
    ax.set_ylim(24, 50)
    ax.set_axis_off()

    # Filter data for the specific date and plot the corresponding values
    temp = contiguous_states[contiguous_states['Date'] == date]
    if not temp.empty:
        temp.plot(ax=ax, column='IncomeNeeded', cmap='viridis', legend=False)

# Generate dates for animation
dates = sorted(data_long['Date'].dropna().unique())
dates = dates[::3]  # Reduce frames for smoother animation

# Calculate FPS to fit the animation into approximately 15 seconds
total_duration = 15  # seconds
fps = len(dates) / total_duration

# Create the animation
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a .gif file
output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Income_Affordability_Animation.gif"
ani.save(output_path, writer='pillow', fps=fps)

plt.show()
print(f"Animation saved to {output_path}")


# In[9]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Identify columns that represent dates
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

# Prepare the data for merging
data_long = pd.melt(data, id_vars=['RegionName', 'StateName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Handle invalid date formats

# Drop rows where Date conversion failed
data_long = data_long.dropna(subset=['Date'])

# Path to the shapefile
shapefile_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\ne_110m_admin_0_countries.shp"

# Load the shapefile of U.S. states
gdf = gpd.read_file(shapefile_path)
gdf = gdf[gdf['CONTINENT'] == 'North America']  # Filter for North America
gdf = gdf.rename(columns={'NAME': 'StateName'})  # Adjust column name for merging

# Check for mismatches in StateName
missing_states = set(data_long['StateName'].unique()) - set(gdf['StateName'].unique())
if missing_states:
    print(f"States in the data but not in the shapefile: {missing_states}")

# Merge the GeoDataFrame with the data
merged = gdf.merge(data_long, on='StateName', how='left')

# Filter the GeoDataFrame to include only contiguous U.S. states
contiguous_states = merged[~merged['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# Set up the base map
fig, ax = plt.subplots(figsize=(18, 12))

# Create a placeholder for the colorbar
vmin = data_long['IncomeNeeded'].min()
vmax = data_long['IncomeNeeded'].max()
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.036, pad=0.04)
cbar.set_label('Income Needed for Housing Affordability ($)', fontsize=15)

def update(date):
    # Clear the previous data but keep static elements like colorbar and map boundaries
    ax.cla()

    # Re-plot the base map with boundaries
    contiguous_states.boundary.plot(ax=ax, color='black')

    # Update the title for the current date
    ax.set_title(f'Housing Affordability in the U.S. on {date.strftime("%Y-%m-%d")}', fontsize=18)

    # Set appropriate limits for better visualization
    ax.set_xlim(-130, -65)
    ax.set_ylim(24, 50)
    ax.set_axis_off()

    # Filter data for the specific date and plot the corresponding values
    temp = contiguous_states[contiguous_states['Date'] == date]
    if not temp.empty:
        temp.plot(ax=ax, column='IncomeNeeded', cmap='viridis', legend=False)

# Generate dates for animation
dates = sorted(data_long['Date'].dropna().unique())
dates = dates[::3]  # Reduce frames for smoother animation

# Calculate FPS to fit the animation into approximately 15 seconds
total_duration = 15  # seconds
fps = len(dates) / total_duration

# Create the animation
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a .gif file
output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Income_Affordability_Animation.gif"
ani.save(output_path, writer='pillow', fps=fps)

plt.show()
print(f"Animation saved to {output_path}")


# In[10]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# State abbreviation to full name mapping
state_abbreviation_to_full = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
    'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
    'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# Map state abbreviations to full names
data['StateName'] = data['StateName'].map(state_abbreviation_to_full)

# Identify columns that represent dates
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

# Prepare the data for merging
data_long = pd.melt(data, id_vars=['RegionName', 'StateName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Handle invalid date formats

# Drop rows where Date conversion failed
data_long = data_long.dropna(subset=['Date'])

# Path to the shapefile
shapefile_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\ne_110m_admin_0_countries.shp"

# Load the shapefile of U.S. states
gdf = gpd.read_file(shapefile_path)
gdf = gdf[gdf['CONTINENT'] == 'North America']  # Filter for North America
gdf = gdf.rename(columns={'NAME': 'StateName'})  # Adjust column name for merging

# Merge the GeoDataFrame with the data
merged = gdf.merge(data_long, on='StateName', how='left')

# Filter the GeoDataFrame to include only contiguous U.S. states
contiguous_states = merged[~merged['StateName'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# Set up the base map
fig, ax = plt.subplots(figsize=(18, 12))

# Create a placeholder for the colorbar
vmin = data_long['IncomeNeeded'].min()
vmax = data_long['IncomeNeeded'].max()
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.036, pad=0.04)
cbar.set_label('Income Needed for Housing Affordability ($)', fontsize=15)

def update(date):
    # Clear the previous data but keep static elements like colorbar and map boundaries
    ax.cla()

    # Re-plot the base map with boundaries
    contiguous_states.boundary.plot(ax=ax, color='black')

    # Update the title for the current date
    ax.set_title(f'Housing Affordability in the U.S. on {date.strftime("%Y-%m-%d")}', fontsize=18)

    # Set appropriate limits for better visualization
    ax.set_xlim(-130, -65)
    ax.set_ylim(24, 50)
    ax.set_axis_off()

    # Filter data for the specific date and plot the corresponding values
    temp = contiguous_states[contiguous_states['Date'] == date]
    if not temp.empty:
        temp.plot(ax=ax, column='IncomeNeeded', cmap='viridis', legend=False)

# Generate dates for animation
dates = sorted(data_long['Date'].dropna().unique())
dates = dates[::3]  # Reduce frames for smoother animation

# Calculate FPS to fit the animation into approximately 15 seconds
total_duration = 15  # seconds
fps = len(dates) / total_duration

# Create the animation
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a .gif file
output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Income_Affordability_Animation.gif"
ani.save(output_path, writer='pillow', fps=fps)

plt.show()
print(f"Animation saved to {output_path}")


# In[11]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Map CBSA names to the shapefile
# Ensure that RegionName aligns with the shapefile's CBSA names
data['RegionName'] = data['RegionName'].str.title()  # Title case to match shapefile formatting

# Identify columns that represent dates
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

# Prepare the data for merging
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Handle invalid date formats
data_long = data_long.dropna(subset=['Date'])  # Drop invalid dates

# Path to the new CBSA shapefile
shapefile_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\cb_2018_us_cbsa_500k.shp"

# Load the CBSA shapefile
gdf = gpd.read_file(shapefile_path)

# Rename the column to align with the data
# Assuming the shapefile has a column for CBSA names (e.g., "NAME" or "CBSA_T")
gdf = gdf.rename(columns={'NAME': 'RegionName'})  # Update if the column name differs

# Merge the GeoDataFrame with the data
merged = gdf.merge(data_long, on='RegionName', how='left')

# Debug: Check merged data
print(merged.head())
print(merged['IncomeNeeded'].notnull().sum(), "non-null IncomeNeeded values")

# Test plot for a single date
sample_date = pd.Timestamp('2024-10-31')
temp = merged[merged['Date'] == sample_date]
print(temp.head())  # Debug: Check filtered data for the sample date

# Plot the static map
fig, ax = plt.subplots(figsize=(18, 12))
gdf.boundary.plot(ax=ax, color="black", linewidth=0.5)
if not temp.empty:
    temp.plot(ax=ax, column='IncomeNeeded', cmap='viridis', legend=True)
    plt.title(f"Housing Affordability on {sample_date.strftime('%Y-%m-%d')}")
else:
    print("No data available for the selected date.")
plt.show()


# In[12]:


# Assuming 'RegionName' in your dataset contains only city names
# Append state abbreviations from the 'StateName' column
data['RegionName'] = data['RegionName'] + ', ' + data['StateName']
data['RegionName'] = data['RegionName'].str.title()  # Convert to title case for alignment


# In[13]:


# Check mismatches after preprocessing
missing_regions = set(data['RegionName'].unique()) - set(gdf['RegionName'].unique())
print(f"Regions in the dataset but not in the shapefile: {missing_regions}")


# In[14]:


# Remove redundant state abbreviations in RegionName
data['RegionName'] = data['RegionName'].str.replace(r',\s+\w+$', '', regex=True)  # Removes ", State"


# In[15]:


# Check for mismatched regions again
missing_regions = set(data['RegionName'].unique()) - set(gdf['RegionName'].unique())
print(f"Regions in the dataset but not in the shapefile: {missing_regions}")


# In[16]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Clean the RegionName column to remove redundant state abbreviations
data['RegionName'] = data['RegionName'].str.replace(r',\s+\w+$', '', regex=True)

# Identify columns that represent dates
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

# Prepare the data for merging
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Handle invalid date formats
data_long = data_long.dropna(subset=['Date'])  # Drop invalid dates

# Path to the new CBSA shapefile
shapefile_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\cb_2018_us_cbsa_500k.shp"

# Load the CBSA shapefile
gdf = gpd.read_file(shapefile_path)

# Rename the column to align with the data
gdf = gdf.rename(columns={'NAME': 'RegionName'})  # Update if the column name differs

# Merge the GeoDataFrame with the data
merged = gdf.merge(data_long, on='RegionName', how='left')

# Debug: Check merged data
print(merged.head())
print(merged['IncomeNeeded'].notnull().sum(), "non-null IncomeNeeded values")

# Test plot for a single date
sample_date = pd.Timestamp('2024-10-31')
temp = merged[merged['Date'] == sample_date]
print(temp.head())  # Debug: Check filtered data for the sample date

# Plot the static map
fig, ax = plt.subplots(figsize=(18, 12))
gdf.boundary.plot(ax=ax, color="black", linewidth=0.5)
if not temp.empty:
    temp.plot(ax=ax, column='IncomeNeeded', cmap='viridis', legend=True)
    plt.title(f"Housing Affordability on {sample_date.strftime('%Y-%m-%d')}")
else:
    print("No data available for the selected date.")
plt.show()


# In[17]:


# Print unique values from dataset and shapefile for comparison
print("Unique RegionName values in dataset:")
print(data['RegionName'].unique()[:50])  # First 50 unique values from dataset
print("\nUnique RegionName values in shapefile:")
print(gdf['RegionName'].unique()[:50])  # First 50 unique values from shapefile


# In[18]:


# Identify unmatched regions
missing_regions = set(data['RegionName'].unique()) - set(gdf['RegionName'].unique())
print(f"Regions in the dataset but not in the shapefile: {missing_regions}")


# In[19]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
# Melt the dataset to long format for easier plotting
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')

# Convert the 'Date' column to a datetime type
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')

# Drop rows with NaT in the 'Date' column
data_long = data_long.dropna(subset=['Date'])

# Interactive Visualization 1: Time-Series Line Chart for a Selected Metro Area
metro_area = "New York"  # You can change this to any metro area in your dataset
filtered_data = data_long[data_long['RegionName'] == metro_area]

fig1 = px.line(filtered_data, x='Date', y='IncomeNeeded', title=f'Income Needed Over Time in {metro_area}',
               labels={'IncomeNeeded': 'Income Needed ($)', 'Date': 'Date'},
               hover_data=['IncomeNeeded'])
fig1.update_traces(mode='lines+markers')

# Interactive Visualization 2: Bar Chart of Latest Income Needed for Top Metro Areas
latest_data = data_long[data_long['Date'] == data_long['Date'].max()]  # Get the latest date's data
latest_data = latest_data.sort_values(by='IncomeNeeded', ascending=False).head(10)  # Top 10 metro areas

fig2 = px.bar(latest_data, x='RegionName', y='IncomeNeeded', title='Top 10 Metro Areas by Income Needed (Latest)',
              labels={'IncomeNeeded': 'Income Needed ($)', 'RegionName': 'Metro Area'},
              hover_data=['IncomeNeeded'])
fig2.update_traces(marker_color='blue')

# Show the visualizations
fig1.show()
fig2.show()


# In[20]:


import pandas as pd
import plotly.express as px

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Sort values for better animation
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])

# Create the bar chart race
fig = px.bar(data_long,
             x="IncomeNeeded",
             y="RegionName",
             color="RegionName",
             animation_frame="Date",
             orientation="h",
             title="Income Needed Over Time by Metro Area",
             labels={"IncomeNeeded": "Income Needed ($)", "RegionName": "Metro Area"},
             height=800,
             width=1000)

fig.update_layout(
    xaxis=dict(title="Income Needed ($)", range=[0, data_long['IncomeNeeded'].max() * 1.1]),
    yaxis=dict(title=""),
    showlegend=False,
    title=dict(font=dict(size=24))
)

# Save the animation as a GIF
fig.write_html(r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race.html")
fig.show()


# In[23]:


import pandas as pd
import plotly.express as px
from plotly.io import write_image
import os

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Focus on the top 20 metro areas per frame
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])
data_long['Rank'] = data_long.groupby('Date')['IncomeNeeded'].rank(method='first', ascending=False)
data_long = data_long[data_long['Rank'] <= 20]  # Keep only the top 20

# Create a folder to store frames
output_folder = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race_Frames"
os.makedirs(output_folder, exist_ok=True)

# Create frames for each date
dates = sorted(data_long['Date'].unique())
for i, date in enumerate(dates):
    # Filter data for the specific date
    frame_data = data_long[data_long['Date'] == date]
    
    # Create the plot for the current frame
    fig = px.bar(frame_data,
                 x="IncomeNeeded",
                 y="RegionName",
                 color="RegionName",
                 orientation="h",
                 title=f"Top 20 Metro Areas by Income Needed ({date.strftime('%B %Y')})",
                 labels={"IncomeNeeded": "Income Needed ($)", "RegionName": "Metro Area"},
                 height=800,
                 width=1000)
    
    # Update layout for better aesthetics
    fig.update_layout(
        xaxis=dict(title="Income Needed ($)", range=[0, data_long['IncomeNeeded'].max() * 1.1]),
        yaxis=dict(title="", autorange="reversed"),  # Reverse y-axis for horizontal bars
        showlegend=False,
        title=dict(font=dict(size=24))
    )
    
    # Save the frame as a PNG
    frame_file = os.path.join(output_folder, f"frame_{i:04d}.png")
    fig.write_image(frame_file)

# Combine frames into a GIF using ffmpeg
gif_output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race.gif"
os.system(f"ffmpeg -framerate 10 -i {output_folder}/frame_%04d.png -vf 'fps=10,scale=1280:-1' {gif_output_path}")

print(f"Bar Chart Race GIF saved to: {gif_output_path}")


# In[24]:


pip uninstall kaleido
pip install kaleido


# In[25]:


pip install --upgrade plotly


# In[26]:


import plotly.io as pio
pio.kaleido.scope



# In[27]:


import pandas as pd
import plotly.express as px
import os
import subprocess

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Focus on the top 20 metro areas per frame
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])
data_long['Rank'] = data_long.groupby('Date')['IncomeNeeded'].rank(method='first', ascending=False)
data_long = data_long[data_long['Rank'] <= 20]  # Keep only the top 20

# Create a folder to store frames
output_folder = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race_Frames"
os.makedirs(output_folder, exist_ok=True)

# Generate frames for each date
dates = sorted(data_long['Date'].unique())
for i, date in enumerate(dates):
    # Filter data for the specific date
    frame_data = data_long[data_long['Date'] == date]
    
    # Create the plot for the current frame
    fig = px.bar(frame_data,
                 x="IncomeNeeded",
                 y="RegionName",
                 color="RegionName",
                 orientation="h",
                 title=f"Top 20 Metro Areas by Income Needed ({date.strftime('%B %Y')})",
                 labels={"IncomeNeeded": "Income Needed ($)", "RegionName": "Metro Area"},
                 height=800,
                 width=1000)
    
    # Update layout for better aesthetics
    fig.update_layout(
        xaxis=dict(title="Income Needed ($)", range=[0, data_long['IncomeNeeded'].max() * 1.1]),
        yaxis=dict(title="", autorange="reversed"),  # Reverse y-axis for horizontal bars
        showlegend=False,
        title=dict(font=dict(size=24))
    )
    
    # Save the frame as a PNG
    frame_file = os.path.join(output_folder, f"frame_{i:04d}.png")
    fig.write_image(frame_file)

# Combine frames into a GIF using ffmpeg
gif_output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race.gif"
ffmpeg_command = [
    "ffmpeg", "-framerate", "10", "-i",
    os.path.join(output_folder, "frame_%04d.png"),
    "-vf", "fps=10,scale=1280:-1", "-y", gif_output_path
]
subprocess.run(ffmpeg_command)

print(f"Bar Chart Race GIF saved to: {gif_output_path}")


# In[28]:


frame_file = f'"{os.path.join(output_folder, f"frame_{i:04d}.png")}"'


# In[29]:


import plotly.express as px
fig = px.scatter(x=[1, 2, 3], y=[4, 5, 6])
fig.write_image("test_image.png")


# In[ ]:


import pandas as pd
import plotly.express as px
import os
import subprocess

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Focus on the top 20 metro areas per frame
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])
data_long['Rank'] = data_long.groupby('Date')['IncomeNeeded'].rank(method='first', ascending=False)
data_long = data_long[data_long['Rank'] <= 20]  # Keep only the top 20

# Create a folder to store frames
output_folder = r"C:\Users\Nimith_Narapareddy\Documents\Python_Scripts\Bar_Chart_Race_Frames"
os.makedirs(output_folder, exist_ok=True)

# Generate frames for each date
dates = sorted(data_long['Date'].unique())
for i, date in enumerate(dates):
    # Filter data for the specific date
    frame_data = data_long[data_long['Date'] == date]
    
    # Create the plot for the current frame
    fig = px.bar(frame_data,
                 x="IncomeNeeded",
                 y="RegionName",
                 color="RegionName",
                 orientation="h",
                 title=f"Top 20 Metro Areas by Income Needed ({date.strftime('%B %Y')})",
                 labels={"IncomeNeeded": "Income Needed ($)", "RegionName": "Metro Area"},
                 height=800,
                 width=1000)
    
    # Update layout for better aesthetics
    fig.update_layout(
        xaxis=dict(title="Income Needed ($)", range=[0, data_long['IncomeNeeded'].max() * 1.1]),
        yaxis=dict(title="", autorange="reversed"),  # Reverse y-axis for horizontal bars
        showlegend=False,
        title=dict(font=dict(size=24))
    )
    
    # Save the frame as


# In[30]:


import pandas as pd
import plotly.express as px
import os
import subprocess

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Focus on the top 20 metro areas per frame
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])
data_long['Rank'] = data_long.groupby('Date')['IncomeNeeded'].rank(method='first', ascending=False)
data_long = data_long[data_long['Rank'] <= 20]  # Keep only the top 20

# Create a folder to store frames
output_folder = r"C:\Users\Nimith_Narapareddy\Documents\Python_Scripts\Bar_Chart_Race_Frames"
os.makedirs(output_folder, exist_ok=True)

# Generate frames for each date
dates = sorted(data_long['Date'].unique())
for i, date in enumerate(dates):
    # Filter data for the specific date
    frame_data = data_long[data_long['Date'] == date]
    
    # Create the plot for the current frame
    fig = px.bar(frame_data,
                 x="IncomeNeeded",
                 y="RegionName",
                 color="RegionName",
                 orientation="h",
                 title=f"Top 20 Metro Areas by Income Needed ({date.strftime('%B %Y')})",
                 labels={"IncomeNeeded": "Income Needed ($)", "RegionName": "Metro Area"},
                 height=800,
                 width=1000)
    
    # Update layout for better aesthetics
    fig.update_layout(
        xaxis=dict(title="Income Needed ($)", range=[0, data_long['IncomeNeeded'].max() * 1.1]),
        yaxis=dict(title="", autorange="reversed"),  # Reverse y-axis for horizontal bars
        showlegend=False,
        title=dict(font=dict(size=24))
    )
    
    # Save the frame as an HTML file (Plotly rendering)
    frame_file = os.path.join(output_folder, f"frame_{i:04d}.html")
    with open(frame_file, "w") as f:
        f.write(fig.to_html(full_html=False))

# Combine frames into a video using ffmpeg
gif_output_path = r"C:\Users\Nimith_Narapareddy\Documents\Python_Scripts\Bar_Chart_Race.mp4"
ffmpeg_command = [
    "ffmpeg", "-framerate", "10", "-i",
    os.path.join(output_folder, "frame_%04d.html"),
    "-vf", "fps=10,scale=1280:-1", "-y", gif_output_path
]
subprocess.run(ffmpeg_command)

print(f"Bar Chart Race Video saved to: {gif_output_path}")


# In[31]:


import pandas as pd
import plotly.express as px
import os
import subprocess

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Focus on the top 20 metro areas per frame
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])
data_long['Rank'] = data_long.groupby('Date')['IncomeNeeded'].rank(method='first', ascending=False)
data_long = data_long[data_long['Rank'] <= 20]  # Keep only the top 20

# Create a folder to store frames (use a folder in Documents or relative path)
output_folder = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race_Frames"
os.makedirs(output_folder, exist_ok=True)  # Ensure the directory exists

# Generate frames for each date
dates = sorted(data_long['Date'].unique())
for i, date in enumerate(dates):
    # Filter data for the specific date
    frame_data = data_long[data_long['Date'] == date]
    
    # Create the plot for the current frame
    fig = px.bar(frame_data,
                 x="IncomeNeeded",
                 y="RegionName",
                 color="RegionName",
                 orientation="h",
                 title=f"Top 20 Metro Areas by Income Needed ({date.strftime('%B %Y')})",
                 labels={"IncomeNeeded": "Income Needed ($)", "RegionName": "Metro Area"},
                 height=800,
                 width=1000)
    
    # Update layout for better aesthetics
    fig.update_layout(
        xaxis=dict(title="Income Needed ($)", range=[0, data_long['IncomeNeeded'].max() * 1.1]),
        yaxis=dict(title="", autorange="reversed"),  # Reverse y-axis for horizontal bars
        showlegend=False,
        title=dict(font=dict(size=24))
    )
    
    # Save the frame as a PNG
    frame_file = os.path.join(output_folder, f"frame_{i:04d}.png")
    fig.write_image(frame_file)

# Combine frames into a GIF using ffmpeg
gif_output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race.gif"
ffmpeg_command = [
    "ffmpeg", "-framerate", "10", "-i",
    os.path.join(output_folder, "frame_%04d.png"),
    "-vf", "fps=10,scale=1280:-1", "-y", gif_output_path
]
subprocess.run(ffmpeg_command)

print(f"Bar Chart Race GIF saved to: {gif_output_path}")


# In[32]:


import pandas as pd
import plotly.express as px
import os
import subprocess

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Focus on the top 20 metro areas per frame
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])
data_long['Rank'] = data_long.groupby('Date')['IncomeNeeded'].rank(method='first', ascending=False)
data_long = data_long[data_long['Rank'] <= 20]  # Keep only the top 20

# Create a folder to store frames
output_folder = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race_Frames"
os.makedirs(output_folder, exist_ok=True)  # Ensure the directory exists

# Generate frames for each date
dates = sorted(data_long['Date'].unique())
for i, date in enumerate(dates):
    # Filter data for the specific date
    frame_data = data_long[data_long['Date'] == date]
    
    # Create the plot for the current frame
    fig = px.bar(frame_data,
                 x="IncomeNeeded",
                 y="RegionName",
                 color="RegionName",
                 orientation="h",
                 title=f"Top 20 Metro Areas by Income Needed ({date.strftime('%B %Y')})",
                 labels={"IncomeNeeded": "Income Needed ($)", "RegionName": "Metro Area"},
                 height=800,
                 width=1000)
    
    # Update layout for better aesthetics
    fig.update_layout(
        xaxis=dict(title="Income Needed ($)", range=[0, data_long['IncomeNeeded'].max() * 1.1]),
        yaxis=dict(title="", autorange="reversed"),  # Reverse y-axis for horizontal bars
        showlegend=False,
        title=dict(font=dict(size=24))
    )
    
    # Save the frame as a PNG
    frame_file = os.path.join(output_folder, f"frame_{i:04d}.png")
    fig.write_image(frame_file)

# Combine frames into a video using ffmpeg
video_output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race.mp4"
ffmpeg_command = [
    "ffmpeg", "-framerate", "10", "-i",
    os.path.join(output_folder, "frame_%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf", "fps=30", "-y", video_output_path
]
subprocess.run(ffmpeg_command)

print(f"Bar Chart Race Video saved to: {video_output_path}")


# In[33]:


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import subprocess

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Focus on the top 20 metro areas per frame
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])
data_long['Rank'] = data_long.groupby('Date')['IncomeNeeded'].rank(method='first', ascending=False)
data_long = data_long[data_long['Rank'] <= 20]  # Keep only the top 20

# Sort data for smoother animation
data_long = data_long.sort_values(by=['Date', 'Rank'])

# Create the animation
fig, ax = plt.subplots(figsize=(12, 8))

def update(date):
    ax.clear()
    frame_data = data_long[data_long['Date'] == date].sort_values(by='Rank')
    ax.barh(frame_data['RegionName'], frame_data['IncomeNeeded'], color='skyblue')
    ax.set_title(f"Top 20 Metro Areas by Income Needed ({date.strftime('%B %Y')})", fontsize=16)
    ax.set_xlabel("Income Needed ($)", fontsize=12)
    ax.set_xlim(0, data_long['IncomeNeeded'].max() * 1.1)

dates = sorted(data_long['Date'].unique())
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a video
video_output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race.mp4"
ani.save(video_output_path, writer='ffmpeg', fps=10)

print(f"Bar Chart Race Video saved to: {video_output_path}")


# In[36]:


sudo install ffmpeg



# In[37]:


ffmpeg -version


# In[38]:


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Focus on the top 20 metro areas per frame
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])
data_long['Rank'] = data_long.groupby('Date')['IncomeNeeded'].rank(method='first', ascending=False)
data_long = data_long[data_long['Rank'] <= 20]  # Keep only the top 20

# Sort data for smoother animation
data_long = data_long.sort_values(by=['Date', 'Rank'])

# Create the animation
fig, ax = plt.subplots(figsize=(12, 8))

def update(date):
    ax.clear()
    frame_data = data_long[data_long['Date'] == date].sort_values(by='Rank')
    ax.barh(frame_data['RegionName'], frame_data['IncomeNeeded'], color='skyblue')
    ax.set_title(f"Top 20 Metro Areas by Income Needed ({date.strftime('%B %Y')})", fontsize=16)
    ax.set_xlabel("Income Needed ($)", fontsize=12)
    ax.set_xlim(0, data_long['IncomeNeeded'].max() * 1.1)

# Generate frames for each date
dates = sorted(data_long['Date'].unique())
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a GIF using Pillow
gif_output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race.gif"
ani.save(gif_output_path, writer='pillow', fps=10)

print(f"Bar Chart Race GIF saved to: {gif_output_path}")


# In[39]:


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Focus on the top 20 metro areas per frame
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])
data_long['Rank'] = data_long.groupby('Date')['IncomeNeeded'].rank(method='first', ascending=False)
data_long = data_long[data_long['Rank'] <= 20]  # Keep only the top 20

# Sort data for smoother animation
data_long = data_long.sort_values(by=['Date', 'Rank'])

# Create the animation
fig, ax = plt.subplots(figsize=(14, 9))  # Increased figure size for better visuals

def update(date):
    ax.clear()
    frame_data = data_long[data_long['Date'] == date].sort_values(by='IncomeNeeded', ascending=False)
    ax.barh(frame_data['RegionName'], frame_data['IncomeNeeded'], color='skyblue', edgecolor='black')
    ax.set_title(f"Housing Affordability: Top 20 Metro Areas by Income Needed\n{date.strftime('%B %Y')}", fontsize=20, pad=20)
    ax.set_xlabel("Income Needed ($)", fontsize=14)
    ax.set_ylabel("Metro Area", fontsize=14)
    ax.set_xlim(0, data_long['IncomeNeeded'].max() * 1.1)  # Add some padding
    ax.tick_params(axis='both', labelsize=12)
    ax.invert_yaxis()  # Highest value on top
    # Add gridlines for better readability
    ax.grid(axis='x', linestyle='--', alpha=0.7)

# Generate frames for each date
dates = sorted(data_long['Date'].unique())
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a GIF using Pillow
gif_output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race_Improved.gif"
ani.save(gif_output_path, writer='pillow', fps=15)  # Increased fps for smoother animation

print(f"Improved Bar Chart Race GIF saved to: {gif_output_path}")


# In[40]:


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the housing data
file_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Metro_new_homeowner_income_needed_downpayment_0.20_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
data = pd.read_csv(file_path)

# Prepare the data
date_columns = [col for col in data.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
data_long = pd.melt(data, id_vars=['RegionName'], value_vars=date_columns, var_name='Date', value_name='IncomeNeeded')
data_long['Date'] = pd.to_datetime(data_long['Date'], errors='coerce')  # Convert Date to datetime
data_long = data_long.dropna(subset=['Date', 'IncomeNeeded'])  # Drop rows with NaT or missing values

# Filter data from March 2020 onwards
data_long = data_long[data_long['Date'] >= '2020-03-01']

# Focus on the top 20 metro areas per frame
data_long = data_long.sort_values(by=['Date', 'IncomeNeeded'], ascending=[True, False])
data_long['Rank'] = data_long.groupby('Date')['IncomeNeeded'].rank(method='first', ascending=False)
data_long = data_long[data_long['Rank'] <= 20]  # Keep only the top 20

# Sort data for smoother animation
data_long = data_long.sort_values(by=['Date', 'Rank'])

# Create the animation
fig, ax = plt.subplots(figsize=(14, 9))  # Increased figure size for better visuals

def update(date):
    ax.clear()
    frame_data = data_long[data_long['Date'] == date].sort_values(by='IncomeNeeded', ascending=False)
    ax.barh(frame_data['RegionName'], frame_data['IncomeNeeded'], color='skyblue', edgecolor='black')
    ax.set_title(f"Housing Affordability: Top 20 Metro Areas by Income Needed\n{date.strftime('%B %Y')}", fontsize=20, pad=20)
    ax.set_xlabel("Income Needed ($)", fontsize=14)
    ax.set_ylabel("Metro Area", fontsize=14)
    ax.set_xlim(0, data_long['IncomeNeeded'].max() * 1.1)  # Add some padding
    ax.tick_params(axis='both', labelsize=12)
    ax.invert_yaxis()  # Highest value on top
    # Add gridlines for better readability
    ax.grid(axis='x', linestyle='--', alpha=0.7)

# Generate frames for each date
dates = sorted(data_long['Date'].unique())
ani = FuncAnimation(fig, update, frames=dates, repeat=False)

# Save the animation as a GIF using Pillow
gif_output_path = r"C:\Users\Nimith Narapareddy\Documents\Python Scripts\Bar_Chart_Race_COVID.gif"
ani.save(gif_output_path, writer='pillow', fps=15)  # Increased fps for smoother animation

print(f"Bar Chart Race GIF (COVID onwards) saved to: {gif_output_path}")


# In[ ]:




