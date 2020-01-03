/* program to compare a given formula and slp */

#include <stdio.h>
#include "circuit.h"
#include "poly.h"
#include "conv.h"

const int num_evals = 1000000;

int main(int argc, char** argv) {
  PolyT p1, p2;
  SLPT q1, q2;
  EvalT e1, e2;
  FILE* infile;
  unsigned int seed;
  int i, j;

  if (argc != 4) {
    printf("Usage: %s poly_file slp_file seed\n", argv[0]);
    return -1;
  }

  seed = atoi(argv[3]);
  printf("Using seed %u\n\n", seed);
  srand(seed);

  infile = fopen(argv[1], "r");
  poly_fread(infile, p1);
  fclose(infile);

  printf("Poly 1: ");
  poly_print(p1);

  poly2slp(q1, p1, 0);
  printf("SLP 1: ");
  output(q1, stdout);
  printf("\n");

  infile = fopen(argv[2], "r");
  input(q2, infile);
  fclose(infile);

  printf("SLP 2: ");
  output(q2, stdout);
  
  slp2poly(p2, q2, 0, 0, 0);
  printf("Poly 2: ");
  poly_print(p2);

  printf("\n");
  printf("poly_equality: %d\n", poly_equality(p1, p2));

  printf("\nRandom tests...");
  fflush(stdout);
  eval_init(e1, q1);
  eval_init_size(e2, q2->inputs, q2->length);
  eval_set_slp(e2, q2);
  assert(q1->inputs == q2->inputs);
  for (i = 0; i < num_evals; ++i) {
    for (j = 0; j < q1->inputs; ++j) {
      e1->inputs[j] = e2->inputs[j] = rand() % (1L<<20) - (1L<<19);
    }
    evaluate(e1);
    evaluate(e2);
    if (e1->outputs[q1->length - 1] != e2->outputs[q2->length - 1]) {
      printf("UNEQUAL on iteration %d\n", i);
      break;
    }
  }
  if (i == num_evals) printf("equal in all %d iterations\n", num_evals);

  eval_clear(e1);
  eval_clear(e2);
  poly_clear(p1);
  poly_clear(p2);
  slp_clear(q1);
  slp_clear(q2);

  return 0;
}
