/**
 * Grammar for Moire markup language.
 *
 * @author Sergey Vartanov
 * @since 2 September 2022
 */
grammar Moire;

document : markup EOF ;
markup : ( tag | TEXT | WHITESPACE | escapedCharacter | DELIMITER )+ ;
tag : TAG_NAME ( WHITESPACE? argument )* ;
argument : CURLY_OPEN markup CURLY_CLOSE ;
escapedCharacter : BACKSLASH (BACKSLASH | CURLY_OPEN | CURLY_CLOSE) ;

DELIMITER : '\n\n' ;
BACKSLASH : '\\' ;
CURLY_OPEN : '{' ;
CURLY_CLOSE : '}' ;
fragment IDENTIFIER : [A-Za-z0-9_]+;
TAG_NAME: BACKSLASH IDENTIFIER;
WHITESPACE : [ \t\n\r]+;
TEXT : [A-Za-z. \n\t\r]+;