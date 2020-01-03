/* program to generate a (bad) SLP for any given polynomial */

#include "conv.h"
#include "poly.h"
#include "circuit.h"

int main() {
  PolyT p, p2;
  SLPT q;

  fprintf(stderr, "Polynomial: ");
  poly_read(p);
  
  poly2slp(q, p, 0);
  output(q, stdout);

  slp2poly(p2, q, 0);
  fprintf(stderr, "\nCheck: ");
  poly_fprint(stderr, p2);

  return 0;
}
