This package contains the code for COLA Version 3.0

---------------------------------------------------------------------------------------------------------
UNPACKING: unzip the file into a directory

COMPILING: Under Linux, Solaris, Cygwin (tested): run make, an executable file COLA is generated.
           Under Windows: we suggest to use the free IDE Dev-C++ (http://www.bloodshed.net/devcpp.html,
                          we used the version 4.9.9.1).
                          we provide a project file (Constraint solver.dev) to be loaded
                          otherwise we suggest to edit the makefile.win and adapt it to other compilers
           Note: when compiling under Windows AND Cygwin, you should erase the files *.o before
                 recompiling with the other operating systems (or equivalently launch > make clean).

LAUNCHING: run the executable with the parameters described in main.c
           Command line will be > COLA xxx under Windows and > ./COLA xxx under other systems if path
           is not set to current directory.

MODIFYING: Execution modes, how to modify the code etc.. are in the file *main.c*
           The .c and .h files contain a short documentation for the relevant functions

WEB:       the package can be downloaded from: http://www2.unipr.it/~dalpalu/research/COLA.html

CONTACT:   alessandro.dalpalu AT unipr.it

---------------------------------------------------------------------------------------------------------
LIST OF FILES:

0-README.txt			this file

Constraint solver.dev		dev c++ project file (for windows users)
Constraint solver.layout	dev c++ project file (for windows users)

makefile			makefile for Unix-Linux
Makefile.win			makefile for windows (for dev c++ installation)

data.txt			protein data file, used for Protein Structure Prediction
table.txt			energy pairwise function, used for Protein Structure Prediction

main.c				Program files
load.c
load.h
AllVariables.c
AllVariables.h
Constraint.c
Constraint.h
ConstraintStore.c
ConstraintStore.h
Domain.c
Domain.h
Pattern.c
Pattern.h
Search.c
Search.h
SearchBest.c
SearchBest.h
SearchBestHeurBBF.c
SearchBestHeurBBF.h
SearchComplete.c
SearchComplete.h
SearchXYZBestHeur.c
SearchXYZBestHeur.h
TrailStack.c
TrailStack.h
Utils.c
Utils.h
Variable.c
Variable.h

1KON.pdb			proteins containing some rigid blocks
1ZDD.pdb			used in the example in data.txt
EOF	