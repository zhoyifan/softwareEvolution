import pandas as pd
import math

from distutils.version import StrictVersion,LooseVersion

directory="/media/z19941225110/CD_ROM_POS/master/SoftwareEvolution/Assignment-2-2020-master"
cloc=pd.read_csv(f"{directory}/output/cloc.csv")
cloc=cloc.set_index('version')

repeat=pd.read_csv(f"{directory}/output/repeatMatrix.csv")
repeat=repeat.set_index('Unnamed: 0')
sim=repeat.copy()
for RowVersion,row in sim.iterrows():
    for ColVersion, value in row.items():
        if(RowVersion==ColVersion):
            sim.loc[RowVersion,ColVersion]=1
            continue
        if(math.isnan(value)==False):
            print(value)
            # print(f"{RowVersion}   {ColVersion}")
            a=value/(cloc.loc[RowVersion,'sum']+cloc.loc[ColVersion,'sum'])
            sim.loc[RowVersion,ColVersion]=a
            if(a>1):
                print(f"error,{RowVersion},{ColVersion} is greater than 1.")
                # exit()
numRow,numCol=sim.shape

sim = sim.reindex(index=pd.Index(sorted(sim.index, key=LooseVersion)))
sim=sim[sorted(sim.columns, key=LooseVersion)]

for row in range(0,numRow):
    for col in range(0,row):
        if(math.isnan(sim.iloc[row,col])):
            sim.iloc[row,col]=0
print(sim)
sim.to_csv(f'{directory}/output/similarity.csv',index=True)

