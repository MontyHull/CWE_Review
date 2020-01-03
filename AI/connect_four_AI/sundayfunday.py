import sys

#Gets the point value of the board
def eval(array):
    score = 0
    for i in range(5,-1,-1):
        for j in range(7):
            score += up_again(array,i,j)
            score += horizontal_again(array,i,j)
            score += up_right_again(array,i,j)
            score += up_left_again(array,i,j)
    return score

def up_again(array,x,y):
    user = 'R'
    op = 'B'
    count = 0
    bad_count = 0
    if(x>=3):
        if(array[x][y] == user):
            count += 1
        elif(array[x][y] == op):
            bad_count += 1
        if(array[x-1][y] == user):
            count += 1
        elif(array[x-1][y] == op):
            bad_count += 1
        if(array[x-2][y] == user):
            count += 1
        elif(array[x-2][y] == op):
            bad_count += 1
        if(array[x-3][y] == user):
            count += 1
        elif(array[x-3][y] == op):
            bad_count += 1

        if(count > 0 and bad_count == 0):
            return 10**count
        elif(bad_count > 0 and count == 0):
            return -1*(10**count)
        else:
            return 0
    return 0

def horizontal_again(array,x,y):
    user = 'R'
    op = 'B'
    count = 0
    bad_count = 0
    if(y <= 3):
        if(array[x][y] == user):
            count += 1
        elif(array[x][y] == op):
            bad_count += 1
        if(array[x][y+1] == user):
            count += 1
        elif(array[x][y+1] == op):
            bad_count += 1
        if(array[x][y+2] == user):
            count += 1
        elif(array[x][y+2] == op):
            bad_count += 1
        if(array[x][y+3] == user):
            count += 1
        elif(array[x][y+3] == op):
            bad_count += 1

        if(count > 0 and bad_count == 0):
            return 10**count
        elif(bad_count > 0 and count == 0):
            return -1*(10**count)
        else:
            return 0
    return 0

def up_right_again(array,x,y):
    user = 'R'
    op = 'B'
    count = 0
    bad_count = 0
    if(x > 2 and y <= 3):
        if(array[x][y] == user):
            count += 1
        elif(array[x][y] == op):
            bad_count += 1
        if(array[x-1][y+1] == user):
            count += 1
        elif(array[x-1][y+1] == op):
            bad_count += 1
        if(array[x-2][y+2] == user):
            count += 1
        elif(array[x-2][y+2] == op):
            bad_count += 1
        if(array[x-3][y+3] == user):
            count += 1
        elif(array[x-3][y+3] == op):
            bad_count += 1

        if(count > 0 and bad_count == 0):
            return 10**count
        elif(bad_count > 0 and count == 0):
            return -1*(10**count)
        else:
            return 0
    return 0

def up_left_again(array,x,y):
    user = 'R'
    op = 'B'
    count = 0
    bad_count = 0
    if(x > 2 and y <= 3):
        if(array[x][y] == user):
            count += 1
        elif(array[x][y] == op):
            bad_count += 1
        if(array[x-1][y-1] == user):
            count += 1
        elif(array[x-1][y-1] == op):
            bad_count += 1
        if(array[x-2][y-2] == user):
            count += 1
        elif(array[x-2][y-2] == op):
            bad_count += 1
        if(array[x-3][y-3] == user):
            count += 1
        elif(array[x-3][y-3] == op):
            bad_count += 1

        if(count > 0 and bad_count == 0):
            return 10**count
        elif(bad_count > 0 and count == 0):
            return -1*(10**count)
        else:
            return 0
    return 0




def maxi(board,alpha,beta,depth=1):
    if(depth == 0):
        return [eval(board),1]
    for i in range(7):
        new_board = Board(True,board)
        move_stay = new_board.move(i+1,user)
        if(move_stay == 1):
            continue
        v = mini(new_board.get_array(),alpha,beta,depth-1)
        if v[0] > alpha[0]:
            alpha = [v[0],i+1]
        if beta[0] <= alpha[0]:
            return alpha
    return alpha

