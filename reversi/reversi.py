import random

class Reversi:
        def __init__(self, dim):
                # initialize board
                # 1=black piece, 2=white piece, 0=empty

                self.board = [[0]*dim for i in range(dim)]
                self.board[dim//2-1][dim//2-1] = 1
                self.board[dim//2][dim//2] = 1
                self.board[dim//2][dim//2-1] = 2
                self.board[dim//2-1][dim//2] = 2

        def initial_position(self):
                return Reversi.Position(self.board, 1, [4, 2, 2], 0)

        class Position:
                def __init__(self, board, turn, pieces, no_moves_count):
                        self.board = board
                        self.turn = turn
                        self.pieces = pieces
                        self.no_moves_count = no_moves_count

                def legal_moves(self):
                        # go through each row, col, and diagonal
                        # to find all legal moves

                        moves = set()
                        dim = len(self.board)

                        # simple state machine with following states:
                        # searching - haven't encountered a piece of
                        #       the turn player's color
                        # encountered - found turn player's piece
                        # encompassing - found opponent's piece
                        #       after your own piece
                        state = "Searching"
                        def state_machine(piece, row, col):
                                nonlocal state
                                if state == "Searching":
                                        if piece == self.turn:
                                                state = "Encountered"
                                elif state == "Encountered":
                                        if piece == 3 - self.turn:
                                                state = "Encompassing"
                                        elif piece == 0:
                                                state = "Searching"
                                elif state == "Encompassing":
                                        if piece == 0:
                                                moves.add((row, col))
                                                state = "Searching"
                                        elif piece == self.turn:
                                                state = "Encountered"

                        # along rows
                        for row in range(dim):
                                for col in range(dim):
                                        state_machine(self.board[row][col], row, col)
                                state = "Searching"
                        for row in range(dim):
                                for col in range(dim - 1, -1, -1):
                                        state_machine(self.board[row][col], row, col)
                                state = "Searching"

                        # along columns
                        for col in range(dim):
                                for row in range(dim):
                                        state_machine(self.board[row][col], row, col)
                                state = "Searching"
                        for col in range(dim):
                                for row in range(dim - 1, -1, -1):
                                        state_machine(self.board[row][col], row, col)
                                state = "Searching"

                        # along forward diagonals
                        for lim in range(dim):
                                for col in range(lim, -1, -1):
                                        state_machine(self.board[lim-col][col], lim-col, col)
                                state = "Searching"
                        for lim in range(dim):
                                for col in range(dim - 1, lim, -1):
                                        state_machine(self.board[dim-col+lim][col], dim-col+lim, col)
                        for lim in range(dim):
                                for row in range(lim, -1, -1):
                                        state_machine(self.board[row][lim-row], row, lim-row)
                                state = "Searching"
                        for lim in range(dim):
                                for row in range(dim - 1, lim, -1):
                                        state_machine(self.board[row][dim-row+lim], row, dim-row+lim)

                        # along backward diagonals
                        for lim in range(dim+1):
                                for row in range(lim):
                                        state_machine(self.board[row][dim-lim+row], row, dim-lim+row)
                                #       print(dim-lim+row, row, end=", ")
                                # print("")
                                state = "Searching"
                        for lim in range(dim-1, -1, -1):
                                for col in range(lim):
                                        state_machine(self.board[dim-lim+col][col], dim-lim+col, col)
                                state = "Searching"
                        for lim in range(dim+1):
                                for row in range(lim-1, -1 , -1):
                                        state_machine(self.board[row][dim-lim+row], row, dim-lim+row)
                                state = "Searching"
                        for lim in range(dim-1, -1, -1):
                                for col in range(lim-1, -1, -1):
                                        state_machine(self.board[dim-lim+col][col], dim-lim+col, col)
                                state = "Searching"

                        if len(moves) > 0:
                                return(list(moves))
                        else:
                                return [None]

                def result(self, move):
                        # result of placing a piece in the "move" indices

                        new_board = [row[:] for row in self.board]
                        new_pieces = self.pieces[:]

                        if not move:
                                return(Reversi.Position(new_board, 3-self.turn, new_pieces, self.no_moves_count+1))

                        new_board[move[0]][move[1]] = self.turn

                        # simple state machine with following states:
                        # encountered - found turn player's piece
                        # encompassing - found opponent's piece
                        #       after your own piece
                        # stop - this direction needs no flipping
                        # flip - this direction requires flipping
                        state = "Encountered"

                        def state_machine(piece, row, col):
                                nonlocal state
                                if state == "Encountered":
                                        if piece == 3 - self.turn:
                                                state = "Encompassing"
                                        else:
                                                state = "Stop"
                                elif state == "Encompassing":
                                        if piece == self.turn:
                                                state = "Flip"
                                        elif piece == 0:
                                                state = "Encountered"

                        # check in all 8 directions for where flips are necessary
                        for direction in [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]:
                                new_row = move[0]+direction[0]
                                new_col = move[1]+direction[1]
                                state = "Encountered"

                                # go through each direction to see if flipping is necessary
                                while(new_row >= 0 and new_row < len(self.board) and new_col >= 0 and new_col < len(self.board)):
                                        state_machine(self.board[new_row][new_col], new_row, new_col)
                                        if state == "Stop" or state == "Flip":
                                                break
                                        new_row += direction[0]
                                        new_col += direction[1]

                                # then, flip all opposing colors until you reach one of your own colors
                                if state == "Flip":
                                        new_row = move[0]
                                        new_col = move[1]

                                        while(new_row >= 0 and new_row < len(self.board) and new_col >= 0 and new_col < len(self.board)):
                                                new_row += direction[0]
                                                new_col += direction[1]
                                                if self.board[new_row][new_col] == 3 - self.turn:
                                                        new_pieces[self.turn] += 1
                                                        new_pieces[3-self.turn] -= 1
                                                        new_board[new_row][new_col] = self.turn
                                                else:
                                                        break

                        new_pieces[0] += 1
                        new_pieces[self.turn] += 1

                        return(Reversi.Position(new_board, 3-self.turn, new_pieces, 0))

                # return player to make next move in this position
                def next_player(self):
                        return self.turn

                # checks if the given move is a corner move
                def is_corner(self, move):
                        return move == (0, 0) or move == (0, 7) or move == (7, 0) or move == (7, 7)

                # checks if the given move is on the edge of the board
                def is_edge(self, move):
                        if not move:
                                return False
                        return move[0] == 0 or move[0] == 7 or move[1] == 0 or move[1] == 7

                # checks if the given move is adjacent to a corner
                def is_corner_adjacent(self, move):
                        return (move == (1,0) or move == (0,1) or move == (6,0) or move == (7,1)
                                        or move == (6,7) or move == (7,6) or move == (0,6) or move == (1,7)
                                        or move == (1,1) or move == (1,6) or move == (6,1) or move == (6,6))

                # gets score for minimax heuristic based on number of corners taken
                def corner_score(self):
                        corner_score = 0
                        for corner in [(0,0), (0,7), (7,0), (7,7)]:
                                if self.board[corner[0]][corner[1]] == 2:
                                        corner_score += -1
                                elif self.board[corner[0]][corner[1]] == 1:
                                        corner_score += 1
                        return corner_score

                # gets score for minimax heuristic based on number of corner-adjacent spots taken
                def corner_adjacent_score(self):
                        score = 0
                        for adjacent in [(1,0),(0,1),(6,0),(7,1),(6,7),(7,6),(0,6),(1,7),(1,1),(1,6),(6,1),(6,6)]:
                                if self.board[adjacent[0]][adjacent[1]] == 2:
                                        score += 1
                                elif self.board[adjacent[0]][adjacent[1]] == 1:
                                        score += -1
                        return score

                # return array of total pieces, p1 pieces, and p2 pieces
                def get_pieces(self):
                        return self.pieces

                # checks if game is over
                def game_over(self):
                        if self.pieces[0] == 64 or self.no_moves_count > 1:
                                return True
                        return False

                # returns winner of a game
                def winner(self):
                        if self.pieces[1] > self.pieces[2]:
                                return 1
                        elif self.pieces[1] < self.pieces[2]:
                                return -1
                        else:
                                return 0

                def __str__(self):
                        to_print = "   "
                        for i in range(8):
                                to_print += ' '+str(i)+' '
                        to_print += '\n'
                        for i, row in enumerate(self.board):
                                to_print += ' '+str(i)+' '
                                for char in row:
                                        if char == 0:
                                                to_print += '[ ]'
                                        elif char == 1:
                                                to_print += '[●]'
                                        elif char == 2:
                                                to_print += '[○]'
                                to_print += '\n'
                        return to_print

                def __hash__(self):
                        to_hash = [row[:] for row in self.board]
                        for i in range(len(to_hash)):
                                to_hash[i] = tuple(to_hash[i])
                        return hash(tuple(to_hash)) + self.turn

                def __eq__(self, other):
                        if self.board == other.board and self.turn == other.turn:
                                return True
                        else:
                                return False

if __name__ == '__main__':
        p1_wins = 0
        p2_wins = 0
        game = Reversi(8)

        for i in range(1000):
                pos = game.initial_position()
                # print(pos)
                while(not pos.game_over()):
                        moves = pos.legal_moves()
                        # print(moves)
                        # print("----------------------------")
                        pos = pos.result(moves[random.randint(0, len(moves)-1)])
                        # print(pos)
                        # print(pos.get_pieces())
                # print(pos)
                # print(pos.winner(), pos.get_pieces())
                if pos.winner() == 0:
                        p1_wins += 0.5
                        p2_wins += 0.5
                elif (pos.winner() > 0 and i % 2 == 0) or (pos.winner() < 0 and i % 2 == 1):
                        p1_wins += 1
                else:
                        p2_wins += 1
        print(p1_wins, p2_wins)