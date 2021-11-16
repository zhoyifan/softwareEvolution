# Statement for our implementation on Assignment-2-2020

The "git clone" command will copy all versions of jQuery in the csv file into folder "input" and all the outputs including similarity matrices, interactive heatmaps(*.html) and so on are stored in "output" folder.
The commands that we used to generate heatmaps are in "commands.txt".

The execution flow of the scripts is shown in the flow chart "process.png"(or "process.dia", "process.svg"). 
1.prep.py:  download different versions of source code of jquery.
2.to_ignore.py: get the string consist of all names of files/folders that need to be excluded. 
3.jsinspect_repeat_repeatatitive.py: analyse the output from jsinspect, exclude the overlap (merge sort) and get the real repeat value.
4.count_file.py: execute cloc command in python code os.system(), accumulate the numbers of lines and generate a csv file.
5.calculate_sim.py: our customized method to calculate similarity.
6.heatmap.py: draw a heatmap, based on result of similarity and cloc.
7.bar.py: draw a barchart based on result of cloc.

For classic similarity method in paper, do not run "3.jsinspect_repeat_repeatatitive.py" and "5.calculate_sim.py". As substitution, run "-3.jsinspect_repeat_repeatatitive_classic.py" and "-5.calculate_sim_classic.py".













Template repository for the second assignment, containing a Docker project that clones the relevant version of jQuery, and sets up a working copy of JsInspect. 

# Dockerfile

The docker file sets up a docker image where three things 
are prepared:
- JsInspect is installed, such that you can run it from the 
command line.
- Cloc is installed.
- All versions of jQuery specified in `jquery_releases.csv` are 
cloned and downloaded to `/usr/jquery-data`.

When running the container a bash shell is opened such that you
can manually execute commands to run JsInspect and cloc. 

## Using this image

Build using `docker build -t 2imp25-assignment2 .`

Then run using 
`docker run -it --rm -v "$PWD/out:/out" 2imp25-assignment 2`. 
We again mount an out directory linked to the host file system
such that you can copy out files from the container. 

When the container is running you can execute bash commands
as if it is a virtual machine. 

# Suggestions

This repository does not contain all files and steps needed to
run the analysis for assignment 2. To analyze the capability of 
JsInspect to detect various clones you could for instance
consider expanding the `Dockerfile` to copy in the manually 
constructed clones to a directory `/usr/manual-clones`. Such 
that you can then run JsInspect on those files. 
