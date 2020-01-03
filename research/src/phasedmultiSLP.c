#include "circuit.h"
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <omp.h>
#include <unistd.h>
#include "conv.h"
#include "mpi.h"
#include "poly.h"

/* specifies which rank the master is sending to */
int which_rank;
/* the origianl count of how many ranks exist */
int orig_np;

/* iterates up so that a saved slp will have a unique name */
int iter;

int eval_pos;

#define phaseLen1 (2)
#define phaseLen2 (1)
#define phaseLen3 (1)
#define phaseLen4 (3)
#define phaseLen5 (phaseLen4 - 1)

#define phaseArray0 (phaseLen1)
#define phaseArray1 (phaseArray0 + phaseLen2)
#define phaseArray2 (phaseArray1 + phaseLen3)
#define phaseArray3 (phaseArray2 + phaseLen4)
#define phaseArray4 (phaseArray3 + phaseLen5)

#define numb_operations (phaseArray4)

/* global variables... how naughty! */
SLPT s;
EvalT ev;
long answer = 0;
PolyT poly1, poly2;
int rank;
long count = 0;

void phase5p2(int op, int ind2, int curout) {
  OpCode opCode;
  int l;
  Index arg1;
  Value src1;
  Value src2;
  FILE* fp;
  char output_location[200];
  long answer1;


  if (op == phaseArray4) {
    assert(ind2 == phaseArray3);
    eval_set_slp(ev, s);
    count++;	

    for(l = eval_pos; l < phaseArray2; l++){
      /* src1:
      * arg1 is always an index */
      arg1 = s->ops[l].arg1;

      /* src from input or output */
      if(arg1 >= 0){  src1 = ev->outputs[arg1];  }
      else{  src1 = ev->inputs[input_index(arg1)];  }

      /* src2: */
      /* src2 is value,from outputs, or from inputs */

      assert(s->ops[l].type == REGULAR);
      if(s->ops[l].arg2.ind >= 0){
        src2 = ev->outputs[s->ops[l].arg2.ind];
      }
      else{
        assert(s->ops[l].arg2.ind < 0);
        src2 = ev->inputs[input_index(s->ops[l].arg2.ind)];
      }

      /* add,mul,sub */

      if(s->ops[l].func == ADD){  ev->outputs[l] = src1 + src2;  }
      else if(s->ops[l].func == SUB){  ev->outputs[l] = src1 - src2;  }
      else{  assert(s->ops[l].func == MUL);  ev->outputs[l] = src1 * src2;  }
    }

    for(; l < phaseArray3; l++){

      /* src1:
      * arg1 is always an index */
      arg1 = s->ops[l].arg1;

      /* src from input or output */
      if(arg1 >= 0){  src1 = ev->outputs[arg1];  }
      else{  src1 = ev->inputs[input_index(arg1)];  }

      /* src2: */
      /* src2 is value,from outputs, or from inputs */

      assert(s->ops[l].type == REGULAR);
      if(s->ops[l].arg2.ind >= 0){
        src2 = ev->outputs[s->ops[l].arg2.ind];
      }
      else{
        assert(s->ops[l].arg2.ind < 0);
        src2 = ev->inputs[input_index(s->ops[l].arg2.ind)];
      }

      /* add,mul,sub */

      assert(s->ops[l].func == MUL);
      ev->outputs[l] = src1 * src2;
    }



    /* only phase5 */

    for(; l < numb_operations; l++){

      /* src1:
      * arg1 is always an index */

      arg1 = s->ops[l].arg1;


      /* src from input or output */

      assert(arg1 >= 0);
      src1 = ev->outputs[arg1];


      assert(s->ops[l].type == REGULAR);
      assert(s->ops[l].arg2.ind>=0);
      src2 = ev->outputs[s->ops[l].arg2.ind];

      /* add,mul,sub */

      if(s->ops[l].func == ADD){  ev->outputs[l] = src1 + src2;  }
      else if(s->ops[l].func == SUB){  ev->outputs[l] = src1 - src2;  }
    }

    answer1 = ev->outputs[numb_operations-1];


    /* evaluate here */

    if(answer1 == answer){
      /* if they evaluate the same then turn the slp to a poly*/
      slp2poly(poly2,s,1,0,0);

      /* check if the two polynomials are equal */
      if(poly_equality(poly1,poly2)){
        /* if equal print the new slp to a file */

        sprintf(output_location, "./wwwrank-%d:number-%d",rank,iter);
        fp = fopen(output_location,"w");
        output(s,fp);
        fclose(fp);

        iter++;

        printf("We found it!\n");
      }
    }


    return;
  }

  for (opCode = ADD; opCode <= SUB; opCode += 2) {
    regular_op(s->ops + op, opCode, curout, ind2);
    phase5p2(op+1,  ind2+1, op);
    eval_pos = op;

  }
}

