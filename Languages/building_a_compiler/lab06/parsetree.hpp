/* SI 413 Fall 2013
 * parsetree.hpp
 * This is a C++ header file for the ParseTree class.
 * A ParseTree is recursively defined with a very simple structure.
 */

#ifndef PARSETREE_HPP
#define PARSETREE_HPP

#include <fstream>
#include <string>
#include <vector>
using namespace std;

class ParseTree {
 private:
  string label;
  vector<ParseTree*> children;

  /* Adds this node in the tree, and its children to the 
   * .dot file attached to fout.
   * nodes is a count of the number of nodes already added,
   * so that names will be unique.
   */
  int addToDot(ofstream& fout, int& nodes) {
    int root = ++nodes;
    fout << "\tn" << root << " [label=\"" << label << "\"];" << endl;
    for (vector<ParseTree*>::iterator iter = children.begin();
      iter != children.end(); ++iter)
    {
      int child = (*iter)->addToDot(fout,nodes);
      fout << "\tn" << root << " -> n" << child << ";" << endl;
    }
    return root;
  }

  /* Prints out this node and its children to the named output
   * stream, to the specified level of indentation.
   */
  void plainTextOut(ostream& out, int indent) {
    out << label;
    for (vector<ParseTree*>::iterator iter = children.begin();
      iter != children.end(); ++iter)
    {
      out << endl;
      for (int i=0; i<indent; ++i) out.put(' ');
      out << "( ";
      (*iter)->plainTextOut(out, indent + 2);
      out << " )";
    }
  }

 public:
  /* The following are constructors to create a ParseTree
   * with anywhere from 0-7 children.
   * It's probably bad programming practice to have multiple constructors
   * instead of just using the addChild method, but this makes the ypp 
   * code smaller.
   */
  ParseTree (const char* l) :label(l), children(0) { }
  ParseTree (const char* l, ParseTree* c1) :label(l), children(1) {
    children[0] = c1;
  }
  ParseTree (const char* l, ParseTree* c1, ParseTree* c2) 
    :label(l), children(2) 
  {
    children[0] = c1;
    children[1] = c2;
  }
  ParseTree (const char* l, ParseTree* c1, ParseTree* c2, ParseTree* c3) 
    :label(l), children(3) 
  {
    children[0] = c1;
    children[1] = c2;
    children[2] = c3;
  }
  ParseTree (const char* l, 
    ParseTree* c1, ParseTree* c2, ParseTree* c3, ParseTree* c4) 
    :label(l), children(4) 
  {
    children[0] = c1;
    children[1] = c2;
    children[2] = c3;
    children[3] = c4;
  }
  ParseTree (const char* l, 
    ParseTree* c1, ParseTree* c2, ParseTree* c3, ParseTree* c4, ParseTree* c5) 
    :label(l), children(5) 
  {
    children[0] = c1;
    children[1] = c2;
    children[2] = c3;
    children[3] = c4;
    children[4] = c5;
  }
  ParseTree (const char* l, 
    ParseTree* c1, ParseTree* c2, ParseTree* c3, ParseTree* c4, 
    ParseTree* c5, ParseTree* c6) 
    :label(l), children(6) 
  {
    children[0] = c1;
    children[1] = c2;
    children[2] = c3;
    children[3] = c4;
    children[4] = c5;
    children[5] = c6;
  }
  ParseTree (const char* l, 
    ParseTree* c1, ParseTree* c2, ParseTree* c3, ParseTree* c4, 
    ParseTree* c5, ParseTree* c6, ParseTree* c7) 
    :label(l), children(7) 
  {
    children[0] = c1;
    children[1] = c2;
    children[2] = c3;
    children[3] = c4;
    children[4] = c5;
    children[5] = c6;
    children[6] = c7;
  }

  /* Destructor to free all the memory allocated by this tree. */
  ~ParseTree() {
    for (vector<ParseTree*>::iterator iter = children.begin();
      iter != children.end(); ++iter)
    {
      delete *iter;
    }
    children.clear();
  }

  /* Adds a new child under this node. */
  void addChild(ParseTree* c) {
    children.push_back(c);
  }

  /* Indicates whether this is a leaf in the tree or if it has children. */
  bool isLeaf() {
    return children.empty();
  }

  /* Writes this ParseTree to a .dot file as named. */
  void writeDot(const char* fname) {
    ofstream fout(fname);
    int nodes = 0;
    fout << "digraph g {" << endl;
    addToDot(fout,nodes);
    fout << "}" << endl;
    fout.close();
  }

  /* Writes this ParseTree to the named stream as plain text. */
  void writeTo(ostream& out) {
    plainTextOut(out, 0);
    out << endl;
  }
};

#endif //PARSETREE_HPP
