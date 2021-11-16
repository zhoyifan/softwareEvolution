'''
Script clones each version of jQuery in the input csv
file into its own directory.
'''

import csv
import os

releases = []
directory='/media/z19941225110/CD_ROM_POS/master/SoftwareEvolution/Assignment-2-2020-master'
if __name__ == "__main__":
    with open(f"{directory}/jquery_releases.csv", mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            releases.append(row)
            line_count += 1


        print('Processed '+str(line_count)+' lines.')
    for release in releases:
        # print(release['tag'])
        command = f"git clone -b {release['tag']} --single-branch --depth 1 https://github.com/jquery/jquery.git {directory}/input/{release['tag']}"

        print("Executing ",command)
        os.system(command)
