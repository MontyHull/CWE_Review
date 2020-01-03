#include "circuit.h"
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <omp.h>

OpCode last_op = SUB;

/* Used for reading SLP from a file */
void input(SLPT s,FILE* fp)
{
  int fscanner;
  int i;
  OpCode which_op;
  /* Length of SLP and number of inputs */
  long length, inputs;

  /* the index for the regular_op and the function of the op */
  long ind1,ind2;
  char OpC,Reg_Scal;

  /* Reading in the number of inputs and length of the SLP */
  fscanner = fscanf(fp," %ld %ld", &inputs, &length);
  assert(fscanner == 2);

  /* Initalize the SLP and run a loop to fill it in */
  slp_init(s, inputs, length);

  for(i = 0; i < length;i++){
    /* reading in each line for regular/scalar operations */
    fscanner = fscanf(fp," %ld %c %ld %c",&ind1, &OpC, &ind2, &Reg_Scal);
    assert(fscanner == 4);

    /* Checking if the operation needs to be multiplied,added,or subtracted */
    if(OpC == 'x'){
      which_op = MUL;
    }
    else if(OpC == 'a'){
      which_op = ADD;
    }
    else{
      assert(OpC =='s');
      which_op = SUB;
    }

    /* Performs a regular_op */
    if(Reg_Scal == 'r'){
      regular_op(get_op(s, i), which_op, ind1, ind2);
    }
    /* Performs a scalar_op */
    else{
      assert(Reg_Scal =='s');
      scalar_op(get_op(s, i), which_op, ind1, ind2);
    }
  }
}


/* Used for writing slp to a file */
void output(const SLPT s, FILE* fp){

  /* Length of SLP and number of inputs */
  int length, inputs;
  Op* x;
  int i;
  char op;

  length = s->length;
  inputs = s->inputs;

  fprintf(fp,"%d %d\n",inputs, length);

  /* Reading in each opperation and printing it based off of its function(ADD/SUB/DIV)
     and also checking it's OpType */
  for(i = 0; i < length;i++){
    x = get_op(s,i);

    if(x->func == MUL){
      op = 'x';
    }
    else if(x->func == ADD){
      op = 'a';
    }
    else{
      assert(x->func == SUB);
      op = 's';
    }

    if(x->type == REGULAR){
      fprintf(fp,"%ld %c %ld r\n",x->arg1,op,x->arg2.ind);
    }
    else{
      assert(x->type == SCALAR);
      fprintf(fp,"%ld %c %ld s\n",x->arg1,op,x->arg2.literal);
    }
  }
}


void evaluate(EvalT e) {
  const SLP* p = e->slp;

  /* iterate through array of ops (aka length of SLP) */
  int i;
  Index arg1;
  Value src1;
  Value src2;

  for(i = 0; i < p[0].length; i++){
    /* src1:
     * arg1 is always an index */
    arg1 = p->ops[i].arg1;

    /* check if arg1 is from the input or output */
    /* src1 is index from outputs */
    if(arg1 >= 0){
      src1 = e->outputs[arg1];
    }
    /* src1 is index from inputs */
    else{
      src1 = e->inputs[input_index(arg1)];
    }


    /* src2: */

    /* src2 is value */
    if(p->ops[i].type == SCALAR){
      src2 = p->ops[i].arg2.literal;
    }
    /* src2 is index from outputs */
    else if(p->ops[i].arg2.ind >= 0){
      assert(p->ops[i].type == REGULAR);
      src2 = e->outputs[p->ops[i].arg2.ind];
    }
    /* src2 is index from inputs */
    else{
      assert(p->ops[i].type == REGULAR && p->ops[i].arg2.ind < 0);
      src2 = e->inputs[input_index(p->ops[i].arg2.ind)];
    }


    /* addition */
    if(p->ops[i].func == ADD){
      e->outputs[i] = src1 + src2;
    }
    /* subtraction */
    else if(p->ops[i].func == SUB){
      e->outputs[i] = src1 - src2;
    }
    /* multiplication */
    else{
      assert(p->ops[i].func == MUL);
      e->outputs[i] = src1 * src2;
    }
  }
}


