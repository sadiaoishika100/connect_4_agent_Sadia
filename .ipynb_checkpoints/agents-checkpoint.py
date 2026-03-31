import abc
import random
import time
from functools import lru_cache

class Agent(abc.ABC):
    def __init__(self, name, time_limit=1.0):
        self.name = name
        self.time_limit = time_limit

    @abc.abstractmethod
    def get_action(self, game):
        pass

class HumanAgent(Agent):
    def _is_integer(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def get_action(self, game):
        print("Pick a move from the following legal moves via index or move name:")
        legal_moves = list(enumerate(game.actions()))
        for idx, move in legal_moves:
            print(f"{idx}: {move}")
        while True:
            choice = input("Enter your chosen move: ")
            if self._is_integer(choice):
                choice = int(choice)
                if 0 <= choice < len(legal_moves):
                    return legal_moves[choice][1]
                else:
                    print("Invalid index. Please try again.")
            else:
                for idx, move in legal_moves:
                    if str(move) == choice:
                        return move
                print("Invalid move name. Please try again.")

class RandomAgent(Agent):
    def get_action(self, game):
        valid_locations = game.actions()
        return random.choice(valid_locations)

def get_max_connected(game, r, c, player):
    game.board[r][c] = player
    max_count = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, game.connect_length):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < game.height and 0 <= nc < game.width and game.board[nr][nc] == player:
                count += 1
            else:
                break
        for i in range(1, game.connect_length):
            nr, nc = r - dr * i, c - dc * i
            if 0 <= nr < game.height and 0 <= nc < game.width and game.board[nr][nc] == player:
                count += 1
            else:
                break
        if count > max_count:
            max_count = count
    game.board[r][c] = 0
    return max_count

class HeuristicAgent(Agent):
    def get_action(self, game):
        valid_locations = game.actions()
        if not valid_locations:
            return None
            
        player = game.to_move()
        opponent = -player
        
        block_3 = []
        block_2 = []
        grow_3 = []
        grow_2 = []
        
        for col in valid_locations:
            # Find the row where the piece would land
            r = game.height - 1
            while r >= 0 and game.board[r][col] != 0:
                r -= 1
                
            # Check opponent's potential connections if they played here
            opp_connected = get_max_connected(game, r, col, opponent)
            # Check own potential connections if playing here
            own_connected = get_max_connected(game, r, col, player)
            
            if opp_connected >= 4:
                block_3.append(col)
            elif opp_connected >= 3:
                block_2.append(col)
            elif own_connected >= 4:
                grow_3.append(col)
            elif own_connected >= 3:
                grow_2.append(col)
                
        # Return based on priority buckets
        if block_3:
            return random.choice(block_3)
        if block_2:
            return random.choice(block_2)
        if grow_3:
            return random.choice(grow_3)
        if grow_2:
            return random.choice(grow_2)
            
        return random.choice(valid_locations)

class StudentAgent(Agent):
    def get_action(self, game):
        self.start_time = time.time()
        # 0.5s time limit
        self.deadline = self.time_limit - 0.5
        
        valid_moves = game.actions()
        if not valid_moves:
            return None

        # moves to check the center first. Improves Alpha-Beta pruning.
        valid_moves.sort(key=lambda x: abs(x - game.width // 2))
        
        best_move_so_far = valid_moves[0]
        player = game.to_move()

        # Iterative Deepening code before time runs out
        for depth in range(1, 100):
            try:
                move = self.alpha_beta_search(game, depth, player, valid_moves)
                if move is not None:
                    best_move_so_far = move
            except TimeoutError:
                break
                
        return best_move_so_far

    def alpha_beta_search(self, game, depth, player, valid_moves):
        best_val = -float('inf')
        best_move = None
        alpha = -float('inf')
        beta = float('inf')

        for move in valid_moves:
            if self.is_time_up(): raise TimeoutError()
            game.apply_action(move)
            val = self.min_value(game, depth - 1, alpha, beta, player)
            game.undo_action()
            
            if val > best_val:
                best_val = val
                best_move = move
            alpha = max(alpha, val)
        
        return best_move

    def max_value(self, game, depth, alpha, beta, player):
        if self.is_time_up(): raise TimeoutError()
        if game.is_terminal() or depth == 0:
            return self.evaluate(game, player)

        v = -float('inf')
        for move in game.actions():
            game.apply_action(move)
            v = max(v, self.min_value(game, depth - 1, alpha, beta, player))
            game.undo_action()
            if v >= beta: return v
            alpha = max(alpha, v)
        return v

    def min_value(self, game, depth, alpha, beta, player):
        if self.is_time_up(): raise TimeoutError()
        if game.is_terminal() or depth == 0:
            return self.evaluate(game, player)

        v = float('inf')
        for move in game.actions():
            game.apply_action(move)
            v = min(v, self.max_value(game, depth - 1, alpha, beta, player))
            game.undo_action()
            if v <= alpha: return v
            beta = min(beta, v)
        return v

    def is_time_up(self):
        return (time.time() - self.start_time) > self.deadline

    def evaluate(self, game, player):
        if game.is_win():
            return 1000000 if game.to_move() != player else -1000000
        
        if len(game.actions()) == 0:
            return 0

        score = 0
        center_col = game.width // 2
        for r in range(game.height):
            if game.board[r][center_col] == player:
                score += 5
            elif game.board[r][center_col] == -player:
                score -= 5
        
        return score
