from sly import Lexer, Parser
import GameLogic
import sys

mat = GameLogic.init_board()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

prompt = f"{bcolors.BOLD}2048 > {bcolors.ENDC}"

class TestLexer(Lexer):
    tokens = {ADD, SUBTRACT, MULTIPLY, DIVIDE, LEFT, RIGHT, UP, DOWN, ASSIGN, TO, VAR, IS, VALUE, IN, ID, NUMBER}

    literals = {',', '.', '(', ')'}

    ignore = ' \t'

    ID              = r'[a-zA-Z][a-zA-z0-9_]*'
    NUMBER          = r'\d+'

    ID['ADD']       = ADD
    ID['SUBTRACT']  = SUBTRACT
    ID['MULTIPLY']  = MULTIPLY
    ID['DIVIDE']    = DIVIDE 

    ID['LEFT']      = LEFT
    ID['RIGHT']     = RIGHT 
    ID['UP']        = UP
    ID['DOWN']      = DOWN

    ID['ASSIGN']    = ASSIGN 
    ID['TO']        = TO    

    ID['VAR']       = VAR 
    ID['IS']        = IS

    ID['VALUE']     = VALUE
    ID['IN']        = IN

    def error(self, t):
        print(f"{bcolors.FAIL}{prompt}{bcolors.OKBLUE}Illegal character '%s'{bcolors.ENDC}" % t.value[0])
        self.index += 1


