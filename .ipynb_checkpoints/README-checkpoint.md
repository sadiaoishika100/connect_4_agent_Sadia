# Connect 4 Agent Assignment

In this project, you will be creating your own AI agent to play Connect 4. Your agent will be pitted against other students to determine who is the best agent.

## Your Task

Your goal is to implement the `StudentAgent` class located in `agents.py`. Your agent will compete against other agents, including a baseline `HeuristicAgent` and potentially your classmates' agents in a tournament setting. 

Currently, `StudentAgent` just picks a random valid move. You'll need to write Python code inside the `get_action` method to return the best possible column index to play your piece. 

In addition to your code, you must fill out the `about_agent.md` file explaining your agent's overall strategy and how your custom heuristic works. **LLM Policy:** You are allowed to use LLMs (like ChatGPT, Claude, etc.) to brainstorm ideas or understand algorithmic concepts. However, **all code must be written by you**, you must fully understand everything your code is doing, and **all writing in `about_agent.md` must be entirely your own words.**

### Time Limits

Your agent must return an action within the allotted `time_limit` (e.g., 5 seconds depending on the tournament configuration). If your agent takes too long, it will be forcefully terminated and you will **forfeit** the game. 

You should use the `time` module to track how long your agent has been thinking to ensure you don't stall:
```python
import time

def get_action(self, game):
    start_time = time.time()
    # Keep checking time.time() - start_time to avoid exceeding self.time_limit
    ...
```

## Testing Your Agent

You can test your agent by running `python3 game.py` in your terminal. By default, `game.py` is configured to run a 3-game tournament between your `StudentAgent` and the baseline `HeuristicAgent`. To understand your competition, you can test against:
- **`RandomAgent`**: Picks a legal move completely at random.
- **`HeuristicAgent`**: A very basic (and frankly, quite bad) agent that only looks 1 step ahead to block immediate threats or take immediate wins. 

If your agent is working properly with even a small search depth, it should consistently crush the `HeuristicAgent`. Feel free to open `game.py` and modify the tournament matchups to test against `RandomAgent`, `HumanAgent` (to play against your code yourself!), or even an older saved version of your own agent to ensure you are making progress.

## Strategies and Suggestions

Here are some core AI concepts you should consider incorporating to make your agent highly competitive:

1. **Minimax Algorithm**: At the heart of most adversarial board game AIs is the Minimax algorithm. Use it to explore the game tree by assuming your opponent will also play optimally.
2. **Alpha-Beta Pruning**: Exploring all possible moves is too slow. Implement Alpha-Beta pruning to safely skip over branches of the game tree that can't possibly influence the final decision. This allows your agent to look much further ahead in the same amount of time.
3. **Depth-Limited Search & Heuristic Evaluation**: You won't be able to search the entire game tree down to a leaf node (a win/loss/draw) in the middle of the game because the search space is far too large. Instead, search down to a specific depth limit, and then use a strong heuristic evaluation function to accurately score those non-terminal board states.
4. **Iterative Deepening**: Instead of searching to a fixed depth, start by searching to depth 1, then depth 2, then depth 3, and so on. If you run out of time during depth 4, you can safely fall back to the best move you found at depth 3. This is the optimal way to utilize your remaining time well.
5. **Efficient State Management**: Instead of creating a brand new game state at every node inside your search tree by calling `game.copy()` (which is computationally expensive), modify the existing board state directly! Use `game.apply_action(action)` to step forward, evaluate, and then explicitly call `game.undo_action()` to revert the step. 
6. **Symmetry/Board Caching**: Connect 4 game states are symmetrical down the middle. You can cut down your search space massively by caching the evaluations of boards you've already seen, recognizing that a mirrored version of a known board produces the exact same evaluation.
7. **Research**: Don't stop here! Feel free to look online for any other ideas regarding Connect 4 algorithms. You might find inspiration for opening maneuvers, custom bitboard data structures, or advanced evaluation metrics.

## Libraries

### Suggested Internal Python Libraries
These are built directly into Python and require no installation:
- `math`, `time`, `functools.lru_cache`, `collections`, `itertools`, `random`

### Allowed External Libraries (Require Installation)
You are permitted to use the following external libraries to accelerate your search or manage arrays:
- `numpy`, `scipy`, `numba`, `pytorch`, `tensorflow`, `bitarray`, `gmpy2`, `joblib`

*Note: If there is another library you find interesting and would like to use, please email me to suggest it!*

### C Extensions
If you really want to maximize the depth of your search tree within the time limit, suggest looking into how to write C code that a Python file can run (for example, using C-extensions). Processing your board evaluations in native C can yield massive speedups!

Good luck!
