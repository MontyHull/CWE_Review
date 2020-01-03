/* SI 413 Fall 2015
 * regall.hpp
 * C++ header file providing the RegAll class.
 */

#ifndef REGALL_HPP
#define REGALL_HPP

#include <iostream>
#include <cstdlib>
#include <vector>
using namespace std;

/*
 *  RegAll - a simplistic REGister ALLocator
 */
class RegAll {
  private:
    int *regs;
    int size;
    int low;

    /*
     * bfmi, for low sizes
     */
    int
    findFirst() {
	int i = 0;
	int retval = -1;
	for (i=0; i < size ; i++) {
	    if (regs[i] == 0) {
		retval = i;
		break;
	    }
	}
	return retval;
    }


  public:
    RegAll() { 
	regs = new int[10];
	size = 10;
	low = 0;
    }

    RegAll(int howmany) { 
	regs = new int[howmany];
	size = howmany;
	low = 0;
    }

    ~RegAll()
    {
	low = 0;
	delete regs;
    }

    /*
     * use up a register
     */
    int
    allocReg()
    {
	int r = findFirst();
	regs[r] = 1;
	return r;
    } // allocReg

    /*
     * make it available again
     */
    void
    freeReg(int r)
    {
	if (r >=0 & r < size) {
	    regs[r] = 0;
	}
    } // freeReg

    /*
     * see the next free one, but don't allocate it
     */
    int
    peekReg()
    {
	return findFirst();
    } // peekReg

    /*
     * return a ptr to a vector of busy registers, which can be used like this:
     *	for (int i = 0; i < vi->size(); i++) {
     *      cout << (*vi)[i] << endl;
     *  }
     */
    vector<int> *
    areBusy()
    {
	int i;
	vector<int> *v = new vector<int>();

	for (i=0; i < size ; i++) {
	    if (regs[i] != 0) {
		v->push_back(i);
	    }
	}
	return v;
	
    } // areBusy
	

}; // class RegAll

#endif // REGALL_HPP
