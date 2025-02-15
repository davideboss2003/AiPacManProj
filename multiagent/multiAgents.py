# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Inițializăm scorul
        score = successorGameState.getScore()

        # 1. Distanța până la cel mai apropiat aliment
        food_positions = newFood.asList()
        if food_positions:
            min_food_distance = min(util.manhattanDistance(newPos, food) for food in food_positions)
            score += 10 / min_food_distance  # Invers proporțional: mai aproape = mai bine

        # 2. Evitarea fantomelor
        for ghostState, scaredTime in zip(newGhostStates, newScaredTimes):
            ghost_position = ghostState.getPosition()
            ghost_distance = util.manhattanDistance(newPos, ghost_position)

            if scaredTime > 0:  # Fantomă speriată (poate fi mâncată)
                score += 200 / (ghost_distance + 1)
            else:  # Fantomă activă (trebuie evitată)
                if ghost_distance < 2:  # Risc de coliziune
                    score -= 500
                else:
                    score -= 10 / ghost_distance  # Penalizare invers proporțională

        # 3. Evitarea "STOP"
        if action == Directions.STOP:
            score -= 50

        return score


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(state, depth, agentIndex):
            # 1. Dacă jocul este câștigat/pierdut sau adâncimea a fost atinsă
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # 2. Dacă este rândul lui Pacman (Maximizer)
            if agentIndex == 0:
                return maxValue(state, depth)

            # 3. Dacă este rândul unei fantome (Minimizer)
            return minValue(state, depth, agentIndex)

        def maxValue(state, depth):
            v = float("-inf")
            actions = state.getLegalActions(0)
            for action in actions:
                successor = state.generateSuccessor(0, action)
                v = max(v, minimax(successor, depth, 1))  # Fantoma 1 urmează
            return v

        def minValue(state, depth, agentIndex):
            v = float("inf")
            actions = state.getLegalActions(agentIndex)
            numAgents = state.getNumAgents()
            for action in actions:
                successor = state.generateSuccessor(agentIndex, action)
                if agentIndex == numAgents - 1:  # Ultima fantomă
                    v = min(v, minimax(successor, depth + 1, 0))  # Trecem la Pacman
                else:  # Următoarea fantomă
                    v = min(v, minimax(successor, depth, agentIndex + 1))
            return v

            # Găsim cea mai bună acțiune pentru Pacman

        bestAction = None
        bestValue = float("-inf")
        actions = gameState.getLegalActions(0)
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            value = minimax(successor, 0, 1)  # Fantoma 1 urmează
            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        def alphaBeta(state, depth, agentIndex, alpha, beta):
            # 1. Condiție de oprire (joc câștigat/pierdut sau adâncime maximă atinsă)
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # 2. Pacman (Maximizer)
            if agentIndex == 0:
                return maxValue(state, depth, alpha, beta)

            # 3. Fantome (Minimizer)
            return minValue(state, depth, agentIndex, alpha, beta)

        def maxValue(state, depth, alpha, beta):
            v = float("-inf")
            actions = state.getLegalActions(0)
            for action in actions:
                successor = state.generateSuccessor(0, action)
                v = max(v, alphaBeta(successor, depth, 1, alpha, beta))
                if v > beta:  # Pruning
                    return v
                alpha = max(alpha, v)
            return v

        def minValue(state, depth, agentIndex, alpha, beta):
            v = float("inf")
            actions = state.getLegalActions(agentIndex)
            numAgents = state.getNumAgents()
            for action in actions:
                successor = state.generateSuccessor(agentIndex, action)
                if agentIndex == numAgents - 1:  # Ultima fantomă
                    v = min(v, alphaBeta(successor, depth + 1, 0, alpha, beta))
                else:  # Următoarea fantomă
                    v = min(v, alphaBeta(successor, depth, agentIndex + 1, alpha, beta))
                if v < alpha:  # Pruning
                    return v
                beta = min(beta, v)
            return v

        # Selectează cea mai bună acțiune pentru Pacman
        bestAction = None
        alpha = float("-inf")
        beta = float("inf")
        bestValue = float("-inf")

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = alphaBeta(successor, 0, 1, alpha, beta)
            if value > bestValue:
                bestValue = value
                bestAction = action
            alpha = max(alpha, bestValue)

        return bestAction
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