void phase5p1( int op) {
  int ind0, ind2, curout, nextop;

  for (ind0 = phaseArray2; ind0 < phaseArray3; ++ind0) {
    /* ind0 is the start of the chain */
    curout = ind0;
    nextop = op;
    for (ind2 = phaseArray2; ind2 < ind0; ++ind2) {
      /* all indices less than ind0 get subtracted */
      regular_op(s->ops + nextop, SUB, curout, ind2);
      curout = nextop;
      ++nextop;
    }
    /* add or subtract all indices greater than ind0 */
    phase5p2(nextop,  ind0+1, curout);
    eval_pos = op;
  }
}

void phase4(int op, int ind1, int ind2){

  OpCode opCode;

  opCode = MUL;

  if(op == phaseArray3){

    phase5p1(phaseArray3);

    return;
  }

  /* iterates from negative indexes (inputs) to positive indexes (outputs)
  * the number of outputs increases by 1 for each operation */
  for(; ind1 < phaseArray0; ind1++){
    for(; ind2 < phaseArray2; ind2++){
      regular_op(s->ops+op,opCode,ind1,ind2);

      /* recursive call */
      phase4(op+1, ind1, ind2+1);
      eval_pos = op;

    }
    ind2 = phaseArray0;
  }
}

void phase3(int op){
  int ind1,ind2;
  OpCode opCode;

  if(op == phaseArray2){
    phase4(phaseArray2, s->inputs*-1, phaseArray0);
    return;
  }

  /* addition */
  opCode = ADD;
  for(ind1 = phaseArray0; ind1 < op; ind1++){
    for(ind2 = phaseArray0; ind2 < op; ind2++){
      regular_op(s->ops+op,opCode,ind1,ind2);

      /* recursive call */
      phase3(op+1);
      eval_pos = op;

    }
  }

  /* subtraction */
  opCode = SUB;
  for(ind1 = phaseArray0; ind1 < op; ind1++){
    for(ind2 = phaseArray0; ind2 < op; ind2++){
      regular_op(s->ops+op,opCode,ind1,ind2);

      /* recursive call */
      phase3(op+1);
      eval_pos = op;

    }
  }
}

void phase2(int op, int ind1, int ind2){
  OpCode opCode;

  opCode = MUL;

  if(op == phaseArray1){
    phase3(phaseArray1);
    return;
  }

  /* iterates from negative indexes (inputs) to positive indexes (outputs)
  * the number of outputs increases by 1 for each operation */
  for(; ind1 < phaseArray0; ind1++){
    for(; ind2 < phaseArray0; ind2++){
      regular_op(s->ops+op,opCode,ind1,ind2);

      /* recursive call */
      phase2(op+1, ind1, ind2+1);
      eval_pos = op;

    }
    ind2 = ind1 + 1;
  }
}

void phase1p2(int op){
  int ind1,ind2;
  OpCode opCode;

  if(op == phaseArray0){

    phase2(phaseArray0, s->inputs*-1, s->inputs*-1);
    return;
  }

  /* addition */
  opCode = ADD;
  for(ind1 = s->inputs*-1; ind1 < op; ind1++){
    for(ind2 = ind1; ind2 < op; ind2++){
      regular_op(s->ops+op,opCode,ind1,ind2);

      /* recursive call */
      phase1p2(op+1);
      eval_pos = op;

    }
  }

  /* subtraction */
  opCode = SUB;
  for(ind1 = s->inputs*-1; ind1 < op; ind1++){
    for(ind2 =s->inputs*-1; ind2 < op; ind2++){
      regular_op(s->ops+op,opCode,ind1,ind2);

      /* recursive call */
      phase1p2(op+1);
      eval_pos = op;

    }
  }
}


void phase1p1(int op,int desired_length,char* SLP_array,int SLP_size){
  int ind1,ind2;
  OpCode opCode;

  if(op == desired_length){
    output_buf(s,SLP_array);
    MPI_Send(SLP_array,SLP_size,MPI_BYTE,which_rank,0,MPI_COMM_WORLD);
    which_rank++;
    if(which_rank == orig_np){  which_rank = 1;}
    return;
  }


  /* addition */
  opCode = ADD;
  for(ind1 =  s->inputs*-1; ind1 < op; ind1++){
    for(ind2 = ind1; ind2 < op; ind2++){
      regular_op(s->ops+op,opCode,ind1,ind2);

      /* recursive call */
      phase1p1(op+1,desired_length,SLP_array,SLP_size);
    }
  }

  /* subtraction */
  opCode = SUB;
  for(ind1 =  s->inputs*-1; ind1 < op; ind1++){
    for(ind2 =  s->inputs*-1; ind2 < op; ind2++){
      regular_op(s->ops+op,opCode,ind1,ind2);
      /* recursive call */
      phase1p1(op+1,desired_length,SLP_array,SLP_size);
    }
  }
}



