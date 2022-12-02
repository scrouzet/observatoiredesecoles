import pandas as pd
import geopandas
import folium
import matplotlib.pyplot as plt

# Get the school location data from the geojson files dl from opendata-toulouse
path_to_data_elem = "./data/ecoles-elementaires-publiques.geojson"
gdf_elem = geopandas.read_file(path_to_data_elem)
gdf_elem['niveau'] = 'élémentaire'
print(f'df length is {len(gdf_elem)}, width is {len(gdf_elem.columns)}')
path_to_data_mater = "./data/ecoles-maternelles-publiques.geojson"
gdf_mater = geopandas.read_file(path_to_data_mater)
gdf_mater['niveau'] = 'maternelle'
print(f'df length is {len(gdf_mater)}, width is {len(gdf_mater.columns)}')
gdf = pd.concat([gdf_elem, gdf_mater], axis=0)
print(f'df length is {len(gdf)}, width is {len(gdf.columns)}')

gdf = gdf.loc[:, ("ecole", "niveau", "codsti", "index", "codpos", "rne", "libelle", "secteur_action_scolaire", "geometry")]
# geometry est encodé en MULTIPOINT mais ne contient qu'un POINT donc on l'explode
# cela permets de corriger un bug plus tard avec popup et tootip de explore() qui ne fonctionnent pas
# avec MULTIPOINT https://github.com/geopandas/geopandas/issues/2190
gdf = gdf.explode()

gdf['nom_ecole'] = 'Ecole ' + gdf['niveau'] + ' ' + gdf['ecole']

gdf.to_json()
gdf.to_file("results/base_data.json", driver="GeoJSON")  
gdf.to_excel("results/base_data.xlsx")


# for i in range(len(gdf["ecole"])):
#     nom = gdf["ecole"].iloc[i]
#     if " " in nom:
#         print(nom)
#     #gdf["ecole"].iloc[i] = mock_database.get(x["name"][i])