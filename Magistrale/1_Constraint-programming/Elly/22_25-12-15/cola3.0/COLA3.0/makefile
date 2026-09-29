CPP  = g++
CC   = gcc
RES  = 
OBJ  = AllVariables.o Constraint.o ConstraintStore.o load.o main.o Pattern.o Search.o Variable.o Utils.o TrailStack.o SearchComplete.o SearchSimple.o SearchBest.o SearchBestHeurBBF.o $(RES)
LINKOBJ  = $(OBJ)
LIBS =
INCS =
CXXINCS = 
BIN  = "COLA"
CXXFLAGS = $(CXXINCS) -w   -fexpensive-optimizations -O3 -g3
CFLAGS = $(INCS)   -w -fexpensive-optimizations -O3 -g3

.PHONY: all clean

all: "COLA"

clean: 
	rm -f $(OBJ) $(BIN)

$(BIN): $(OBJ)
	$(CPP) $(LINKOBJ) -o "COLA" $(LIBS)

AllVariables.o: AllVariables.c
	$(CPP) -xc++ -c AllVariables.c -o AllVariables.o $(CXXFLAGS)

Constraint.o: Constraint.c
	$(CPP) -xc++ -c Constraint.c -o Constraint.o $(CXXFLAGS)

ConstraintStore.o: ConstraintStore.c
	$(CPP) -xc++ -c ConstraintStore.c -o ConstraintStore.o $(CXXFLAGS)

load.o: load.c
	$(CPP) -xc++ -c load.c -o load.o $(CXXFLAGS)

main.o: main.c
	$(CPP) -xc++ -c main.c -o main.o $(CXXFLAGS)

Pattern.o: Pattern.c
	$(CPP) -xc++ -c Pattern.c -o Pattern.o $(CXXFLAGS)

Search.o: Search.c
	$(CPP) -xc++ -c Search.c -o Search.o $(CXXFLAGS)

Utils.o: Utils.c
	$(CPP) -xc++ -c Utils.c -o Utils.o $(CXXFLAGS)

Variable.o: Variable.c
	$(CPP) -xc++ -c Variable.c -o Variable.o $(CXXFLAGS)

TrailStack.o: TrailStack.c
	$(CPP) -xc++ -c TrailStack.c -o TrailStack.o $(CXXFLAGS)

SearchComplete.o: SearchComplete.c
	$(CPP) -xc++ -c SearchComplete.c -o SearchComplete.o $(CXXFLAGS)

SearchBest.o: SearchBest.c
	$(CPP) -xc++ -c SearchBest.c -o SearchBest.o $(CXXFLAGS)

SearchSimple.o: SearchSimple.c
	$(CPP) -xc++ -c SearchSimple.c -o SearchSimple.o $(CXXFLAGS)

SearchBestHeurBBF.o: SearchBestHeurBBF.c
	$(CPP) -xc++ -c SearchBestHeurBBF.c -o SearchBestHeurBBF.o $(CXXFLAGS)
