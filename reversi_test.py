from reversi_utils import EMPTY,WHITE,BLACK
import reversi_utils as utils

def test_generate_board():
    b=utils.generate_board()
    assert b[0][0]==EMPTY
    assert b[3][4]==BLACK
    assert b[3][3]==WHITE

def test_reversi_rule():
    b=utils.generate_board()
    assert not utils.can_flip(b,2,3,WHITE)
    assert utils.can_flip(b,2,3,BLACK)
    assert utils.flip(b,2,3,BLACK)==1
    assert utils.count_stone(b,BLACK)==4
    assert utils.count_stone(b,WHITE)==1
    print_board(b)
    assert utils.can_flip(b,2,2,WHITE)
    assert utils.flip(b,2,2,WHITE)==1
    print_board(b)
    assert utils.can_flip(b,3,2,BLACK)
    assert utils.flip(b,3,2,BLACK)==1
    print_board(b)
    assert utils.can_flip(b,2,4,WHITE)
    assert utils.flip(b,2,4,WHITE)==2
    print_board(b)
    assert utils.can_flip(b,1,5,BLACK)
    assert utils.flip(b,1,5,BLACK)==1
    print_board(b)

def print_board(board:list[list[int]]):
    ST=["・","X","O"]
    print(" 0 1 2 3 4 5 6 7")
    for y,row in enumerate(board):
        print(f"{y}"+(" ".join([ST[i] for i in row])))

if __name__=="__main__":
    test_reversi_rule()