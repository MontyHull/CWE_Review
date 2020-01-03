/* SI 413 Fall 2016
 * Lab 9 Starter Code
 * This file contains the implementations of longer methods in the
 * AST class hierarchy.
 * YOUR NAME HERE
 */

#include "ast.hpp"

SymbolTable ST; // The actual declaration of the global symbol table

/* Adds this node and all children to the output stream in DOT format. 
 * nextnode is the index of the next node to add. */
void AST::addToDot(ostream& out, int& nextnode) {
  int root = nextnode;
  ++nextnode;
  out << "\tn" << root << " [label=\"" << nodeLabel << "\"];" << endl;
  for (int i=0; i < children.size(); ++i) {
    int child = nextnode;
    children[i]->addToDot(out, nextnode);
    out << "\tn" << root << " -> n" << child << ";" << endl;
  }
}

/* Writes this AST to a .dot file as named. */
void AST::writeDot(const char* fname) {
  ofstream fout(fname);
  int nodes = 1;
  fout << "digraph AST {" << endl;
  addToDot (fout, nodes);
  fout << "}" << endl;
  fout.close();
}

// ArithOp constructor
ArithOp::ArithOp(Exp* l, Oper o, Exp* r) { 
  op = o;
  left = l;
  right = r;
  nodeLabel = "Exp:ArithOp:";
  switch(o) {
    case ADD: nodeLabel += '+'; break;
    case SUB: nodeLabel += '-'; break;
    case MUL: nodeLabel += '*'; break;
    case DIV: nodeLabel += '/'; break;
    case MOD: nodeLabel += '%'; break;
    default:  nodeLabel += "ERROR";
  }
  ASTchild(left);
  ASTchild(right);
}

// Evaluates an arithmetic operation
Value ArithOp::eval() {
  int l = left->eval().num();
  int r = right->eval().num();
  switch(op) {
    case ADD: return l + r;
    case SUB: return l - r;
    case MUL: return l * r;
    case DIV: 
    case MOD:
      if (r != 0) return ((op == DIV) ? (l / r) : (l % r));
      else if (!error) {
        error = true;
        errout << "ERROR: Divide by zero" << endl;
      }
      return Value();
    default:  return Value(); // shouldn't get here...
  }
}

// Constructor for CompOp
CompOp::CompOp(Exp* l, Oper o, Exp* r) {
  op = o;
  left = l;
  right = r;
  nodeLabel = "Exp:CompOp:";
  switch(o) {
    case LT: nodeLabel += "<";  break;
    case GT: nodeLabel += ">";  break;
    case LE: nodeLabel += "<="; break;
    case GE: nodeLabel += ">="; break;
    case EQ: nodeLabel += "=";  break;
    case NE: nodeLabel += "!="; break;
    default: nodeLabel += "ERROR"; break;
  }
  ASTchild(left);
  ASTchild(right);
}

// Constructor for BoolOp
BoolOp::BoolOp(Exp* l, Oper o, Exp* r) {
  op = o;
  left = l;
  right = r;
  nodeLabel = "Exp:BoolOp:";
  if (o == AND) nodeLabel += "and";
  else nodeLabel += "or";
  ASTchild(left);
  ASTchild(right);
}

// Appends b to the end of a and returns the result.
Stmt* Stmt::append(Stmt* a, Stmt* b) {
  if (! a->hasNext()) return b;
  Stmt* last = a;
  while (last->getNext()->hasNext()) last = last->getNext();
  last->setNext(b);
  return a;
}

// Default constructor for Stmt.
// This HAS to be declared here because it uses NullStmt, which
// hasn't been defined yet in the header file!
Stmt::Stmt() {
  next = new NullStmt();
  children.push_back(next);
}



