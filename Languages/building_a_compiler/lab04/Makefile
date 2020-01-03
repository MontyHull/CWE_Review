# SI 413 Fall 2013
# Lab 4
# Makefile for simple calculator

CXX=clang++
CXXFLAGS=

# Since it is the first rule, it is what will get made if
# we call "make" with no arguments.
calc: calc.tab.o lex.yy.o colorout.hpp
	$(CXX) $(CXXFLAGS) -o calc lex.yy.o calc.tab.o

# Bison generates a C++ source file and a C++ header file.
calc.tab.cpp calc.tab.hpp: calc.ypp
	bison -d calc.ypp

# Flex generates just a C++ source file.
lex.yy.cpp: calc.lpp
	flex -o lex.yy.cpp calc.lpp

# The lex file includes the header from Bison.
lex.yy.o: lex.yy.cpp calc.tab.hpp
	$(CXX) $(CXXFLAGS) -c lex.yy.cpp

calc.tab.o: calc.tab.cpp
	$(CXX) $(CXXFLAGS) -c calc.tab.cpp

# The following line makes "make" automatically clean up these
# files for you when they are no longer needed.
.INTERMEDIATE: calc.tab.o lex.yy.o lex.yy.cpp calc.tab.cpp calc.tab.hpp

# Run "make clean" to clear all extra files.
.PHONY: clean
clean:
	-rm -f *.o *.yy.cpp *.tab.?pp calc
