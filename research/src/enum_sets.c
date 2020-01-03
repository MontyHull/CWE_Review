#include <stdio.h>
#include <string.h>
#include "circuit.h"
#include <math.h>
#include <stdlib.h>
#include "poly.h"
#include "conv.h"
#include <unistd.h>

long count;
long count1;
int eval_pos;

FILE* fp;
int rank;
int iter;

void phase5(SLPT s,int op,const int* phaseArray,EvalT ev,long answer,PolyT poly1,PolyT poly2,int rank){
    int ind1,ind2;
    OpCode opCode;


    if(op == phaseArray[4]){
        count ++;
        return;
    }

    /* iterates from negative indexes (inputs) to positive indexes (outputs)
     * the number of outputs increases by 1 for each operation */
    for(ind1 = phaseArray[2]; ind1 < op; ind1++){
        for(ind2 = phaseArray[2]; ind2 < op; ind2++){
            for(opCode = ADD; opCode <= SUB; opCode+=2){
                regular_op(s->ops+op,opCode,ind1,ind2);

                /* recursive call */
                phase5(s,op+1,phaseArray,ev,answer,poly1,poly2,rank);
                eval_pos = op;

            }
        }
    }
}




void phase5p2(SLPT s, int op, const int* phaseArray, int ind2, int curout,EvalT ev,long answer,PolyT poly1,PolyT poly2,int rank) {
  OpCode opCode;
  int l;
  Index arg1;
  Value src1;
  Value src2;
  FILE* fp;
  char output_location[200];


  if (op == phaseArray[4]) {
    assert(ind2 == phaseArray[3]);
    ++count;


    /* TODO base case stuff here */
    for(l = eval_pos; l < s->length; l++){
      /* src1:
      * arg1 is always an index */
      arg1 = s->ops[l].arg1;

      /* src from input or output */
      if(arg1 >= 0){  src1 = ev->outputs[arg1];  }
      else{  src1 = ev->inputs[input_index(arg1)];  }

      /* src2: */
      /* src2 is value,from outputs, or from inputs */
      if(s->ops[l].type == SCALAR){
        src2 = s->ops[l].arg2.literal;
      }
      else if(s->ops[l].arg2.ind >= 0){
        assert(s->ops[l].type == REGULAR);
        src2 = ev->outputs[s->ops[l].arg2.ind];
      }
      else{
        assert(s->ops[l].type == REGULAR && s->ops[l].arg2.ind < 0);
        src2 = ev->inputs[input_index(s->ops[l].arg2.ind)];
      }

      /* add,mul,sub */
      if(s->ops[l].func == ADD){  ev->outputs[l] = src1 + src2;  }
      else if(s->ops[l].func == SUB){  ev->outputs[l] = src1 - src2;  }
      else{  assert(s->ops[l].func == MUL);  ev->outputs[l] = src1 * src2;  }
    }

    /* evaluate here */

    if(ev->outputs[s->length-1] == answer){
      /* if they evaluate the same then turn the slp to a poly*/
      slp2poly(poly2,s,1,0,0);

      /* check if the two polynomials are equal */
      if(poly_equality(poly1,poly2)){
        /* if equal print the new slp to a file */

        sprintf(output_location, "./output/rank-%d:number-%d",rank,iter);
        fp = fopen(output_location,"w");
        output(s,fp);
        fclose(fp);

        iter++;

        /*printf("We found it!\n");*/
      }
    }


    return;
  }

  for (opCode = ADD; opCode <= SUB; opCode += 2) {
    regular_op(s->ops + op, opCode, curout, ind2);
    phase5p2(s, op+1, phaseArray, ind2+1, op,ev,answer,poly1,poly2,rank);
    eval_pos = op;

  }
}

void phase5p1(SLPT s, int op, const int* phaseArray,EvalT ev,long answer,PolyT poly1,PolyT poly2,int rank) {
  int ind0, ind2, curout, nextop;

  for (ind0 = phaseArray[2]; ind0 < phaseArray[3]; ++ind0) {
    /* ind0 is the start of the chain */
    curout = ind0;
    nextop = op;
    for (ind2 = phaseArray[2]; ind2 < ind0; ++ind2) {
      /* all indices less than ind0 get subtracted */
      regular_op(s->ops + nextop, SUB, curout, ind2);
      curout = nextop;
      ++nextop;
    }
    /* add or subtract all indices greater than ind0 */
    phase5p2(s, nextop, phaseArray, ind0+1, curout,ev,answer,poly1,poly2,rank);
    /*TODO should evalpos be set to op here? */
  }
}

