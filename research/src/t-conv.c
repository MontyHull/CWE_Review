#include "conv.h"
#include <stdio.h>
#include <time.h>

int main() {
  SLPT p, p2;
  PolyT q, q2;

  printf("Enter an SLP:\n");
  input(p, stdin);

  slp2poly(q, p, 0);
  printf("\npolynomial: ");
  poly_print(q);

  poly2slp(p2, q, 0);
  printf("\nEquivalent SLP:\n");
  output(p2, stdout);

  slp2poly(q2, p2, 0);
  printf("\nShould be same poly: ");
  poly_print(q2);

  slp_clear(p);
  slp_clear(p2);
  poly_clear(q);
  poly_clear(q2);
  return 0;
}