class TestParser(Parser):
    
    tokens = TestLexer.tokens
    

    # 16 Moves
    @_('oper direct "."')
    def expr(self, p):
        # Call 2048 move function with param direction and operation
        # p[1] is Direction
        # p[0] is Operation
        global mat
        method = p[1].lower()
        mat, update_flag = getattr(GameLogic, method)(mat, p[0])

        if update_flag :
            GameLogic.add_random_tile(mat)

        GameLogic.print_board(mat)
        return 0


    @_('LEFT', 'RIGHT', 'UP', 'DOWN')
    def direct(self, p):
        return p[0]


    @_('ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE')
    def oper(self, p):
        return p[0]


    # VALUE ASSIGNMENT TO COORDINATE
    @_('ASSIGN NUMBER TO NUMBER "," NUMBER "."', 'ASSIGN value TO NUMBER "," NUMBER "."')
    def expr(self, p):
        global mat
        EMPTY = 0
        x = int(p[3])
        y = int(p[5])

        if p[1] == None:
            return -1

        if not x in range(1, 5) or not y in range(1,5):
            print(f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4{bcolors.ENDC}")
            print("-1", file=sys.stderr)

            return -1
        
        else:
            mat[x-1][y - 1] = int(p[1])
            if (mat[x-1][y - 1] == EMPTY):
                GameLogic.tileNames[x-1][y-1].clear()
            GameLogic.print_board(mat)

        return 0
    

    # VALUE ASSIGNMENT TO NAMED TILE
    @_('ASSIGN NUMBER TO ID "."', 'ASSIGN value TO ID "."')
    def expr(self, p):
        global mat
        EMPTY = 0

        x = -1 
        y = -1

        for i in range(4):
            for j in range(4):
                if p[3] in GameLogic.tileNames[i][j]:
                    x, y = i, j


        if x == -1 or y == -1:
            print(f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}There is no tile named {p[3]}{bcolors.ENDC}")
            print("-1", file=sys.stderr)

            return None

        
        else:
            mat[x][y] = int(p[1])
            if (mat[x][y] == EMPTY):
                GameLogic.tileNames[x][y] = []
            GameLogic.print_board(mat)

        return 0
    

    @_('VALUE IN NUMBER "," NUMBER')
    def value(self, p):
        x = int(p[2])
        y = int(p[4])

        EMPTY = 0

        if not x in range(1, 5) or not y in range(1,5):
            print(f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4{bcolors.ENDC}")
            print("-1", file=sys.stderr)

            return None

        someValue = mat[x-1][y-1]

        if someValue != EMPTY:
            # print (someValue)
            return someValue
        
        else:
            # print("EMPTY")
            return 0


    @_('VALUE IN ID')
    def value(self, p):
        x = -1 
        y = -1

        for i in range(4):
            for j in range(4):
                if p[2] in GameLogic.tileNames[i][j]:
                    x, y = i, j


        EMPTY = 0

        if x == -1 or  y == -1:
            print(f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}There is no tile named {p[2]}{bcolors.ENDC}")
            print("-1", file=sys.stderr)

            return None

        someValue = mat[x][y]

        if someValue != EMPTY:
            print (f"{bcolors.HEADER}{prompt}{bcolors.OKBLUE}{someValue}{bcolors.ENDC}")
            return someValue
        
        else:
            print(f"{bcolors.HEADER}{prompt}{bcolors.OKBLUE}EMPTY{bcolors.ENDC}")
            return 0


    @_('NUMBER "," NUMBER IS ID "."')
    def expr(self, p):
        # p[4] is ID
        # p[0] and p[2] are x,y coordinates

        EMPTY = 0
        global mat
        x = int(p[0])
        y = int(p[2])

        if not x in range(1, 5) or not y in range(1,5):
            print(f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4{bcolors.ENDC}")
            print("-1", file=sys.stderr)

        
        else:
            for i in range(4):
                for j in range(4):
                    if p[4] in GameLogic.tileNames[i][j]:
                        print (f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}Error! Name already assigned to {1 + i},{1 + j}{bcolors.ENDC}")
                        print("-1", file=sys.stderr)

                        return -1

            # If unique Name only then...
            if mat[x-1][y-1] == EMPTY:
                print(f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}Error! Can not assign name to empty tile{bcolors.ENDC}")
                print("-1", file=sys.stderr)
                return -1

            GameLogic.tileNames[x-1][y - 1].append(p[4])
            GameLogic.print_board(mat)

        return 0


    @_('VAR ID IS NUMBER "," NUMBER "."')
    def expr(self, p):
        # p[1] is ID
        # p[3] and p[5] are x,y coordinates
        
        global mat
        EMPTY = 0
        x = int(p[3])
        y = int(p[5])

        if not x in range(1, 5) or not y in range(1,5):
            print(f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4{bcolors.ENDC}")
            print("-1", file=sys.stderr)

        
        else:
            for i in range(4):
                for j in range(4):
                    if p[1] in GameLogic.tileNames[i][j]:
                        print (f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}Error! Name already assigned to {1 + i},{1 + j}{bcolors.ENDC}")
                        print("-1", file=sys.stderr)
                        return -1

            # If unique Name only then...
            if mat[x-1][y-1] == EMPTY:
                print(f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}Error! Can not assign name to empty tile{bcolors.ENDC}")
                print("-1", file=sys.stderr)
                return -1

            GameLogic.tileNames[x-1][y - 1].append(p[1])
            GameLogic.print_board(mat)

        return 0
    

    @_('ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'ASSIGN', 'TO', 'VAR', 'IS', 'VALUE', 'IN')
    def keyword(self, p):
        return p[0]


    @_('VALUE IN NUMBER "," NUMBER "."')
    def expr(self, p):
        x = int(p[2])
        y = int(p[4])

        EMPTY = 0

        if not x in range(1, 5) or not y in range(1,5):
            print(f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4{bcolors.ENDC}")
            print("-1", file=sys.stderr)
            return -1

        someValue = mat[x-1][y-1]

        if someValue != EMPTY:
            print (f"{bcolors.HEADER}{prompt}{bcolors.OKBLUE}{someValue}{bcolors.ENDC}")

            print()
            for i in range(4):
                for j in range(4):
                    print(mat[i][j], end=" ", file=sys.stderr)


            for i in range(4):
                for j in range(4):
                    if len(GameLogic.tileNames[i][j]) != 0:
                        print(f"{1+i},{1+j}", end="", file=sys.stderr)
                        print(*GameLogic.tileNames[i][j], sep=",", file=sys.stderr, end=" ")
            
            print(file = sys.stderr)

            return someValue
        
        else:
            print(f"{bcolors.HEADER}{prompt}{bcolors.OKBLUE}EMPTY{bcolors.ENDC}")
            print()
            for i in range(4):
                for j in range(4):
                    print(mat[i][j], end=" ", file=sys.stderr)
                
            for i in range(4):
                for j in range(4):
                    if len(GameLogic.tileNames[i][j]) != 0:
                        print(f"{1+i},{1+j}", end="", file=sys.stderr)
                        print(*GameLogic.tileNames[i][j], sep=",", file=sys.stderr, end=" ")

            print(file = sys.stderr)
            return 0


    @_('VALUE IN ID "."')
    def expr(self, p):

        x = -1 
        y = -1

        for i in range(4):
            for j in range(4):
                if p[2] in GameLogic.tileNames[i][j]:
                    x, y = i, j


        EMPTY = 0

        if x == -1 or  y == -1:
            print(f"{bcolors.WARNING}{prompt}{bcolors.OKBLUE}There is no tile named {p[2]}{bcolors.ENDC}")
            print("-1", file=sys.stderr)
            return -1

        someValue = mat[x][y]

        if someValue != EMPTY:
            print (f"{bcolors.HEADER}{prompt}{bcolors.OKBLUE}{someValue}{bcolors.ENDC}")
            print()
            for i in range(4):
                for j in range(4):
                    print(mat[i][j], end=" ", file=sys.stderr)
                
            for i in range(4):
                for j in range(4):
                    if len(GameLogic.tileNames[i][j]) != 0:
                        print(f"{1+i},{1+j}", end="", file=sys.stderr)
                        print(*GameLogic.tileNames[i][j], sep=",", file=sys.stderr, end=" ")

            print(file = sys.stderr)
            return someValue
        
        else:
            print(f"{bcolors.HEADER}{prompt}{bcolors.OKBLUE}EMPTY{bcolors.ENDC}")

            print()
            for i in range(4):
                for j in range(4):
                    print(mat[i][j], end=" ", file=sys.stderr)
                
            for i in range(4):
                for j in range(4):
                    if len(GameLogic.tileNames[i][j]) != 0:
                        print(f"{1+i},{1+j}", end="", file=sys.stderr)
                        print(*GameLogic.tileNames[i][j], sep=",", file=sys.stderr, end=" ")

            print(file = sys.stderr)
            return 0


    @_(
        'oper direct',

        'NUMBER "," NUMBER IS keyword',
        'NUMBER "," NUMBER IS ID',
        'NUMBER "," NUMBER IS NUMBER',

        'ASSIGN NUMBER TO NUMBER "," NUMBER',

        'VAR NUMBER IS NUMBER "," NUMBER',
        'VAR ID IS NUMBER "," NUMBER',
        'VAR keyword IS NUMBER "," NUMBER',

        'VALUE IN NUMBER "," NUMBER',
        'VALUE IN ID',

        'ASSIGN NUMBER TO ID',
        'ASSIGN value TO ID'

    )
    def expr(self, p):
        print(f"{bcolors.FAIL}{prompt}{bcolors.OKBLUE}End commands with full stop!{bcolors.ENDC}")
        print("-1", file=sys.stderr)
        return -1
        

    @_(
        'NUMBER "," NUMBER IS keyword "."',
        'NUMBER "," NUMBER IS NUMBER "."',      
    )
    def expr(self, p):
        print(f"{bcolors.FAIL}{prompt}{bcolors.OKBLUE}Variable Name cannot be {p[4]}, Use Non-Keyword AlphaNumeric String!{bcolors.ENDC}")
        print("-1", file=sys.stderr)
        return -1


    @_(
        'VAR keyword IS NUMBER "," NUMBER "."',
        'VAR NUMBER IS NUMBER "," NUMBER "."'      
    )
    def expr(self, p):
        print(f"{bcolors.FAIL}{prompt}{bcolors.OKBLUE}Variable Name cannot be {p[1]}, Use Non-Keyword AlphaNumeric String!{bcolors.ENDC}")
        print("-1", file=sys.stderr)
        return -1


    def error(self, p):
        print(f"{bcolors.FAIL}{prompt}{bcolors.OKBLUE}Syntax Error! {bcolors.ENDC}")
        print("-1", file=sys.stderr)

        while True:
            tok = next(self.tokens, None)
            if not tok:
                break
        
        self.restart()          #double check
        # return -1


if __name__ == '__main__':

    parser  = TestParser()
    lexer   = TestLexer()

    print(f"{bcolors.OKGREEN}{prompt}{bcolors.OKBLUE}Hi, I am the 2048-game Engine.{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}{prompt}{bcolors.OKBLUE}The Start state is{bcolors.ENDC}")

    # print("-1", file=sys.stderr)

    GameLogic.print_board(mat)

    GameLogic.subopt = input(f"\n{bcolors.OKGREEN}{prompt}{bcolors.OKBLUE}Enter 1 if SUBTRACT LEFT. on 4 2 2 4 is 4 4 0 0.\n{bcolors.OKGREEN}{prompt}{bcolors.OKBLUE}Enter 2 if SUBTRACT LEFT. on 4 2 2 4 is 4 0 4 0.\n{bcolors.OKGREEN}{prompt}{bcolors.OKBLUE}{bcolors.ENDC}")
    
    if GameLogic.subopt != "1" and GameLogic.subopt != "2":
        print(f"\n{bcolors.FAIL}{prompt}{bcolors.OKBLUE} Invalid Input : {GameLogic.subopt}{bcolors.ENDC}")
        GameLogic.subopt = "1"
    
    print(f"\n{bcolors.OKGREEN}{prompt}{bcolors.OKBLUE} Selected : {GameLogic.subopt}{bcolors.ENDC}")


    while True:
        try:
            pr = f"\n\n{bcolors.OKGREEN}{prompt}{bcolors.ENDC}"
            text = input(pr)

        except EOFError:
            break



        if text:
            # print(text)
            result  = parser.parse(lexer.tokenize(text))
            # print(result)


