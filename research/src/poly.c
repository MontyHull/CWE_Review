#include "poly.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <ctype.h>

int poly_cmp_nvars = 0;

void poly_init2(PolyT f, int nvars, long alloc) {
  long i;
  ExponT* eptr;

  f->nvars = nvars;
  f->len = 0;
  f->alloc = alloc;

  f->expon_data = malloc(f->nvars * f->alloc * sizeof *f->expon_data);
  f->terms = malloc(f->alloc * sizeof *f->terms);

  for (i = 0, eptr = f->expon_data; i < f->alloc; ++i, eptr += nvars) {
    f->terms[i].expons = eptr;
  }
}

void _poly_reserve(PolyT f, long alloc) {
  if (f->alloc < alloc) {
    long new_alloc;
    long i;
    ExponT* newdata;
    ExponT* neweptr;

    if (alloc > 2 * f->alloc) new_alloc = alloc;
    else new_alloc = 2 * f->alloc;

    newdata = malloc(new_alloc * f->nvars * sizeof *f->expon_data);
    f->terms = realloc(f->terms, new_alloc * sizeof *f->terms);

    for (i = 0, neweptr = newdata; i < f->alloc; ++i, neweptr += f->nvars) {
      memcpy(neweptr, f->terms[i].expons, f->nvars * sizeof *neweptr);
      f->terms[i].expons = neweptr;
    }
    for (; i < new_alloc; ++i, neweptr += f->nvars) {
      f->terms[i].expons = neweptr;
    }

    free(f->expon_data);
    f->expon_data = newdata;

    f->alloc = new_alloc;
  }
  assert(f->alloc >= alloc);
}

void _poly_normalize(PolyT f) {
  long i = 0, j = 0;
  poly_cmp_nvars = f->nvars;
  qsort(f->terms, f->len, sizeof *f->terms, poly_term_cmp);
  while (j < f->len) {
    if (i != j) {
      /* copy the term down */
      f->terms[i].coeff = f->terms[j].coeff;
      {
        ExponT* temp = f->terms[i].expons;
        f->terms[i].expons = f->terms[j].expons;
        f->terms[j].expons = temp;
      }
    }

    /* combine matching terms */
    for (++j; j < f->len && poly_term_cmp(f->terms + i, f->terms + j) == 0; ++j) {
      f->terms[i].coeff += f->terms[j].coeff;
    }

    /* check for zero coeff from cancellation */
    if (f->terms[i].coeff != 0) ++i;
  }
  f->len = i;
}




static __inline__ void _poly_term_copy(PolyT p1, long ind1, const PolyT p2, long ind2,
      int mainline,int ptcline, int rank,int op) {
  assert(p1->nvars == p2->nvars);
  if(ind1 > p1->alloc){ printf("the mainline is %d, ptcopy is %d and rank is %d and op is %d\n",mainline,ptcline,rank,op);}
  assert(ind1 < p1->alloc);
  assert(ind2 < p2->len);
  p1->terms[ind1].coeff = p2->terms[ind2].coeff;
  memcpy(p1->terms[ind1].expons, p2->terms[ind2].expons, p1->nvars * sizeof(ExponT));
}

void poly_addmul(PolyT f, const PolyT a, CoeffT c, const PolyT b,int mainline,int rank,int op) {
  long aind = 0, bind = 0, find = 0;
  PolyT temp;

  assert(a->nvars == b->nvars);

  /* special cases; adding zero polynomial */
  if (a->len == 0) {
    poly_set(f, b);
    return;
  }
  else if (b->len == 0 || c == 0) {
    poly_set(f, a);
    return;
  }

  /* check for "aliasing" between inputs and output */
  if (f == a) {
    poly_init2(temp, a->nvars, a->len);
    poly_set(temp, a);
    a = temp;
    if (f == b) b = temp;
  }
  else if (f == b) {
    poly_init2(temp, b->nvars, b->len);
    poly_set(temp, b);
    b = temp;
  }

  /* ensure number of variables match */
  if (f->nvars != a->nvars) {
    poly_clear(f);
    poly_init2(f, a->nvars, a->len + b->len);
  }
  else _poly_reserve(f, a->len + b->len);

  if(f->alloc < a->len + b->len){ printf("the mainline is %d, rank is %d and op is %d\n",mainline,rank,op);}
  assert(f->alloc >= a->len + b->len);

  /* merge and combine like terms */
  poly_cmp_nvars = f->nvars;
  while (aind < a->len && bind < b->len) {
    int cmp = poly_term_cmp(a->terms + aind, b->terms + bind);

    if (cmp < 0) {
      _poly_term_copy(f, find, a, aind,mainline,123,rank,op);
      ++aind, ++find;
    }
    else if (cmp > 0) {
      _poly_term_copy(f, find, b, bind,mainline,127,rank,op);
      f->terms[find].coeff *= c;
      ++bind, ++find;
    }
    else { /* (cmp == 0) */
      _poly_term_copy(f, find, a, aind,mainline,132,rank,op);
      f->terms[find].coeff += c * b->terms[bind].coeff;
      if (f->terms[find].coeff) {
        /* only do this if the coefficient is not zero */
        memcpy(f->terms[find].expons, a->terms[aind].expons, f->nvars * sizeof(ExponT));
        ++find;
      }
      ++aind, ++bind;
    }
  }

  for (; aind < a->len; ++aind, ++find) {
    _poly_term_copy(f, find, a, aind,mainline,144,rank,op);
  }

  for (; bind < b->len; ++bind, ++find) {
    _poly_term_copy(f, find, b, bind,mainline,148,rank,op);
    f->terms[find].coeff *= c;
  }

  assert(find <= f->alloc);
  f->len = find;

  if (temp == a || temp == b) poly_clear(temp);
}

