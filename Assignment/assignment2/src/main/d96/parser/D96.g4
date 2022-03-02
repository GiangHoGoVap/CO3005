/* ID: 1952968 */
grammar D96;

@lexer::header {
from lexererr import *
}

options {
	language = Python3;
}

program: classdecl+ EOF;
classdecl: Class ID (COLON ID)? LP member* RP;
member: attr | constructor | destructor | method;
attr: vardecl_ | vardeclass;

vardecl_: AttriType iden idenlist* COLON typ SEMI;
iden: DollaID | ID;
idenlist: COMMA (DollaID | ID);

vardeclass: AttriType (DollaID | ID) varlist expr SEMI;
varlist: COMMA (DollaID | ID) varlist expr COMMA
	   | COLON typ ASSIGN;

primi: BOOLEAN | INT | FLOAT | STRING;
typ: primi | arrtype | ID;
arrtype: Array LS (primi | arrtype) COMMA INTLIT_ARR RS;

constructor: Constructor LB paramlist? RB blockstate;
destructor: Destructor LB RB blockstate;
method: (DollaID | ID) LB paramlist? RB blockstate;
paramlist: param (SEMI param)*;
param: idlist COLON typ;
idlist: ID (COMMA ID)*;
blockstate: LP blockstmt? RP;

/* Statements */
stmt: assignstmt
	| foreachstmt
	| ifstmt
	| breakstmt
	| continuestmt
	| returnstmt
	| instancestmt
	| invocastmt
	| blockstate;

varstmt: varstmt_decl_ | varstmt_declass;
varstmt_decl_: AttriType idlist COLON typ SEMI;
varstmt_declass: AttriType ID varstmt_list expr SEMI;
varstmt_list: COMMA ID varstmt_list expr COMMA
			| COLON typ ASSIGN;

assignstmt: assign_body SEMI;
assign_body: assign_lhs ASSIGN expr;
assign_lhs: element_expr | scalar_var;

// ifstmt: If LB expr RB LP blockstmt RP elseif_part* else_part?;
// elseif_part: Elseif LB expr RB blockstmt;
// else_part: Else blockstmt;

// ifstmt: If LB expr RB LP blockstmt RP (Elseif LB expr RB LP blockstmt RP)* (Else LP blockstmt RP)?;
ifstmt: If LB expr RB blockstate (Elseif LB expr RB blockstate)* (Else blockstate)?;

foreachstmt: Foreach LB scalar_var In expr DOUBLEDOT expr (By expr)? RB LP blockstmt RP;
breakstmt: Break SEMI;
continuestmt: Continue SEMI;
returnstmt: Return expr? SEMI;

scalar_var: scalar_helper INSTANTAC ID
		  | ID STATICAC DollaID
		  | ID;

scalar_helper: scalar_helper INSTANTAC ID arg?
			 | invocast_helper
			 | Self
			 | ID;

instance_helper: New ID arg
			   | instance_helper INSTANTAC ID arg?
			   | instance_helper index_operators
			   | invocast_helper
			   | LB instance_helper RB
			   | Self
			   | ID;

invocast_helper: ID STATICAC DollaID arg?;
instancestmt: instance_helper INSTANTAC ID arg SEMI;
invocastmt: ID STATICAC DollaID arg SEMI;
arg: LB exprlist? RB;
blockstmt: statement+;
statement: varstmt | stmt;

DOUBLEDOT: '..';

/* Integer literal for Array */
INTLIT_ARR: INT_LIT_ARR {self.text = self.text.replace("_","")};
INT_LIT_ARR: BIN_ | DEC_ | OCTAL_ | HEXA_;

BIN_: '0' [bB]('1' [01]* ('_' [01]+)*);
DEC_: [1-9][0-9]* ('_' [0-9]+)*;
OCTAL_: '0' ([1-7][0-7]* ('_' [0-7]+)*);
HEXA_: '0' [xX]([1-9A-F][0-9A-F]* ('_' [0-9A-F]+)*);

/* Integer literal */
INTLIT: INT_LIT {self.text = self.text.replace("_","")};
INT_LIT: BIN | DEC | OCTAL | HEXA;

BIN: '0' [bB]('1' [01]* ('_' [01]+)* | '0');
DEC: '0' | [1-9][0-9]* ('_' [0-9]+)*;
OCTAL: '0' ([1-7][0-7]* ('_' [0-7]+)* | '0');
HEXA: '0' [xX]([1-9A-F][0-9A-F]* ('_' [0-9A-F]+)* | '0');

