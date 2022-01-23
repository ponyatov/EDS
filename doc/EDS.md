# EDS: Executable Data Structure

- Any **active data structures** can be executed the same way as Lisp language
  executes lists.

- These structures are **binary homoiconic** at a level of program memory (RAM)
  the same as Lisp is homoiconic at a program source code:
  - `program = data`

- The directed cyclic object (hyper)graph is a universal data structure that can
  represent any data, which is especially useful in computer languages and
  compilers design (see AST trees, attribute grammar).
  - nodes are objects provided by any mainstream OOP-based programming language
    /C++/
  - graph edges between objects are defined by raw computer pointers, so they
    can't be attributed and a source of reference can't be found
    (unidirectional links)
