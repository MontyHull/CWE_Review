/* SI 413 Fall 2016
* Lab 9 Starter Code
* ast.hpp
* This is a C++ header file for the AST class hierarchy.
* YOUR NAME HERE
*/

#ifndef AST_HPP
#define AST_HPP

#include <cstdlib>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <stack>
#include <set>
#include <map>
using namespace std;

#include "colorout.hpp"
#include "value.hpp"
#include "st.hpp"

// This global variable is the actual global symbol table object.
// It is actually declared in the ast.cpp file, so we put keyword "extern"
// here.
extern SymbolTable ST;

// Declare the output streams to use everywhere
extern colorout resout;
extern colorout errout;

// Global variable to indicate if an error has occurred.
extern bool error;

// Global variable to indicate there is a human typing at a keyboard
extern bool showPrompt;

// This enum type gives codes to the different kinds of operators.
// Basically, each oper below such as DIV becomes an integer constant.
enum Oper {
    ADD, SUB,
    MUL, DIV, MOD,
    LT, GT, LE, GE,
    EQ, NE,
    AND, OR, NOT,
    WWINL, WNONL
};

// These are forward declarations for the classes defined below.
// They show the class hierarchy.
class AST;
class Stmt;
class NullStmt;
class Block;
class IfStmt;
class WhileStmt;
class NewStmt;
class Asn;
class Write;
class Debug;
class Exp;
class Id;
class Num;
class BoolExp;
class ArithOp;
class CompOp;
class BoolOp;
class NegOp;
class NotOp;
class Read;
class Lambda;
class Funcall;

/* The AST class is the super-class for abstract syntax trees.
* Every type of AST (or AST node) has its own subclass.
*/
class AST {
private:
    /* Adds this node and all children to the output stream in DOT format.
    * nextnode is the index of the next node to add. */
    void addToDot(ostream& out, int& nextnode);

protected:
    // These two protected fields determine the structure of the AST.
    int suNum;
    string nodeLabel;
    vector<AST*> children;

    // Inserts a new AST node as a child of this one.
    // (where the new node is inserted depends on which subclass.)
    virtual void ASTchild(AST* child) = 0;

public:
    /* Writes this AST to a .dot file as named. */
    void writeDot(const char* fname);

    /* Makes a new "empty" AST node. */
    AST() { nodeLabel = "EMPTY"; }
};

/* Every AST node that is not a Stmt is an Exp.
* These represent actual computations that return something
* (in particular, a Value object).
*/
class Exp :public AST {
protected:
    // Inserts a new AST as a child of this one.
    void ASTchild(AST* child) { children.push_back(child); }

public:
    /* This is the method that must be overridden by all subclasses.
    * It should perform the computation specified by this node, and
    * return the resulting value that gets computed. */
    virtual Value eval() {
        if (!error) {
            errout << "eval() not yet for "
            << nodeLabel << " nodes!" << endl;
            error = true;
        }
        return Value();
    }
    virtual int suCount(__attribute__((unused)) int lor) {
        if (!error) {
            errout << "suCount() not yet implemented for "
            << nodeLabel << endl;
            error = true;
        }
        if(lor == 1){
            return 1;
        }
        else{
            return 0;
        }
    }
};

/* An identifier, i.e. variable or function name. */
class Id :public Exp {
private:
    string val;

public:
    // Constructor from a C-style string
    Id(const char* v) {
        val = v;
        nodeLabel = "Exp:Id:" + val;
    }

    // Returns a reference to the stored string value.
    string& getVal() { return val; }

    Value eval() { return ST.lookup(val); }

    int suCount(int lor){ return lor; }
};

/* A literal number in the program. */
class Num :public Exp {
private:
    int val;

public:
    Num(int v) {
        val = v;
        // Converting integers to strings is a little annoying...
        ostringstream label;
        label << "Exp:Num:" << val;
        nodeLabel = label.str();
    }

    // To evaluate, just return the number!
    Value eval() { return val; }

    //TODO
    //TODO if this causes problems think harder
    //TODO
    int suCount(int lor){ return lor; }

};

/* A literal boolean value like "true" or "false" */
class BoolExp :public Exp {
private:
    bool val;

public:
    BoolExp(bool v) {
        val = v;
        nodeLabel = "Exp:Bool:";
        if (v) nodeLabel += "true";
        else nodeLabel += "false";
    }

    Value eval() { return val; }
    int suCount(int lor){ return lor; }

};

/* A binary opration for arithmetic, like + or *. */
class ArithOp :public Exp {
private:
    Oper op;
    Exp* left;
    Exp* right;

public:
    ArithOp(Exp* l, Oper o, Exp* r);

    Value eval();
    int suCount(__attribute__((unused)) int lor){
        int lval = left->suCount(1);
        int rval = right->suCount(0);
        if(lval > rval){return lval;}
        else if(rval > lval){return rval;}
        else{return lval+1;}
    }
};

/* A binary operation for comparison, like < or !=. */
class CompOp :public Exp {
private:
    Oper op;
    Exp* left;
    Exp* right;

public:
    CompOp(Exp* l, Oper o, Exp* r);

