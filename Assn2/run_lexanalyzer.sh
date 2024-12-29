#!/bin/bash

# Step 1: Running Flex on the .l file
flex lexanalyzer.l

# Step 2: Compiling the generated lex.yy.c using gcc
gcc lex.yy.c -o lexanalyzer -lfl

echo "Running Lex Analyzer with automatic input..."

./lexanalyzer < input.txt

# echo "int a = 5 + 3;" | ./lexanalyzer