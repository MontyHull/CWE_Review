/* Header file defining algebraic circuits and associated operations. */

#ifndef CIRCUIT_H
#define CIRCUIT_H

#include <stdlib.h>
#include <assert.h>
#include <stdio.h>

typedef long Value;
typedef long Index;

typedef union {
  Index ind;
  Value literal;
} Arg;

typedef enum {
  ADD=1,
  MUL,
  SUB
} OpCode;

extern OpCode last_op;

typedef enum {
  REGULAR=1,
  SCALAR
} OpType;

typedef struct {
  OpCode func;
  OpType type;
  Index arg1;
  Arg arg2;
} Op;
typedef Op OpT[1];

typedef struct {
  long length;
  long inputs;
  Op* ops;
} SLP;
typedef SLP SLPT[1];

typedef struct {
  const SLP* slp;
  Value* inputs;
  Value* outputs;
} Eval;
typedef Eval EvalT[1];

/* returns a random integer from 0 up to (x-1) */
static __inline__ int rand_bound(int x) {
  int res, min;
  assert(x > 0);
  min = (((unsigned int) RAND_MAX) + 1) % ((unsigned int) x);
  for (res = rand(); res < min; res = rand());
  return res % x;
}

static __inline__ void regular_op(OpT op, OpCode func, Index ind1, Index ind2) {
  op->func = func;
  op->type = REGULAR;
  op->arg1 = ind1;
  op->arg2.ind = ind2;
}

static __inline__ void scalar_op(OpT op, OpCode func, Index ind1, Value val2) {
  op->func = func;
  op->type = SCALAR;
  op->arg1 = ind1;
  op->arg2.literal = val2;
}

static __inline__ Op* get_op(const SLPT p, Index ind) {
  assert(ind >= 0 && ind < p->length);
  return p->ops + ind;
}

static __inline__ long input_index(Index ind) {
  assert(ind < 0);
  return -(ind + 1);
}

static __inline__ void slp_init(SLPT p, long inputs, long len) {
  p->length = len;
  p->inputs = inputs;
  p->ops = calloc(p->length, sizeof *p->ops);
}

static __inline__ void slp_clear(SLPT p) {
  free(p->ops);
}

static __inline__ void eval_init(EvalT e, const SLPT p) {
  e->slp = p;
  e->inputs = malloc(p->inputs * sizeof *e->inputs);
  e->outputs = malloc(p->length * sizeof *e->outputs);
}

static __inline__ void eval_init_size(EvalT e, long inputs, long length) {
  e->slp = NULL;
  e->inputs = malloc(inputs * sizeof *e->inputs);
  e->outputs = malloc(length * sizeof *e->outputs);
}

static __inline__ void eval_set_slp(EvalT e, const SLPT p) {
  e->slp = p;
}

static __inline__ void eval_clear(EvalT e) {
  free(e->inputs);
  free(e->outputs);
}

void evaluate(EvalT e);


/* Returns 1 if the two programs evaluate to the same result on num_trials
 * different settings of random inputs.
 * Only the last num_outputs results in each program are checked
 * for equality. */
int slp_equal_multi(const SLPT p1, const SLPT p2, long num_outputs, long num_trials);

/* Checks only for the last outputs being equal, on 10 different random runs. */
static __inline__ int slp_equal(const SLPT p1, const SLPT p2) {
  return slp_equal_multi(p1, p2, 1, 10);
}

void input(SLPT s,FILE* fp);

void output(const SLPT s, FILE* fp);

/* returns the number of bytes needed to store the given SLP */
static __inline__ size_t byte_size(const SLPT s) {
  return sizeof s->length + sizeof s->inputs + s->length * sizeof *s->ops;
}

/* Reads an SLP from the given array.
 * The last argument init should be 1 iff s has already been initialized.
 */
void input_buf(SLPT s, const char* data, int init);

/* writes the given SLP to memory at the given pointer location.
 * It is assumed the memory has enough room according to byte_size().
 */
void output_buf(const SLPT s, char* data);

/* s should already be initialized with the desired length and # of vars. */
void random_slp(SLPT s);

void findSLP(SLPT s,int op,FILE* fp);

void findPhaseSLP(SLPT s,int op,int phase,int numPhases,long* phaseArray);

#endif
/* CIRCUIT_H */
