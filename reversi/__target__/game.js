// Transcrypt'ed from Python, 2020-12-28 13:15:35
var math = {};
var random = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_random__ from './random.js';
__nest__ (random, '', __module_random__);
import * as __module_math__ from './math.js';
__nest__ (math, '', __module_math__);
var __name__ = '__main__';

const iterations = 1000;
const ai_strat = (function __lambda__ () {
	return mcts_strategy (iterations, 'Corner');
});
let current_moves = [];
let current_position = null;

export var Reversi =  __class__ ('Reversi', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, dim) {
		self.board = (function () {
			var __accu0__ = [];
			for (var i = 0; i < dim; i++) {
				__accu0__.append([]);
				for (var j = 0; j < dim; j++) {
					__accu0__[i].append(0);
				}
			}
			return __accu0__;
		}) ();
		self.board [dim / 2 - 1] [dim / 2 - 1] = 1;
		self.board [dim / 2] [dim / 2] = 1;
		self.board [dim / 2] [dim / 2 - 1] = 2;
		self.board [dim / 2 - 1] [dim / 2] = 2;
	});},
	get initial_position () {return __get__ (this, function (self) {
		return Reversi.Position (self.board, 1, [4, 2, 2], 0);
	});},
	Position: __class__ ('Position', [object], {
		__module__: __name__,
		get __init__ () {return __get__ (this, function (self, board, turn, pieces, no_moves_count) {
			self.board = board;
			self.turn = turn;
			self.pieces = pieces;
			self.no_moves_count = no_moves_count;
		});},
		get legal_moves () {return __get__ (this, function (self) {
			var moves = set ();
			var dim = len (self.board);
			var state = 'Searching';
			var state_machine = function (piece, row, col) {
				if (state == 'Searching') {
					if (piece == self.turn) {
						state = 'Encountered';
					}
				}
				else if (state == 'Encountered') {
					if (piece == 3 - self.turn) {
						state = 'Encompassing';
					}
					else if (piece == 0) {
						state = 'Searching';
					}
				}
				else if (state == 'Encompassing') {
					if (piece == 0) {
						moves.add (tuple ([row, col]));
						state = 'Searching';
					}
					else if (piece == self.turn) {
						state = 'Encountered';
					}
				}
			};
			for (var row = 0; row < dim; row++) {
				for (var col = 0; col < dim; col++) {
					state_machine (self.board [row] [col], row, col);
				}
				var state = 'Searching';
			}
			for (var row = 0; row < dim; row++) {
				for (var col of range (dim - 1, -(1), -(1))) {
					state_machine (self.board [row] [col], row, col);
				}
				var state = 'Searching';
			}
			for (var col = 0; col < dim; col++) {
				for (var row = 0; row < dim; row++) {
					state_machine (self.board [row] [col], row, col);
				}
				var state = 'Searching';
			}
			for (var col = 0; col < dim; col++) {
				for (var row of range (dim - 1, -(1), -(1))) {
					state_machine (self.board [row] [col], row, col);
				}
				var state = 'Searching';
			}
			for (var lim = 0; lim < dim; lim++) {
				for (var col of range (lim, -(1), -(1))) {
					state_machine (self.board [lim - col] [col], lim - col, col);
				}
				var state = 'Searching';
			}
			for (var lim = 0; lim < dim; lim++) {
				for (var col of range (dim - 1, lim, -(1))) {
					state_machine (self.board [(dim - col) + lim] [col], (dim - col) + lim, col);
				}
			}
			for (var lim = 0; lim < dim; lim++) {
				for (var row of range (lim, -(1), -(1))) {
					state_machine (self.board [row] [lim - row], row, lim - row);
				}
				var state = 'Searching';
			}
			for (var lim = 0; lim < dim; lim++) {
				for (var row of range (dim - 1, lim, -(1))) {
					state_machine (self.board [row] [(dim - row) + lim], row, (dim - row) + lim);
				}
			}
			for (var lim = 0; lim < dim + 1; lim++) {
				for (var row = 0; row < lim; row++) {
					state_machine (self.board [row] [(dim - lim) + row], row, (dim - lim) + row);
				}
				var state = 'Searching';
			}
			for (var lim of range (dim - 1, -(1), -(1))) {
				for (var col = 0; col < lim; col++) {
					state_machine (self.board [(dim - lim) + col] [col], (dim - lim) + col, col);
				}
				var state = 'Searching';
			}
			for (var lim = 0; lim < dim + 1; lim++) {
				for (var row of range (lim - 1, -(1), -(1))) {
					state_machine (self.board [row] [(dim - lim) + row], row, (dim - lim) + row);
				}
				var state = 'Searching';
			}
			for (var lim of range (dim - 1, -(1), -(1))) {
				for (var col of range (lim - 1, -(1), -(1))) {
					state_machine (self.board [(dim - lim) + col] [col], (dim - lim) + col, col);
				}
				var state = 'Searching';
			}
			if (len (moves) > 0) {
				return list (moves);
			}
			else {
				return [null];
			}
		});},
		get result () {return __get__ (this, function (self, move) {
			var new_board = (function () {
				var __accu0__ = [];
				for (var row of self.board) {
					__accu0__.append (row.__getslice__ (0, null, 1));
				}
				return __accu0__;
			}) ();
			var new_pieces = self.pieces.__getslice__ (0, null, 1);
			if (!(move)) {
				return Reversi.Position (new_board, 3 - self.turn, new_pieces, self.no_moves_count + 1);
			}
			new_board [move [0]] [move [1]] = self.turn;
			var state = 'Encountered';
			var state_machine = function (piece, row, col) {
				if (state == 'Encountered') {
					if (piece == 3 - self.turn) {
						state = 'Encompassing';
					}
					else {
						state = 'Stop';
					}
				}
				else if (state == 'Encompassing') {
					if (piece == self.turn) {
						state = 'Flip';
					}
					else if (piece == 0) {
						state = 'Encountered';
					}
				}
			};
			for (var direction of [[-(1), -(1)], [-(1), 0], [-(1), 1], [0, -(1)], [0, 1], [1, -(1)], [1, 0], [1, 1]]) {
				var new_row = move [0] + direction [0];
				var new_col = move [1] + direction [1];
				var state = 'Encountered';
				while (new_row >= 0 && new_row < len (self.board) && new_col >= 0 && new_col < len (self.board)) {
					state_machine (self.board [new_row] [new_col], new_row, new_col);
					if (state == 'Stop' || state == 'Flip') {
						break;
					}
					new_row += direction [0];
					new_col += direction [1];
				}
				if (state == 'Flip') {
					var new_row = move [0];
					var new_col = move [1];
					while (new_row >= 0 && new_row < len (self.board) && new_col >= 0 && new_col < len (self.board)) {
						new_row += direction [0];
						new_col += direction [1];
						if (self.board [new_row] [new_col] == 3 - self.turn) {
							new_pieces [self.turn] += 1;
							new_pieces [3 - self.turn] -= 1;
							new_board [new_row] [new_col] = self.turn;
						}
						else {
							break;
						}
					}
				}
			}
			new_pieces [0] += 1;
			new_pieces [self.turn] += 1;
			return Reversi.Position (new_board, 3 - self.turn, new_pieces, 0);
		});},
		get next_player () {return __get__ (this, function (self) {
			return self.turn;
		});},
		get is_corner () {return __get__ (this, function (self, move) {
			return move == tuple ([0, 0]) || move == tuple ([0, 7]) || move == tuple ([7, 0]) || move == tuple ([7, 7]);
		});},
		get is_edge () {return __get__ (this, function (self, move) {
			if (!(move)) {
				return false;
			}
			return move [0] == 0 || move [0] == 7 || move [1] == 0 || move [1] == 7;
		});},
		get is_corner_adjacent () {return __get__ (this, function (self, move) {
			return move == tuple ([1, 0]) || move == tuple ([0, 1]) || move == tuple ([6, 0]) || move == tuple ([7, 1]) || move == tuple ([6, 7]) || move == tuple ([7, 6]) || move == tuple ([0, 6]) || move == tuple ([1, 7]) || move == tuple ([1, 1]) || move == tuple ([1, 6]) || move == tuple ([6, 1]) || move == tuple ([6, 6]);
		});},
		get corner_score () {return __get__ (this, function (self) {
			var corner_score = 0;
			for (var corner of [tuple ([0, 0]), tuple ([0, 7]), tuple ([7, 0]), tuple ([7, 7])]) {
				if (self.board [corner [0]] [corner [1]] == 2) {
					corner_score += -(1);
				}
				else if (self.board [corner [0]] [corner [1]] == 1) {
					corner_score += 1;
				}
			}
			return corner_score;
		});},
		get corner_adjacent_score () {return __get__ (this, function (self) {
			var score = 0;
			for (var adjacent of [tuple ([1, 0]), tuple ([0, 1]), tuple ([6, 0]), tuple ([7, 1]), tuple ([6, 7]), tuple ([7, 6]), tuple ([0, 6]), tuple ([1, 7]), tuple ([1, 1]), tuple ([1, 6]), tuple ([6, 1]), tuple ([6, 6])]) {
				if (self.board [adjacent [0]] [adjacent [1]] == 2) {
					score += 1;
				}
				else if (self.board [adjacent [0]] [adjacent [1]] == 1) {
					score += -(1);
				}
			}
			return score;
		});},
		get get_pieces () {return __get__ (this, function (self) {
			return self.pieces;
		});},
		get game_over () {return __get__ (this, function (self) {
			if (self.pieces [0] == 64 || self.no_moves_count > 1) {
				return true;
			}
			return false;
		});},
		get winner () {return __get__ (this, function (self) {
			if (self.pieces [1] > self.pieces [2]) {
				return 1;
			}
			else if (self.pieces [1] < self.pieces [2]) {
				return -(1);
			}
			else {
				return 0;
			}
		});},
		get __str__ () {return __get__ (this, function (self) {
			var to_print = `   `;
			for (var i = 0; i < 8; i++) {
				to_print += ` ${str(i)} `;
			}
			to_print += `<br>`;
			for (var [i, row] of enumerate (self.board)) {
				to_print += ` ${str(i)} `;
				for (var char of row) {
					if (char == 0) {
						to_print += `[ ]`;
					}
					else if (char == 1) {
						to_print += `[●]`;
					}
					else if (char == 2) {
						to_print += `[○]`;
					}
				}
				to_print += '<br>';
			}
			return to_print;
		});},
		get __hash__ () {return __get__ (this, function (self) {
			var to_hash = (function () {
				var __accu0__ = [];
				for (var row of self.board) {
					__accu0__.append (row.__getslice__ (0, null, 1));
				}
				return __accu0__;
			}) ();
			for (var i = 0; i < len (to_hash); i++) {
				to_hash [i] = tuple (to_hash [i]);
			}
			return String((tuple (to_hash)) + self.turn);
		});},
		get __eq__ () {return __get__ (this, function (self, other) {
			if (self.board == other.board && self.turn == other.turn) {
				return true;
			}
			else {
				return false;
			}
		});}
	})
});

