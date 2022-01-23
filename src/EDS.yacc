%{
    #include "EDS.hpp"
%}

%defines %union { Object* o; }

%token<o> Q LABEL COLON
%token GUI
%token<o> CMD0

%%
REPL:
    | REPL Q            { q();                                }
    | REPL LABEL COLON  { D.push($2); colon();                }
    | REPL GUI          { exit(App(argc,argv).exec());        }
    | REPL CMD0         { assert(compile); compile->push($2); }
