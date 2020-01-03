/* program to convert any SLP to the canonical polynomial form */

#include "conv.h"
#include "poly.h"
#include "circuit.h"
#include <stdio.h>

int main(int argc, char** argv) {
  PolyT p;
  SLPT q;

  if (argc > 2) {
    printf("Usage: %s [filename]\n", argv[0]);
    return -1;
  }
  else if (argc == 2) {
    FILE* infile = fopen(argv[1], "r");
    input(q, infile);
    fclose(infile);
  }
  else {
    fprintf(stderr, "Straight-line program: \n");
    input(q, stdin);
  }

  slp2poly(p, q, 0, 10, 10);

  poly_print(p);

  poly_clear(p);
  slp_clear(q);

  return 0;
}
