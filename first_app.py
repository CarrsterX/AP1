
import GF
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
    return point

#data_load_state = st.text('Loading data...')
DATA_PATH = 'talca_ciclovias.geojson'
graph=create_graph(DATA_PATH)
node_data = load_node_data(graph)
edge_data = load_edge_data(graph)
tree=create_tree(node_data)
G = GF.grafo(node_data, edge_data)


#inicio del mapa con  el layer para graficar los datos

nodes_layer = pdk.Layer(
    "HexagonLayer",
    data=node_data,
    get_position="[lon, lat]",
    auto_highlight=True,
    elevation_scale=2,
    radius=15,##radio del objeto generado
    pickable=True,
    elevation_range=[0, 50],
    extruded=True,
    coverage=0.5,
)
# Set the viewport location
view_state = pdk.ViewState(
    longitude=node_data.mean()['lon'], latitude=node_data.mean()['lat'], zoom=13, min_zoom=1, max_zoom=15, pitch=40.5, bearing=-27.36
)
layers1=[nodes_layer]
layers2=[nodes_layer]
# Combined all of it and render a viewport
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=layers1,
    initial_view_state=view_state
)
g = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=layers2,
    initial_view_state=view_state
)

#buscador de las rutas con el cual aplicar dikstra y bellman ford
st.header('Caminos mas cortos')
init_point=None
dest_point=None

initial = st.text_input('Ingrese direccion de inicio:') 
if initial:
    ret,address_data=geocode(initial)
    if ret:
        coords=address_data['features'][0]['geometry']['coordinates']
        init_point=nearest_node(coords,node_data,tree,address_data)
        st.write('Punto de inicio mas cercano : '+str(init_point))
    else:
        st.write('Punto de inicio no encontrado')
        

destiny = st.text_input('Ingrese direccion de llegada:')
if destiny:
    ret,address_data=geocode(destiny)
    if ret:
        coords=address_data['features'][0]['geometry']['coordinates']
        dest_point=nearest_node(coords,node_data,tree,address_data)
        st.write('Punto de destino mas cercano : '+str(dest_point))
    else:
        st.write('Punto de inicio no encontrado')

if st.button('Encontrar ruta mas corta'):
    if not init_point is None and not dest_point is None:
        st.write('inicio : '+ str(init_point.name)+'fin : '+ str(dest_point.name))
        Rb,Eb,Db = GF.bellman_ford(G, init_point.name, dest_point.name)
        Rd,Ed,Dd = GF.dijkstra(G, init_point.name, dest_point.name)
        
        st.write("El tiempo de ejecucion: ")
        st.write("Dijkstra: "+ str(Ed) +"              "+ "Bellman ford: " + str(Eb))
        st.write("Distancia: ")
        st.write("Dijkstra: "+ str(Dd) +"              "+ "Bellman ford: " + str(Db))
        st.write("")
        st.write("CAMINO GRAFICADO EN COLOR ROJO")
        camino_Dijkstra = GF.camino(G,Rd) 
        camino_Bellman = GF.camino(G,Rb) 
        caminitoDijkstra = GF.layer_caminito(camino_Dijkstra)
        caminitoBellman = GF.layer_caminito(camino_Bellman)
        layers1.append(caminitoDijkstra)
        layers2.append(caminitoBellman)
        r.update()
        g.update()
    else:
        st.write('Debe ingresar puntos de inicio y destino')
st.write("Mapa generado para representar caminos dijkstra")
st.write(r)
st.write("Mapa generado para representar caminos bellman ford")
st.write(g)


