import cvxpy as cvx
import numpy as np
import json


rider_file = open('1.json')
rider_raw = rider_file.read()
riders = json.loads(rider_raw)

v_data = []
w_data = []

for rider in riders:
    v_data.append(float(rider['value']))
    w_data.append(0.01 * float(rider['popularity']))

v = np.array(v_data)
w = np.array(w_data)

x = cvx.Bool(len(riders))

popularity = cvx.Variable()
cost = cvx.Variable()

objective = cvx.Maximize(popularity)

constraints = []

constraints.append(popularity == w * x)
constraints.append(cost == v * x)
constraints.append(cost <= 50000000)
constraints.append(sum(x) == 9)

problem = cvx.Problem(objective, constraints)
problem.solve()

#print "optimal value", problem.value
#print cost.value

team = np.where(x.value > 0.99)[0]

for rider in team:
    print riders[rider]['name']