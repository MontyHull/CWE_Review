PROGS=pat1 pat2
CXX=clang++

# Default target
all: $(PROGS) ${PROGS:=.output}

# Dependencies
$(PROGS:=.yy.o): %.yy.o: %.tab.hpp
$(PROGS:=.tab.o): %.o: %.hpp
$(PROGS:=.yy.o) $(PROGS:=.tab.o): parsetree.hpp

# Rules to generate the final compiled parser programs
$(PROGS): %: %.tab.o %.yy.o
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ $^

# Generic rule for compiling C++ programs from source
# (Actually, make also defines this by default.)
%.o: %.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $<

# Generic rule for running C++-style flex code generation
# For instance, this will make 'pat.yy.cpp' from 'pat.lpp'.
%.yy.cpp: %.lpp
	flex -o $@ $<

# Generic rule for bison code generation
%.tab.cpp %.tab.hpp: %.ypp
	bison -d $<

# Rule to make .output CFSM specifications from bison
%.output: %.ypp
	bison -v $<

.PHONY: clean all
clean:
	rm -f *.o *.yy.cpp *.tab.* $(PROGS) pat.dot pat.pdf $(PROGS:=.output)
