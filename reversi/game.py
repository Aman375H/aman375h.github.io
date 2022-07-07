import math
import random

class Reversi:
        def __init__(self, dim):
                # initialize board
                # 1=black piece, 2=white piece, 0=empty

                self.board = [[0]*dim for i in range(dim)]
                self.board[dim/2-1][dim/2-1] = 1
                self.board[dim/2][dim/2] = 1
                self.board[dim/2][dim/2-1] = 2
                self.board[dim/2-1][dim/2] = 2

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
# gets values of different move positions on board in order
# to improve minimax function
board_values = [[[0]*2 for j in range(8)] for i in range(8)]

# takes in number of iterations and returns
# function that returns best Reversi move to
# make from given position
def mcts_strategy(iterations, default):

        # implicit "tree" for tree search is a dict of
        # positions and stats
        pos_table = {}
        pos_table["total_plays"] = 0

        # table of move type successes and totals for MAST
        move_table = {'corner': [0,0], 'edge': [0,0], 'corner_adjacent': [0,0], 'center': [0,0]}

        # function to return
        def fxn(pos):
                if pos not in pos_table:
                        pos_table[pos] = [0, 0]

                # run one MCTS playout per iteration
                for i in range(iterations):
                        mcts(pos)
                        pos_table["total_plays"] += 1

                # for key in move_table:
                #       if move_table[key][1] > 0:
                #               print(key, move_table[key][0] / move_table[key][1], end=", ")
                # print("")

                # for row in board_values:
                #       for stat in row:
                #               if stat[1]:
                #                       print('['+"{:.2f}".format(stat[0]/stat[1])+']', end="")
                #               else:
                #                       print('[ .  ]', end="")
                #       print("")
                # print("------------------")

                # retrieve best move seen so far from root's children
                player = pos.next_player()
                best_move = None
                if player == 1:
                        best_val = -1000000000
                else:
                        best_val = 1000000000
                moves = pos.legal_moves()
                for move in moves:
                        child = pos.result(move)
                        if child not in pos_table:
                                continue
                        else:
                                val = pos_table[child][0] / pos_table[child][1]

                        # maximize for player 1
                        if player == 1:
                                if val > best_val:
                                        best_val = val
                                        best_move = move

                        # minimize for player 2
                        else:
                                if val < best_val:
                                        best_val = val
                                        best_move = move
                return best_move

        # implement MCTS with UCB as tree policy
        # and heuristic as default policy
        def mcts(pos):
                if pos.game_over():
                        result = pos.winner()
                        if result == 1:
                                return result
                        if result == 0:
                                return 0.5
                        if result == -1:
                                return 0

                player = pos.next_player()
                moves = pos.legal_moves()
                best_move = None
                best_child = None
                if player == 1:
                        best_UCB = -1000000000
                else:
                        best_UCB = 1000000000

                for move in moves:
                        child = pos.result(move)
                        # if we haven't seen child, we are at an expandable node
                        # switch to default policy and update child, parent stats
                        if child not in pos_table:

                                # choose type of playout to carry out
                                if default == "MAST":
                                        value = mast_playout(child)
                                elif default == "Heuristic":
                                        value = static_guided_playout(child)
                                elif default == "Corner":
                                        value = corner_playout(child)
                                elif default == "Random":
                                        value = random_playout(child)
                                elif default == "Multi":
                                        value = 0
                                        for i in range(3):
                                                value += random_playout(child)
                                        value /= 3

                                # update_move_table(child, move, value)
                                pos_table[child] = [value, 1]
                                pos_table[pos] = [pos_table[pos][0] + value, pos_table[pos][1]+1]
                                return value

                        # the node is not expandable, we choose best child based on UCB
                        else:
                                ucb = UCB(pos_table[child][0], pos_table[child][1], player)
                                # maximize for player 1
                                if player == 1:
                                        if best_UCB < ucb:
                                                best_UCB = ucb
                                                best_move = move
                                                best_child = child

                                # minimize for player 2
                                else:
                                        if best_UCB > ucb:
                                                best_UCB = ucb
                                                best_move = move
                                                best_child = child

                # move to best child
                result = mcts(best_child)

                update_move_table(pos, best_move, result)

                # backpropagate stats
                pos_table[pos] = [pos_table[pos][0] + result, pos_table[pos][1]+1]
                return result

        # implements UCB to balance exploration and exploitation for both players
        def UCB(wins, plays, player):
                if player == 1:
                        return 2*(wins/plays) + math.sqrt((2*math.log(pos_table["total_plays"])) / plays)
                else:
                        return 2*(wins/plays) - math.sqrt((2*math.log(pos_table["total_plays"])) / plays)

        # update stats for types of moves and board position values
        def update_move_table(pos, move, value):
                if not move:
                        return
                if pos.is_corner(move):
                        move_table['corner'][0] += value
                        move_table['corner'][1] += 1
                elif pos.is_corner_adjacent(move):
                        move_table['corner_adjacent'][0] += value
                        move_table['corner_adjacent'][1] += 1
                elif pos.is_edge(move):
                        move_table['edge'][0] += value
                        move_table['edge'][1] += 1
                else:
                        move_table['center'][0] += value
                        move_table['center'][1] += 1

                board_values[move[0]][move[1]][0] += value
                board_values[move[0]][move[1]][1] += 1

        # simulates random playout, returns value from first player perspective
        def random_playout(pos):
                if pos.game_over():
                        result = pos.winner()
                        if result == 1:
                                return result
                        if result == 0:
                                return 0.5
                        if result == -1:
                                return 0
                moves = pos.legal_moves()
                random_move = moves[random.randrange(len(moves))]
                return random_playout(pos.result(random_move))

        # simulates heuristic-guided playout (ex. always choose corners if available, etc..)
        # returns value from first player perspective
        def static_guided_playout(pos):
                if pos.game_over():
                        result = pos.winner()
                        if result == 1:
                                return result
                        if result == 0:
                                return 0.5
                        if result == -1:
                                return 0
                moves = pos.legal_moves()
                best = None

                for move in moves:
                        if pos.is_corner(move):
                                best = move
                                break
                        elif pos.is_edge(move):
                                best = move

                if best:
                        return static_guided_playout(pos.result(best))
                else:
                        random_move = moves[random.randrange(len(moves))]
                        return static_guided_playout(pos.result(random_move))

        # simulate playout based on MAST
        def mast_playout(pos):
                if pos.game_over():
                        result = pos.winner()
                        if result == 1:
                                return result
                        if result == 0:
                                return 0.5
                        if result == -1:
                                return 0

                moves = pos.legal_moves()

                # sort move types by success rates in past
                best_types = []
                for key in move_table:
                        if move_table[key][1] > 0:
                                best_types.append([key, move_table[key][0] / move_table[key][1]])

                if pos.next_player() == 1:
                        best_types.sort(key = lambda category: category[1], reverse = True)
                else:
                        best_types.sort(key = lambda category: category[1])

                categorized_moves = {'corner': [], 'corner_adjacent': [], 'edge': [], 'center': []}

                # put each move in a category
                for move in moves:
                        if pos.is_corner(move):
                                categorized_moves['corner'].append(move)
                        elif pos.is_corner_adjacent(move):
                                categorized_moves['corner_adjacent'].append(move)
                        elif pos.is_edge(move):
                                categorized_moves['edge'].append(move)
                        else:
                                categorized_moves['center'].append(move)

                # pick random move from list of best type
                for best_type in best_types:
                        move_list = categorized_moves[best_type[0]]
                        if len(move_list) > 0:
                                return mast_playout(pos.result(move_list[random.randrange(len(move_list))]))

                return random_playout(pos.result(moves[random.randrange(len(moves))]))

        # chooses actions based on moving into corners when available, else random
        # very simple, but had best performance
        def corner_playout(pos):
                if pos.game_over():
                        result = pos.winner()
                        if result == 1:
                                return result
                        if result == 0:
                                return 0.5
                        if result == -1:
                                return 0
                moves = pos.legal_moves()

                for move in moves:
                        if pos.is_corner(move):
                                return corner_playout(pos.result(move))

                return corner_playout(pos.result(moves[random.randrange(len(moves))]))

        return fxn

def human_game(ai_strat):
    ai = ai_strat()
    board = Reversi(8)
    position = board.initial_position()

    while not position.game_over():
        print(position)
        pieces = position.get_pieces()
        print("Computer's Pieces: ", pieces[1], "Your pieces: ", pieces[2])
        if position.next_player()-1 == 0:
            print("Computer Move...")
            move = ai(position)
        else:
            print("Your Move...")
            moves = position.legal_moves()
            for i, move in enumerate(moves):
                print(i, ": ", move)
            index = ''
            while not index.isnumeric() or int(index) >= len(moves) or int(index) < 0:
                index = input("Enter Move Number: ")

            move = moves[int(index)]

        position = position.result(move)

    print(position)
    pieces = position.get_pieces()
    print("Computer's Pieces: ", pieces[1], "Your pieces: ", pieces[2])
    if position.winner() == 0:
        print('Draw!')
    elif (position.winner() > 0):
        print('Aww, you lost :(')
    else:
        print('You won!')

human_game(lambda: mcts_strategy(500, "Corner"))
