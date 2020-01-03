#include "circuit.h"
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <omp.h>
#include <unistd.h>
#include "mpi.h"

int main(int argc, char**argv){

  /* variables used for mpi initization and calls */
  int ierr, np, rank;

  /* used to pass the size of the arrays holding slps */
  int SLP_size[2];

  /* char arrays used for holding the SLP */
  char* SLP_array;


  /* The two slps to be used and the flag for equality */
  SLPT slp1,slp2;
  int if_equal,answer;

  /* File pointer for input */
  FILE* fp1;
  FILE* fp2;

  /* initialized MPI */
  ierr = 0;
  ierr |= MPI_Init(&argc, &argv);
  ierr |= MPI_Comm_size(MPI_COMM_WORLD, &np);
  ierr |= MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  assert(ierr == 0);

  /* seeding random gen with time and rank */
  srand(time(NULL) + (rank*100));

  /*
  rank 0 will read in the files
  turn them into SLPs
  */
  if(rank == 0){

    /* reading in files */
    fp1 = fopen("1","r");
    fp2 = fopen("2","r");

    /* turning files into SLPs */
    input(slp1,fp1);
    input(slp2,fp2);

    /* closing files like a good programmer */
    fclose(fp1);
    fclose(fp2);

    /* determining size of the SLPs */
    SLP_size[0] = (int)byte_size(slp1);
    SLP_size[1] = (int)byte_size(slp2);
  }

  /* Broadcasting out the size of each array */
  MPI_Bcast(SLP_size,2,MPI_INT,0,MPI_COMM_WORLD);

  /* malloc the arrays again so that they can recieve from bcast */
  SLP_array = malloc(SLP_size[0] + SLP_size[1]);

  /* Turning the SLP_array back into an SLP */
  if(rank == 0){
    output_buf(slp1,SLP_array);
    output_buf(slp2,SLP_array+SLP_size[0]);
  }


  /* Broadcasts the char arrays that hold the SLPs) */
  MPI_Bcast(SLP_array,SLP_size[0]+SLP_size[1],MPI_BYTE,0,MPI_COMM_WORLD);

  /* turns char arrays into slps */
  if(rank != 0){
    input_buf(slp1,SLP_array,0);
    input_buf(slp2,SLP_array+SLP_size[0],0);
  }

  /* checks for equality */
  if_equal = slp_equal_multi(slp1,slp2,1,10);

  MPI_Reduce(&if_equal,&answer,1,MPI_INT,MPI_BAND,0,MPI_COMM_WORLD);
  if(rank == 0){
    if(answer == 1){
      printf("The SLPs are equal\n");
    }
    else{
      printf("The SLPs are not equal\n");
    }
  }


  /* clears the slps */
  slp_clear(slp1);
  slp_clear(slp2);
  free(SLP_array);

  /* finalizes MPI and exit */
  MPI_Finalize();
  return 0;
}
