#include "circuit.h"
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <omp.h>
#include <unistd.h>
#include "conv.h"
#include "poly.h"

int main(){


  /* the slp that we are creating */
  SLPT s;
  FILE* fp;
  /* the operations for the regular_op function */
  int ind1,ind2;
  OpCode opCode;

  /* running count of operations completed thus far */
  int op=0;
  int numb_inputs = 9;

  /* loop variable */
  int i;
  int total_length;


  /* used for phase five counting */
  int counter;

  /* how many operations in each phase */
  int phase_one = 3;
  int phase_two = 3;
  int phase_three = 3;
  int phase_four = 3;
  int phase_five = 2;

  /* used to determine if the phases have been filled */
  int complete_first = 0;
  int complete_second = 0;
  int complete_third = 0;
  int complete_fourth = 0;

  /* seeding rand with time */
  srand(time(NULL));

  /* the length of all the phases added together */
  total_length = phase_one + phase_two + phase_three + phase_four + phase_five;

  /*init the slp to be built */
  slp_init(s,numb_inputs,total_length);

  /* phase one add/sub inputs only */
  while(complete_first < phase_one){
    ind1 = rand_bound(numb_inputs+complete_first)-numb_inputs;
    ind2 = rand_bound(numb_inputs+complete_first)-numb_inputs;
    opCode = rand_bound(2) ? ADD : SUB;
    regular_op(s->ops+op,opCode,ind1,ind2);
    complete_first++;
    op++;
  }
  printf("%d  ops completed after phase 1\n",op);

  /* phase two mul inputs and phase1 outputs */
  while(complete_second < phase_two){
    ind1 = rand_bound(numb_inputs+phase_one)-numb_inputs;
    ind2 = rand_bound(numb_inputs+phase_one)-numb_inputs;
    /* to reduce overlab ind1 must be less then ind2 */
    regular_op(s->ops+op,MUL,ind1,ind2);
    complete_second++;
    op++;
  }
  printf("%d ops completed after phase 2\n",op);


  /* phase three add/sub phase 2 outputs */
  while(complete_third < phase_three){
    ind1 = rand_bound(phase_two+complete_third)+phase_one;
    ind2 = rand_bound(phase_two+complete_third)+phase_one;
    opCode = rand_bound(2) ? ADD : SUB;
    regular_op(s->ops+op,opCode,ind1,ind2);
    complete_third++;
    op++;
  }
  printf("%d ops completed after phase 3\n",op);

  /* phase 4 multiply input/phase1 outputs by phase2/phase3 outputs*/
  while(complete_fourth < phase_four){
    ind1 = rand_bound(numb_inputs+phase_one)-numb_inputs;
    ind2 = rand_bound(phase_two+phase_three)+phase_one;
    regular_op(s->ops+op,MUL,ind1,ind2);
    complete_fourth++;
    op++;
  }
  printf("%d ops completed after phase 4\n",op);



  /* phase5 */
  /* pick random place in the four phases to start */
  ind1 = rand_bound(phase_four);
  /* pick a random operation */
  opCode = rand_bound(2) ? ADD : SUB;

  /* used so that the ind2 can be constantly updated */
  counter = ind1;
  ind1 = ind1 +  phase_one + phase_two + phase_three;
  for(i = 1; i < phase_four; i++){
    ind2 = ((counter+i)%phase_four) + phase_one + phase_two + phase_three;
    regular_op(s->ops+op,opCode,ind1,ind2);
    opCode = rand_bound(2) ? ADD : SUB;
    op++;
    ind1 = phase_one+phase_two+phase_three+phase_four+i-1;

  }

  printf("%d ops completed after phase 5\n",op);
  fp = fopen("phasesoflife.txt","w");
  output(s,fp);
  fclose(fp);
  slp_clear(s);
  printf("total_length = %d\n",total_length);

  return 0;
}
