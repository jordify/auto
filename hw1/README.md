## Submission
Author: Jorge Gómez 

Assignment: EEL6935 Homework #1

Title: Topology Management in Peer-to-Peer Systems

### Directory Contents
*  hw1.py \- The python source code for this assignment
*  paper/simData{1,2}D.png \- Results in picture form
*  paper/hw1.otl \- My notes taken while writing code and the report
*  paper/hw1.pdf \- A report detailing the results of this assignment
*  paper/hw1.tex \- The file used to generate the pdf report
*  paper/dist.bib \- Bibliography for works cited in the report

### Compiling and running

This assignment was written and tested with Python 2.7.1. There is no
compilation required just run with the command:

`python hw1.pdf -N 1000 -k 20 -d 1 -c 50`

That last command would have simulated over 50 cycles, a system of size
1000, a neighborhood size of 20, and a 1-Dimensional distance calculation.

`python hw1.pdf --help`

The program would output all of the possible command-line flags.
