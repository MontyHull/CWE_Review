#include "circuit.h"
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <omp.h>

int main()
{
  SLPT slp1,slp2;
  int if_equal;
  FILE* fp;
  srand(time(NULL));

  fp = fopen("3x3determinant","r");
  input(slp1,fp);
  fclose(fp);

  fp = fopen("3x3detlong.tx","r");
  input(slp2,fp);
  fclose(fp);

  if_equal = slp_equal_multi(slp1,slp2,1,10);

  printf("if_equal = %d\n",if_equal);

  slp_clear(slp1);
  slp_clear(slp2);
  return 0;
}
