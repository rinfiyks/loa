from board import Board
from search import alphabeta_search

def game_loop():
    b = Board.initial_board()
    while True:
        print(b)
        input('')
        b = alphabeta_search(b)

def main():
    print('Lines of Action')
    game_loop()

if __name__ == '__main__':
    main()
