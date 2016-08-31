# coding: utf-8
import cvxpy as cvx
import numpy as np
import json

# Load newest dataset
rider_file = open('20.json')
rider_raw = rider_file.read()
riders = json.loads(rider_raw)

# Helper to find index from name
def find_name(list, name):
    return int(next((x for x in list if x['name'] == name), None)['id']) - 1

# What was our previous team constellation?
old_team = []
old_team.append(find_name(riders, 'Peter Sagan'))
old_team.append(find_name(riders, 'Chris Froome'))
old_team.append(find_name(riders, 'Matteo Bono'))
old_team.append(find_name(riders, u'Michael Mørkøv'))
old_team.append(find_name(riders, 'Marcel Kittel'))
old_team.append(find_name(riders, 'Bernhard Eisel'))
old_team.append(find_name(riders, 'Fabio Sabatini'))
old_team.append(find_name(riders, 'Daniel Teklehaimanot'))
old_team.append(find_name(riders, u'Chris Anker Sørensen'))
# Turn into NP array
old_team = np.array(old_team)

# Weights (value, popularity...)
v_data = []
w_data = []
# Trend
t_data = []

for rider in riders:
    v_data.append(float(rider['value']))
    w_data.append(0.01 * float(rider['popularity']))
    t_data.append(float(rider['growth_tot']))

v = np.array(v_data)
w = np.array(w_data)
t = np.array(t_data)

print t

x = cvx.Bool(len(riders))

popularity = cvx.Variable()
cost = cvx.Variable()
growth = cvx.Variable()

objective = cvx.Maximize(popularity)

constraints = []

constraints.append(popularity == w * x)
constraints.append(growth == t * x)
constraints.append(cost == v * x)
constraints.append(cost <= 62100000)
constraints.append(sum(x) == 9)

# Exclude/Include riders
constraints.append(x[find_name(riders, 'Rafal Majka')] == 0)
constraints.append(x[find_name(riders, 'Marcel Kittel')] == 1)

constraints.append(x[find_name(riders, 'Chris Froome')] == 1)
constraints.append(x[find_name(riders, 'Daniel Teklehaimanot')] == 1)
constraints.append(x[find_name(riders, 'Fabio Sabatini')] == 1)
constraints.append(x[find_name(riders, 'Matteo Bono')] == 1)


#constraints.append(x[find_name(riders, 'Nairo Quintana')] == 0)

problem = cvx.Problem(objective, constraints)
problem.solve()

print "Metric:", problem.value
print "Team Value:", cost.value

team = np.where(x.value > 0.99)[0]

#print np.sort(team)
#print np.sort(old_team)

for rider in team:
    print riders[rider]['name']

