/* Simple multivariate polynomial manipulation utilities. */

#ifndef POLY_H
#define POLY_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

typedef unsigned short ExponT;
typedef long CoeffT;

typedef struct {
  CoeffT coeff;
  ExponT* expons;
} Term;

typedef struct {
  int nvars;
  long len;
  long alloc;
  ExponT* expon_data;
  Term* terms;
} Poly;
typedef Poly PolyT[1];

/* initialilze with saved space for alloc terms */



void poly_init2(PolyT f, int nvars, long alloc);

static __inline__ void poly_init(PolyT f, int nvars) {
  poly_init2(f, nvars, 10);
}


/* ensures space for at least alloc terms */
void _poly_reserve(PolyT f, long alloc);

static __inline__ void poly_clear(PolyT f) {
  free(f->terms);
  free(f->expon_data);
}

/* makes sure the terms are sorted with no duplicate terms. */
void _poly_normalize(PolyT f);

static __inline__ void poly_set(PolyT f, const PolyT a) {
  if (f == a) return;
  else {
    long i;

    if (f->nvars != a->nvars) {
      poly_clear(f);
      poly_init2(f, a->nvars, a->len);
    }
    else _poly_reserve(f, a->len);

    for (i = 0; i < a->len; ++i) {
      f->terms[i].coeff = a->terms[i].coeff;
      memcpy(f->terms[i].expons, a->terms[i].expons, a->nvars * sizeof(ExponT));
    }

    f->len = a->len;
  }
}

/* sets f to the zero polynomial */
static __inline__ void poly_zero(PolyT f) {
  f->len = 0;
}

/* sets f to the single variable x_{which_var} */
static __inline__ void poly_set_var(PolyT f, int which_var) {
  assert(f->alloc >= 1);
  f->terms[0].coeff = 1;
  memset(f->terms[0].expons, 0, f->nvars * sizeof(ExponT));
  f->terms[0].expons[which_var] = 1;
  f->len = 1;
}

/* sets f to the constant c */
static __inline__ void poly_set_const(PolyT f, CoeffT c) {
  poly_zero(f);
  assert(f->alloc >= 1);
  if (c != 0) {
    f->terms[0].coeff = c;
    memset(f->terms[0].expons, 0, f->nvars * sizeof(ExponT));
    f->len = 1;
  }
}

/* helper function to compare two exponent tuples */
extern int poly_cmp_nvars;
# pragma omp threadprivate(poly_cmp_nvars)
static __inline__ int poly_term_cmp(const void* t1, const void* t2) {
  int i;
  const ExponT* e1 = ((Term*)t1)->expons;
  const ExponT* e2 = ((Term*)t2)->expons;
  for (i = 0; i < poly_cmp_nvars; ++i) {
    if (e1[i] > e2[i]) return -1;
    if (e1[i] < e2[i]) return 1;
  }
  return 0;
}

/* adds f = a + c*b where c is a scalar */
void poly_addmul(PolyT f, const PolyT a, CoeffT c, const PolyT b,int mainline,int rank,int op);

/* adds f = a + b */
static __inline__ void poly_add(PolyT f, const PolyT a, const PolyT b,int mainline,int rank) {
  poly_addmul(f, a, 1, b,mainline,rank,1);
}

/* subtracts f = a - b */
static __inline__ void poly_sub(PolyT f, const PolyT a, const PolyT b,int mainline,int rank) {
  poly_addmul(f, a, -1, b,mainline,rank,2);
}

/* multiplies f = a * b */
void poly_mul(PolyT f, const PolyT a, const PolyT b);

/* adds f = a + s where s is a scalar */
static __inline__ void poly_sadd(PolyT f, const PolyT a, CoeffT s,int mainline,int rank) {
  PolyT zeropoly;
  zeropoly->len = zeropoly->alloc = 0;
  zeropoly->nvars = a->nvars;
  poly_addmul(f, zeropoly, s, a,mainline,rank,3);
}

/* f = a * s where s is a scalar */
static __inline__ void poly_smul(PolyT f, const PolyT a, CoeffT s) {
  long i;
  if (s == 0) {
    poly_zero(f);
    return;
  }
  poly_set(f, a);
  for (i = 0; i < f->len; ++i) {
    f->terms[i].coeff *= s;
  }
}

void poly_fprint(FILE* stream, const PolyT f);

static __inline__ void poly_print(const PolyT f) {
  poly_fprint(stdout, f);
}

void poly_fread(FILE* stream, PolyT f);

static __inline__ void poly_read(PolyT f) {
  poly_fread(stdin, f);
}

/* returns 1 iff the exponent array is zero */
static __inline__ int zero_expon(const ExponT* expons, int nvars) {
  int i;
  for (i = 0; i < nvars; ++i) {
    if (expons[i]) return 0;
  }
  return 1;
}

int poly_equality(const PolyT p1, const PolyT p2);

#endif /* POLY_H */
