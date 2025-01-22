import geopandas as gpd

#from google.colab import files
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from shapely.geometry.point import Point
from matplotlib.patches import Patch
import contextily as ctx
from pyproj import Proj, transform
import numpy as np

path_to_file = 'data/KommuneGrenser.geojson'

norge = gpd.read_file(path_to_file)
print(norge.head())

land_boundary_path = 'data/norway_wof.geojson'
fastland = gpd.read_file(land_boundary_path)

norge = norge.to_crs(fastland.crs)

norge = gpd.overlay(norge, fastland, how='intersection')
norge['value'] = norge['kommunenummer'].astype(int) / max(norge['kommunenummer'].astype(int))
norge['value'] = np.random.rand(len(norge))  # Replace this with actual values

### Plotting

bbox = norge.total_bounds

fig, ax = plt.subplots(figsize=(18, 18))

norge.plot(column='value', cmap='viridis', legend=True, ax=ax, edgecolor='black')
# Set x and y axis limits to ensure full map is shown
# Calculate padding as a percentage of the range (e.g., 2% padding)
x_pad = (bbox[2] - bbox[0]) * 0.05  # 2% of the width
y_pad = (bbox[3] - bbox[1]) * 0.05  # 2% of the height

# Set x and y axis limits with padding
ax.set_xlim([bbox[0] - x_pad, bbox[2] + x_pad])
ax.set_ylim([bbox[1] - y_pad, bbox[3] + y_pad])

#ax = norge.plot(ax=ax) 

# Adding basemap - by specifying the URL of the basemap provider
basemap_url = 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'
ctx.add_basemap(ax, url=basemap_url)

# Setting x-axis limits to cover only the extent of the US
# ax.set_xlim(bbox[0], bbox[2]) #easiest method using bounding box values

#ax.set_xlim(bbox[0], -60)

for idx, row in norge.iterrows():
    state_name = str(row['kommunenummer'])  # Assuming 'NAME' is the column containing state names
    centroid = row.geometry.centroid
    ax.annotate(text=state_name, xy=(centroid.x, centroid.y),
                xytext=(3, 3), textcoords="offset points",
                ha='center', fontsize=5, color='black')


src_crs=Proj(init='epsg:4258') #mercator projection
dst_crs=Proj(init='epsg:4258')
# Converting x-axis (longitude) tick coordinates to degrees
lon_ticks = [transform(src_crs, dst_crs, x, 0)[0] for x in ax.get_xticks()]

# Converting y-axis (latitude) tick coordinates to degrees
lat_ticks = [transform(src_crs, dst_crs, 0, y)[1] for y in ax.get_yticks()]

ax.set_xticklabels([f"{lon:.2f}°W" for lon in lon_ticks])
ax.set_yticklabels([f"{lat:.2f}°N" for lat in lat_ticks])


#Adding scale to map
points = gpd.GeoSeries(
    [Point(-73.5, 40.5), Point(-74.5, 40.5)], crs=4258
)  # Geographic WGS 84 - degrees
points = points.to_crs(32619)  # Projected WGS 84 - meters
distance_meters = points[0].distance(points[1])
ax.add_artist(ScaleBar(distance_meters,
                       label="Scale",
    location="lower right",  # in relation to the whole plot
    label_loc="top",
    scale_loc="bottom",  # in relation to the line
                       ))

# Adding a legend to the map
legend_elements = [Patch(facecolor='blue', edgecolor='black', label='Random Numbers')]
ax.legend(handles=legend_elements, loc='upper right')

# Adding title to the plot
plt.title("Norge")