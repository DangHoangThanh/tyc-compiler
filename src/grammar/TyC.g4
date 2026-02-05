grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// TODO: Define grammar rules here

// ----------------------------------------------------------------------------
// Parser Rules
// ----------------------------------------------------------------------------

/**
 * Program Structure
 * A TyC program consists of a sequence of struct declarations and function declarations.
 */
program
    : globalDecl* EOF
    ;

globalDecl
    : structDecl
    | funcDecl
    ;

// --- Struct Declaration ---
// Form: struct <identifier> { <type> <member>; ... };
structDecl
    : STRUCT ID LBRACE structMember* RBRACE SEMI
    ;

structMember
    : type_ ID SEMI
    ;

// --- Function Declaration ---
// Form: <return_type> <identifier>(<parameter_list>) { <statement_list> }
// Return type can be explicit type, void, or omitted (inferred).
funcDecl
    : returnType? ID LPAREN paramList? RPAREN block
    ;

returnType
    : type_
    | VOID
    ;

paramList
    : param (COMMA param)*
    ;

// Parameters must have explicit types (no auto)
param
    : type_ ID
    ;

// --- Types ---
// Explicit types only (int, float, string, or struct name)
type_
    : INT
    | FLOAT
    | STRING
    | ID  // Struct type name
    ;

// --- Statements ---
block
    : LBRACE blockItem* RBRACE
    ;

// A block can contain variable declarations and statements
blockItem
    : varDecl
    | stmt
    ;

stmt
    : block
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    | semiStmt // Handle extra semicolons if necessary or empty statements
    ;

// Variable Declaration
// Supports: auto or explicit type with/without init
// Structs can be initialized with { ... }
varDecl
    : AUTO ID (ASSIGN expr)? SEMI
    | type_ ID (ASSIGN (expr | structInitializer))? SEMI
    ;

structInitializer
    : LBRACE (expr (COMMA expr)*)? RBRACE
    ;

// Control Flow Statements
ifStmt
    : IF LPAREN expr RPAREN stmt (ELSE stmt)?
    ;

whileStmt
    : WHILE LPAREN expr RPAREN stmt
    ;


// For loop
// Case 1: Init is declaration (includes ';')
// Case 2: Init is expression (needs ';')
// Case 3: Empty (needs ';')
forControl
    : varDecl                 # ForInitDecl
    | expr? SEMI              # ForInitExpr
    ;

// forStmt using forControl
forStmt
    : FOR LPAREN forControl expr? SEMI expr? RPAREN stmt
    ;

switchStmt
    : SWITCH LPAREN expr RPAREN LBRACE switchBlockStatementGroup* RBRACE
    ;

switchBlockStatementGroup
    : switchLabel+ blockItem*
    ;

switchLabel
    : CASE expr COLON
    | DEFAULT COLON
    ;

breakStmt
    : BREAK SEMI
    ;

continueStmt
    : CONTINUE SEMI
    ;

returnStmt
    : RETURN expr? SEMI
    ;

exprStmt
    : expr SEMI
    ;

semiStmt
    : SEMI
    ;

// --- Expressions ---
// Precedence follows the specification table strictly.
expr
    : expr (INC | DEC)                  # PostfixExpr
    | (INC | DEC) expr                  # PrefixExpr
    | (BANG | PLUS | MINUS) expr        # UnaryExpr
    | expr DOT ID                       # MemberAccessExpr
    | expr (MUL | DIV | MOD) expr       # MultiplicativeExpr
    | expr (PLUS | MINUS) expr          # AdditiveExpr
    | expr (LT | LE | GT | GE) expr     # RelationalExpr
    | expr (EQUAL | NOTEQUAL) expr      # EqualityExpr
    | expr AND expr                     # LogicalAndExpr
    | expr OR expr                      # LogicalOrExpr
    | <assoc=right> expr ASSIGN expr    # AssignmentExpr
    | expr LPAREN argList? RPAREN         # FunctionCallExpr
    | primary                           # PrimaryExprRule
    ;

argList
    : expr (COMMA expr)*
    ;

primary
    : LPAREN expr RPAREN
    | ID
    | literal
    ;

literal
    : INT_LITERAL
    | FLOAT_LITERAL
    | STRING_LITERAL
    ;










// ----------------------------------------------------------------------------
// Lexer Rules
// ----------------------------------------------------------------------------

// Keywords
AUTO     : 'auto';
BREAK    : 'break';
CASE     : 'case';
CONTINUE : 'continue';
DEFAULT  : 'default';
ELSE     : 'else';
FLOAT    : 'float';
FOR      : 'for';
IF       : 'if';
INT      : 'int';
RETURN   : 'return';
STRING   : 'string';
STRUCT   : 'struct';
SWITCH   : 'switch';
VOID     : 'void';
WHILE    : 'while';

// Operators
PLUS     : '+';
MINUS    : '-';
MUL      : '*';
DIV      : '/';
MOD      : '%';
EQUAL    : '==';
NOTEQUAL : '!=';
LT       : '<';
GT       : '>';
LE       : '<=';
GE       : '>=';
OR       : '||';
AND      : '&&';
BANG     : '!';
INC      : '++';
DEC      : '--';
ASSIGN   : '=';
DOT      : '.';

// Separators
LBRACK   : '[';
RBRACK   : ']';
LBRACE   : '{';
RBRACE   : '}';
LPAREN   : '(';
RPAREN   : ')';
SEMI     : ';';
COMMA    : ',';
COLON    : ':';

// Literals

// Integer: Decimal only, 0-9
INT_LITERAL
    : '0' 
    | [1-9] [0-9]*
    ;

// Float: Decimal or Scientific
FLOAT_LITERAL
    : [0-9]+ '.' [0-9]* EXPONENT?  // 123.456, 1.
    | '.' [0-9]+ EXPONENT?         // .5
    | [0-9]+ EXPONENT              // 123e4
    ;

fragment EXPONENT
    : [eE] [+-]? [0-9]+
    ;

// String: "..." with escape sequences
STRING_LITERAL
    : '"' (ESCAPE_SEQ | ~["\\\r\n])* '"'
        {self.text = self.text[1:-1]}
    ;

fragment ESCAPE_SEQ
    : '\\' [bfnrt"\\']
    ;

// Identifiers
ID
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;

// Comments and Whitespace
BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;

LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;

WS
    : [ \t\r\n\f]+ -> skip
    ;



// --- Error Rules ---
ERROR_CHAR
    : . 
    ;

ILLEGAL_ESCAPE
    : '"' (ESCAPE_SEQ | ~["\\\r\n])* '\\' ~[bfnrt"\\\r\n]
    ;

UNCLOSE_STRING
    : '"' (ESCAPE_SEQ | ~["\\\r\n])* ;
