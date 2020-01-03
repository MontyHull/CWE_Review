#include "circuit.h"
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <omp.h>
#include <unistd.h>
#include "conv.h"
#include "poly.h"
#include "slpmake.h"

long count;
int eval_pos;
int iter;


/*
TODO Notes for transferring the evaluation
1. Must add int iter and eval_pos as global variables
2. Must add eval_pos = op below each recursive call in for loops
3. Must add all of the correct parameters
*/

/*

eval struct dropped into an enumarative approach

*/

void phase_five(SLPT slp,int op,int* phases,EvalT ev,long answer,PolyT poly1,PolyT poly2){
  int i,j,k,l;
  Index arg1;
  Value src1;
  Value src2;

  /* use for print out correct SLPs
  FILE* fp;
  char output_location[200];
  */

  /* base case */
  if(op == (phases[0]+phases[1])+phases[2]+phases[3]+phases[4]){
    count++;


    for(l = eval_pos; l < slp->length; l++){
      /* src1:
      * arg1 is always an index */
      arg1 = slp->ops[l].arg1;

      /* src from input or output */
      if(arg1 >= 0){  src1 = ev->outputs[arg1];  }
      else{  src1 = ev->inputs[input_index(arg1)];  }

      /* src2: */
      /* src2 is value,from outputs, or from inputs */
      if(slp->ops[l].type == SCALAR){
        src2 = slp->ops[l].arg2.literal;
      }
      else if(slp->ops[l].arg2.ind >= 0){
        assert(slp->ops[l].type == REGULAR);
        src2 = ev->outputs[slp->ops[l].arg2.ind];
      }
      else{
        assert(slp->ops[l].type == REGULAR && slp->ops[l].arg2.ind < 0);
        src2 = ev->inputs[input_index(slp->ops[l].arg2.ind)];
      }

      /* add,mul,sub */
      if(slp->ops[l].func == ADD){  ev->outputs[l] = src1 + src2;  }
      else if(slp->ops[l].func == SUB){  ev->outputs[l] = src1 - src2;  }
      else{  assert(slp->ops[l].func == MUL);  ev->outputs[l] = src1 * src2;  }
    }

    /* evaluate here */

    if(ev->outputs[slp->length-1] == answer){
      /* if they evaluate the same then turn the slp to a poly*/
      slp2poly(poly2,slp,1,0,0);

      /* check if the two polynomials are equal */
      if(poly_equality(poly1,poly2)){
        /* if equal print the new slp to a file */
        /*
        sprintf(output_location, "./output/rank-%d:number-%d",rank,iter);
        fp = fopen(output_location,"w");
        output(s2,fp);
        fclose(fp);
        */
        iter++;

        /*printf("We found it!\n");*/
      }
    }


    return;
  }

  /* iterates from negative indexes (inputs) to positive indexes (outputs)
  * the number of outputs increases by 1 for each operation */
  for(i = phases[0]+phases[1]+phases[2]+phases[3]; i < phases[0]+phases[1]+phases[2]+phases[3]+phases[4]; i++){
    for(j = phases[0]+phases[1]+phases[2]+phases[3]; j < phases[0]+phases[1]+phases[2]+phases[3]+phases[4]; j++){
      for(k = 0; k < 2; k++){
        if(k == 0){
            regular_op(slp->ops+op,ADD,i,j);
            phase_five(slp,op+1,phases,ev,answer,poly1,poly2);
            eval_pos = op;
        }
        else{
          regular_op(slp->ops+op,SUB,i,j);
          phase_five(slp,op+1,phases,ev,answer,poly1,poly2);
          eval_pos = op;

        }
      }
    }
  }
}

