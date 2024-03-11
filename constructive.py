import pandas as pd
import numpy as np
import openpyxl
import time 

inicio = time.time()

#reading data
df = pd.read_csv("TOP_instances_csv/TOP1.csv", sep = ";")
data = df.to_numpy()

#number of nodes
num_nodes = int(data[0][0])

#visited nodes
visited = [0]

#not visited nodes
#not_visited = np.arange(1,num_nodes)
not_visited = [i for i in range(1,num_nodes)]
#weights vector
weights = data[3:, 2:3]

#positions
positions = data[3:, 0:2]

#number of travelers
num_travelers = int(data[1][0])

#time limit
tmax = int(data[2][0])
print('Restricción; ',tmax)
#paths
paths = [[0] for _ in range(num_travelers)]

def dist_matrix(positions):
    dist = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            dist[i,j] = np.sqrt((positions[i, 0]-positions[j, 0])**2 + (positions[i, 1]-positions[j, 1])**2)
    return dist

def ratio_matrix(distance_matrix, weights):
    ratio = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                ratio[i, j] = -1
            else:
                ratio[i, j] = weights[j]/distance_matrix[i, j]
    return ratio

def find_best_ratio(start_node, not_visited, ratio_matrix):
    best_ratio = 0
    best_node = 0
    for node in not_visited:
        ratio = ratio_matrix[start_node][node]
        if (ratio > best_ratio):
            best_ratio = ratio
            best_node = node
    return best_node, best_ratio

def rutas(d, tmax):
    d = dist_matrix(positions)
    #distancia_recorrida = 0
    func_ob = 0
    while tmax > 0 and len(not_visited)>0:   
        for trav in range(num_travelers):
            if len(not_visited)>0:
                a_path = paths[trav]
                last_node = a_path[-1]
                next_node, best_ratio = find_best_ratio(start_node=last_node, not_visited=not_visited, ratio_matrix=d)
                a_path.append(next_node)
                tmax = tmax - d[last_node][next_node]
                #distancia_recorrida += d[last_node][next_node]
                func_ob += weights[next_node]
                not_visited.remove(next_node)
    return paths, func_ob

distancias = dist_matrix(positions = positions)
relaciones = ratio_matrix(distance_matrix = distancias, weights = weights)
rutas_final, obj = rutas(d = distancias, tmax = tmax)

final = time.time()

tiempo_total = final - inicio

p = pd.DataFrame(rutas_final)
print(p)
print('Objetivo = ', obj)
print('Tiempo = ', tiempo_total)

#p.to_excel('archivo_prueba.xlsx',sheet_name='pandequeso', index = False, header = False)
#FALTA POR HACER:
## Añadir distancia recorrida por cada individuo
## Añadir función objetivo
## Organizar información en dataframe