int slp_equal_multi(const SLPT p1, const SLPT p2, long num_outputs, long num_trials){

  int i,x,j;
  int numb_inputs;
  int is_equal = 1;
  int p1out,p2out;

  EvalT eval1;
  EvalT eval2;

  p1out = p1->length;
  p2out = p2->length;

  assert(p1->inputs == p2->inputs);
  numb_inputs = p1->inputs;

  /* check to see how many outputs each eval has
  if one has less then the number we need to check throw error */
  if(p1out < num_outputs || p2out < num_outputs){
    printf("number of outputs in SLP is less than number of outputs needed\n");
    return 0;
  }

  /* Start for loop for num_trials here */
  omp_set_num_threads(16);
  #pragma omp parallel for private(eval1,eval2,i,x) reduction(&&:is_equal) schedule(guided,1)
  for(j = 0; j < num_trials; j++){
    if(is_equal){
      eval_init(eval1,p1);
      eval_init(eval2,p2);

      for(i = 0; i < numb_inputs; i++){
        x = rand()%(1L<<20)-(1L<<19);
        eval1->inputs[i] = x;
        eval2->inputs[i] = x;
      }


      evaluate(eval1);
      evaluate(eval2);



      /* for loop checking the outputs of both SLPs against each other */
      for(i = 1; i < num_outputs+1; i++){
        if(eval1->outputs[p1out-i] != eval2->outputs[p2out-i])
        {
          /* states that the outputs are not equal */
          is_equal = 0;
        }
      }


      /* must clear evals before reassigning them */
      eval_clear(eval1);
      eval_clear(eval2);
    }
    else{ /* Do nothing */ }
  }
  /* If you exit the for statement everything should be equal so return 1 */
  return is_equal;
}

void input_buf(SLPT s, const char* data, int init) {
  size_t offset = 0;
  long len;

  memcpy(&len, data + offset, sizeof s->length);
  offset += sizeof s->length;

  memcpy(&s->inputs, data + offset, sizeof s->inputs);
  offset += sizeof s->inputs;

  if (init) {
    /* already initialized */
    if (s->length != len)
      s->ops = realloc(s->ops, s->length * sizeof *s->ops);
  }
  else {
    /* not initialized yet */
    s->ops = malloc(len * sizeof *s->ops);
  }
  s->length = len;

  memcpy(s->ops, data + offset, s->length * sizeof *s->ops);

  assert(offset + s->length * sizeof *s->ops == byte_size(s));
}

/* takes SLP and converts to char array */
void output_buf(const SLPT s, char* data) {
  size_t offset = 0;

  memcpy(data + offset, &s->length, sizeof s->length);
  offset += sizeof s->length;

  memcpy(data + offset, &s->inputs, sizeof s->inputs);
  offset += sizeof s->inputs;

  memcpy(data + offset, s->ops, s->length * sizeof *s->ops);

  assert(offset + s->length * sizeof *s->ops == byte_size(s));
}

void random_slp(SLPT s) {
  /* note: assumes srand() already called. */
  long i;
  for (i = 0; i < s->length; ++i) {
    s->ops[i].func = rand_bound(3) + 1;
    if (i == 0 || rand_bound(2)) /* input or output arg */
      s->ops[i].arg1 = -1 - rand_bound(s->inputs);
    else
      s->ops[i].arg1 = rand_bound(i);
    if (rand_bound(2)) { /* scalar or non-scalar */
      s->ops[i].type = SCALAR;
      s->ops[i].arg2.literal = rand_bound(16) - 8;
    }
    else {
      s->ops[i].type = REGULAR;
      if (i == 0 || rand_bound(2)) /* input or output 2nd arg */
        s->ops[i].arg2.ind = -1 - rand_bound(s->inputs);
      else
        s->ops[i].arg2.ind = rand_bound(i);
    }
  }
}