/* Float literal */
FLOATLIT: INTPART DECPART EXPOPART* {self.text = self.text.replace("_","")}
		| INTPART EXPOPART {self.text = self.text.replace("_","")}
		| DECPART EXPOPART {self.text = self.text.replace("_","")};
fragment INTPART: DEC;
fragment DECPART: '.' DIGIT*;
fragment EXPOPART: [eE][+-]? DIGIT+;
fragment DIGIT: [0-9];

/* Boolean literal */
BOOLLIT: 'True' | 'False';

/* String literal */
STRLIT: '"' (STR_CHAR | ESCSEQ)* '"' {
	content = str(self.text) 
	self.text = content[1:-1]
};

literal: INTLIT_ARR
	   | INTLIT
	   | FLOATLIT
	   | BOOLLIT
	   | STRLIT
	   | index_arrlit
	   | multi_arrlit;

index_arrlit: Array arg;
exprlist: expr (COMMA expr)*;
multi_arrlit: Array LB index_arrlit+ RB;

operands: literal | Self | Null | ID;

element_expr: scalar_var index_operators;
index_operators: (LS expr RS)+;

/* Expressions */
expr: expr1 (STRCONCATE | COMPARESTR) expr1 | expr1;
expr1: expr2 (EQUAL | NOTEQUAL | SMALLER | GREATER | SMALLEREQUAL | GREATEREQUAL) expr2 | expr2;
expr2: expr2 (LOGICALAND | LOGICALOR) expr3 | expr3;
expr3: expr3 (ADDITION | SUBTRACTION) expr4 | expr4;
expr4: expr4 (MULTIPLICATION | DIVISION | MODULO) expr5 | expr5;
expr5: LOGICALNOT expr5 | expr6;
expr6: SUBTRACTION expr6 | expr7;
expr7: expr7 LS expr7 RS | expr8;
expr8: expr8 INSTANTAC ID arg? | expr9;
expr9: ID STATICAC DollaID arg? | expr10;
expr10: New ID arg | expr11;
expr11: operands | LB expr RB;

/* Comment */
BlockComment: '##' .*? '##' -> skip;

/* Keywords */
Break: 'Break';
Continue: 'Continue';
If: 'If';
Elseif: 'Elseif';
Else: 'Else';
Foreach: 'Foreach';
Array: 'Array';
In: 'In';
Return: 'Return';
Null: 'Null';
Class: 'Class';
Constructor: 'Constructor';
Destructor: 'Destructor';
New: 'New';
By: 'By';
Self: 'Self';
AttriType: 'Val' | 'Var';

/* Operators */
LOGICALNOT: '!';
LOGICALAND: '&&';
LOGICALOR: '||';
EQUAL: '==';
ASSIGN: '=';
NOTEQUAL: '!=';
ADDITION: '+';
SUBTRACTION: '-';
MULTIPLICATION: '*';
DIVISION: '/';
MODULO: '%';
GREATER: '>';
GREATEREQUAL: '>=';
SMALLER: '<';
SMALLEREQUAL: '<=';
COMPARESTR: '==.';
STRCONCATE: '+.';
INSTANTAC: '.';
STATICAC: '::';

LB: '(';
RB: ')';
LP: '{';
RP: '}';
LS: '[';
RS: ']';
SEMI: ';';
COLON: ':';
COMMA: ',';

INT: 'Int';
FLOAT: 'Float';
BOOLEAN: 'Boolean';
STRING: 'String';

fragment STR_CHAR: ~[\\"\n];
fragment ESCSEQ: '\\b'
			   | '\\f'
			   | '\\r'
			   | '\\n'
			   | '\\t'
			   | '\\\''
			   | '\\\\'
			   | '\'"';
fragment ESCERROR: '\\' ~[bfrnt'\\] | '\'' ~'"';

/* Identifiers */
ID: [a-zA-Z_][a-zA-Z0-9_]*;
DollaID: '$' [a-zA-Z0-9_]+;

WS: [ \t\r\n]+ -> skip; // skip spaces, tabs, newlines

ERROR_CHAR: .{raise ErrorToken(self.text)};
UNCLOSE_STRING: '"' (STR_CHAR | ESCSEQ)* (EOF | '\n') {
	content = str(self.text)
	esc = '\n'
	if content[-1] in esc:
		raise UncloseString(content[1:-1])
	else:
		raise UncloseString(content[1:])
};

ILLEGAL_ESCAPE: '"' (STR_CHAR | ESCSEQ)* ESCERROR {
	content = str(self.text) 
	raise IllegalEscape(content[1:])
};