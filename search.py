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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    # Stack omdat Expands the search tree following the deepest node → LIFO queue
    stackDFS = util.Stack()
    stackDFS.push((problem.getStartState(), []))
    visited = set() # set omdat O(1), [] zou O(n) zijn om iets te vinden

    while not stackDFS.isEmpty():
        state, path = stackDFS.pop() # state voor huidige op te halen en path voor pacman te bewegen

        if problem.isGoalState(state): # voor beweging pacman te returnen
            return path

        if state not in visited:
            visited.add(state)
            for node in problem.getSuccessors(state):
                if node[0] not in visited:
                    stackDFS.push((node[0], path + [node[1]]))

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queueBFS = util.Queue() # queue omdat Expands the search tree following the shallowest node → FIFO queue
    queueBFS.push((problem.getStartState(), []))
    visited = set()  # set omdat O(1), [] zou O(n) zijn om iets te vinden

    while not queueBFS.isEmpty():
        state, path = queueBFS.pop()  # state voor huidige op te halen en path voor pacman te bewegen

        if problem.isGoalState(state):  # voor beweging pacman te returnen
            return path

        for node in problem.getSuccessors(state):
            if node[0] not in visited:
                visited.add(state) # niet meer zelfde state meerdere keer bij verschillende paths
                queueBFS.push((node[0], path + [node[1]]))

    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    prioQueueUCS = util.PriorityQueue() # Priority Queue omdat UCS de knoop met de laagste totale padkosten als eerste uitbreidt
    prioQueueUCS.push((problem.getStartState(), [], 0), 0)
    visited = set()

    while not prioQueueUCS.isEmpty():
        state, path, cost = prioQueueUCS.pop()  # Haal de staat met de laagste kosten op

        if problem.isGoalState(state):  # Controleer of we het doel hebben bereikt
            return path

        if state not in visited:
            visited.add(state)

            # problem.getSuccessors geeft een lijst van (successor, action, stepCost) terug
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    newPath = path + [action]
                    newCost = cost + stepCost
                    prioQueueUCS.push((successor, newPath, newCost), newCost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    prioQueueAStar = util.PriorityQueue() # Priority Queue omdat A* zoekt op basis van de gecombineerde kosten f(n) = g(n) + h(n)
    startState = problem.getStartState()
    startHeuristic = heuristic(startState, problem)
    prioQueueAStar.push((startState, [], 0), startHeuristic)
    visited = set()  # Set om bij te houden welke staten al definitief zijn verwerkt

    while not prioQueueAStar.isEmpty():
        state, path, cost = prioQueueAStar.pop()  # Haal de knoop op met de laagste f(n) kosten

        if problem.isGoalState(state):  # Controleer of we het doel hebben bereikt
            return path

        if state not in visited:
            visited.add(state)

            # problem.getSuccessors geeft (successor, action, stepCost) terug
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    newPath = path + [action]
                    newCost = cost + stepCost

                    # De prioriteit voor A* is de werkelijke kosten plus de heuristische schatting
                    heuristicCost = heuristic(successor, problem)
                    totalPriority = newCost + heuristicCost
                    prioQueueAStar.push((successor, newPath, newCost), totalPriority)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
