%{
    #include "EDS.hpp"
%}

%option noyywrap yylineno

%%
#[^\n]*     {}                      // line comment

"?"         {TOKEN(Token,Q);}
":"         {TOKEN(Token,COLON);}

".gui"      {return GUI;}

"nop"       {TOKEN(Cmd,CMD0);}
"halt"      {TOKEN(Cmd,CMD0);}

[a-zA-Z_]+: {yyless(yyleng-1);TOKEN(Label,LABEL);}

[ \t\r\n]+  {}                      // drop spaces
.           { yyerror("lexer"); }   // any undefined char
