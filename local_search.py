import constructive
import pandas as pd
import time
import random
import numpy as np

alpha = 1

inicio = time.time()

sol_ini = constructive.rutas_final.copy()
no_vis = constructive.not_visited.copy()
ganancias = constructive.scores.copy()
pesos = constructive.weights.copy()
distancias = constructive.distancias_por_ind.copy()
matriz = constructive.distancias.copy()

def distancia_total_recorr(rutas, mat_dis):
    dista = []
    dis = 0
    for i in range(len(rutas)):
        #print(f'Rutas: {rutas}, Rutas en i: {rutas[i]}')
        for j in range(len(rutas[i])-1): # corrected line
            dis += mat_dis[rutas[i][j]-1][rutas[i][j+1]-1]
        dista.append(dis)
        dis = 0
    return dista

def swap(sol, j,k):
    a = sol.copy()
    pos1 = a[j]
    pos2 = a[k]
    a[j] = pos2
    a[k] = pos1
    return a

def insertDown(solt,i,j):
        s = list(solt.copy())
        aux = s[i]
        s.pop(i)
        s.insert(j, aux)
        return s

def reversada(solt, i, j):
        s = list(solt.copy())
        s[i:j+1] = reversed(s[i:j+1])
        return s

def orden(solucion, distancias):
    nuevas_soluciones = []
    for i in range(len(solucion)):
        mejor_distancia = distancias[i]
        nueva_solucion = solucion[i][:]
        for j in range(1, len(solucion[i])-1):
            for k in range(1, len(solucion[i])-1):
                if alpha == 1:
                    posible = swap(nueva_solucion, j, k)
                    aux = [posible]
                    dis_posible = distancia_total_recorr(aux, matriz)[0]
                    if dis_posible < mejor_distancia:
                        mejor_distancia = dis_posible
                        nueva_solucion = posible
                        if k < j:  # Elimina cruces que queden después de eliminar cruces
                            j = k
                            break
                elif alpha == 2:
                    posible = insertDown(nueva_solucion, j, k)
                    aux = [posible]
                    dis_posible = distancia_total_recorr(aux, matriz)[0]
                    if dis_posible < mejor_distancia:
                        mejor_distancia = dis_posible
                        nueva_solucion = posible
                        if k < j:  # Elimina cruces que queden después de eliminar cruces
                            j = k
                            break
                elif alpha == 3:
                    posible = reversada(nueva_solucion, j, k)
                    aux = [posible]
                    dis_posible = distancia_total_recorr(aux, matriz)[0]
                    if dis_posible < mejor_distancia:
                        mejor_distancia = dis_posible
                        nueva_solucion = posible
                        if k < j:  # Elimina cruces que queden después de eliminar cruces
                            j = k
                            break
        nuevas_soluciones.append(nueva_solucion)
        distancias[i] = mejor_distancia
    return nuevas_soluciones, distancias

#BEST IMPROVEMENT
def buscar_mejor_solucion(solucion, distancias):
    mejor_solucion = solucion
    mejor_distancia = sum(distancias)

    solucion_actual = solucion
    distancia_actual = mejor_distancia

    while True:
        solucion_actual, distancias = orden(solucion_actual, distancias)
        distancia_actual = sum(distancias)

        if distancia_actual < mejor_distancia:
            mejor_solucion = solucion_actual
            mejor_distancia = distancia_actual
        else:
            break

    return mejor_solucion, mejor_distancia


rutas_final, mejor_distancia = buscar_mejor_solucion(sol_ini, distancias)

fin = time.time()
tiempo = 1000*(fin-inicio)

def distancia_total(rutas, mat_dis):
    dista = []
    dis = 0
    for i in range(len(rutas)):
        for j in range(len(rutas[i])-1): # corrected line
            dis += mat_dis[rutas[i][j]-1][rutas[i][j+1]-1]
        dista.append(dis)
        dis = 0
    return dista

def ganancias(rutas):
    a = []
    suma = 0
    for i in range(len(rutas)):
        for j in range(len(rutas[i])-1):
            suma += pesos[rutas[i][j]-1][0]
        a.append(suma)
        suma = 0
    return a

def num_nod(rutas):
    n = []
    for i in range(len(rutas)):
        n.append(len(rutas[i]))
    return n

distancias_por_ind = distancia_total(rutas=rutas_final, mat_dis=matriz)
numero = num_nod(rutas_final)
scores = ganancias(rutas_final)
objetivo = sum(scores)
#print(f'Solunción LS{alpha}: {rutas_final}')

##########################################################################
'''Esto elimina nodos repetidos en las rutas'''
def eliminar_repetidos(lista):
    res = []
    for i in lista:
        if i not in res:
            res.append(i)
    return res

def eliminar_repetidos_de_todas(lista):
    res = []
    for sublista in lista:
        res.append(eliminar_repetidos(sublista))
    return res

elim = eliminar_repetidos_de_todas(eliminar_repetidos(rutas_final))
#print(f'Distancias: {distancias_por_ind}')

'''Estos son los vecinadrios que me pidió Rivera'''
def infactible(rutas, distancias):
    for i in range(len(distancias_por_ind)):
        if distancias[i] > constructive.tmax:
            while (distancias[i] > constructive.tmax):
                rand = random.randint(1, len(rutas[i])-2)
                rutas_copy = rutas.copy()
                rutas_copy[i].pop(rand)
                new_dist = distancia_total(rutas_copy, matriz)
                if new_dist[i] < distancias[i]:
                    distancias[i] = new_dist[i]
                    rutas = rutas_copy.copy()                              
    return rutas, distancias

r,d = infactible(elim, distancias_por_ind)
print(f'Restricción:{constructive.tmax}')
print(f'Nuevas rutas: {r}')
print(f'Nuevas distancias: {d}')
print(f'NO VISITADOS {no_vis}')
print(f'GANANCIAAAAS: {ganancias(r)}')

def add_nodes(rutas, not_visited, mat_dist):
    tmax = constructive.tmax
    act_dis = distancia_total(rutas, mat_dist)
    best_dis = 10000000
    best_i = 0
    best_j = 0
    best_n = 0
    no = not_visited.copy()
    for i in range(len(rutas)):
        for j in range(1,len(rutas[i])-2):
            for k in range(len(no)):
                n = not_visited[k]
                n1 = rutas[i][j-1]
                n2 = rutas[i][j]
                new_dist = act_dis[i] - mat_dist[n1-1][n2-1] + mat_dist[n1-1][n-1] + mat_dist[n-1][n2-1]
                if new_dist <= tmax and new_dist < best_dis:
                    best_dis = new_dist
                    best_i = i
                    best_j = j
                    best_n = n      
    if best_n != 0:
        rutas[best_i].insert(best_j, best_n)
        distancias = distancia_total(rutas, mat_dist)
        gana = ganancias(rutas)
    return rutas, no, distancias, gana

a, b, c, gana = add_nodes(r, no_vis, matriz)
print(f'Rutas:{a}')
print(f'No visitados:{b}')
print(f'NDIS: {c}')
print(f'Gana: {gana}')