export var mcts_strategy = function (iterations, py_default) {
	var pos_table = dict ({});
	pos_table ['total_plays'] = 0;
	var move_table = dict ([['corner', [0, 0]], ['edge', [0, 0]], ['corner_adjacent', [0, 0]], ['center', [0, 0]]]);
	var fxn = function (pos, iterations) {
		if (!__in__(pos.__hash__(), pos_table)) {
			pos_table [pos.__hash__()] = [0, 0];
		}
		for (var i = 0; i < iterations; i++) {
			mcts (pos);
			pos_table ['total_plays'] += 1;
		}
		var player = pos.next_player ();
		var best_move = null;
		if (player == 1) {
			var best_val = -(1000000000);
		}
		else {
			var best_val = 1000000000;
		}
		var moves = pos.legal_moves ();
		for (var move of moves) {
			var child = pos.result (move);
			if (!__in__ (child.__hash__(), pos_table)) {
				continue;
			}
			else {
				var val = pos_table [child.__hash__()] [0] / pos_table [child.__hash__()] [1];
			}
			if (player == 1) {
				if (val > best_val) {
					var best_val = val;
					var best_move = move;
				}
			}
			else if (val < best_val) {
				var best_val = val;
				var best_move = move;
			}
		}
		return best_move;
	};
	var mcts = function (pos) {
		if (pos.game_over ()) {
			var result = pos.winner ();
			if (result == 1) {
				return result;
			}
			if (result == 0) {
				return 0.5;
			}
			if (result == -(1)) {
				return 0;
			}
		}
		var player = pos.next_player ();
		var moves = pos.legal_moves ();
		var best_move = null;
		var best_child = null;
		if (player == 1) {
			var best_UCB = -(1000000000);
		}
		else {
			var best_UCB = 1000000000;
		}
		for (var move of moves) {
			var child = pos.result (move);
			if (!__in__ (child.__hash__(), pos_table)) {
				if (py_default == 'MAST') {
					var value = mast_playout (child);
				}
				else if (py_default == 'Heuristic') {
					var value = static_guided_playout (child);
				}
				else if (py_default == 'Corner') {
					var value = corner_playout (child);
				}
				else if (py_default == 'Random') {
					var value = random_playout (child);
				}
				else if (py_default == 'Multi') {
					var value = 0;
					for (var i = 0; i < 3; i++) {
						value += random_playout (child);
					}
					value /= 3;
				}
				pos_table [child.__hash__()] = [value, 1];
				pos_table [pos.__hash__()] = [pos_table [pos.__hash__()] [0] + value, pos_table [pos.__hash__()] [1] + 1];
				return value;
			}
			else {
				var ucb = UCB (pos_table [child.__hash__()] [0], pos_table [child.__hash__()] [1], player);
				if (player == 1) {
					if (best_UCB < ucb) {
						var best_UCB = ucb;
						var best_move = move;
						var best_child = child;
					}
				}
				else if (best_UCB > ucb) {
					var best_UCB = ucb;
					var best_move = move;
					var best_child = child;
				}
			}
		}
		var result = mcts (best_child);
		update_move_table (pos, best_move, result);
		pos_table [pos.__hash__()] = [pos_table [pos.__hash__()] [0] + result, pos_table [pos.__hash__()] [1] + 1];
		return result;
	};
	var UCB = function (wins, plays, player) {
		if (player == 1) {
			return 2 * (wins / plays) + math.sqrt ((2 * math.log (pos_table ['total_plays'])) / plays);
		}
		else {
			return 2 * (wins / plays) - math.sqrt ((2 * math.log (pos_table ['total_plays'])) / plays);
		}
	};
	var update_move_table = function (pos, move, value) {
		if (!(move)) {
			return ;
		}
		if (pos.is_corner (move)) {
			move_table ['corner'] [0] += value;
			move_table ['corner'] [1] += 1;
		}
		else if (pos.is_corner_adjacent (move)) {
			move_table ['corner_adjacent'] [0] += value;
			move_table ['corner_adjacent'] [1] += 1;
		}
		else if (pos.is_edge (move)) {
			move_table ['edge'] [0] += value;
			move_table ['edge'] [1] += 1;
		}
		else {
			move_table ['center'] [0] += value;
			move_table ['center'] [1] += 1;
		}
	};
	var random_playout = function (pos) {
		if (pos.game_over ()) {
			var result = pos.winner ();
			if (result == 1) {
				return result;
			}
			if (result == 0) {
				return 0.5;
			}
			if (result == -(1)) {
				return 0;
			}
		}
		var moves = pos.legal_moves ();
		var random_move = moves [random.choice(moves)];
		return random_playout (pos.result (random_move));
	};
	var static_guided_playout = function (pos) {
		if (pos.game_over ()) {
			var result = pos.winner ();
			if (result == 1) {
				return result;
			}
			if (result == 0) {
				return 0.5;
			}
			if (result == -(1)) {
				return 0;
			}
		}
		var moves = pos.legal_moves ();
		var best = null;
		for (var move of moves) {
			if (pos.is_corner (move)) {
				var best = move;
				break;
			}
			else if (pos.is_edge (move)) {
				var best = move;
			}
		}
		if (best) {
			return static_guided_playout (pos.result (best));
		}
		else {
			var random_move = moves [random.choice(moves)];
			return static_guided_playout (pos.result (random_move));
		}
	};
	var mast_playout = function (pos) {
		if (pos.game_over ()) {
			var result = pos.winner ();
			if (result == 1) {
				return result;
			}
			if (result == 0) {
				return 0.5;
			}
			if (result == -(1)) {
				return 0;
			}
		}
		var moves = pos.legal_moves ();
		var best_types = [];
		for (var key of move_table) {
			if (move_table [key] [1] > 0) {
				best_types.append ([key, move_table [key] [0] / move_table [key] [1]]);
			}
		}
		if (pos.next_player () == 1) {
			best_types.py_sort (__kwargtrans__ ({key: (function __lambda__ (category) {
				return category [1];
			}), reverse: true}));
		}
		else {
			best_types.py_sort (__kwargtrans__ ({key: (function __lambda__ (category) {
				return category [1];
			})}));
		}
		var categorized_moves = dict ([['corner', []], ['corner_adjacent', []], ['edge', []], ['center', []]]);
		for (var move of moves) {
			if (pos.is_corner (move)) {
				categorized_moves ['corner'].append (move);
			}
			else if (pos.is_corner_adjacent (move)) {
				categorized_moves ['corner_adjacent'].append (move);
			}
			else if (pos.is_edge (move)) {
				categorized_moves ['edge'].append (move);
			}
			else {
				categorized_moves ['center'].append (move);
			}
		}
		for (var best_type of best_types) {
			var move_list = categorized_moves [best_type [0]];
			if (len (move_list) > 0) {
				return mast_playout (pos.result (move_list [random.randrange (len (move_list))]));
			}
		}
		return random_playout (pos.result (moves [random.choice(moves)]));
	};
	var corner_playout = function (pos) {
		if (pos.game_over ()) {
			var result = pos.winner ();
			if (result == 1) {
				return result;
			}
			if (result == 0) {
				return 0.5;
			}
			if (result == -(1)) {
				return 0;
			}
		}
		var moves = pos.legal_moves ();
		for (var move of moves) {
			if (pos.is_corner (move)) {
				return corner_playout (pos.result (move));
			}
		}
		return corner_playout (pos.result (moves [random.choice(moves)]));
	};
	return fxn;
};

