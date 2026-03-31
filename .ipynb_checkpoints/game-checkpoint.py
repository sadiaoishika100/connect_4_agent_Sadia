import time
import random
import multiprocessing
from connect4 import ConnectFour
from agents import HumanAgent, RandomAgent, HeuristicAgent, StudentAgent

def _get_action_worker(agent, game, queue):
    """Worker process function to get the agent's action."""
    action = agent.get_action(game)
    queue.put(action)

def play_game(agent_1, agent_2, render=True):
    b = ConnectFour()
    agents = {1: agent_1, -1: agent_2}
    
    while not b.is_terminal():
        if render:
            print(b)
            print(f"\nPlayer {b.to_move()}'s turn ({agents[b.to_move()].name})")
        
        current_agent = agents[b.to_move()]
        game_copy = b.copy()
        
        if isinstance(current_agent, HumanAgent):
            action = current_agent.get_action(game_copy)
            b.result(action)
        else:
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=_get_action_worker, args=(current_agent, game_copy, q))
            
            start_time = time.time()
            p.start()
            
            # Wait for the agent to finish or the time limit to expire
            p.join(current_agent.time_limit)
            
            if p.is_alive():
                # The process is still running after timeout, so terminate it
                p.terminate()
                p.join()
                time_taken = time.time() - start_time
                print(f"Player {b.to_move()} ({current_agent.name}) exceeded the time limit! Terminated after {time_taken:.3f}s. Limit was {current_agent.time_limit}s.")
                print(f"Player {-b.to_move()} wins by forfeit!")
                return -b.to_move()
            
            if not q.empty():
                action = q.get()
            else:
                # If the queue is empty and the process is dead, it likely crashed
                print(f"Player {b.to_move()} ({current_agent.name}) failed or crashed.")
                print(f"Player {-b.to_move()} wins by forfeit!")
                return -b.to_move()
                
            b.result(action)
        
        if render:
            print(f"Action chosen: Column {action}\n")
    
    if render:
        print(b)
        if b.is_win():
            print(f"Player {-b.to_move()} wins!")
        else:
            print("It's a draw!")
    
    if b.is_win():
        return -b.to_move()
    return 0

def run_tournament(p1_class, p2_class, time_limit=5.0):
    print("=== 3 Game Tournament ===")
    
    p1 = p1_class("Player 1", time_limit=time_limit)
    p2 = p2_class("Player 2", time_limit=time_limit)
    
    score_p1 = 0
    score_p2 = 0
    draws = 0
    
    # Game 1: p1 goes first
    print("\n--- Game 1: Player 1 goes first ---")
    result = play_game(p1, p2, render=True)
    if result == 1:
        score_p1 += 1
    elif result == -1:
        score_p2 += 1
    else:
        draws += 1
        
    # Game 2: p2 goes first
    print("\n--- Game 2: Player 2 goes first ---")
    result = play_game(p2, p1, render=True)
    if result == -1:
        score_p1 += 1
    elif result == 1:
        score_p2 += 1
    else:
        draws += 1
        
    # Game 3: Random person goes first
    print("\n--- Game 3: Random player goes first ---")
    if random.choice([True, False]):
        print("Player 1 was randomly chosen to go first.")
        result = play_game(p1, p2, render=True)
        if result == 1:
            score_p1 += 1
        elif result == -1:
            score_p2 += 1
        else:
            draws += 1
    else:
        print("Player 2 was randomly chosen to go first.")
        result = play_game(p2, p1, render=True)
        if result == -1:
            score_p1 += 1
        elif result == 1:
            score_p2 += 1
        else:
            draws += 1
            
    print("\n=== Tournament Results ===")
    print(f"Player 1 ({p1.name}): {score_p1} wins")
    print(f"Player 2 ({p2.name}): {score_p2} wins")
    print(f"Draws: {draws}")

if __name__ == "__main__":
    # Ensure macOS spawn start method works correctly by guarding execution
    multiprocessing.set_start_method('spawn', force=True)
    # Example tournament
    run_tournament(StudentAgent, HumanAgent, time_limit=1.0)