void phase_four(SLPT slp,int op,int* phases,EvalT ev,int answer,PolyT poly1,PolyT poly2){
  int i,j;

  /* base case */
  if(op == (phases[0]+phases[1]+phases[2]+phases[3])){
    phase_five(slp,op,phases,ev,answer,poly1,poly2);
    return;
  }

  /* iterates from negative indexes (inputs) to positive indexes (outputs)
  * the number of outputs increases by 1 for each operation */
  for(i = slp->inputs*-1; i < phases[0]; i++){
    for(j = phases[0]+phases[1]; j < phases[0]+phases[1]+phases[2]; j++){
      regular_op(slp->ops+op,MUL,i,j);
      phase_four(slp,op+1,phases,ev,answer,poly1,poly2);
      eval_pos = op;
    }
  }
}

void phase_three(SLPT slp,int op,int* phases,EvalT ev,int answer,PolyT poly1,PolyT poly2){
  int i,j,k;

  /* base case */
  if(op == (phases[0]+phases[1])+phases[2]){
    phase_four(slp,op,phases,ev,answer,poly1,poly2);
    return;
  }

  /* iterates from negative indexes (inputs) to positive indexes (outputs)
  * the number of outputs increases by 1 for each operation */
  for(i = phases[0]+phases[1]; i < phases[0]+phases[1]+phases[2]; i++){
    for(j = phases[0]+phases[1]; j < phases[0]+phases[1]+phases[2]; j++){
      for(k = 0; k < 2; k++){
        if(k == 0){
          regular_op(slp->ops+op,ADD,i,j);
          phase_three(slp,op+1,phases,ev,answer,poly1,poly2);
          eval_pos = op;
        }
        else{
          regular_op(slp->ops+op,SUB,i,j);
          phase_three(slp,op+1,phases,ev,answer,poly1,poly2);
          eval_pos = op;

        }
      }
    }
  }
}

void phase_two(SLPT slp,int op,int* phases,EvalT ev,int answer,PolyT poly1,PolyT poly2){
  int i,j;

  /* base case */
  if(op == (phases[0]+phases[1])){
    phase_three(slp,op,phases,ev,answer,poly1,poly2);
    return;
  }

  /* iterates from negative indexes (inputs) to positive indexes (outputs)
  * the number of outputs increases by 1 for each operation */
  for(i = slp->inputs*-1; i < phases[0]; i++){
    for(j = slp->inputs*-1; j < phases[0]; j++){
        regular_op(slp->ops+op,MUL,i,j);
        phase_two(slp,op+1,phases,ev,answer,poly1,poly2);
        eval_pos = op;
    }
  }
}


void phase_one(SLPT slp,int op,int* phases,EvalT ev,int answer,PolyT poly1,PolyT poly2){
  int i,j,k;

  /* base case */
  if(op == phases[0]){
    phase_two(slp,op,phases,ev,answer,poly1,poly2);
    return;
  }

  /* iterates from negative indexes (inputs) to positive indexes (outputs)
  * the number of outputs increases by 1 for each operation */
  for(i = slp->inputs*-1; i < phases[0]-1; i++){
    for(j = slp->inputs*-1; j < phases[0]-1; j++){
      for(k = 0; k < 2; k++){
        if(k == 0){
          regular_op(slp->ops+op,ADD,i,j);
          phase_one(slp,op+1,phases,ev,answer,poly1,poly2);
          eval_pos = op;
        }
        else{
          regular_op(slp->ops+op,SUB,i,j);
          phase_one(slp,op+1,phases,ev,answer,poly1,poly2);
          eval_pos = op;

        }
      }
    }
  }
}




int main(){

  SLPT slp;
  int* phases;
  EvalT ev;
  long answer;
  PolyT poly1,poly2;
  phases = malloc(5 * sizeof(int));
  phases[0] = 1;
  phases[1] = 1;
  phases[2] = 1;
  phases[3] = 1;
  phases[4] = 1;



  eval_pos = 0;
  iter = 0;

  slp_init(slp,4,5);

  eval_init(ev,slp);
  answer =100;
  poly_init(poly2,9);

  poly_init(poly1,9);
  count = 0;
  phase_one(slp,0,phases,ev,answer,poly1,poly2);
  printf("count = %ld\n",count);
  return 0;
}
