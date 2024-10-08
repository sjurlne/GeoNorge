import geopandas as gpd
import numpy as np

# Theirs

import plotly.express as px

df = px.data.election()
geojson = px.data.election_geojson()

print(df["district"][2])
print(geojson["features"][0]["properties"])

import plotly.express as px

df = px.data.election()
geojson = px.data.election_geojson()

fig = px.choropleth(df, geojson=geojson, color="Bergeron",
                    locations="district", featureidkey="properties.district",
                    projection="mercator"
                   )
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()



# MINE
path_to_file = 'data/KommuneGrenser.geojson'

norge = gpd.read_file(path_to_file)

df = norge[['kommunenavn','kommunenummer']].drop_duplicates()
df['number'] = (-1) * df['kommunenummer'].astype(int) / max(df['kommunenummer'].astype(int))

with open(path_to_file, 'r') as file:
    geojson = json.load(file)

fig = px.choropleth(df, geojson=geojson, color="number",
                    locations="kommunenummer", featureidkey="kommunenummer",
                    projection="mercator"
                   )
fig.update_geos(fitbounds="geojson", visible=False)
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