export var turn = function(position) {
	var ai = ai_strat ();

	if (position.game_over()) {
		document.getElementById("moveVal").value = "";
		document.getElementById("available").innerText = "";
		document.getElementById("board").innerText = position.__str__();
		var pieces = position.get_pieces ();
		document.getElementById("pieces").innerText = "Computer's Pieces (Filled): " + pieces [1] + ', Your pieces (Hollow): ' + pieces [2];
		if (position.winner () == 0) {
			document.getElementById("available").innerText = 'Draw!';
		}
		else if (position.winner () == 1) {
			document.getElementById("available").innerText = 'Aww you lost.. :(';
		}
		else {
			document.getElementById("available").innerText = 'You won!';
		}
	}

	document.getElementById("board").innerHTML = position.__str__();
	var pieces = position.get_pieces ();
	document.getElementById("pieces").innerText = "Computer's Pieces (Unfilled): " + pieces [1] + ', Your pieces (Filled): ' + pieces [2];

	if (position.next_player () - 1 == 1) {
		document.getElementById("move").innerText = 'Computer Move...';
		var move = ai (position, iterations);
		turn(position.result(move));
	}
	else {
		document.getElementById("move").innerHTML = 'Your Move... (Moves indicate where to place your next piece)<br>Moves are formatted as: row number, column number';
		current_moves = position.legal_moves ();
		current_position = position;
		for (let i = 0; i < current_moves.length; i++) {
			document.getElementById("available").innerText = document.getElementById("available").innerText + i + ': ' + current_moves[i] + '\n';
		}
	}
};

export var handleMove = function() {
	const index = document.getElementById("moveVal").value; 
	if(!(Number.isInteger (parseInt(index))) || parseInt (index) >= current_moves.length || parseInt (index) < 0) {
		return;
	}
	else {
		var move = current_moves [int (index)];
		document.getElementById("moveVal").value = "";
		document.getElementById("available").innerText = "";
		turn(current_position.result(move));
	}
};

export var human_game = function () {
	var board = Reversi (8);
	var position = board.initial_position ();
	turn(position);
};

human_game ((function __lambda__ () {
	return mcts_strategy (500, 'Corner');
}), 500);

//# sourceMappingURL=game.map