def mini(board,alpha,beta,depth=1):
    if(depth == 0):
        return [eval(board),1]
    for i in range(7):
        new_board = Board(True,board)
        move_stay = new_board.move(i+1,user)
        if(move_stay == 1):
            continue
        v = maxi(new_board.get_array(),alpha,beta,depth-1)
        if v[0] < beta[0]:
            beta = [v[0],i+1]
        if beta[0] <= alpha[0]:
            return beta
    return beta





class Board:
    def __init__(self,old=False,bard=False):
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                if old:
                    self.board[i].append(bard[i][j])
                else:
                    self.board[i].append('*')

    def get_array(self):
        return self.board

    def pretty_print(self):
        print()
        for i in range (7):
            for j in range(7):
                if(i < 6):
                    print(str(self.board[i][j]),end="")
                    if(j == 6):
                        print(i+1,end="")
                else:
                    print(str((j+1)),end="")
            print()

    def move(self,move,user):
        if(int(move) > 7 or int(move) < 1):
            print("Please enter a valid move between 1 and 7")
        else:
            for i in range(5,-1,-1):
                if(self.board[i][int(move)-1] == '*'):
                    self.board[i][int(move)-1]= user
                    return 0
                if(i == 0):
                    #print("This column is full, please choose a valid move")
                    return 1

    def won(self,user):
        for i in range(5,-1,-1):
            for j in range(7):
                self.up(user,i,j)
                self.right(user,i,j)
                self.up_left(user,i,j)
                self.up_right(user,i,j)

    def up(self,user,x,y):
        if(x>=3):
            if(self.board[x][y] == user):
                if(self.board[x-1][y] == user):
                    if(self.board[x-2][y] == user):
                        if(self.board[x-3][y] == user):
                            self.pretty_print()
                            print()
                            if(user == 'B'):
                                print("Black player wins!")
                            else:
                                print("Red player wins!")
                            print()
                            sys.exit()

    def right(self,user,x,y):
        if(y <= 3):
            if(self.board[x][y] == user):
                if(self.board[x][y+1] == user):
                    if(self.board[x][y+2] == user):
                        if(self.board[x][y+3] == user):
                            self.pretty_print()
                            print()
                            if(user == 'B'):
                                print("Black player wins!")
                            else:
                                print("Red player wins!")
                            print()
                            sys.exit()

    def up_left(self,user,x,y):
        if(x >= 2 and y >= 3):
            if(self.board[x][y] == user):
                if(self.board[x-1][y-1] == user):
                    if(self.board[x-2][y-2] == user):
                        if(self.board[x-3][y-3] == user):
                            self.pretty_print()
                            print()
                            if(user == 'B'):
                                print("Black player wins!")
                            else:
                                print("Red player wins!")
                            print()
                            sys.exit()

    def up_right(self,user,x,y):
        if(x >= 2 and y <= 3):
            if(self.board[x][y] == user):
                if(self.board[x-1][y+1] == user):
                    if(self.board[x-2][y+2] == user):
                        if(self.board[x-3][y+3] == user):
                            self.pretty_print()
                            print()
                            if(user == 'B'):
                                print("Black player wins!")
                            else:
                                print("Red player wins!")
                            print()
                            sys.exit()

#initialize the board
board = Board()
who = input("Who will be the first to go? ")
if(who == 'h'):
    user = 'B'
else:
    user = 'R'

if(len(sys.argv) == 1):
    depth = 1;
else:
    depth = int(sys.argv[1])

won = False
moves = 0
while not won:
    board.pretty_print()
    print()

    if(user == 'B'):
        where = input("Black player, what's your move? ")
    else:
        move = maxi(board.get_array(),[-10**10,1],[10**10,1],depth)
        where = move[1]
        print("Red Player, what's your move? "+str(move[1]))
    good_move = board.move(where,user)

    if(good_move == 0):
        board.won(user)
        moves = moves +1
        if(moves == 42):
            print("All possible moves have been made. This is a draw")
            sys.exit()
        if(user == 'B'):
            user = 'R'
        else:
            user = 'B'
