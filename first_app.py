import streamlit as st
import pandas as pd
import numpy as np
import json_graph as jgraph
import pydeck as pdk
import geocoder
from scipy.spatial import KDTree

st.title('Ciclovias en Talca')

@st.cache
def load_node_data(graph):    
    df=pd.DataFrame.from_dict(graph.nodes, orient='index',columns=['lon','lat'])
    return df

@st.cache
def load_edge_data(graph):    
    df=pd.DataFrame.from_dict(graph.edges, orient='index')
    return df

@st.cache
def create_graph(DATA_PATH):
    return jgraph.json_graph(DATA_PATH)

def create_tree(DATA_PATH):
    return KDTree(node_data.values)

def geocode(address):
    address=address+", Talca CL"
    res=geocoder.osm(address)
    return res.ok,res.geojson

def nearest_node(coords,node_data,tree,address_data):
    d,i=tree.query(coords)
    point=node_data.iloc[i]
    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=address_data,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        get_line_color=[0, 0, 0],
    )
    return point,geojson_layer

#data_load_state = st.text('Loading data...')
DATA_PATH = 'talca_ciclovias.geojson'
graph=create_graph(DATA_PATH)
node_data = load_node_data(graph)
tree=create_tree(node_data)

#buscador de las rutas con el cual aplicar dikstra y bellman ford
st.header('Caminos mas cortos')
init_point=None
dest_point=None

initial = st.text_input('Ingrese direccion de inicio:') 
if initial:
    ret,address_data=geocode(initial)
    if ret:
        coords=address_data['features'][0]['geometry']['coordinates']
        init_point,initial_geojson=nearest_node(coords,node_data,tree,address_data)
        st.write('Punto de inicio mas cercano : '+str(init_point))
        layers.append(initial_geojson)
        r.update()
    else:
        st.write('Punto de inicio no encontrado')
        

destiny = st.text_input('Ingrese direccion de llegada:')
if destiny:
    ret,address_data=geocode(destiny)
    if ret:
        coords=address_data['features'][0]['geometry']['coordinates']
        dest_point,dest_geojson=nearest_node(coords,node_data,tree,address_data)
        st.write('Punto de destino mas cercano : '+str(dest_point))
        layers.append(dest_geojson)
        r.update()
    else:
        st.write('Punto de inicio no encontrado')

if st.button('Encontrar ruta mas corta'):
    if not init_point is None and not dest_point is None:
        st.write('inicio : '+ str(init_point.name))
        st.write('fin : '+ str(dest_point.name))
        dist,path=graph.dijkstra(init_point.name,'largo')
        st.write('distance : '+ str(dist[dest_point.name]))
    else:
        st.write('Debe ingresar puntos de inicio y destino')


#inicio del mapa con  el layer para graficar los datos

nodes_layer = pdk.Layer(
    "HexagonLayer",
    data=node_data,
    get_position="[lon, lat]",
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 100],
    extruded=True,
    coverage=0.5,
)

edges_layer = pdk.Layer(
    "GeoJsonLayer",
    data=graph.draw_graph(),
    pickable= True,
    stroked= False,
    filled= True,
    extruded= True,
    lineWidthScale= 20,
    lineWidthMinPixels= 2,
    getFillColor= [160, 160, 180, 200],  
    getRadius= 100,
    getLineWidth= 10,
    getElevation= 30
)
# Set the viewport location
view_state = pdk.ViewState(
    longitude=node_data.mean()['lon'], latitude=node_data.mean()['lat'], zoom=10, min_zoom=1, max_zoom=15, pitch=40.5, bearing=-27.36
)
layers=[nodes_layer,edges_layer]
# Combined all of it and render a viewport
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=layers,
    initial_view_state=view_state
)
st.pydeck_chart(r)
