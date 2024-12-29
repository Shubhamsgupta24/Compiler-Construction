#!/bin/bash

# Step 1: Running Flex on the .l file
flex scientific_calculator.l

# Step 2: Compiling the YACC file
yacc -d scientific_calculator.y

# Step 2: Compiling the generated lex.yy.c using gcc
cc lex.yy.c y.tab.c -ll -lm

# Step 3 : Running the final output file
echo "Running Scietifc Calculator with autmoated script..."
./a.out