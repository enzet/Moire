/**
 * Grammar for Moire markup language.
 *
 * @author Sergey Vartanov
 * @since 19 August 2023
 */
grammar Moire;

document : markup ;
markup : ( DELIMITER | tag | TEXT | WHITESPACE | escapedCharacter )+ ;
tag : TAG_NAME ( WHITESPACE argument )* ;
argument : CURLY_OPEN argumentElement ( SEMICOLON argumentElement )* CURLY_CLOSE ;
argumentElement : markup | KEY markup ;
escapedCharacter : BACKSLASH (BACKSLASH | CURLY_OPEN | CURLY_CLOSE | COLON | SEMICOLON ) ;

DELIMITER : '\n\n' ;
BACKSLASH : '\\' ;
CURLY_OPEN : '{' ;
CURLY_CLOSE : '}' ;
COLON : ':' ;
SEMICOLON : ';' ;
fragment IDENTIFIER : [A-Za-z0-9_]+ ;
TAG_NAME : BACKSLASH IDENTIFIER ;
KEY : IDENTIFIER COLON ;
WHITESPACE : [ \t\n\r]+ ;
TEXT : [A-Za-z. \t\r0-9]+ ;