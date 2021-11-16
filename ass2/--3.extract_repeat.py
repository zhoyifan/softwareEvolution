#extract repeat matrix from jsinspect > result.txt

import re
import pandas as pd
print("pandas version: ",pd.__version__)
directory="/media/z19941225110/CD_ROM_POS/master/SoftwareEvolution/Assignment-2-2020-master"
repeatBegin=r"Match - (\d+) instances"
repeatInstance=r"\./(\d+\.\d+(\.\d+)*)/src/\S+\:(\d+)\,(\d+)"
instanceCounter=0
listOfMaps=[] # list of "mapOfVersions"
mapOfVersions={}#version:number of lines
result=open(f"{directory}/output/result.txt",'r')
numline=0
for line in result:
    numline+=1
    beginMatch=re.match(repeatBegin,line)
    instanceMatch=re.match(repeatInstance,line)
    if(beginMatch!=None):
        if(instanceCounter!=0):
            print("bug  ",line)
            print("instanceCounter is ",instanceCounter)
            break
        instanceCounter=int(beginMatch.group(1))
        mapOfVersions={}
    elif(instanceMatch!=None):
        if(instanceCounter<=0):
            print("bug  ",line)
            break
        # print(instanceCounter,"  ",line )
        version=instanceMatch.group(1)
        repeatStart=int(instanceMatch.group(3))
        repeatEnd=int(instanceMatch.group(4))
        repeatLine=repeatEnd-repeatStart+1
        mapOfVersions[version]=mapOfVersions.get(version,0)+repeatLine
        instanceCounter-=1
        if(instanceCounter==0):
            listOfMaps.append(mapOfVersions)
            mapOfVersions={}
result.close()
# print(listOfMaps)
releases=pd.read_csv(f"{directory}/jquery_releases.csv")
versions=list(releases.sort_values(by=['tag'])['tag'])
matrix=pd.DataFrame(0,index=versions,columns=versions)
for i in listOfMaps:
    group=list(i.items())
    for j in range(0,len(group)):
        for k in range(j+1,len(group)):
            version1=max(group[j][0],group[k][0])
            version2=min(group[j][0],group[k][0])
            if(version1==version2):
               continue 
            matrix.loc[version1,version2]+=group[j][1]+group[k][1]
matrix.to_csv(f"{directory}/output/repeatMatrix.csv")
print(matrix)

            