typedef struct {
  long aind;
  const Term* bterm;
  Term pterm;
} MulHeap;

static __inline__ void add_expons(ExponT* x, const ExponT* a, const ExponT* b, int n) {
  int i;
  for (i = 0; i < n; ++i) x[i] = a[i] + b[i];
}

static __inline__ void heap_swap(MulHeap* heap, long i, long j) {
  long tempai = heap[i].aind;
  const Term* tempbt = heap[i].bterm;
  CoeffT tempc = heap[i].pterm.coeff;
  ExponT* tempe = heap[i].pterm.expons;
  assert(i != j);
  heap[i].aind = heap[j].aind;
  heap[j].aind = tempai;
  heap[i].bterm = heap[j].bterm;
  heap[j].bterm = tempbt;
  heap[i].pterm.coeff = heap[j].pterm.coeff;
  heap[j].pterm.coeff = tempc;
  heap[i].pterm.expons = heap[j].pterm.expons;
  heap[j].pterm.expons = tempe;
}

void poly_mul(PolyT f, const PolyT a, const PolyT b) {
  long find = -1, i, cur;
  PolyT temp;
  MulHeap* heap;
  long heaplen;
  ExponT* expon_pool;
  int nvars = a->nvars;

  /* ensure number of variables match */
  assert(a->nvars == b->nvars);
  if (f->nvars != nvars) {
    poly_clear(f);
    poly_init2(f, nvars, a->len * b->len);
  }
  else _poly_reserve(f, a->len * b->len);

  /* special case: multiply by zero */
  if (a->len == 0 || b->len == 0) {
    poly_zero(f);
    return;
  }

  /* check for "aliasing" between inputs and output */
  if (f == a) {
    poly_init2(temp, nvars, a->len);
    poly_set(temp, a);
    a = temp;
    if (f == b) b = temp;
  }
  else if (f == b) {
    poly_init2(temp, nvars, b->len);
    poly_set(temp, b);
    b = temp;
  }

  /* ensure len(a) >= len(b) */
  if (a->len < b->len) {
    const Poly* temp = a;
    a = b;
    b = temp;
  }

  /* initialize the heap. There is one entry for each term in b. */
  heap = malloc(b->len * sizeof *heap);
  heap[0].pterm.expons = expon_pool = malloc(b->len * nvars * sizeof *expon_pool);
  for (i = 0; i < b->len; ++i) {
    /* assign expon pointer in heap entry from the pool */
    if (i) heap[i].pterm.expons = heap[i-1].pterm.expons + nvars;
    /* assign rest of the heap entry */
    heap[i].aind = 0;
    heap[i].bterm = b->terms + i;
    heap[i].pterm.coeff = a->terms[0].coeff * b->terms[i].coeff;
    add_expons(heap[i].pterm.expons, a->terms[0].expons, b->terms[i].expons, nvars);
  }
  heaplen = i;

  /* run the heap multiplication */
  poly_cmp_nvars = nvars;
  while (1) {
    assert(find < 0 || poly_term_cmp(f->terms + find, &heap[0].pterm) <= 0);
    if (find < 0 || poly_term_cmp(f->terms + find, &heap[0].pterm) < 0) {
      /* move to next term in f if the exponents are different */
      if (find < 0 || f->terms[find].coeff != 0) ++find;
      assert(find >= 0 || find < f->alloc);
      memcpy(f->terms[find].expons, heap[0].pterm.expons, nvars * sizeof(ExponT));
      f->terms[find].coeff = heap[0].pterm.coeff;
    }
    else f->terms[find].coeff += heap[0].pterm.coeff;

    /* update the term on top of the heap */
    if (++heap[0].aind == a->len) {
      /* special case: this term in b is finished. Remove from the heap. */
      if (--heaplen == 0) break;
      heap_swap(heap, 0, heaplen);
    }
    else {
      const Term* aterm = a->terms + heap[0].aind;
      heap[0].pterm.coeff = aterm->coeff * heap[0].bterm->coeff;
      add_expons(heap[0].pterm.expons, aterm->expons, heap[0].bterm->expons, nvars);
    }

    /* bubble down to restore the heap */
    cur = 0;
    while (2*cur + 1 < heaplen) {
      long child = 2*cur + 1;
      if (child + 1 < heaplen && poly_term_cmp(&heap[child].pterm, &heap[child+1].pterm) > 0)
        ++child;
      if (poly_term_cmp(&heap[cur].pterm, &heap[child].pterm) <= 0) break;
      heap_swap(heap, cur, child);
      cur = child;
    }
  }

  f->len = find + 1;

  /* clean-up */
  free(expon_pool);
  free(heap);
  if (temp == a || temp == b) poly_clear(temp);
}

