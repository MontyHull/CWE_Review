#include "poly.h"

const int nvars = 3;

int main() {
  int eq;

  PolyT f, g, h;
  poly_init(f, nvars);
  poly_init(g, nvars);
  poly_init(h, nvars);

  printf("f = ");
  fflush(stdout);
  poly_read(f);
  poly_print(f);
  printf("\n");

  printf("g = ");
  fflush(stdout);
  poly_read(g);
  poly_print(g);
  printf("\n");

  eq = poly_equality(f, g);
  if (eq) printf("they are equal.\n");
  else printf("they aren't equal.\n");
  printf("\n");

  poly_add(h, f, g);
  printf("f + g = ");
  poly_print(h);
  printf("\n");

  poly_sub(h, f, g);
  printf("f - g = ");
  poly_print(h);
  printf("\n");

  poly_mul(h, f, g);
  printf("f * g = ");
  poly_print(h);
  printf("\n");

  return 0;
}
