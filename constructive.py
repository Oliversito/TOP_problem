import pandas as pd
import numpy as np
import time

#reading data
df = pd.read_csv("TOP_instances_csv/TOP13.csv", sep=";")
data = df.to_numpy()

#number of nodes
num_nodes = int(data[0][0])

#visited nodes
visited = [0]

#not visited nodes
not_visited = [i for i in range(1, num_nodes)]

#weights vector
weights = data[3:, 2:3]

#positions
positions = data[3:, 0:2]

#number of travelers
num_travelers = int(data[1][0])

#time limit
tmax = int(data[2][0]) / 10

#paths
paths = [[0] for _ in range(num_travelers)]


def dist_matrix(positions):
    dist = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            dist[i, j] = np.sqrt((positions[i, 0] - positions[j, 0]) ** 2 + (positions[i, 1] - positions[j, 1]) ** 2)
    return dist


def ratio_matrix(distance_matrix, weights):
    ratio = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                ratio[i, j] = -1
            else:
                ratio[i, j] = ((weights[i] - weights[j]) / (distance_matrix[i, j] + 1))
    return ratio


def find_best_ratio(start_node, not_visited, ratio_matrix):
    best_ratio = 0
    best_node = 0
    for node in not_visited:
        ratio = ratio_matrix[start_node][node]
        if ratio > best_ratio:
            best_ratio = ratio
            best_node = node
    return best_node, best_ratio


def rutas(d, tmax):
    d = dist_matrix(positions)
    func_ob = []
    Tmax = [tmax for _ in range(num_travelers)]
    for i in range(len(Tmax)):
        while Tmax[i] > 0 and len(not_visited) > 0:
            for trav in range(num_travelers):
                if len(not_visited) > 0:
                    a_path = paths[trav]
                    last_node = a_path[-1]
                    next_node, best_ratio = find_best_ratio(start_node=last_node, not_visited=not_visited,
                                                             ratio_matrix=d)
                    a_path.append(next_node)
                    Tmax[trav] = Tmax[trav] - d[last_node][next_node]
                    func_ob.append(weights[next_node])
                    not_visited.remove(next_node)
    for trav in range(num_travelers):  # Agregar el último nodo a la lista después del ciclo
        a_path = paths[trav]
        a_path.append(num_nodes)
    return paths, func_ob


distancias = dist_matrix(positions=positions)
relaciones = ratio_matrix(distance_matrix=distancias, weights=weights)
rutas_final, obj = rutas(d=distancias, tmax=tmax)


def distancia_total_recorr(rutas, mat_dis, vec_pes):
    dista = []
    dis = 0
    for i in range(len(rutas)):
        for j in range(len(rutas[i])):
            dis += mat_dis[i][j]
        dista.append(dis)
        dis = 0
    return dista


distancias_por_ind = distancia_total_recorr(rutas=rutas_final, mat_dis=distancias, vec_pes=weights)

# Presentación de datos
for i, j in zip(rutas_final, distancias_por_ind):
    i.append(j)

objetivo = 0
for i in range(len(obj)):
    objetivo += obj[i]

obj_por_ind = []
suma = 0
for i in range(num_travelers):
    for j in range(len(rutas_final[i])):
        suma += obj[j]
    obj_por_ind.append(suma)
    
dat = pd.DataFrame(rutas_final)
print('Restricción: ', tmax)
print('Distancias por individuo: ', distancias_por_ind)
print('Rutas: \n', dat)
print('Vector objetivo: ', obj)
print('Función objetivo: ', objetivo)
print('Función por individuo: \n', obj_por_ind)
