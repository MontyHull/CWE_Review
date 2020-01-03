#include "circuit.h"
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <omp.h>
#include <unistd.h>
#include "conv.h"
#include "poly.h"
#include "mpi.h"

/* specifies which rank the master is sending to */
int which_rank;

/* the origianl count of how many ranks exist */
int orig_np;

/* iterates up so that a saved slp will have a unique name */
int iter;

/* build's an slp up to the desired number of operations */
void build_slp(SLPT s2,int op,int desired_op,char* SLP_array,int SLP_size){
  int ind1,ind2;
  OpCode opCode;

  /* base case */
  if(op == desired_op){
    /* turns it into an array */
    output_buf(s2,SLP_array);

    /* sends array to a different rank  */
    MPI_Send(SLP_array,SLP_size,MPI_BYTE,which_rank,0,MPI_COMM_WORLD);

    /* if you have iterated through every rank then start over */
    which_rank++;
    if(which_rank == orig_np){  which_rank = 1;}

    return;
  }

  /* iterates from negative indexes (inputs) to positive indexes (outputs)
  * the number of outputs increases by 1 for each operation */
  for(ind1 = s2->inputs*-1; ind1 < op; ind1++){
    for(ind2 = s2->inputs*-1; ind2 < op; ind2++){
      for(opCode = ADD; opCode <= SUB; opCode++){
        regular_op(s2->ops+op,opCode,ind1,ind2);

        /* recursive call */
        build_slp(s2,op+1,desired_op,SLP_array,SLP_size);
      }
    }
  }
}

/* finishes building an SLP starting at op */
/* op should match desired op from build slp */
void finish_slp(SLPT s2,int op,EvalT eval1,EvalT eval2, PolyT poly1, PolyT poly2,long answer1,int rank){
  int ind1,ind2;
  OpCode opCode;

  /* used to print to a file */
  FILE* fp;
  char output_location[200];

  /* base case */
  if(op == s2->length){
    printf("yes\n");
    eval_set_slp(eval2, s2);

    /* evaluates after slp has been built */
    evaluate(eval2);

    /* checks if new slp evaluates to same as a known slp */
    if(eval2->outputs[s2->length-1] == answer1){
      /* if they evaluate the same then turn the slp to a poly*/
      slp2poly(poly2,s2,1,0,0);

      /* check if the two polynomials are equal */
      if(poly_equality(poly1,poly2)){
        /* if equal print the new slp to a file */
        sprintf(output_location, "./output/rank-%d:number-%d",rank,iter);
        iter++;
        fp = fopen(output_location,"w");
        output(s2,fp);
        /*printf("We found it!\n");*/
        fclose(fp);
      }
    }

    return;
  }

  /* iterates from negative indexes (inputs) to positive indexes (outputs)
  * the number of outputs increases by 1 for each operation */
  for(ind1 = s2->inputs*-1; ind1 < op; ind1++){
    for(ind2 = s2->inputs*-1; ind2 < op; ind2++){
      for(opCode = ADD; opCode <= SUB; opCode++){
        regular_op(s2->ops+op,opCode,ind1,ind2);
        /* recursive call */
        finish_slp(s2,op+1,eval1,eval2,poly1,poly2,answer1,rank);
      }
    }
  }
}


int main(int argc, char** argv){

  /* variables used for mpi initization and calls */
  int ierr, np, rank;

  /* only used by rank 0 to read in a known solution */
  PolyT poly1,poly2;

  /* used to evaluate poly in rank 0 */
  /* brings in a random slp in all other ranks for testing */
  SLPT s1,s2;

  /* used to evaluate SLPs and the inputs they're given */
  EvalT eval1,eval2;

  /* used to read poly in rank 0 */
  /* used to output correct SLPs in all other ranks */
  FILE* fp;

  /* used to convert a value to an int for comparison */
  long answer1;

  /* loop and temp variables */
  int i;
  int desired_op =2;
  int numb_operations = 3;

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
  assert(argc == 1);

  /* seeding rand with rank */
  srand(time(NULL)+(rank*100));

  /*
  Beginning of rank 0 initialization
  */
  if(rank == 0){
    /* declaring that the first rank to send to is rank 1 */
    which_rank = 1;

    /* setting the global variable to the value of np */
    orig_np = np;

    /* read in a poly from a file */
    fp = fopen("2detpoly.txt", "r");
    assert(fp);
    poly_fread(fp,poly1);
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

    /* evaluating first slp and setting the final output to answer1 */
    evaluate(eval1);
    answer1 = eval1->outputs[s1->length-1];
  }

  /* initialize the slp that is to be built */
  slp_init(s2,s1->inputs,numb_operations);

  if(rank == 0){
    /* builds an slp up to the desired_op, and then sends it to differing ranks */
    build_slp(s2,0,desired_op,SLP_array,SLP_size);

    /* sends a tag to every other rank in order for them to quit */
    for(i = 1; i < np;i++){
      MPI_Send(SLP_array,SLP_size,MPI_BYTE,i,1,MPI_COMM_WORLD);
    }
  }

  if(rank != 0){

    /* recieves the partially built SLP */
    MPI_Recv(SLP_array,SLP_size,MPI_BYTE,0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

    /* initialize eval2 */
    eval_init_size(eval2,s2->inputs,s2->length);

    /* set eval2 inputs */
    for(i = 0; i < s2->inputs; i++){
      eval2->inputs[i] = eval1->inputs[i];
    }

    /* while you are still recieving new SLPs */
    while(status.MPI_TAG != 1){
      /* Changes array back to SLP */
      input_buf(s2,SLP_array,1);

      /* finish building the slp starting at desired_op and check for equality */
      finish_slp(s2,desired_op,eval1,eval2,poly1,poly2,answer1,rank);

      /* recieve the next slp to finish, or the signal to quit */
      MPI_Recv(SLP_array,SLP_size,MPI_BYTE,0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
    }

    /* clear the stucts */
    eval_clear(eval2);
    poly_clear(poly2);
    eval_clear(eval1);
  }

  /* Free all polys and slps */
  poly_clear(poly1);
  slp_clear(s1);
  slp_clear(s2);

  free(SLP_array);

  MPI_Finalize();
  return 0;
}
