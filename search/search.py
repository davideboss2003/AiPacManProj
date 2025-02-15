# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))


    stack = util.Stack()
    start_state = problem.getStartState() # la fel obtinem starea de start


    stack.push((start_state, []))
    visited = set()

    # explorm nodurile
    while not stack.isEmpty():
        state, path = stack.pop()


        if problem.isGoalState(state):
            return path


        if state not in visited:
            visited.add(state)

            successors = problem.getSuccessors(state)
            for successor, action, _ in reversed(successors):
                if successor not in visited:
                    stack.push((successor, path + [action]))

    # If no solution is found, return an empty path
    return []
    util.raiseNotDefined()







def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    start_state = problem.getStartState()  #lunam starea lui pacman de unde incepe in labirint

    # facem enqueue la start state si emply poath
    queue.push((start_state, []))  #start state e pozitia curenta si [] calea parcursa pana acum
    visited = set() #tine evid starilor deja vizitate

    while not queue.isEmpty():
        # Dequeue  current state si  pathu din queue
        state, path = queue.pop()

        # verificam daca starea curebta e tinta(unde trebuie sa ajunga Pacman) returnam calea care ajunge acolo
        if problem.isGoalState(state):
            return path

        # marcam starea ca vizitata daca nu a fost vizitata
        if state not in visited:
            visited.add(state)

            # Enqueue successors with updated paths
            # successor e starea urmatoare  si action miscare necesara ot a ajunge acolo
            for successor, action, _ in problem.getSuccessors(state):
                if successor not in visited:
                    queue.push((successor, path + [action]))

    # If no solution is found, return an empty path
    return []






    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # Initialize the priority queue with the start state and a cost of 0
    priority_queue = util.PriorityQueue()
    start_state = problem.getStartState()

    # Push the start state with a cost of 0
    priority_queue.push((start_state, []), 0)
    visited = {}

    while not priority_queue.isEmpty():
        # Pop the node with the lowest cumulative cost
        state, path = priority_queue.pop()
        cost = problem.getCostOfActions(path)

        # If we reached the goal state, return the path
        if problem.isGoalState(state):
            return path

        # Check if this state has been visited with a lower cost before
        if state not in visited or visited[state] > cost:
            visited[state] = cost

            # Explore successors with updated paths and costs
            for successor, action, step_cost in problem.getSuccessors(state):
                new_cost = cost + step_cost
                if successor not in visited or visited[successor] > new_cost:
                    priority_queue.push((successor, path + [action]), new_cost)

    # If no solution is found, return an empty path
    return []
















    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    Funcția euristică trebuie să ia două argumente: o stare (state) și problema de căutare (problem).
    Codul tău primește heuristic ca argument cu valoare implicită nullHeuristic
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:

    # Inițializează coada de priorități și adaugă starea de start
    priority_queue = util.PriorityQueue()
    start_state = problem.getStartState()

    # Starea de start are cost 0 și valoarea euristicii aplicate la start_state
    priority_queue.push((start_state, []), 0 + heuristic(start_state, problem))
    visited = {}

    while not priority_queue.isEmpty():
        # Extrage nodul cu cel mai mic cost f(n) = g(n) + h(n)
        state, path = priority_queue.pop()
        cost = problem.getCostOfActions(path)

        # Verificăm dacă am ajuns la starea obiectiv
        if problem.isGoalState(state):
            return path

        # Verifică dacă nodul curent a fost vizitat cu un cost mai mic anterior
        if state not in visited or visited[state] > cost:
            visited[state] = cost

            # Extinde succesorii cu costul actualizat și euristica
            for successor, action, step_cost in problem.getSuccessors(state):
                new_cost = cost + step_cost
                priority = new_cost + heuristic(successor, problem)
                if successor not in visited or visited[successor] > new_cost:
                    priority_queue.push((successor, path + [action]), priority)

    # Dacă nu găsim o soluție, returnăm o listă goală
    return []



    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
