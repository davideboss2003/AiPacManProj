# Pacman AI Project

This project implements **AI search algorithms** for solving various Pacman navigation problems. It includes **uninformed search strategies** like **DFS, BFS, UCS**, and **informed search** using **A* with heuristics**. Additionally, it explores **adversarial search** with **Minimax and Alpha-Beta Pruning**, allowing Pacman to compete against ghosts.

## Features
- **Pathfinding Algorithms**: Implements **DFS, BFS, UCS, and A*** to guide Pacman to food efficiently.
- **Heuristic Optimization**: Custom heuristics improve **A* and Corners Problem performance**.
- **Adversarial AI**: Pacman competes against ghosts using **Minimax and Alpha-Beta Pruning**.
- **Multi-Agent Systems**: Reflex-based and strategic agents for handling dynamic environments.

## Implemented Algorithms
### Search-Based Agents
| Algorithm | Description |
|-----------|-------------|
| **DFS (Depth-First Search)** | Explores paths deeply before backtracking. Not optimal but finds a solution. |
| **BFS (Breadth-First Search)** | Explores all nodes at a given depth first, guaranteeing the shortest path. |
| **UCS (Uniform Cost Search)** | Expands the least-cost path first, ensuring the optimal solution. |
| **A* Search** | Uses a heuristic (e.g., Manhattan Distance) to improve efficiency. |

### Adversarial Search (Multi-Agent Pacman)
| Algorithm | Description |
|-----------|-------------|
| **Minimax** | Pacman maximizes score, ghosts minimize it. Explores entire game tree. |
| **Alpha-Beta Pruning** | Optimized Minimax, skipping irrelevant branches to improve efficiency. |
| **Reflex Agent** | Uses simple rules to decide the best move based on immediate surroundings. |

