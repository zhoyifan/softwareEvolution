# Introduction

This repository serves as an example starting point for the first assignment of Software Evolution 2019-2020.
Inside is a DockerFile and example Python script that reads input from a directory `/input`, and that writes 
output to `/output/links.csv` containing the identified trace links. 

The source code you hand in should be a docker project, with in the root directory a `Dockerfile`. If you 
are unfamilar with [Docker](https://www.docker.com/) please take some time to read up on its concepts, and
following a getting started guide. 

This readme describes the requirements your solution should satisfy, including the format of the input and
output files, and how this template can be used, as well as what docker commands we will use while grading
your submission. 

Please note that this repository is a starting point for a Python 3 project. However, you are 
free to use any programming language and environment, as long as the project you submit is a Docker project
that runs on Docker for Linux containers, and which can be run using the commands specified below. 

# Requirements

Your program should read two `.csv` files, `low.csv`, and `high.csv` from the folder `/input`, match the 
requirements in `high.csv` with `low.csv` as described in the assignment, and then output a `links.csv`
in the `/output` directory. To determine which match type should be used, the first command line argument 
provided to your program is an integer specifying which match type should be used. 

- **0**: No filtering.
- **1**: Similarity of at least .25.
- **2**: Similarity of at least .67 of the most similar low level requirement. 
- **3**: Your own custom technique. 

Each `.csv` file used should use `,` as a delimiter between cells, `\n` as a delimiter between lines, and 
`"` as a quote character. 

The files in the input directory have two columns, `id`, and `text`. Where `id` is
the identifier of the requirement, and `text` is the contents of the requirement. 

`links.csv`, generated by your program, should have two columns. `id`, which contains the `id` of 
the **high** level requirement, 
and `links` which is a comma separated list of all **low** level requirement ids that link to that particular
**high** level requirement. 

**Note:** if for a particular high level requirement you find no links, then there
should be an entry in `links.csv` for that **high** level requirement with an empty `links` list. 

Finally, you should read the ground truth `input/links.csv`, compare this to the links generated by
your tool (`output/links.csv`), and use the ground truth to compute the precision, recall, and F-measure. 

# Using this DockerFile

To run the project the following docker command will be used: 

`docker build -t 2imp25-assignment-1 ./`

This builds a docker image according to the `DockerFile`, and tags the built image as `2imp25-assignment-1`. 

For example to run the docker image using the matcher that requires a similarity of at least .25 (match type: 1) we 
execute the following command.

Windows (Powershell): `docker run --rm -v "$pwd\dataset-1:/input" -v "$pwd\output:/output" 2imp25-assignment-1 1`

Linux: `docker run --rm -v "$PWD/dataset-1:/input" -v "$PWD/output:/output" 2imp25-assignment-1 1`

The command runs the previously built container. The `-v` commands mounts two directories ([Volumes](https://docs.docker.com/storage/volumes/)) on the host
file system in the container. One `$PWD/dataset-1:/input` maps the host directory `./dataset-1` to the 
container folder `./input`, and the second one maps the host directory `./output` to container directory
`/output`. `2imp25-assignment-1` is the name of the tag that was given during the build step, and the 
final argument `1` is the match type that should be used by the trace link finder. 

By providing a different host directory for the input mount a different dataset can be provided to the 
program. e.g. this repository provides two datasets, `dataset-1` and `dataset-2`. However, when grading
we will be using a third, previously unseen dataset to evaluate how your algorithm performs. 

Therefore, please take care such that we can run your submitted source code using the two described docker commands,
and extract a `links.csv` file. **If your DockerFile fails to build, no output file is written to `/output/links.csv`, or
the `/output/links.csv` file is not formatted correctly, points will be subtracted.** 