#include "circuit.h"
#include <stdio.h>
#include <time.h>

int main() {
  int i,x;
  EvalT eval22;
  
  /* create a circuit for 2x2 determinant*/
  SLPT det22;
  
  srand(time(NULL));

  slp_init(det22, 4, 3);

  regular_op(get_op(det22, 0), MUL, -1, -2);
  regular_op(get_op(det22, 1), MUL, -3, -4);
  scalar_op(get_op(det22, 2), SUB, 0, 1);

  eval_init(eval22, det22);
  
  /*int x = rand()%(1L<<20)-(1L<<19);*/
  x = rand()%20-10;
  for(i = 0; i < eval22->slp[0].inputs; i++){
    eval22->inputs[i] = x;
    /*x = rand()%(1L<<20)-(1L<<19);*/
    x = rand()%20-10;
  }
  for(i = 0; i < eval22->slp[0].inputs; i++){
    printf("%s%ld\n","input: ",eval22->inputs[i]);
  }
  
  printf("\n");
  
  evaluate(eval22);
  
  for(i = 0; i < eval22->slp[0].length; i++){
    printf("%ld\n",eval22->outputs[i]);
  }

  eval_clear(eval22);

  slp_clear(det22);
  return 0;
}
