import random

infinity = 1e400

class Board():

    def __init__(self, board, size, to_move):
        self.board = board
        self.size = size
        self.to_move = to_move

    def __str__(self):
        def colour_square(s):
            if s == 1:
                return '\033[92mO\033[0m'
            elif s == 2:
                return '\033[91mO\033[0m'
            else:
                return ' '

        output = '┌' + '─' * self.size + '┐\n'
        for line in self.board:
            output += '│' + ''.join([colour_square(x) for x in line]) + '│\n'
        output += '└' + '─' * self.size + '┘\n'
        output += 'to move: ' + str(self.to_move)
        return output

    @classmethod
    def initial_board(self, size = 8):
        board = [[0 for _ in range(size)] for _ in range(size)]
        for x in range(1, size - 1):
            board[0][x] = 1
            board[size - 1][x] = 1
            board[x][0] = 2
            board[x][size - 1] = 2
        return Board(board, size, 1)

    def get_available_moves(self):
        boards = []
        for x in range(self.size):
            for y in range(self.size):
                boards += self.get_moves_for_square(x, y)
        return list(map(lambda b: Board(b, self.size, 3 - self.to_move), boards))

    def get_moves_for_square(self, x, y):
        boards = []
        if self.board[x][y] == self.to_move:
            h_move_size = self.size - self.board[x].count(0)

            v_move_size = 0
            for i in range(self.size):
                if self.board[i][y] != 0:
                    v_move_size += 1

            d1_move_size = self.get_diagonal_1_move_size(x, y)
            d2_move_size = self.get_diagonal_2_move_size(x, y)

            boards += self.get_move(x, y, 0, 1, h_move_size)
            boards += self.get_move(x, y, 0, -1, h_move_size)
            boards += self.get_move(x, y, 1, 0, v_move_size)
            boards += self.get_move(x, y, -1, 0, v_move_size)
            boards += self.get_move(x, y, 1, 1, d1_move_size)
            boards += self.get_move(x, y, -1, -1, d1_move_size)
            boards += self.get_move(x, y, 1, -1, d2_move_size)
            boards += self.get_move(x, y, -1, 1, d2_move_size)
        return boards

    # \
    def get_diagonal_1_move_size(self, x, y):
        move_size = 1
        x_pos = x
        y_pos = y
        for i in range(self.size):
            x_pos += 1
            y_pos += 1
            if x_pos >= self.size or y_pos >= self.size:
                break
            if self.board[x_pos][y_pos] != 0:
                move_size += 1

        x_pos = x
        y_pos = y
        for i in range(self.size):
            x_pos -= 1
            y_pos -= 1
            if x_pos < 0 or y_pos < 0:
                break
            if self.board[x_pos][y_pos] != 0:
                move_size += 1

        return move_size

    # /
    def get_diagonal_2_move_size(self, x, y):
        move_size = 1
        x_pos = x
        y_pos = y
        for i in range(self.size):
            x_pos += 1
            y_pos -= 1
            if x_pos >= self.size or y_pos < 0:
                break
            if self.board[x_pos][y_pos] != 0:
                move_size += 1

        x_pos = x
        y_pos = y
        for i in range(self.size):
            x_pos -= 1
            y_pos += 1
            if x_pos < 0 or y_pos >= self.size:
                break
            if self.board[x_pos][y_pos] != 0:
                move_size += 1

        return move_size

    def get_move(self, x, y, x_dir, y_dir, move_size):
        x_pos = x
        y_pos = y
        for i in range(0, move_size):
            x_pos += x_dir
            y_pos += y_dir
            # check if moving off the edge of the board
            if x_pos < 0 or x_pos >= self.size or y_pos < 0 or y_pos >= self.size:
                return []
            # check if jumping over opponent's checker
            if self.board[x_pos][y_pos] == 3 - self.to_move and i < move_size - 1:
                return []
            # check if landing on own checker
            if self.board[x_pos][y_pos] == self.to_move and i == move_size - 1:
                return []

        new_board = [i[:] for i in self.board]
        new_board[x][y] = 0
        new_board[x_pos][y_pos] = self.to_move
        return [new_board]

    def is_terminal_state(self):
        return self.winner() != -1

    def winner(self):
        is_p1_connected = self.is_connected(1)
        is_p2_connected = self.is_connected(2)
        if is_p1_connected and not is_p2_connected:
            return 1
        elif is_p2_connected and not is_p1_connected:
            return 2
        elif is_p1_connected and is_p2_connected:
            return 0
        else:
            return -1

    def is_connected(self, player):
        return self.count_connected_groups(player) == 1

    def count_connected_groups(self, player):
        groups = []
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != player: continue
                groups_to_merge = [[(x, y)]]
                groups_to_preserve = []
                for g in groups:
                    if self.is_connected_to_group(x, y, g):
                        groups_to_merge += [g]
                    else:
                        groups_to_preserve += [g]
                groups = groups_to_preserve
                merged = [s for g in groups_to_merge for s in g]
                groups += [merged]
        return len(groups)

    def is_connected_to_group(self, x, y, group):
        for (i, j) in group:
            if abs(x - i) <= 1 and abs(y - j) <= 1:
                return True
        return False

    def score(self):
        winner = self.winner()
        if winner != -1:
            if winner == 0:
                return 0
            if winner == self.to_move:
                return infinity
            else:
                return -infinity
        return self.player_score(self.to_move) - self.player_score(3 - self.to_move)

    def player_score(self, player):
        coords = []
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == player:
                    coords.append((x, y))
        v = self.variance(coords)
        if v == 0: return infinity
        inv_v = 1 / v
        inv_g = 1 / self.count_connected_groups(player)
        return inv_v + 3 * inv_g

    def variance(self, coords):
        n = len(coords)
        if n == 1: return 0
        x_sum = sum([c[0] for c in coords])
        y_sum = sum([c[1] for c in coords])
        x_mean = x_sum / n
        y_mean = y_sum / n
        x_var = sum(map(lambda i: (i[0] - x_mean)**2, coords)) / (n - 1)
        y_var = sum(map(lambda i: (i[1] - y_mean)**2, coords)) / (n - 1)
        return x_var + y_var
