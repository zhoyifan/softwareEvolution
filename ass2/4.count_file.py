# count number of lines
import pandas as pd
import re
import os
directory="/media/z19941225110/CD_ROM_POS/master/SoftwareEvolution/Assignment-2-2020-master"

exclude_dir=open(f'{directory}/output/cloc_exclude_dir.txt','r')
not_match_d=exclude_dir.read()
exclude_dir.close()
exclude_file=open(f'{directory}/output/cloc_exclude_file.txt','r')
not_match_f=exclude_file.read()
exclude_file.close()
command=rf'cloc --not-match-d "{not_match_d}" --not-match-f "{not_match_f}" --match-f "(\.js$)|(\.jsx$)" --skip-uniqueness'
print(command)
######################
# Remember to update the not-match/ignore value in command jsinspect!
##########################
releases=pd.read_csv(f"{directory}/jquery_releases.csv")
versions=list(releases.sort_values(by=['tag'])['tag'])

for ver in versions:
    # print(ver)
    commandNow=f"{command} {directory}/input/{ver} > {directory}/output/{ver}.txt"
   
    os.system(commandNow)
numLines=pd.DataFrame(index=versions,columns=["files","blank","comment","code",'sum'])
pattern=r"SUM:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)"
for ver in versions:
    clocResult=open(f"{directory}/output/{ver}.txt",'r')
    for i in clocResult:
        patternMatch=re.match(pattern,i)
        if(patternMatch!=None):
            numLines.loc[ver,"files"]=int(patternMatch.group(1))
            numLines.loc[ver,"blank"]=int(patternMatch.group(2))
            numLines.loc[ver,"comment"]=int(patternMatch.group(3))
            numLines.loc[ver,"code"]=int(patternMatch.group(4))
            numLines.loc[ver,"sum"]=numLines.loc[ver,"blank"]+numLines.loc[ver,"comment"]+numLines.loc[ver,"code"]
    clocResult.close()
numLines['version'] = numLines.index
numLines.to_csv(f"{directory}/output/cloc.csv",index=False)