    Value eval() {
        int l = left->eval().num();
        int r = right->eval().num();
        if (l < r)       return op == LT || op == LE || op == NE;
        else if (l == r) return op == LE || op == EQ || op == GE;
        else             return op == GT || op == GE || op == NE;
    }

    int suCount(__attribute__((unused)) int lor){
        int lval = left->suCount(1);
        int rval = right->suCount(0);
        if(lval > rval){return lval;}
        else if(rval > lval){return rval;}
        else{return lval+1;}
    }
};

/* A binary operation for boolean logic, like "and". */
class BoolOp :public Exp {
private:
    Oper op;
    Exp* left;
    Exp* right;

public:
    BoolOp(Exp* l, Oper o, Exp* r);

    Value eval() {
        bool a = left->eval().tf();
        if (op == OR && a) return true;
        else if (op == AND && !a) return false;
        else return right->eval().tf();
    }
    int suCount(__attribute__((unused)) int lor){
        int lval = left->suCount(1);
        int rval = right->suCount(0);
        if(lval > rval){return lval;}
        else if(rval > lval){return rval;}
        else{return lval+1;}
    }

};

/* This class represents a unary negation operation. */
class NegOp :public Exp {
private:
    Exp* right;

public:
    NegOp(Exp* r) {
        nodeLabel = "Exp:NegOp";
        right = r;
        ASTchild(right);
    }

    Value eval() { return - right->eval().num(); }
    int suCount(__attribute__((unused)) int lor){return right->suCount(0);}
};

/* This class represents a unary "not" operation. */
class NotOp :public Exp {
private:
    Exp* right;

public:
    NotOp(Exp* r) {
        nodeLabel = "Exp:NotOp";
        right = r;
        ASTchild(right);
    }

    Value eval() { return ! right->eval().tf(); }
    int suCount(__attribute__((unused)) int lor){return right->suCount(0);}

};

/* A read expression. */
class Read :public Exp {
public:
    Read() { nodeLabel = "Exp:Read"; }

    Value eval() {
        int v;
        if (showPrompt) cerr << "read> ";
        cin >> v;
        return v;
    }

    //TODO may just return 1
    int suCount(int lor){return lor;}
};

/* A Stmt is anything that can be evaluated at the top level such
* as I/O, assignments, and control structures.
* The last child of any statement is the next statement in sequence.
*/
class Stmt :public AST {
private:
    // Pointer to the next statement in sequence.
    Stmt* next;

protected:
    // Inserts a new AST as a child of this one.
    void ASTchild(AST* child) {
        // This inserts before the last thing in the vector,
        // i.e., just before the "next" statement
        children.insert(children.end()-1, child);
    }

public:
    /* This static method is for building sequences of statements by the
    * parser. It takes two statements, and appends one at the end of the other.
    * The returned value is a pointer to the new statement representing
    * the sequence.
    */
    static Stmt* append(Stmt* a, Stmt* b);

    /* Default constructor. The next statement will be set to NullStmt. */
    Stmt ();

    // This constructor sets the next statement manually.
    Stmt (Stmt* nextStmt) {
        if (nextStmt != NULL) children.push_back(nextStmt);
        next = nextStmt;
    }

    // Getter and setter for the next statement in sequence.
    Stmt* getNext() { return next; }
    void setNext(Stmt* nextStmt) {
        children.back() = nextStmt;
        next = nextStmt;
    }

    // This should only be false in the NullStmt class.
    bool hasNext() { return next != NULL; }

    /* This is the command that must be implemented everywhere to
    * execute this Stmt - that is, do whatever it is that this statement
    * says to do. */
    virtual void exec() {
        if (!error) {
            errout << "exec() not yet implemented for "
            << nodeLabel << " nodes!" << endl;
            error = true;
        }
    }

    virtual void suTraverse() {
        if (!error) {
            errout << "suTraverse() not yet implemented for "
            << nodeLabel << endl;
            error = true;
        }
    }
};

/* This class is necessary to terminate a sequence of statements. */
class NullStmt :public Stmt {
public:
    NullStmt() :Stmt(NULL) {
        nodeLabel = "Stmt:Null";
    }

    // Nothing to execute!
    void exec() { }

    void suTraverse(){ }
};

/* This is a statement for a block of code, i.e., code enclosed
* in curly braces { and }.
* Eventually, this is where scopes will begin and end.
*/
class Block :public Stmt {
private:
    Stmt* body;
    int left_val;
    int right_val;

public:
    Block(Stmt* b) {
        nodeLabel = "Stmt:Block";
        body = b;
        ASTchild(body);
    }

    void exec() {
        body->exec();
        getNext()->exec();
    }
    void suTraverse(){
        resout << "Need 0 registers for " << nodeLabel << endl;
        body->suTraverse();
        getNext()->suTraverse();

    }
};

/* This class is for "if" AND "ifelse" statements. */
class IfStmt :public Stmt {
private:
    Exp* clause;
    Stmt* ifblock;
    Stmt* elseblock;
    int left_val;
    int right_val;
    int total;

public:
    IfStmt(Exp* e, Stmt* ib, Stmt* eb) {
        nodeLabel = "Stmt:If";
        clause = e;
        ifblock = ib;
        elseblock = eb;
        ASTchild(clause);
        ASTchild(ifblock);
        ASTchild(elseblock);

    }

