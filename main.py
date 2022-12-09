import sys
import numpy as np
import pandas as pd
import geopandas
import folium
import matplotlib.pyplot as plt
from folium.plugins import FloatImage

# list_var = ['note_moyen', 'note_vetuste', 'note_encadrement', 'note_encadrement_particulier',
#           'note_climat', 'note_cantine', 'note_abord_securise', 'note_relation_mairie']
list_var = ['note_vetuste', 'note_encadrement', 'note_climat', 'note_cantine', 'note_abord_securise']

list_var_display = ['Vétusté des locaux 🏫', 'Moyens humains 🧑‍🏫', 'Adaptation climat 🥵🥶🌿', 'Cantine 🥘🥕', 'Sécurité des abords 🚶‍♀️👮']

image_legend = 'images/legend_width100.png'

def get_form_responses(url):
     form_df = pd.read_csv(url+'export?gid=0&format=csv', index_col=0, parse_dates=['Timestamp'])
     form_df.columns = form_df.columns.str.replace(' ', '')
     form_df.rename(columns = {
          "Pourcommencer,veuillezsélectionnervotreécole:": 'nom_ecole',
          "Suruneéchellede1à5,commentévaluez-vouslesmoyensallouésauxécoles?":'note_moyen', 
          "Suruneéchellede1à5,commentévaluez-vousl'étatdevétustédesbâtimentsdevotreécole?":'note_vetuste',
          "Suruneéchellede1à5,commentjugez-vousleniveaud'encadrementglobaldesenfantsàl'école?":'note_encadrement',
          "Suruneéchellede1à5,commentconsidérez-vousleniveaud'encadrementdevotreenfant?":'note_encadrement_particulier',
          "Suruneéchellede1à5,pensez-vousquel'écoledevotreenfantsoitadaptéeaudérèglementclimatique?":'note_climat',
          "Suruneéchellede1à5,commentévaluez-vouslaqualitédesrepasservisàlacantine?":'note_cantine',
          "Suruneéchellede1à5,considérez-vousquelesabordsdevotreécolesoientsuffisammentsécurisés?":'note_abord_securise',
          "Suruneéchellede1à5,considérez-vousquevousêtessuffisammentécoutésparlaMairiedeToulouse?":'note_relation_mairie',
          }, inplace = True)
     # Drop rows when ecole has not been specified
     form_df = form_df.dropna(subset=['nom_ecole'])
     # Keep only the relevant columns for the map
     form_df = form_df[['nom_ecole'] + list_var]
     return(form_df)

def aggregate_form_responses(form_df):
     # Aggregate data -> average multiple answers
     df_agg = form_df.groupby('nom_ecole').agg({
#          'note_moyen': ['mean', 'count'],
          'note_vetuste': ['mean', 'count'],
          'note_encadrement': ['mean', 'count'],
#          'note_encadrement_particulier': ['mean', 'count'],
          'note_climat': ['mean', 'count'],
          'note_cantine': ['mean', 'count'],
          'note_abord_securise': ['mean', 'count'],
#          'note_relation_mairie': ['mean', 'count'],
          'note_encadrement': ['mean', 'count'],
          })
     # Flatten the multi-index, easier to analyze after
     df_agg.columns = df_agg.columns.map('_'.join)
     # Rename columns
     #df_agg.rename(columns = {'note_moyen_count': 'compte'}, inplace = True)
     #df_agg.columns = df_agg.columns.str.replace('_count', '')
     df_agg.columns = df_agg.columns.str.replace('_mean', '')
     return(df_agg) 

def get_ecole_geodata():
     '''
     base_data is generated using `get_ecole_location.py` based on 
     opendata files downloaded separately
     '''
     # Get the school location data (generated with get_ecole_location.py)
     gdf = geopandas.read_file('./results/base_data.json')
     gdf = gdf[['nom_ecole', 'geometry']]
     # Fill the df with empty data
     for var in list_var:
          gdf[var] = np.nan
          gdf[var+'_count'] = 0
     gdf = gdf.set_index('nom_ecole') # make ecole the index
     gdf['ecole'] = gdf.index # but keep an ecole column
     return(gdf)


