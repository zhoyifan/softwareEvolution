#extract repeat matrix from jsinspect > result.txt

import re
import pandas as pd

from distutils.version import StrictVersion,LooseVersion

print("pandas version: ",pd.__version__)
directory="/media/z19941225110/CD_ROM_POS/master/SoftwareEvolution/Assignment-2-2020-master"
repeatBegin=r"Match - (\d+) instances"
repeatInstance=r"(\d+\.\d+(\.\d+)*)/(\S+\:\d+\,\d+)"
instanceCounter=0
listOfMaps=[] # list of "mapOfVersions"
mapOfVersions={}#version: list of string(file directory and line range)
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
            exit()
        instanceCounter=int(beginMatch.group(1))
        mapOfVersions={}
    elif(instanceMatch!=None):
        if(instanceCounter<=0):
            print("bug  ",line)
            exit()
        # print(instanceCounter,"  ",line )
        version=instanceMatch.group(1)
        repeatRange=instanceMatch.group(3)# file directory and line range
        mapOfVersions.setdefault(version,[]).append(repeatRange)
        instanceCounter-=1
        if(instanceCounter==0):
            for key in mapOfVersions.keys():
                mapOfVersions[key].sort()
            listOfMaps.append(mapOfVersions)
            mapOfVersions={}
result.close()




repeatPair={} #dict of dict. 
#version pair: {verion(only 2 versions): list of string(file path and line range)}
for mapNow in listOfMaps:
    # mapNow is
    # version: list of string(file directory and line range)
    group=list(mapNow.items())
    # "group" is list of tuple.
    # first element of tuple is version number
    # second element of tuple is list of string(file directory and line range).
    for i in range(0,len(group)):
        for j in range(i+1,len(group)):
            # print("group[i][1] is ",group[i][1])
            index=[group[i][0],group[j][0]]
            index.sort(key=LooseVersion)
            index=frozenset(index)
            repeatPair.setdefault(index,dict())
            repeatPair[index][group[i][0]]=repeatPair[index].get(group[i][0],[])+group[i][1]
            repeatPair[index][group[j][0]]=repeatPair[index].get(group[j][0],[])+group[j][1]



# merge(): merge line range intervals 
# input is list of pairs, output is list of pairs
#https://leetcode.com/problems/merge-intervals/discuss/21227/7-lines-easy-Python
def merge(intervals):
    out = []
    for i in sorted(intervals, key=lambda i: i[0]):
        # i[0]-1, since line range include start line and end line.
        if out and i[0]-1 <= out[-1][1]:
            out[-1][1] = max(out[-1][1], i[1])
        else:
            out += i,
            # do not omit the comma above, very important!
    return out
# sum_up(): sum intervals
# input is list of pairs, output is a number
def sum_up(intervals):
    res=0
    for start,end in intervals:
        res+=end-start+1
    return res
# after this for loop, key of repeatPair does not change, value will be a number.
pattern=r"(\S+)\:(\d+)\,(\d+)"
for versionPair, value in repeatPair.items():
    # value is {verion: list of string(file path and line range)}
    totalRepeat=0
    for version, repeats in value.items():
        # repeats is list of string(file path and line range)
        fileMap=dict()# file : list of line range, range may overlap.
        versionRepeat=0
        for repeat in repeats:
            # print("repeat is ",repeat)
            matchNow=re.match(pattern,repeat)
            if(matchNow==None):
                print("fileMap construction error.")
                exit()
            filePath=matchNow.group(1)
            lineStart=int(matchNow.group(2))
            lineEnd=int(matchNow.group(3))
            fileMap.setdefault(filePath,[])
            fileMap[filePath].append([lineStart,lineEnd])
        for filePath in fileMap:
            versionRepeat+=sum_up(merge(fileMap[filePath]))
        totalRepeat+=versionRepeat
    repeatPair[versionPair]=totalRepeat

releases=pd.read_csv(f"{directory}/jquery_releases.csv")
versions=list(releases.sort_values(by=['tag'])['tag'])
matrix=pd.DataFrame(index=versions,columns=versions)
# put the repeat value into the dataframe and export. 
for versionPair, value in repeatPair.items():
    versionList=list(versionPair)
    versionList.sort(key=LooseVersion,reverse=True)
    matrix.loc[versionList[0],versionList[1]]=value
matrix.to_csv(f"{directory}/output/repeatMatrix.csv")
print(matrix)





            