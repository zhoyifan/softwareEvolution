import pandas as pd
import math

from distutils.version import StrictVersion,LooseVersion

directory="/media/z19941225110/CD_ROM_POS/master/SoftwareEvolution/Assignment-2-2020-master"
cloc=pd.read_csv(f"{directory}/output/cloc.csv")
cloc=cloc.set_index('version')

def getCos(V_i,C_i,C_j,V_j):
    denominator=math.sqrt(V_i**2+C_i**2)*math.sqrt(C_j**2+V_j**2)
    return (V_i*C_j+C_i*V_j)/denominator

repeat=pd.read_csv(f"{directory}/output/repeatMatrix.csv")
repeat=repeat.set_index('Unnamed: 0')
sim=repeat.copy()
for RowVersion,row in sim.iterrows():
    for ColVersion, value in row.items():
        if(RowVersion==ColVersion):
            sim.loc[RowVersion,ColVersion]=1
            continue
        if(math.isnan(repeat.loc[RowVersion,ColVersion])==False):
            # print(value)
            # print(f"{RowVersion}   {ColVersion}")
            # a=(value/cloc.loc[RowVersion,'sum']+repeat.loc[ColVersion,RowVersion]/cloc.loc[ColVersion,'sum'])/2
            a=getCos(cloc.loc[RowVersion,'sum'],repeat.loc[RowVersion,ColVersion],repeat.loc[ColVersion,RowVersion],cloc.loc[ColVersion,'sum'])
            versionList=[RowVersion,ColVersion]
            versionList.sort(key=LooseVersion,reverse=True)
            sim.loc[versionList[0],versionList[1]]=a
            sim.loc[versionList[1],versionList[0]]=math.nan
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

