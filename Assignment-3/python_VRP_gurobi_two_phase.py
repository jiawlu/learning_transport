# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:34:58 2018

@author: jiaweil9
"""

import numpy as np
from gurobipy import *
import time

seed = [3,6,10,11]
K = 4

def CostCalculation():
    cost = np.zeros([N,K])
    for i in range(1,N):
        for j in range(K):
            cost[i,j] = distance[0,i]+distance[i,seed[j]]-distance[seed[j],0]
    return cost
    

def DistanceCalculation():
    distance = np.zeros([N,N])
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            distance[i,j] = np.sqrt((coordinate[i][0] - coordinate[j][0])**2 + (coordinate[i][1] - coordinate[j][1])**2)
    return distance


def GAP():
    
    nodes = list(range(1,N))
    vehicles = list(range(K))
    
    model = Model('GAP')
    
    x = model.addVars(nodes, vehicles, name = 'x', vtype = GRB.BINARY)
    model.setObjective(sum([cost[i,k]*x[i,k] for i in nodes for k in vehicles]), GRB.MINIMIZE)
    model.addConstrs(sum([demand[i]*x[i,k] for i in nodes]) <= 100 for k in vehicles)
    model.addConstrs(sum([x[i,k] for k in vehicles]) == 1 for i in nodes)
    
    model.optimize()
    
    if model.status == GRB.Status.OPTIMAL:
        vehicle_customer_map = {}
        solution = model.getAttr('x',x)
        for k in vehicles:
            current_customers = []
            for i in nodes:
                if solution[i,k] == 1:
                    current_customers.append(i)
            vehicle_customer_map[k] = current_customers
        return vehicle_customer_map
    else:
        return -1
        

def TSP():
    vehicle_route_map = {}
    travel_cost = {}
    total_travel_cost = 0
    
    for v in range(K):
        customer_list = vehicle_customer_map[v].copy()
        customer_list_0 = vehicle_customer_map[v].copy()  #without 0
        customer_list.append(0)
        
        model = Model('TSP')
        
        x = model.addVars(customer_list, customer_list, name = 'x', vtype = GRB.BINARY)
        b = model.addVars(customer_list, name = 'b')
        
        model.setObjective(sum([distance[i,j]*x[i,j] for i in customer_list for j in customer_list if i !=j ]), GRB.MINIMIZE)
        model.addConstrs(sum([x[i,j] for j in customer_list if i!=j]) == 1 for i in customer_list)
        model.addConstrs(sum([x[j,i] for j in customer_list if i!=j]) == 1 for i in customer_list)
        model.addConstrs(b[i] + 1 - 999*(1-x[i,j]) <= b[j] for i in customer_list_0 for j in customer_list_0 if i !=j)
        
        model.optimize()
        
        if model.status == GRB.Status.OPTIMAL:
            travel_cost[v] = model.objVal
            total_travel_cost += model.objVal
            current_route = []
            solution = model.getAttr('x',x)
            for i in customer_list:
                for j in customer_list:
                    if i != j and solution[i,j] == 1:
                        current_route.append(str(i)+'_'+str(j))
            vehicle_route_map[v] = current_route
    
    return vehicle_route_map, travel_cost,total_travel_cost


if "__main__" == __name__:
    
    demand = [0,24,19,34,23,30,45,23,20,7,57,43,15,15,18,9]
    coordinate = [[35,20],[40,5],[45,10],[50,5],[50,15],[50,25],[48,30],[42,35],
                  [25,35],[22,39],[10,30],[10,18],[15,15],[10,10],[20,7],[25,9]]
    N = len(demand)
    
    distance = DistanceCalculation()
    cost = CostCalculation()
    time_start = time.time()
    vehicle_customer_map = GAP()
    vehicle_route, travel_cost, total_travel_cost = TSP()
    time_end = time.time()
    print('total calculation time:',time_end - time_start)

    
