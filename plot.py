import json
import matplotlib.pyplot as plt
import numpy as np

no_of_stages = 9
stages = np.arange(1, no_of_stages + 1)
data = []
for x in stages:
    rider_file = open(str(x) + '.json')
    rider_raw = rider_file.read()
    data.append(json.loads(rider_raw))

# Get statistic of interest
key = []
for x in stages:
    key.append(data[x-1][0]['value'])


# Plot it
fig = plt.figure()
plt.plot(stages, key)
plt.xlabel('Stage')
plt.ylabel('Value')
plt.show()