#include "circuit.h"
#include <stdio.h>

int main(){

 SLPT det22;
 FILE* fp1 = fopen("2x2","r");
 FILE* fp2 = fopen("new2x2","w");

 input(det22,fp1);



 output(det22,fp2);

 return 0;
}
