CFLAGS = -ansi -pedantic -Wall -Wextra -Werror -fopenmp -fmax-errors=4 -Wno-long-long -Wno-unused-result -O3 -DNDEBUG -Wno-unused-but-set-variable 
# CFLAGS = -ansi -pedantic -Wall -Wextra -Werror -fopenmp -fmax-errors=4 -Wno-long-long -Wno-unused-result -O0 -ggdb
CC = gcc
MPICC = mpicc

EXES = t-poly test t-io t-conv evaltest gen-slp slp2poly poss_slps rand_slp enum_sets test-rms phasedrand phasedenum formula_slp_compare
MPIEXES = mpiequality multiSLP randmultiSLP norepeatSLP phasedmultiSLP
HEADERS = poly.h circuit.h conv.h slpmake.h
SOURCES = poly.c circuit.c conv.c slpmake.c poss_slps.c rand_slp.c  $(EXES:=.c) $(MPIEXES:=.c)


all: $(EXES)

poly.o t-poly.o: poly.h
slpmake.o: slpmake.h circuit.h
circuit.o test.o t-io.o evaltest.o mpiequality.o poss_slps.o rand_slp.o: circuit.h
conv.o t-conv.o gen-slp.o slp2poly.o multiSLP.o norepeatSLP.o: conv.h poly.h circuit.h
test-rms.o phasedrand.o enum_sets.o formula_slp_compare.o: conv.h poly.h circuit.h
randmultiSLP.o phasedenum.o phasedmultiSLP.o: conv.h poly.h circuit.h slpmake.h


t-poly: poly.o
test t-io evaltest mpiequality poss_slps rand_slp: circuit.o
t-conv gen-slp slp2poly multiSLP norepeatSLP: poly.o circuit.o conv.o
test-rms phasedrand enum_sets formula_slp_compare: poly.o circuit.o conv.o
randmultiSLP phasedenum phasedmultiSLP: poly.o circuit.o conv.o slpmake.o


$(MPIEXES:=.o): %.o: %.c
	$(MPICC) $(CFLAGS) -c $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

$(MPIEXES): %: %.o
	$(MPICC) $(CFLAGS) $^ -o $@

$(EXES): %: %.o
	$(CC) $(CFLAGS) $^ -o $@ -lm

.PHONY: all clean

clean:
	rm -f $(EXES) $(MPIEXES) $(SOURCES:.c=.o)
