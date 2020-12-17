import gurobipy
import time
from utility import p_shape,p_df
penalty = 1000000000

verbose=0

def rtv(tv_graph, rt_graph, tv_cost, param):
    # p_shape(tv_graph)
    # p_shape(rt_graph)
    # p_shape(tv_cost)
    # p_df(tv_graph)
    # p_df(rt_graph)
    # p_df(tv_cost)
    model = gurobipy.Model('RTV-new')
    requests, unique_trips, vehicles = param['requests'], param['unique_trips'], param['vehicles']
    # print(requests, unique_trips, vehicles)
    kai = model.addVars(requests, vtype=gurobipy.GRB.BINARY, name='kai')
    eps = model.addVars(unique_trips, vehicles,
                        vtype=gurobipy.GRB.BINARY, name='eps')
    model.update()

    model.setObjective(gurobipy.quicksum(tv_cost[i, j] * eps[i, j] for i in range(
        unique_trips) for j in range(vehicles)) +
        gurobipy.quicksum(penalty*kai[i] for i in range(requests)), gurobipy.GRB.MINIMIZE)

    for j in range(vehicles):
        model.addConstr(gurobipy.quicksum(eps[i, j] for i in range(
            requests)) <= 1)

    for k in range(requests):
            model.addConstr(gurobipy.quicksum(rt_graph[k, h]*eps[h, c]  for c in range(vehicles) for h in range(unique_trips) )==1)

    start = time.time()
    
    #initialize params
    # for i in range(requests):
    #     kai[i].start=0
    # for i in range(unique_trips):
    #     for j in range(vehicles):
    #         eps[i,j].start=0
    # eps[2,4].start=1

    model.Params.method = 5
    model.optimize()
    interval=time.time()-start
    print("finish within: {}".format(interval))
    if model.status == gurobipy.GRB.Status.OPTIMAL:
        print(f'optimal value: {model.objVal}')
        if verbose:
            for v in model.getVars():
                if v.X>0.99:
                    print(f"{v.varName}：{v.X}")
    return interval