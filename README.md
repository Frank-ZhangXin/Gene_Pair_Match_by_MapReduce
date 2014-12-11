Gene Pair Match by MapReduce
============================

## Introduction

**This program is written by Python 2.7.x**

The function of this tool is to map HiC interactions locations to genes and calculate the number of interactions between genes according to the following criteria.

* Mapping a location to a gene if they are on the same chromosome and overlap with each other.

* If a location is mapped to multiple genes, pick the one whose start is closest to the middle point of the location.

* Only interactions whose locations are mapped to genes are counted, otherwise it is ignored.

>The result of tool can be visualized by Cytoscape to show us the interactions between genes, which can be used to do further analysis by scientists. The tool will be based on MapReduce framework because the problem can be easily done by a divide and conquer algorithm.

----

## About the Data

>There are two kinds of input data in our study. One is the HiC chromosome interaction data. This data describes the two locations of chromosomes binding together. It has two locations of the chromosome with a starting point and ending point on each of them and a count. The second data is the whole human genes which has a gene id, chromosome id, a strand (DNA has double strands), the starting point and the ending point.

----

## File explaination

* **In *gene* file**

1st column: **gene id**:

2nd column: **chromosome id**

3rd column: **strand**

4th column: **start**

5th column: **end**

* **In *test* file**

1st column: **chromosome1 id**:

2nd column: **start1**

3rd column: **end1**

4th column: **chromosome2 id**

5th column: **start2**

6th column: **end2**


----

## Execution

1. There are two input files: gene and test(chromosome fragments)
2. Prompt window input:

>cat test | python hadoop_mapper.py | sort -k1,1 | python hadoop_reducer.py > output.txt


**Execution result** will be in *output.txt*

1st column is 1st chromosome fragment paired gene id

2nd column is 2nd chromosome fragment paired gend id

3rd column is **how many times** two fragments are paired



----
## Thanks
* [Cameron Loader](https://github.com/cloader89)
* Lu Liu
* Tzu-Sheng Hsu
* [Dr. Lama](http://www.cs.utsa.edu/~plama/)

