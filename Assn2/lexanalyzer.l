%{
#include <stdio.h>
#include <string.h>
%}

%%

"int"           { printf("Keyword: %s\n", yytext); }
"float"         { printf("Keyword: %s\n", yytext); }
"return"        { printf("Keyword: %s\n", yytext); }

[a-zA-Z_][a-zA-Z0-9_]* { printf("Identifier: %s\n", yytext); }

[0-9]+          { printf("Integer: %s\n", yytext); }
[0-9]+"."[0-9]+ { printf("Float: %s\n", yytext); }

"+"             { printf("Operator: %s\n", yytext); }
"-"             { printf("Operator: %s\n", yytext); }
"*"             { printf("Operator: %s\n", yytext); }
"/"             { printf("Operator: %s\n", yytext); }

\n              ;  // Ignore newlines
[ \t]           ;  // Ignore whitespaces
.               { printf("Unknown character: %s\n", yytext); }

%%

int main() {
    // Calling the lexer which is a lex function only.
    //It is identifying Identifier,Keywords,Operators and Numbers from the subset of C language.
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}