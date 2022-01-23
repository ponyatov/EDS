/// @file
#ifndef _EDS_H_
#define _EDS_H_

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include <iostream>
#include <sstream>

using namespace std;

#include <QApplication>
#include <QLabel>
#include <QTextStream>
#include <QWidget>

/// @defgroup Core
/// @brief Executable Data Structure

/// @brief base object (hyper)graph node
/// @ingroup Core
class Object {
   protected:
    /// scalar: object name, string/number value,..
    QString value;

   public:
    /// constructors
    Object(QString V);
    virtual ~Object();

    /// @name text tree dump / stringify

    /// full tabbed text tree dump
    QString dump(int depth = 0, QString prefix = "");
    /// `<T:V>` header
    QString head(QString prefix = "");
    /// dump padding
    QString pad(int depth);
    /// class/type tag
    QString tag();
    /// stringified value
    QString val();
};

/// @defgroup Primitive
/// @ingroup Core
/// @brief Scalar data types

class Primitive : public Object {
   public:
    Primitive(QString V) : Object(V) {}
};

/// @defgroup Container
/// @ingroup Core
/// @brief Generic data structures

/// @ingroup Container
class Container : public Object {
   public:
    Container(QString V) : Object(V) {}
};

/// @ingroup Container
/// @brief Ordered container
class Vector : public Container {
   public:
    Vector(QString V) : Container(V) {}
};

/// @ingroup Container
/// @brief LIFO Stack
class Stack : public Container {
   public:
    Stack(QString V) : Container(V) {}
};

/// @ingroup Container
/// @brief FIFO Queue
class Queue : public Container {
   public:
    Queue(QString V) : Container(V) {}
};

/// @ingroup Container
/// @brief string-keyed Associative Array
class Map : public Container {
   public:
    Map(QString V) : Container(V) {}
};

/// @defgroup Meta
/// @ingroup Core
/// @brief Metaprogramming
/// @{

class Meta : public Object {
   public:
    Meta(QString V) : Object(V) {}
};

class App : public Meta {
    QApplication* app;
    QLabel* label;

   public:
    App(int argc, char* argv[]);
    ~App();
    int exec();
};

class Syntax : public Meta {
   public:
    Syntax(QString V) : Meta(V) {}
};

class Token : public Syntax {
   public:
    Token(QString V) : Syntax(V) {}
};

/// @}

/// @defgroup wasd WASD machine
/// @brief FORTH-like object stack machine
/// @{

/// Words vocabulary
extern Map W;
/// Async message queue
extern Queue A;
/// return Stack
extern Stack S;
/// Data stack
extern Stack D;
/// @}

/// @defgroup skelex
/// @brief Lexical Skeleton: script parser for any program
/// @{
extern int yylex();  // \ lexer
extern FILE* yyin;
extern int yylineno;
extern char* yytext;
extern int yyparse();  // \ parser
extern void yyerror(string msg);
/// @}
#include "EDS.parser.hpp"

#define TOKEN(C, X)               \
    {                             \
        yylval.o = new C(yytext); \
        return X;                 \
    }
// /
// skelex

#endif  // _EDS_H_