int main(int argc, char** argv){

  /* variables used for mpi initization and calls */
  int ierr, np;

  /* only used by rank 0 to read in a known solution */
  /* globals PolyT poly1,poly2; */

  /* used to evaluate poly in rank 0 */
  /* brings in a random slp in all other ranks for testing */
  SLPT s1;

  /* used to evaluate SLPs and the inputs they're given */
  EvalT eval1;

  /* used to read poly in rank 0 */
  /* used to output correct SLPs in all other ranks */
  FILE* fp;

  /* used to convert a value to an int for comparison */
  /* global long answer = 0; */

  /* loop and temp variables */
  int i;
  int seed_value;
  int desired_op =1;
  /* Size of the slp that gets bcast */
  int SLP_size;

  /* the SLP that gets bcast in byte form */
  char* SLP_array;

  /* where the status of each recv call is kept */
  MPI_Status status;


  /* intializes the iter for file output */
  iter = 0;

  /* Initalizing MPI */
  ierr = 0;
  ierr |= MPI_Init(&argc, &argv);
  ierr |= MPI_Comm_size(MPI_COMM_WORLD, &np);
  ierr |= MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  assert(ierr == 0);

  /* assert that you have enough arguments to read in from a file */
  assert(argc == 2);

  /* seeding rand with rank */
  seed_value = atoi(argv[1]);
  srand(rank+seed_value);

  eval_pos = 0;

  /*
  Beginning of rank 0 initialization
  */
  if(rank == 0){
    /* declaring that the first rank to send to is rank 1 */
    which_rank = 1;

    /* setting the global variable to the value of np */
    orig_np = np;

    /* read in a poly from a file */
    /* fp = fopen("3detpoly.txt", "r"); */
    fp = fopen("testpoly.txt", "r");
    assert(fp);
    poly_fread(fp,poly1);
    printf("Searching for this polynomial: ");
    poly_print(poly1);
    fclose(fp);

    /* turns your poly into an slp */
    poly2slp(s1,poly1,0);

    /* get size of slp program */
    SLP_size = (int)byte_size(s1);

  }

  /* Bcast size of SLP array */
  MPI_Bcast(&SLP_size,1,MPI_INT,0,MPI_COMM_WORLD);

  /* let all ranks malloc the SLP array */
  SLP_array = malloc(SLP_size);

  /* turn the slp into an array */
  if(rank == 0){
    output_buf(s1,SLP_array);
  }

  /* Bcast the SLP in array format */
  MPI_Bcast(SLP_array,SLP_size,MPI_BYTE,0,MPI_COMM_WORLD);

  if(rank != 0){

    /* Changes array back to SLP */
    input_buf(s1,SLP_array,0);

    /* Changes the slp to a poly for later comparison */
    slp2poly(poly1,s1,0,0,0);

    /* initialize the second poly so we can free it later */
    poly_init2(poly2,1,1);

    /* initialize the first eval so we can check correct answer */
    eval_init(eval1,s1);

    /* inputing random inputs into eval */
    for(i = 0; i < s1->inputs; i++){
      eval1->inputs[i] = rand()%(1L<<20)-(1L<<19);
    }

    /* evaluating first slp and setting the final output to answer */
    evaluate(eval1);
    answer = eval1->outputs[s1->length-1];
  }

  /* initialize the slp that is to be built */
  /* TODO
  slp_init(s,s1->inputs,numb_operations);
  */
  slp_init(s,s1->inputs,numb_operations);

  if(rank == 0){
    /* builds an slp up to the desired_op, and then sends it to differing ranks */
    /*build_slp(s,0,desired_op,SLP_array,SLP_size);*/
    phase1p1(0,desired_op,SLP_array,SLP_size);
    /* sends a tag to every other rank in order for them to quit */
    for(i = 1; i < np;i++){
      MPI_Send(SLP_array,SLP_size,MPI_BYTE,i,1,MPI_COMM_WORLD);
    }
  }

  if(rank != 0){

    /* recieves the partially built SLP */
    MPI_Recv(SLP_array,SLP_size,MPI_BYTE,0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

    /* initialize ev */
    eval_init_size(ev,s->inputs,s->length);
    /* set ev inputs */
    for(i = 0; i < s->inputs; i++){
      ev->inputs[i] = eval1->inputs[i];
    }

    /* while you are still recieving new SLPs */
    while(status.MPI_TAG != 1){
      /* Changes array back to SLP */
      input_buf(s,SLP_array,1);

      /* finish building the slp starting at desired_op and check for equality */
      /*finish_slp(s,desired_op,eval1,ev,poly1,poly2,answer,rank);*/
      eval_pos = 0;
      phase1p2(desired_op);

      /* recieve the next slp to finish, or the signal to quit */
      MPI_Recv(SLP_array,SLP_size,MPI_BYTE,0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
    }
    /* clear the stucts */
    eval_clear(ev);
    poly_clear(poly2);
    eval_clear(eval1);
    if(rank ==1){printf("count = %ld\n",count);} 
 }


  /* Free all polys and slps */
  poly_clear(poly1);
  slp_clear(s1);
  slp_clear(s);

  free(SLP_array);
  MPI_Finalize();
  return 0;
}
