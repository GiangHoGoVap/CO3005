/* ID: 1952968 */
grammar D96;

@lexer::header {
from lexererr import *
}

options {
	language = Python3;
}

program: classdecl+ EOF;
classdecl: Class ID (COLON ID)? LP decl* RP;
decl: attridecl | constructor | destructor | methoddecl;

attridecl: AttriType (vardecl | vardeclass) SEMI;
vardecl: (DollaID | ID) (COMMA (DollaID | ID))* COLON (primi | arrtype | ID);
vardeclass: (DollaID | ID) COMMA vardeclass COMMA expr
		  | (DollaID | ID) COLON (primi | arrtype| ID) ASSIGN expr;

primi: BOOLEAN | INT | FLOAT | STRING | arrtype | ID;
arrtype: Array LS primi COMMA INTLIT_ARR RS;

paramdecl: ID (COMMA ID)* COLON (primi | arrtype | ID);
constructor: Constructor LB (paramdecl (SEMI paramdecl)*)? RB LP blockstmt? RP;
destructor: Destructor LB RB LP blockstmt? RP;
methoddecl: (DollaID | ID) LB (paramdecl (SEMI paramdecl)*)? RB LP blockstmt? RP;

/* Statements */
stmt: varstmt 
	| assignstmt
	| foreachstmt
	| ifstmt
	| breakstmt
	| continuestmt
	| returnstmt
	| instancestmt
	| invocastmt
	| LP blockstmt RP;

varstmt: AttriType (varstmt_decl | varstmt_declass) SEMI;
varstmt_decl: ID (COMMA ID)* COLON (primi | arrtype | ID);
varstmt_declass: ID COMMA varstmt_declass COMMA expr
			   | ID COLON (primi | arrtype | ID) ASSIGN expr;

assignstmt: assign_body SEMI;
assign_body: assign_lhs ASSIGN assign_rhs;
assign_lhs: element_expr | scalar_var;
assign_rhs: assign_body | expr;

ifstmt: if_part elseif_part? else_part?;
if_part: If LB expr RB LP (blockstmt | returnstmt) RP;
elseif_part: Elseif LB expr RB LP (blockstmt | returnstmt) RP elseif_part 
		   | Elseif LB expr RB LP (blockstmt | returnstmt) RP;
else_part: Else LP (blockstmt | returnstmt) RP;

foreachstmt: Foreach LB foreach_param RB LP blockstmt RP;
foreach_param: scalar_var In expr DOUBLEDOT expr (By expr)?;

breakstmt: Break SEMI;
continuestmt: Continue SEMI;
returnstmt: Return expr? SEMI;

scalar_var: scalar_helper INSTANTAC ID
		  | (Self | ID) STATICAC DollaID
		  | ID;

scalar_helper: scalar_helper INSTANTAC (ID | funcall)
			 | invocast_helper
			 | Self 
			 | ID;

instance_helper: New ID LB param? RB
			   | instance_helper INSTANTAC (ID | funcall)
			   | instance_helper index_operators
			   | invocast_helper
			   | Self
			   | ID;

invocast_helper: (Self | ID) STATICAC (DollaID | staticfuncall);
instancestmt: instance_helper INSTANTAC funcall SEMI;
invocastmt: (Self | ID) STATICAC staticfuncall SEMI;
blockstmt: stmt+;

funcall: ID LB param? RB;
staticfuncall: DollaID LB param? RB;

DOUBLEDOT: '..';

/* Integer literal for Array */ 
INTLIT_ARR: INT_LIT_ARR {self.text = self.text.replace("_","")};
INT_LIT_ARR: BIN_
	       | DEC_
	       | OCTAL_
	       | HEXA_;

BIN_: '0' [bB]('1'[01]* ('_' [01]+)*);
DEC_: [1-9][0-9]* ('_' [0-9]+)*;
OCTAL_: '0' ([1-7][0-7]* ('_' [0-7]+)*);
HEXA_: '0' [xX]([1-9A-F][0-9A-F]* ('_' [0-9A-F]+)*);

/* Integer literal */
INTLIT: INT_LIT {self.text = self.text.replace("_","")};
INT_LIT: BIN
	   | DEC
	   | OCTAL
	   | HEXA;

BIN: '0' [bB]('1'[01]* ('_' [01]+)* | '0');
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

literal: INTLIT_ARR | INTLIT | FLOATLIT | BOOLLIT | STRLIT | index_arrlit | multi_arrlit;
index_arrlit: Array LB (expr (COMMA expr)*)? RB;
multi_arrlit: Array LB index_arrlit+ RB;


operands: literal 
		| Self
		| Null
		| ID;

element_expr: expr index_operators;
index_operators: index_operators LS expr RS | LS expr RS;

param: expr (COMMA expr)*;

/* Expressions */
expr: expr1 (STRCONCATE | COMPARESTR) expr1 | expr1;
expr1: expr2 (EQUAL | NOTEQUAL | SMALLER | GREATER | SMALLEREQUAL | GREATEREQUAL) expr2 | expr2;
expr2: expr2 (LOGICALAND | LOGICALOR) expr3 | expr3;
expr3: expr3 (ADDITION | SUBTRACTION) expr4 | expr4;
expr4: expr4 (MULTIPLICATION | DIVISION | MODULO) expr5 | expr5;
expr5: LOGICALNOT expr5 | expr6;
expr6: SUBTRACTION expr6 | expr7;
expr7: expr7 LS expr7 RS | expr8;
expr8: expr8 INSTANTAC (ID | funcall) | expr9;
expr9: (Self | ID) STATICAC (DollaID | staticfuncall) | expr10;
expr10: New expr10 LB param? RB | expr11;
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
UNCLOSE_STRING: '"' (STR_CHAR | ESCSEQ)* (EOF | '\n'){
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