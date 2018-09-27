# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 11:50:18 2018

@author: jiaweil9
"""

from gurobipy import *
import math

K = 4

def VRP_gurobi():
    vehicles = list(range(K))
    nodes = list(range(N))
    nodes_0 = list(range(1,N))
    cost = {}
    for i in nodes:
        for j in nodes:
            if i != j:
                cost[(i,j)] = math.sqrt((coordinate[i][0] - coordinate[j][0])**2 + (coordinate[i][1] - coordinate[j][1])**2)

    arcs = list(cost.keys())
    
    model = Model('VRP')
    
    x = model.addVars(arcs, vehicles, name = 'x', vtype=GRB.BINARY)
    y = model.addVars(nodes, vehicles, name = 'y', vtype=GRB.BINARY)
    b = model.addVars(nodes, vehicles, name = 'b')
    
    model.setObjective(sum([x[i,j,k]*cost[i,j] for i in nodes for j in nodes if i!= j for k in vehicles]),GRB.MINIMIZE)
    
    model.addConstrs((sum([y[i,k] * demand[i] for i in nodes]) <= 100 for k in vehicles), "c2")
    model.addConstr((sum([y[0,k] for k in vehicles]) == K), "c3_1")
    model.addConstrs((sum([y[i,k] for k in vehicles]) == 1 for i in nodes if i != 0), "c3_2")
    
    model.addConstrs((sum([x[i,j,k] for j in nodes if i!=j]) == y[i,k] for k in vehicles for i in nodes), "c5")
    model.addConstrs((sum([x[j,i,k] for j in nodes if i!=j]) == y[i,k] for k in vehicles for i in nodes), "c6")
    
    model.addConstrs((b[i,k] + 1 - 999*(1-x[i,j,k]) <= b[j,k] for k in vehicles for i in nodes_0 for j in nodes_0 if i !=j), "c7")
    
    model.optimize()
    
    if model.status == GRB.Status.OPTIMAL:
        vehicle_route_map = {}
        solution = model.getAttr('x',x)
        for k in vehicles:
            current_route = []
            for i,j in arcs:
                if solution[i,j,k] == 1:
                    current_route.append(str(i)+'_'+str(j))
            vehicle_route_map[k] = current_route
        return vehicle_route_map, model.objVal
    else:
        return -1, -1
            

if "__main__" == __name__:
    
    demand = [0,24,19,34,23,30,45,23,20,7,57,43,15,15,18,9]
    coordinate = [[35,20],[40,5],[45,10],[50,5],[50,15],[50,25],[48,30],[42,35],
                  [25,35],[22,39],[10,30],[10,18],[15,15],[10,10],[20,7],[25,9]]
    N = len(demand)
    
    vehicle_route,total_travel_cost = VRP_gurobi()
