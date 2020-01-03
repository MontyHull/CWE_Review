/* test program for generated karatsuba's algorithm */

#include <iostream>
using namespace std;

// pull in generated code
#include "karatsuba.c"

int main() {
  const int sa = 2;
  const int sb = 2;
  T ab[sa + sb];
  T* a = ab;
  T* b = ab + sa;

  cout << "Enter coeffs of first polynomial: " << flush;
  for (int i=0; i < sa; ++i) cin >> a[i];

  cout << "Enter coeffs of second polynomial: " << flush;
  for (int i=0; i < sb; ++i) cin >> b[i];

  const int sc = sa + sb - 1;
  T c[sc];
  karatsuba(c, ab);

  cout << "Result coeffs:";
  for (int i=0; i < sc; ++i) cout << ' ' << c[i];
  cout << endl;

  return 0;
}
