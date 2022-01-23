%{
    #include "EDS.hpp"
%}

%option noyywrap yylineno

%%
#[^\n]*     {}                      // line comment

"?"         { TOKEN(Token,Q); }

[ \t\r\n]+  {}                      // drop spaces
.           { yyerror("lexer"); }   // any undefined char
