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

MAX_SCORE = float("inf")

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        curX, curY = newPos

        foodNum = successorGameState.getNumFood()
        "*** YOUR CODE HERE ***"
        if currentGameState.isLose():
            return -float("inf")
        elif currentGameState.isWin():
            return float("inf")
        gameStateScore = currentGameState.getScore()
        foodDistance = float("inf")
        for x in range(newFood.width):
            for y in range(newFood.height):
                distance = abs(x - curX) + abs(y - curY)
                if newFood[x][y] and foodDistance > distance:
                    foodDistance = distance
        ghostDistance = float("inf")
        for (ghostState, newScaredTime) in zip(newGhostStates, newScaredTimes):
            distance = util.manhattanDistance(ghostState.getPosition(), newPos)
            if newScaredTime == 0 and ghostDistance > distance:
                ghostDistance = distance
        alpha = -20
        beta = -1
        if ghostDistance > 3:
            awayWithGhost = 400
        else :
            awayWithGhost = 100 * ghostDistance
        if foodDistance == float("inf"):
            # this action will take the last food
            beta = 1
        score = gameStateScore + alpha * foodNum + beta * foodDistance + awayWithGhost
        return score

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        actionLeft = gameState.getLegalActions(0)
        bestScore = -MAX_SCORE
        bestAction = None
        for action in actionLeft:
            successorGameState = gameState.generateSuccessor(0, action)
            score = self.minimax(successorGameState, 0, 1)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

    def minimax(self, gameState, depth, agentIndex):
        tab = ""
        for i in range(depth):
            tab += "\t"
        if gameState.isWin() or gameState.isLose() or depth >= self.depth and (gameState.getNumAgents() == agentIndex + 1 or agentIndex == 0):
            print tab + "terminal depth:" + str(depth) + " agent:" + str(agentIndex) + " score:" + str(self.evaluationFunction(gameState))
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            bestScore = -MAX_SCORE
            for action in legalActions:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                score = self.minimax(successorGameState, depth, 1)
                bestScore = max(bestScore, score)
            print tab + "depth:" + str(depth) + " agent:" + str(agentIndex) + " score:" + str(bestScore)
            return bestScore
        else:
            bestScore = MAX_SCORE
            for action in legalActions:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                if (agentIndex + 1) % gameState.getNumAgents() == 0:
                    score = self.minimax(successorGameState, depth + 1, 0)
                else:
                    score = self.minimax(successorGameState, depth, agentIndex + 1)
                bestScore = min(bestScore, score)
            print tab + "depth:" + str(depth) + " agent:" + str(agentIndex) + " score:" + str(bestScore)
            return bestScore


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        actionLeft = gameState.getLegalActions(0)
        bestScore = -MAX_SCORE
        bestAction = None
        alpha = -MAX_SCORE
        beta = MAX_SCORE
        for action in actionLeft:
            successorGameState = gameState.generateSuccessor(0, action)
            score = self.minimax(successorGameState, 0, 1, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(bestScore, alpha)
        return bestAction

    def minimax(self, gameState, depth, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth >= self.depth and (gameState.getNumAgents() == agentIndex + 1 or agentIndex == 0):
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            bestScore = -MAX_SCORE
            for action in legalActions:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                score = self.minimax(successorGameState, depth, 1, alpha, beta)
                bestScore = max(bestScore, score)
                alpha = max(bestScore, alpha)
                if beta <= alpha:
                    break
            return bestScore
        else:
            bestScore = MAX_SCORE
            for action in legalActions:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                if (agentIndex + 1) % gameState.getNumAgents() == 0:
                    score = self.minimax(successorGameState, depth + 1, 0, alpha, beta)
                else:
                    score = self.minimax(successorGameState, depth, agentIndex + 1, alpha, beta)
                bestScore = min(bestScore, score)
                beta = min(bestScore, beta)
                if beta <= alpha:
                    break
            return bestScore

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        actionLeft = gameState.getLegalActions(0)
        bestScore = -MAX_SCORE
        bestAction = None
        for action in actionLeft:
            successorGameState = gameState.generateSuccessor(0, action)
            score = self.expectimax(successorGameState, 0, 1)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

    def expectimax(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose() or depth >= self.depth and (gameState.getNumAgents() == agentIndex + 1 or agentIndex == 0):
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            bestScore = -MAX_SCORE
            for action in legalActions:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                score = self.expectimax(successorGameState, depth, 1)
                bestScore = max(bestScore, score)
            return bestScore
        else:
            sumScore = 0
            for action in legalActions:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                if (agentIndex + 1) % gameState.getNumAgents() == 0:
                    sumScore += self.expectimax(successorGameState, depth + 1, 0)
                else:
                    sumScore += self.expectimax(successorGameState, depth, agentIndex + 1)
            averageScore = sumScore / float(len(legalActions))
            return averageScore

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newCapsules = currentGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    curX, curY = newPos

    foodNum = currentGameState.getNumFood()
    "*** YOUR CODE HERE ***"
    if currentGameState.isLose():
        return -float("inf")
    elif currentGameState.isWin():
        return float("inf")
    gameStateScore = currentGameState.getScore()
    foodDistance = float("inf")
    for x in range(newFood.width):
        for y in range(newFood.height):
            distance = abs(x - curX) + abs(y - curY)
            if newFood[x][y] and foodDistance > distance:
                foodDistance = distance
    ghostDistance = float("inf")
    for (ghostState, newScaredTime) in zip(newGhostStates, newScaredTimes):
        distance = util.manhattanDistance(ghostState.getPosition(), newPos)
        if newScaredTime == 0 and ghostDistance > distance:
            ghostDistance = distance
    alpha = -20
    beta = -1
    if ghostDistance > 3:
        awayWithGhost = 400
    else:
        awayWithGhost = 100 * ghostDistance
    if foodDistance == float("inf"):
        # this action will take the last food
        beta = 1
    score = gameStateScore + alpha * foodNum + beta * foodDistance + awayWithGhost
    return score

# Abbreviation
better = betterEvaluationFunction

