#include <stdio.h>
#include <string.h>
#include "circuit.h"
#include <math.h>
#include <stdlib.h>
#include "poly.h"
#include "conv.h"

/* counts total number of possible SLPs */
int count;

/* find all possible SLPs */
void findSLP(SLPT s,int op,FILE* fp){
    int ind1,ind2;
    OpCode opCode;
    
    /* base case */
    if(op == s->length){
        output(s,fp); 
        count++;
        
        return;
    }
    
    /* iterates from negative indexes (inputs) to positive indexes (outputs)
     * the number of outputs increases by 1 for each operation */
    for(ind1 = s->inputs*-1; ind1 < op; ind1++){
        for(ind2 = s->inputs*-1; ind2 < op; ind2++){
            for(opCode = ADD; opCode <= SUB; opCode++){
                regular_op(s->ops+op,opCode,ind1,ind2);
                
                /* recursive call */
                findSLP(s,op+1,fp);
            }            
        }
    }
}

int main(){
    SLPT s;
    FILE* fp;
    int inputs,length;
        
    count = 0;
    fp = fopen("slpOutputs","w");
    
    /* get number of inputs and check that it is a perfect square */
    printf("number of inputs: ");
    scanf("%i",&inputs);
    assert((int)sqrt(inputs)*(int)sqrt(inputs) == inputs);
    
    /* get number of operations */
    printf("length: ");
    scanf("%i",&length);
    assert(length > 0);
    
    printf("\n");
    
    /* initialize SLP */
    slp_init(s,inputs,length);
    
    /* function call to find SLPs */
    findSLP(s,0,fp);
    
    
    printf("Total: %i\n",count);
    
    fclose(fp);
    slp_clear(s);
        
    return 0;
}