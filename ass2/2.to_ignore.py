import os
import pandas as pd
to_exclude_dir=set()
to_exclude_file=set()
directory="/media/z19941225110/CD_ROM_POS/master/SoftwareEvolution/Assignment-2-2020-master"
releases=pd.read_csv(f"{directory}/jquery_releases.csv")
versions=tuple(releases.sort_values(by=['tag'])['tag'])
# for version in os.listdir(f"{directory}/input/"):
for version in versions:
    if (os.path.isfile(os.path.join(f"{directory}/input/", version))):
        if(version[-3:]==".js")or(version[-4:]==".jsx"):
            print("bug, there is a file directly in the input folder.")
            exit()
    dirVer=f"{directory}/input/{version}/"
    for i in os.listdir(dirVer):
        if( os.path.isdir(os.path.join(dirVer, i)) ):
            iRegex=i.replace(".",r"\.")
            to_exclude_dir.add(iRegex)        
        elif((i[-3:]==".js")|(i[-4:]==".jsx")):
            iRegex=i.replace(".",r"\.")
            to_exclude_file.add(iRegex)
# print("|".join(to_exclude))

to_exclude_dir.remove('src')
to_exclude_file.remove(r'jquery\.js')


print("In cloc, ")

cloc_exclude_dir='$|^'.join(to_exclude_dir)
cloc_exclude_dir='^'+cloc_exclude_dir+'$'
print(f"exclude directory: {cloc_exclude_dir}")
exclude_dir_export=open(f'{directory}/output/cloc_exclude_dir.txt','w')
exclude_dir_export.write(cloc_exclude_dir)
exclude_dir_export.close()

cloc_to_exclude_file=set(to_exclude_file)
cloc_to_exclude_file.add(r"intro\.js")
cloc_to_exclude_file.add(r"outro\.js")
cloc_to_exclude_file.add(r".*Test\.js")
cloc_exclude_file='$|^'.join(cloc_to_exclude_file)
cloc_exclude_file='^'+cloc_exclude_file+'$'
print(f"exclude file: {cloc_exclude_file}")
exclude_file_export=open(f'{directory}/output/cloc_exclude_file.txt','w')
exclude_file_export.write(cloc_exclude_file)
exclude_file_export.close()


print("\n\n In jsinspect, ")
jsin_to_exclude=to_exclude_dir.union(to_exclude_file)
jsin_to_exclude_str="|".join(jsin_to_exclude)
jsin_extra_files=r"intro\.js|outro\.js|Test\.js"
command=rf'jsinspect --ignore "{jsin_to_exclude_str}|{jsin_extra_files}" -I -L /input/ > /output/result.txt'
print(f"command is : {command}\n\n")
print("please copy, modify, paste and run the command in docker.\n")
print("Command will not be run in python code with os.system(), since default value of max RAM can not be output with command.\n")



# and then execute command,don't forget to add intro\.js|outro\.js|Test\.js
# intro.js, outro.js: will report some bug when in jsinspect.
# Test.js will report some bug in cloc. 
# 1.0.4/src/jquery/coreTest.js
# "Complex regular subexpression recursion limit (32766) exceeded at /usr/bin/cloc line 7327."

######################
# Remember to update the not-match/ignore value in command cloc!
##########################
         