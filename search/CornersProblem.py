import search
from game import Directions, Actions


class CornersProblem(search.SearchProblem):
    def __init__(self, startingGameState):
        """
        Initializează problema cu pereții, poziția de start a lui Pacman și colțurile.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height - 2, self.walls.width - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0  # DO NOT CHANGE

    def getStartState(self):
        return (self.startingPosition, set())

    def isGoalState(self, state):
        position, visited_corners = state
        return len(visited_corners) == len(self.corners)

    def getSuccessors(self, state):
        successors = []
        position, visited_corners = state
        x, y = position

        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)

            if not self.walls[nextx][nexty]:
                next_position = (nextx, nexty)
                next_visited_corners = set(visited_corners)

                if next_position in self.corners:
                    next_visited_corners.add(next_position)

                successors.append(((next_position, next_visited_corners), action, 1))

        self._expanded += 1  # DO NOT CHANGE
        return successors

    def getCostOfActions(self, actions):
        if actions == None:
            return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
        return len(actions)
