from board import Board
from mcts import pure_mcts_search
from search import alphabeta_search

def game_loop():
    b = Board.initial_board()
    while True:
        print(b)
        if (b.is_terminal_state()):
            winner = b.winner()
            if winner == 0:
                print("It's a tie")
            else:
                print("Player {} has won".format(winner))
            break
        b = alphabeta_search(b)

def main():
    print('Lines of Action')
    game_loop()

if __name__ == '__main__':
    main()
