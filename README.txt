ID : 2018A7PS0235G
NAME : NACHIKET AGRAWAL

2048 Extension written in Python, using SLY (SLY LEX YACC).

Library supplied with source code. (else use : pip install sly)

LEXER : 
Handles multi valued digits for numbers and C like variables (alphabet number underscore chars, begins with alphabet) for Variable names
Generates appropriate tokens for keywords

Parser :
Handles all valid syntax with minor Extensions like "ASSIGN VALUE IN a,b TO c,d." or "VALUE IN myVar."
Reports "End with Fullstop error"
Reports "Var cant be keyword error"
Reports Syntax errors for any error not caught by above two
Prints -1 to STDERR iff command has failed else Prints to stderr the state and var names
Prints to STDOUT appropriate value/board/var names


Main :
Asks user to choose between 2 types of SUBTRACTIONS
Presents to user a shell-like environment 


ASSUMPTIONS:
1 based indexing, row is X and column is Y
1 Command per line
0 is empty tile
Var Names dropped for empty tiles
No random tile added if Move doesnt change state
Assign 0 to tile coordinate/name makes it 0