void phase4(SLPT s,int op,const int* phaseArray,EvalT ev,long answer,PolyT poly1,PolyT poly2,int rank){

    int ind1,ind2;
    OpCode opCode;

    opCode = MUL;

    if(op == phaseArray[3]){

        /*count++;*/
        /*printf("%i\n",count);*/

        phase5p1(s,phaseArray[3],phaseArray,ev,answer,poly1,poly2,rank);
        return;
    }

    /* iterates from negative indexes (inputs) to positive indexes (outputs)
     * the number of outputs increases by 1 for each operation */
    for(ind1 = s->inputs*-1; ind1 < phaseArray[0]; ind1++){
        for(ind2 = phaseArray[0]; ind2 < phaseArray[2]; ind2++){
            regular_op(s->ops+op,opCode,ind1,ind2);

            /* recursive call */
            phase4(s,op+1,phaseArray,ev,answer,poly1,poly2,rank);
            eval_pos = op;

        }
    }
}

void phase3(SLPT s,int op,const int* phaseArray,EvalT ev,long answer,PolyT poly1,PolyT poly2,int rank){
    int ind1,ind2;
    OpCode opCode;

    if(op == phaseArray[2]){
        phase4(s,phaseArray[2],phaseArray,ev,answer,poly1,poly2,rank);
        /*output(s,fp);*/
        return;
    }

    /* addition */
    opCode = ADD;
    for(ind1 = phaseArray[0]; ind1 < op; ind1++){
        for(ind2 = phaseArray[0]; ind2 < op; ind2++){
            regular_op(s->ops+op,opCode,ind1,ind2);

            /* recursive call */
            phase3(s,op+1,phaseArray,ev,answer,poly1,poly2,rank);
            eval_pos = op;

        }
    }

    /* subtraction */
    opCode = SUB;
    for(ind1 = phaseArray[0]; ind1 < op; ind1++){
        for(ind2 = phaseArray[0]; ind2 < op; ind2++){
            regular_op(s->ops+op,opCode,ind1,ind2);

            /* recursive call */
            phase3(s,op+1,phaseArray,ev,answer,poly1,poly2,rank);
            eval_pos = op;

        }
    }
}

void phase2(SLPT s,int op,const int* phaseArray,EvalT ev,long answer,PolyT poly1,PolyT poly2,int rank){
    int ind1,ind2;
    OpCode opCode;

    opCode = MUL;

    if(op == phaseArray[1]){

        /*output(s,fp);*/
        /*count++;*/

        phase3(s,phaseArray[1],phaseArray,ev,answer,poly1,poly2,rank);
        return;
    }

    /* iterates from negative indexes (inputs) to positive indexes (outputs)
     * the number of outputs increases by 1 for each operation */
    for(ind1 = s->inputs*-1; ind1 < phaseArray[0]; ind1++){
        for(ind2 = ind1; ind2 < phaseArray[0]; ind2++){
            regular_op(s->ops+op,opCode,ind1,ind2);

            /* recursive call */
            phase2(s,op+1,phaseArray,ev,answer,poly1,poly2,rank);
            eval_pos = op;

        }
    }
}

void phase1(SLPT s,int op,const int* phaseArray,EvalT ev,long answer,PolyT poly1,PolyT poly2,int rank){
    int ind1,ind2;
    OpCode opCode;

    if(op == phaseArray[0]){
        phase2(s,phaseArray[0],phaseArray,ev,answer,poly1,poly2,rank);
        count1++;

        /*count ++;*/
        /*output(s,fp);*/
        return;
    }


    /* addition */
    opCode = ADD;
    for(ind1 = s->inputs*-1; ind1 < op; ind1++){
        for(ind2 = ind1; ind2 < op; ind2++){
            regular_op(s->ops+op,opCode,ind1,ind2);

            /* recursive call */
            phase1(s,op+1,phaseArray,ev,answer,poly1,poly2,rank);
            eval_pos = op;

        }
    }

    /* subtraction */
    opCode = SUB;
    for(ind1 = s->inputs*-1; ind1 < op; ind1++){
        for(ind2 = s->inputs*-1; ind2 < op; ind2++){
            regular_op(s->ops+op,opCode,ind1,ind2);

            /* recursive call */
            phase1(s,op+1,phaseArray,ev,answer,poly1,poly2,rank);
            eval_pos = op;

        }
    }
}

int main(){
    int phaseArray[5];
    int numInputs;
    SLPT s;
    EvalT ev;
    long answer;
    PolyT poly1,poly2;
    rank = 0;

    count = 0;
    answer = 100;
    eval_pos = 0;
    iter = 0;
    fp = fopen("enumSetsOutputs","w");

    numInputs = 9;
    phaseArray[0] = 2;
    phaseArray[1] = phaseArray[0] + 1;
    phaseArray[2] = phaseArray[1] + 1;
    phaseArray[3] = phaseArray[2] + 3;
    phaseArray[4] = phaseArray[3] + 2;


    /* initialize slp */
    slp_init(s,numInputs,phaseArray[4]);
    poly_init(poly1,10);
    poly_init(poly2,10);
    eval_init(ev,s);


    /* start phases */
    phase1(s,0,phaseArray,ev,answer,poly1,poly2,rank);

    printf("count = %ld count1 = %ld\n",count,count1);

    fclose(fp);
    slp_clear(s);

    return 0;
}
