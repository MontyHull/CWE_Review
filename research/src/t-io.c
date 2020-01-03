#include "circuit.h"
#include <stdio.h>
#include <time.h>

int main() {
  SLPT p, q;
  char* buf;
  size_t len;

  srand(time(0));
  slp_init(p, 3, 5);
  random_slp(p);
  
  printf("Original SLP:\n");
  output(p, stdout);

  len = byte_size(p);
  buf = malloc(len);
  output_buf(p, buf);
  input_buf(q, buf, 0);
  
  printf("\nSLP after writing/reading to/from buf:\n");
  output(q, stdout);

  free(buf);
  slp_clear(p);
  slp_clear(q);
  return 0;
}