/* determines which variable letter goes for index 0 */
static __inline__ char get_var0(int nvars) {
  if (nvars <= 3) return 'x';
  else return 'z' - (nvars - 1);
}

void poly_fprint(FILE* stream, const PolyT f) {
  long i;
  int j;
  int sign = 1;
  char var0 = get_var0(f->nvars);

  fprintf(stream, "(%d,%ld)", f->nvars, f->len);
  for (i = 0; i < f->len; ++i) {
    if (i) {
      if (f->terms[i].coeff < 0) {
        fputs(" - ", stream);
        sign = -1;
      }
      else {
        fputs(" + ", stream);
        sign = 1;
      }
    }
    else fputc(' ', stream);
    assert(f->terms[i].coeff != 0);
    if (f->terms[i].coeff == 1 || f->terms[i].coeff == -1) {
      if (f->terms[i].coeff * sign == -1) fputc('-', stream);
      if (zero_expon(f->terms[i].expons, f->nvars))
        fputc('1', stream);
    }
    else fprintf(stream, "%ld", f->terms[i].coeff * sign);
    for (j = 0; j < f->nvars; ++j) {
      if (f->terms[i].expons[j]) {
        fputc(var0 + j, stream);
        if (f->terms[i].expons[j] > 1)
          fprintf(stream, "%hu", f->terms[i].expons[j]);
      }
    }
  }
  fputs(";\n", stream);
}

/* more or less equivalent to fscanf(stream, " %lu") but it
 * stops reading if it sees a sign character + or -.
 * Returns 1 if no characters were read.
 */
static __inline__ long read_unsigned(FILE* stream) {
  char c = '\0';
  long res = 0;
  fscanf(stream, " %c", &c);
  if (!isdigit(c)) res = 1;
  while (isdigit(c)) {
    res *= 10;
    res += c - '0';
    fscanf(stream, "%c", &c);
  }
  ungetc(c, stream);
  return res;
}

/* tries to read a single sign character + or - from the
 * given stream, and returns 1 or -1 accordingly.
 * If there is no sign character, 1 is returned.
 */
static __inline__ int read_sign(FILE* stream) {
  char c = '\0';
  if (fscanf(stream, " %c", &c) == 0) return 1;
  if (c == '+') return 1;
  if (c == '-') return -1;
  ungetc(c, stream);
  return 1;
}

/* tries to read a single variable name from input.
 * Returns the corresponding index, or -1 if no variable
 * was read.
 */
static __inline__ int read_var(FILE* stream, int nvars) {
  char c = '\0';
  int res;
  if (fscanf(stream, " %c", &c) == 0) return -1;
  res = c - get_var0(nvars);
  if (res >= 0 && res < nvars) return res;
  ungetc(c, stream);
  return -1;
}

void poly_fread(FILE* stream, PolyT f) {
  long i;
  int j;
  int res;
  int nvars;
  long len;
  int sign;
  char semi;

  res = fscanf(stream, " (%d,%ld)", &nvars, &len);
  assert (res == 2);

  poly_init2(f, nvars, len);
  f->len = len;

  for (i = 0; i < len; ++i) {
    sign = read_sign(stream);
    f->terms[i].coeff = read_unsigned(stream) * sign;
    memset(f->terms[i].expons, 0, f->nvars * sizeof(ExponT));
    for (j = read_var(stream, nvars); j >= 0; j = read_var(stream, nvars)) {
      f->terms[i].expons[j] = (ExponT) read_unsigned(stream);
    }
  }

  fscanf(stream, " %c", &semi);
  assert(semi == ';');

  _poly_normalize(f);
}

int poly_equality(const PolyT p1, const PolyT p2){

  /* loop variables */
  int i, j;

  /* if the number of variables != return false */
  if(p1->nvars != p2->nvars){
    return 0;
  }

  /* if the length of the polynomials != return false */
  if(p1->len != p2->len){
    return 0;
  }

  /* Itterates through every term */
  for(i = 0; i < p1->len;i++){
    if (p1->terms[i].coeff != p2->terms[i].coeff) return 0;
    /* Itterates through every part of the expons */
    for(j = 0; j < p1->nvars;j++){
      /* If any part of the expons are not equal return false */
      if(p1->terms[i].expons[j] != p2->terms[i].expons[j]){
        return 0;
      }
    }
  }

  /* if all conditions are met return true */
  return 1;
}
