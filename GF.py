import networkx as nx
import streamlit as st
import time as tm

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
       lon = int(node_data.iloc[i].lon) 
       lat = int(node_data.iloc[i].lat)    
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