    void exec() {
        bool cond = clause->eval().tf();
        if (cond) ifblock->exec();
        else elseblock->exec();
        getNext()->exec();
    }
    void suTraverse(){
        resout << "Need " << clause->suCount(1) << " register for " << nodeLabel << endl;
        ifblock->suTraverse();
        elseblock->suTraverse();
        getNext()->suTraverse();
    }
};

/* Class for while statements. */
class WhileStmt :public Stmt {
private:
    Exp* clause;
    Stmt* body;
    int left_val;
    int right_val;

public:
    WhileStmt(Exp* c, Stmt* b) {
        nodeLabel = "Stmt:While";
        clause = c;
        body = b;
        ASTchild(clause);
        ASTchild(body);
    }

    void exec() {
        bool clauseres = clause->eval().tf();
        while (!error && clauseres) {
            body->exec();
            clauseres = clause->eval().tf();
        }
        getNext()->exec();
    }

    void suTraverse(){
        resout << "Need " << clause->suCount(1) << " register for " << nodeLabel << endl;
        body->suTraverse();
        getNext()->suTraverse();
    }

};

/* A "new" statement creates a new binding of the variable to the
* stated value.  */
class NewStmt :public Stmt {
private:
    Id* lhs;
    Exp* rhs;
    int left_val;
    int right_val;

public:
    NewStmt(Id* l, Exp* r) {
        nodeLabel = "Stmt:New";
        lhs = l;
        rhs = r;
        ASTchild(lhs);
        ASTchild(rhs);
    }

    void exec() {
        Value res = rhs->eval();
        if (!error) ST.bind(lhs->getVal(), res);
        getNext()->exec();
    }

    void suTraverse(){
        resout << "Need " << rhs->suCount(1) << " register for " << nodeLabel << endl;
        getNext()->suTraverse();
    }
};

/* An assignment statement. This represents a RE-binding in the symbol table. */
class Asn :public Stmt {
private:
    Id* lhs;
    Exp* rhs;
    int left_val;
    int right_val;

public:
    Asn(Id* l, Exp* r) {
        nodeLabel = "Stmt:Asn";
        lhs = l;
        rhs = r;
        ASTchild(lhs);
        ASTchild(rhs);
    }

    void exec() {
        Value res = rhs->eval();
        if (!error) ST.rebind(lhs->getVal(), res);
        getNext()->exec();
    }

    void suTraverse(){
        resout << "Need " << rhs->suCount(1) << " register for " << nodeLabel << endl;
        getNext()->suTraverse();
    }
};

/* A write statement. */
class Write :public Stmt {
private:
    Exp* val;
    char *strng;
    Oper op;
    int left_val;
    int right_val;

public:
    Write(Oper worwo, Exp* v) {
        nodeLabel = "Stmt:Write";
        val = v;
        strng = NULL;
        op = worwo;	// with or w/o newline
        ASTchild(val);
    }

    Write(Oper worwo, char *str) {
        nodeLabel = "Stmt:Write";
        strng = str;
        val = NULL;
        op = worwo;	// with or w/o newline
        ASTchild(val);
    }

    void exec() {
        if (val) {
            Value res = val->eval();
            if (!error) {
                res.writeTo(resout);
            }
        } else {
            resout << strng;
        }
        // to newline or not to newline, that is the question...
        if (op == WWINL ) {
            resout << endl;
        }

        // on to the next statement
        getNext()->exec();

    } // exec
    void suTraverse(){
        resout << "Need "<< val->suCount(1) <<" register for " << nodeLabel << endl;
        getNext()->suTraverse();
    }

};

/* A lambda expression consists of a parameter name and a body. */
class Lambda :public Exp {
private:
    Id* var;
    Stmt* body;

protected:
    void writeLabel(ostream& out) { out << "lambda:exp" << flush; }

public:
    Lambda(Id* v, Stmt* b) {
        nodeLabel = "Exp:Lambda";
        var = v;
        body = b;
        ASTchild(var);
        ASTchild(body);
    }

    // These getter methods are necessary to support actually calling
    // the lambda sometime after it gets created.
    string& getVar() { return var->getVal(); }
    Stmt* getBody() { return body; }
};

/* A function call consists of the function name, and the actual argument.
* Note that all functions are unary. */
class Funcall :public Exp {
private:
    Exp* funexp;
    Exp* arg;

public:
    Funcall(Exp* f, Exp* a) {
        nodeLabel = "Exp:Funcall";
        funexp = f;
        arg = a;
        ASTchild(funexp);
        ASTchild(arg);
    }
};

class Debug :public Stmt {
private:
    string msg;

public:
    Debug(const char* s) {
        nodeLabel = "Stmt:Debug";
        msg = s;
    }

    void exec() {
        errout << "DEBUG: " << msg << endl;
        getNext()->exec();
    }
};

#endif //AST_HPP
