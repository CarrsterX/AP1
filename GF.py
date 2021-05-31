import networkx as nx
import streamlit as st
import time as tm
import pydeck as pdk
 
def grafo(node, edge):
    nom = 0
    lon = 0
    lat = 0
    
    node_data = node
    edge_data = edge
    G = nx.Graph()
    
    ni = 0
    nf = 0
    pe = 0

    for i in range(len(node_data)):
       nom = int(node_data.iloc[i].name)
       lon = float(node_data.iloc[i].lon) 
       lat = float(node_data.iloc[i].lat)    
       G.add_node(nom, lon=lon, lat=lat)
     
    for i in range(len(edge_data)):
        ni = int(edge_data.iloc[i].name[0])
        nf = int(edge_data.iloc[i].name[1])
        pe = float(edge_data.iloc[i].largo) 
        G.add_edge(ni,nf) 
        G[ni][nf]["weight"] = pe
    
    return G

def dijkstra(grafo, inicio, final):
    S = tm.time()
   
    G = grafo
    I = inicio
    F = final
    D = nx.dijkstra_path_length(G,I,F)

    E = tm.time()
    E = E-S
    
    R = nx.dijkstra_path(G,I,F)

    return R, E, D

def bellman_ford(grafo, inicio, final):
    S = tm.time()
    
    G = grafo
    I = inicio
    F = final
    D = nx.bellman_ford_path_length(G,I,F)
    
    E = tm.time()
    E = E-S
    
    R = nx.bellman_ford_path(G,I,F)

    return R, E, D

def camino(gf, caminos):
    datosTo_mapa = []
    diccionario = {}

    for i in range(len(caminos)):   
        if(i<len(caminos)-1):
            aux=i
            nodo_p = caminos[i]
            pos_p = []
            pos_p.append(gf.nodes[nodo_p]['lon'])
            pos_p.append(gf.nodes[nodo_p]['lat'])

            nodo_h = caminos[aux+1]
            pos_h = []
            pos_h.append(gf.nodes[nodo_h]['lon'])
            pos_h.append(gf.nodes[nodo_h]['lat'])
            
            diccionario = {"start":pos_p,"end":pos_h,"name":""+str(nodo_p)+"-"+str(nodo_h)}
            datosTo_mapa.append(diccionario)
    return datosTo_mapa

def layer_caminito(rallitas):
    dibujito = pdk.Layer(
        "LineLayer",
        data = rallitas,
        get_source_position = "start",
        get_target_position = "end",  
        picking_radius=8,
        get_width=2,
        get_color=255,
        highlight_color=[255, 255, 0],
        auto_highlight=True,
        pickable=True,
    )
    return dibujito