import sys

#########################
# Show Matrix
#
# print the state
#########################
def showMatrix(mat):
	for X in range(3):
		for Y in range(3):
			print mat[X][Y],
		print
	print

#########################
# Get CPU's move
#
# get CPU's move
#########################
def getAIMove(mat):
	global numberOfNodesMinimax
	global numberOfNodesMinimaxAB
	
	move = miniMax(mat)
	moveAB = miniMaxAB(mat)
	
	if move != moveAB:
		# if both algorithms do not return the same solution show an error
		print ('Error: Minimax and Alpha-Beta Pruning based Minimax returned different values!')
	else:
		# else make the move
		if move != None:
			mat[move[0]][move[1]] = PLAYER2

	print 'Number of Nodes without A/B Pruning: ', numberOfNodesMinimax
	print 'Number of Nodes with A/B Pruning: ', numberOfNodesMinimaxAB
	
	# display the state
	showMatrix(mat)
		
#########################
# Successor function
#
# returns all valid next moves
#########################
def nextMoves(mat, player):
	successors = []
	for X in range(3):
		for Y in range(3):
			if mat[X][Y] == BLANK :
				newmat = [row[:] for row in mat]
				newmat[X][Y] = player
				successors.append([newmat, [X, Y]])
	
	# for state, action in successors:
		# showMatrix(state)
		# print 'Action: ', action
	return successors

#########################
# Minimax
#
# returns CPU's move via Minimax algorithm as a list [X, Y]
#########################
def miniMax(root):
	global numberOfNodesMinimax
	numberOfNodesMinimax = 1
	valueAndAction = maxValue(root)
	return valueAndAction[1]
	
#########################
# maxValue
#
# returns best value for the max player
#########################
def maxValue(root):
	global numberOfNodesMinimax
	value = gameover(root)
	
	# if game is over return the value
	if value != GAMENOTOVER:
		return [value, None]

	value = MINUS_INFINITY
	finalAction = None
	
	# check for each successor states
	for state, action in nextMoves(root, PLAYER2):
		numberOfNodesMinimax = numberOfNodesMinimax + 1
		newValue = minValue(state)
		# store the least value
		if value < newValue[0]:
			value = newValue[0]
			finalAction = action
	# return the least value and corresponding action
	return [value,finalAction]

#########################
# minValue
#
# returns best value for the min player
#########################
def minValue(root):
	global numberOfNodesMinimax
	value = gameover(root)
	
	# if game is over return the value
	if value != GAMENOTOVER:
		return [value, None]
		
	value = PLUS_INFINITY
	finalAction = None
	
	# check for each successor states
	for state, action in nextMoves(root, PLAYER1):
		numberOfNodesMinimax = numberOfNodesMinimax + 1
		newValue = maxValue(state)
		# store the highest value
		if value > newValue[0]:
			value = newValue[0]
			finalAction = action
	# return the highest value and corresponding action
	return [value,finalAction]

#########################
# Minimax with Alpha-Beta Pruning
#
# returns CPU's move via Minimax algorithm with Alpha-Beta Pruning as a list [X, Y]
#########################
def miniMaxAB(root):
	global numberOfNodesMinimaxAB
	numberOfNodesMinimaxAB = 1
	valueAndAction = maxValueAB(root, MINUS_INFINITY, PLUS_INFINITY)
	return valueAndAction[1]
	
#########################
# maxValueAB
#
# returns best value for the max player using Alpha-Beta Pruning
#########################
def maxValueAB(root, alpha, beta):
	global numberOfNodesMinimaxAB
	value = gameover(root)
	
	# if game is over return the value
	if value != GAMENOTOVER:
		return [value, None]

	value = MINUS_INFINITY
	finalAction = None
	
	# check for each successor states
	for state, action in nextMoves(root, PLAYER2):
		numberOfNodesMinimaxAB = numberOfNodesMinimaxAB + 1
		newValue = minValueAB(state, alpha, beta)
		# store the least value
		if value < newValue[0]:
			value = newValue[0]
			finalAction = action
			# if value is more than beta do not search any further nodes
			if value >= beta:
				return [value, finalAction]
			# if value is more than alpha update alpha
			if value > alpha:
				alpha = value
	# return the least value and corresponding action
	return [value, finalAction]

