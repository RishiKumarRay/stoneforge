# %%

"""
=======================================
Load and crop Dataset Exercise
=======================================

A tutorial exercise about loading well log datasets
"""

import las2 # local las2 read
import numpy as np
import stoneforge
import  stoneforge.petrophysics.shale_volume as svsh

lasfile = las2.read('../datasets/DP1.las')
DATA = {} # data information from DP1 welllog

for i in range(len(lasfile['curve'])):
    name = lasfile['curve'][i]['mnemonic']
    DATA[name] = lasfile['data'][i]
    print(lasfile['curve'][i])
    
# %%
#====================================================================================#
### Removing NULL values (-999.) by set theory (intersection)

n = len(DATA["DEPT"])

IDX = []
for j in DATA:
    idx = []
    for i in range(n):
        if DATA[j][i] != -999.:
            idx.append(i)
    IDX.append(set(idx))

# clean indexes of original data
idx = set(IDX[0]).intersection(*IDX)

# clean data
c_DATA = {}
for j in DATA:
    c_DATA[j] = []
    for i in idx:
        c_DATA[j].append(DATA[j][i])

    print(j)
    print(np.histogram(c_DATA[j],5)[1])

# %%
#====================================================================================#
### Passing all curves to the international system S.I.

c_DATA["DEPT"] = np.array(c_DATA["DEPT"])*0.3048
c_DATA["SP"] = np.array(c_DATA["SP"])*0.001
c_DATA["CALI"] = np.array(c_DATA["CALI"])*0.0254
c_DATA["DRHO"] = np.array(c_DATA["DRHO"])*1000.
c_DATA["RHOB"] = np.array(c_DATA["RHOB"])*1000.
c_DATA["DT"] = 304800./np.array(c_DATA["DT"])

for j in c_DATA:
    print(j)
    print(np.histogram(c_DATA[j],5)[1])

# %%
#====================================================================================#
### testing some function

c_DATA["VSH"] = stoneforge.petrophysics.shale_volume.vshale_larionov(
    c_DATA["GR"],
    np.min(c_DATA["GR"]),
    np.max(c_DATA["GR"]),
    )

print("VSH")
print(np.histogram(c_DATA["VSH"],5)[0])
print(np.histogram(c_DATA["VSH"],5)[1])