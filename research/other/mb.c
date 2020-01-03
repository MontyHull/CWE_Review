#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
#include <assert.h>

/* total 32GB */
#define SIZE_PER_ALLOC (10000000)
#define ALLOC_PER_THREAD (200)

int main(int argc, char** argv) {
  omp_set_num_threads(16);
  unsigned long total = 0;
  int stop = 0;
#pragma omp parallel shared(total, stdout, stop) default(none)
  {
    int tid = omp_get_thread_num();
    unsigned int seed = ((unsigned int) time(NULL)) + 65537U * (unsigned)tid;
    char** mem;
    int i, j;
    printf("Thread %d started\n", tid);
    mem = calloc(ALLOC_PER_THREAD, sizeof *mem);
    if (mem == NULL) {
#pragma omp atomic write
      stop = 1;
      printf("EARLY OUT OF MEM THREAD %d\n", tid);
    }
    else {
      for (i = 0; i < ALLOC_PER_THREAD; ++i) {
#pragma omp atomic read
        j = stop;
        if (j) {
          printf("STOPPING thread %d\n", tid);
          fflush(stdout);
          break;
        }
        mem[i] = malloc(SIZE_PER_ALLOC);
        if (mem[i] == NULL) {
#pragma omp atomic write
          stop = 1;
          printf("OUT OF MEMORY thread %d\n", tid);
          fflush(stdout);
          break;
        }
        j = 0;
        while (j < SIZE_PER_ALLOC) {
          mem[i][j] = (char) rand_r(&seed);
          j += (unsigned char) mem[i][j];
        }
        mem[i][0] = 'a';
        mem[i][SIZE_PER_ALLOC - 1] = 'z';
#pragma omp critical
        {
          total += SIZE_PER_ALLOC;
          if (total % 100000000U == 0) {
            printf("%.1lf GB allocated (tid %d)\n", ((double)total) / 1000000000.0, tid);
            fflush(stdout);
          }
        }
        for (j = 0; j <= i; ++j) {
          assert(mem[j][0] == 'a');
          assert(mem[j][SIZE_PER_ALLOC - 1] == 'z');
        }
      }
      for (i = 0; i < ALLOC_PER_THREAD; ++i) {
        if (mem[i]) free(mem[i]);
      }
      free(mem);
    }
  }
  return 0;
}
