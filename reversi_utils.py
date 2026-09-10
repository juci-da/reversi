EMPTY,BLACK,WHITE,CAN_FLIP = 0,1,2,3
STATUS = ["□","黒","白","・"]
DIR_OFFSET = [(-1,-1),(-1,0),(-1,1),
              (0,-1),        (0,1),
              (1,-1),(1,0),(1,1)]

def generate_board() -> list[list[int]]:
    board =[ [EMPTY] *8 for _ in range(8)]
    board[3][4] = board[4][3] = BLACK
    board[3][3] = board[4][4] = WHITE
    return board
def  is_on_board(x:int,y:int) -> bool:
    return 0 <= y < 8 and 0 <= x < 8
def toggle(status:int)-> int:
    if status == EMPTY:
        return EMPTY
    return BLACK if status == WHITE else WHITE
def can_flip_dir(board:list[list[int]],
                 x:int,y:int,dx:int,dy:int,who:int) -> bool:
    if board[y][x] != EMPTY:
        return False
    if not is_on_board(x + dx , y + dy):
        return False
    if board[y+dy][x+dx] !=toggle(who):
        return False
    for i in range(2,8):
        if not is_on_board(x+dx*i,y+dy*i):
            return False
        if board[y+dy*i][x+dx*i] == EMPTY:
            return False
        if board[y+dy*i][x+dx*i] == who:
            return True
    return False
def can_flip(board:list[list[int]],
             x:int,y:int,who:int)-> bool:
    for dx,dy in DIR_OFFSET:
        if can_flip_dir(board,x,y,dx,dy,who):
            return True
    return False
def flip_dir(board:list[list[int]],
             x:int,y:int,dx:int,dy:int,who:int)->int:
        if not can_flip_dir(board,x,y,dx,dy,who):
            return 0
        count = 0
        for i in range(1,8):
            if not is_on_board(x+dx*i,y+dy*i):
                break
            if board[y+dy*i][x+dx*i] == who:
                break
            board[y+dy*i][x+dx*i]=who
            count +=1
        return count
def flip(board:list[list[int]],x:int,y:int,who:int) -> int:
    if not can_flip(board,x,y,who):
        return 0
    count=0
    for dx,dy in DIR_OFFSET:
        count +=flip_dir(board,x,y,dx,dy,who)
    board[y][x]=who
    return count
def add_flip_mark(board:list[list[int]],who:int)->list[list[int]]:
    res=generate_board()
    for y in range(8):
        for x in range(8):
            res[y][x]=board[y][x]
            if board[y][x] ==EMPTY:
                if can_flip(board,x,y,who):
                    res[y][x] =CAN_FLIP
    return res
def count_stone(board:list[list[int]],who:int)->int:
    return sum([ row.count(who) for row in board])
def count_stone_both(board:list[list[int]])-> tuple[int,int]:
    return count_stone(board,BLACK),count_stone(board,WHITE)


    
