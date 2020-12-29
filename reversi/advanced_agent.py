from reversi import Reversi
import math
import random

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