if __name__ == "__main__":
     url = sys.argv[1]
     form_df = get_form_responses(url)
     gdf = get_ecole_geodata()
     df_agg = aggregate_form_responses(form_df)
     gdf.update(df_agg) # .set_index('nom_ecole')

     # For convenience with geopandas, with remove the index before plotting
     gdf=gdf.reset_index()

     m = gdf[['ecole', list_var[0], list_var[0]+'_count', 'geometry']].explore(
          column=list_var[0],  # make choropleth based on "BoroName" column
          #scheme="naturalbreaks",  # use mapclassify's natural breaks scheme
          #categorical=True,
          cmap = 'RdYlGn',
          marker_kwds=dict(radius=10, fill=True), # make marker radius 10px with fill
          legend=False, # show legend
          tooltip=False,
          popup=True,
          k=5, # use 10 bins
          vmin=1, vmax=5,
          tiles=None,
          #legend_kwds= dict(caption='Moyenne des notes (de 1 à 5)', colorbar=True, max_labels=5),
          name=list_var_display[0], # name of the layer in the map
          missing_kwds={'color': 'darkgrey', 'label': 'Pas de réponse'},
          overlay=False
     )

     list_var.pop(0)
     list_var_display.pop(0)
     #list_var.remove('note_moyen')
     for k, var in enumerate(list_var): 
          gdf[['ecole', var, var+'_count', 'geometry']].explore(
               m=m, # pass the map object
               column=var,  # make choropleth based on "BoroName" column
               marker_kwds=dict(radius=10, fill=True), # make marker radius 10px with fill
               cmap='RdYlGn',
               tooltip=False,
               popup=True, #'ecole',
               legend=False,
               k=5, # use 10 bins
               vmin=1, vmax=5,
          #      #tooltip_kwds=dict(labels=False), # do not show column label in the tooltip
               name=list_var_display[k], # name of the layer in the map
               missing_kwds={'color': 'darkgrey'},
               show=False,
               overlay=False
          )

     folium.TileLayer('cartodbpositron', control=False).add_to(m)  # use folium to add alternative tiles
     folium.LayerControl(position="topleft", collapsed=False).add_to(m)  # use folium to add layer control
     FloatImage(image_legend, bottom=30, left=1).add_to(m)
     m.save("carte.html")
     gdf.to_csv("./results/resultats.csv")
























# path_to_data = "./data/ecoles-elementaires-publiques.geojson"
# gdf = geopandas.read_file(path_to_data)
# gdf = gdf.loc[:, ("ecole", "codsti", "index", "codpos", "rne", "libelle", "secteur_action_scolaire", "geometry")]

# # creation de notes fictives aléatoires pour le moment
# gdf['note_rue_scolaire'] = np.random.randint(1, 4, gdf.shape[0])
# gdf['note_encadrement'] = np.random.randint(1, 4, gdf.shape[0])
# gdf['note_pollution'] = np.random.randint(1, 4, gdf.shape[0])
# gdf['note_icu'] = np.random.randint(1, 4, gdf.shape[0])

# # geometry est encodé en MULTIPOINT mais ne contient qu'un POINT donc on l'explode
# # cela permets de corriger un bug plus tard avec popup et tootip de explore() qui ne fonctionnent pas
# # avec MULTIPOINT https://github.com/geopandas/geopandas/issues/2190
# gdf = gdf.explode()
# #gdf.head()

# m = gdf[['ecole', 'note_rue_scolaire', 'geometry']].explore(
#      column="note_rue_scolaire",  # make choropleth based on "BoroName" column
#      #scheme="naturalbreaks",  # use mapclassify's natural breaks scheme
#      #categorical=True,
#      cmap = 'RdYlGn',
#      marker_kwds=dict(radius=10, fill=True), # make marker radius 10px with fill
#      legend=False, # show legend
#      popup='ecole',
#      k=3, # use 10 bins
#      vmin=1, vmax=3,
#      tiles=None,
#      #legend_kwds=dict(caption='',colorbar=True, fmt="{:5.2f}"), # do not use colorbar
#      name="rue" # name of the layer in the map
# )

# gdf[['ecole', 'note_encadrement', 'geometry']].explore(
#      m=m, # pass the map object
#      column="note_encadrement",  # make choropleth based on "BoroName" column
#      cmap = 'RdYlGn',
#      popup='ecole',
#      legend=False,
#      marker_kwds=dict(radius=10, fill=True), # make marker radius 10px with fill
#      k=3, # use 10 bins
#      vmin=1, vmax=3,
# #      tooltip="name", # show "name" column in the tooltip
# #      #tooltip_kwds=dict(labels=False), # do not show column label in the tooltip
#       name="encadrement" # name of the layer in the map
# )

# #title_image = 'https://scrouzet.github.io/observatoiredesecoles/title_image.png'
# #folium.plugins.FloatImage(title_image, bottom=75, left=75).add_to(m)

# # loc = 'Observatoire des écoles Toulousaines'
# # title_html = '''
# #              <h3 align="center" style="font-size:16px"><b>{}</b></h3>
# #              '''.format(loc)
# # m.get_root().html.add_child(folium.Element(title_html))

# folium.TileLayer('cartodbpositron', control=False).add_to(m)  # use folium to add alternative tiles
# folium.LayerControl(position="topleft", collapsed=False).add_to(m)  # use folium to add layer control

# m.save("carte.html")
# m.save("results/map_gdf.html")