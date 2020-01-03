#include "circuit.h"
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <omp.h>
#include <unistd.h>
#include "conv.h"
#include "poly.h"
#include "mpi.h"
#include "slpmake.h"

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
  int answer1,answer2;

  /* loop and temp variables */
  int i;
  long j;
  int numb_operations = 26;
  int rand_seed;

  /* Size of the slp that gets bcast */
  int SLP_size;

  /* the SLP that gets bcast in byte form */
  char* SLP_array;

  /* where any correct solutions are stored */
  char output_location[200];



  /* Initalizing MPI */
  ierr = 0;
  ierr |= MPI_Init(&argc, &argv);
  ierr |= MPI_Comm_size(MPI_COMM_WORLD, &np);
  ierr |= MPI_Comm_rank(MPI_COMM_WORLD, &rank);




  assert(ierr == 0);

  /* assert that you have enough arguments to read in from a file */
  assert(argc == 2);

  rand_seed = atoi(argv[1]);
  /* seeding rand with rank */
  srand(rand_seed+rank);


  /* seeding rand with rank */

  /*
  Beginning of rank 0 initialization
  */
  if(rank == 0){

    /* read in a poly from a file */
    fp= fopen("3detpoly.txt", "r");
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
    /* linenumber */
    slp2poly(poly1,s1,0,100,rank);

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


    /* begin proper input */
    slp_init(s2,s1->inputs,numb_operations);

    /* initialize evals */
    eval_init(eval2,s2);


    /* start for loop here */
    for(j = 0; j < 10000000L;j++){
      /* get the random slp */
      phaserand(s2);

      /* set the evals inputs */
      for(i = 0; i < s1->inputs; i++){
        eval2->inputs[i] = eval1->inputs[i];
      }

      /* evaluate the evalT and set the final output to answer */
      evaluate(eval2);
      answer2 = eval2->outputs[s2->length-1];

      if(answer1 == answer2){
        /*turn answer1 and answer 2 into a poly and check if they are equal */
        /* linenumber */
        slp2poly(poly2,s2,1,142,rank);
        if(poly_equality(poly1,poly2)){
          sprintf(output_location, "wwwrank-%d:number-%ld", rank,j);
          fp = fopen(output_location,"w");
          printf("WE FOUND IT!\n");
          /*output to a file in the output dir*/
          output(s2,fp);
          fclose(fp);
        }
      }
    }

    slp_clear(s2);
    eval_clear(eval2);
    poly_clear(poly2);
    eval_clear(eval1);
  }

  /* Free all polys and slps */
  poly_clear(poly1);
  slp_clear(s1);


  free(SLP_array);
  MPI_Finalize();
  return 0;
}