#########################
# minValueAB
#
# returns best value for the min player using Alpha-Beta Pruning
#########################
def minValueAB(root, alpha, beta):
	global numberOfNodesMinimaxAB
	value = gameover(root)
	
	# if game is over return the value
	if value != GAMENOTOVER:
		return [value, None]
		
	value = PLUS_INFINITY
	finalAction = None
	
	# check for each successor states
	for state, action in nextMoves(root, PLAYER1):
		numberOfNodesMinimaxAB = numberOfNodesMinimaxAB + 1
		newValue = maxValueAB(state, alpha, beta)
		# store the highest value
		if value > newValue[0]:
			value = newValue[0]
			finalAction = action
			# if value is less than alpha do not search any further nodes
			if value <= alpha:
				return [value, finalAction]
			# if value is less than beta update beta
			if value < beta:
				beta = value
	# return the highest value and corresponding action
	return [value, finalAction]
	
#########################
# Get user's move
#
# accept input from the console
#########################
def getPlayersMove(mat):
	valid = False
	while not valid:
		try:
			input = raw_input('Enter position:').split()
			X = int(input[0])
			Y = int(input[1])
			if mat[X-1][Y-1] != BLANK:
				raise Exception()
			# if valid then play
			mat[X-1][Y-1] = PLAYER1
			showMatrix(mat)
			valid = True
		except IndexError, e:
			print ('Error! Use this Format: "X<space>Y" where 1 <= X <= 3 AND 1 <= Y <= 3')
		except ValueError, e:
			print ('Error! Use this Format: "X<space>Y" where 1 <= X <= 3 AND 1 <= Y <= 3')
		except Exception, e:
			print ('Error! Position not empty!')

#########################
# gameover
#
# utility + terminal test. Checks if game is over. If game is over it returns who won.
#
# returns +1 if PLAYER1 wins
# returns -1 if PLAYER2 wins
# returns 0 if game is draw
# returns GAMENOTOVER if game not over
#########################	
def gameover(mat):

	# check for winning condition in rows
	for X in range(3):
		Xwins = True
		Owins = True
		for Y in range(3):
			if mat[X][Y] == BLANK:
				Xwins = False
				Owins = False
			elif mat[X][Y] == PLAYER1:
				Owins = False
			elif mat[X][Y] == PLAYER2:
				Xwins = False
		if Xwins:
			return PLAYER1_WINS
		elif Owins:
			return PLAYER2_WINS
			
	# check for winning condition in columns
	for Y in range(3):
		Xwins = True
		Owins = True
		for X in range(3):
			if mat[X][Y] == BLANK:
				Xwins = False
				Owins = False
			elif mat[X][Y] == PLAYER1:
				Owins = False
			elif mat[X][Y] == PLAYER2:
				Xwins = False
		if Xwins:
			return PLAYER1_WINS
		elif Owins:
			return PLAYER2_WINS
			
	# check for winning condition in diagonals
	Xwins = True
	Owins = True
	Xwins2 = True
	Owins2 = True
	for X in range(3):
		if mat[X][X] == BLANK:
			Xwins = False
			Owins = False
		elif mat[X][X] == PLAYER1:
			Owins = False
		elif mat[X][X] == PLAYER2:
			Xwins = False
		
		if mat[X][2 - X] == BLANK:
			Xwins2 = False
			Owins2 = False
		elif mat[X][2 - X] == PLAYER1:
			Owins2 = False
		elif mat[X][2 - X] == PLAYER2:
			Xwins2 = False
	if Xwins or Xwins2:
		return PLAYER1_WINS
	elif Owins or Owins2:
		return PLAYER2_WINS
	else:
		for X in range(3):
			for Y in range(3):
				if mat[X][Y] == BLANK:
					# Valid moves possible
					return GAMENOTOVER
				
	return DRAW
	
#########################
# Main program
#########################
def main():
	matrix = [[BLANK for x in xrange(3)] for x in xrange(3)]
	showMatrix(matrix)
	result = GAMENOTOVER
	
	# play till end of game
	while result == GAMENOTOVER:
		# players turn
		getPlayersMove(matrix)
		result = gameover(matrix)
		if result == GAMENOTOVER:
			# if game not over CPU's turn
			getAIMove(matrix)
		result = gameover(matrix)
	
	# display result
	if result == PLAYER1_WINS:
		print 'Result: You Win!'
	elif result == PLAYER2_WINS:
		print 'Result: You Lose!'
	else:
		print 'Result: Draw!'
		
		
# Global variables / constants
PLAYER1 = 'X'
PLAYER2 = 'O'
PLAYER1_WINS = -1
PLAYER2_WINS = 1
DRAW = 0
BLANK = '_'
GAMENOTOVER = 999
PLUS_INFINITY = 99999
MINUS_INFINITY = -99999
numberOfNodesMinimax = 1
numberOfNodesMinimaxAB = 1

# Execute the main program.
main()
