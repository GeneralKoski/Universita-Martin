#!/bin/bash

module load gnu/5.4.0   cuda/11.5.2
 
cp  ${CUDA_HOME}/samples/5_Simulations/nbody/* .
sed -i 's/\/usr\/local\/cuda/$(CUDA_HOME)/g'  Makefile
sed -i 's/..\/..\/common\/inc/$(CUDA_PATH)\/samples\/common\/inc/g' Makefile
  
make
