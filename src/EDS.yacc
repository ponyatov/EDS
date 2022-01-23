%{
    #include "EDS.hpp"
%}

%defines %union { Object* o; }

%token<o> Q

%%
REPL:
REPL: REPL Q     { cout << D.dump().toStdString() << "\n\n"; }
