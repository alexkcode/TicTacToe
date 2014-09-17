import itertools, collections

def opposite(A):
	return tuple([-1*a for a in A])

def alignCheck(A, B, level='line'):
	"""Are A and B on the same row or column?"""
	diff = 0
	for a, b in zip(A, B):
		if a != b: diff += 1
	if A == B:
		return False
	elif diff == 1 and level == 'line':
		return True 
	elif diff == 2 and level == 'plane':
		return True
	else:
		return False

def diagonalCheck(A, B):
	"""Are A and B on a diagonal together?"""
	# trivial case
	if A == B:
		return False
	else:
		dim = len(B)
		center = tuple([0 for i in range(dim)])
		non_center = set([A, B]).difference([center])
		non_center = list(non_center)[0]
		# one is center one is corner
		if center in (A, B) and 0 not in non_center:	
			return True
		# the squares are across the grid from each other
		elif opposite(A) == B:
			return True
		else:
			return False

def rowDiff(A, B):
	"""If there are 2/3 in a row, where is the empty square?"""
	loc = 0
	for a, b in zip(A, B):
		if a == b: 
			loc += 1
		else:
			break 
	diff = set([-1, 0, 1]).difference([A[loc], B[loc]])
	C = list(A)
	C[loc] = list(diff)[0]
	return tuple(C)

def diagonalDiff(A, B):
	"""If there are 2/3 in a diagonal, where is the empty square?"""
	center = tuple([0 for i in range(len(A))])
	if A == center:
		return opposite(B)
	elif B == center:
		return opposite(A)
	else:
		return center

def findDiff(A, B):
	"""Where is the empty square?"""
	if alignCheck(A, B):
		return rowDiff(A, B)
	elif diagonalCheck(A, B):
		return diagonalDiff(A, B)
	else:
		return None

class square:
	"""A single 'square' or unit of the grid."""
	
	def __init__(self, neighbors, mark):
		"""
		Parameters:
		mark: string
			indicates whether the square is empty, "X" or "O"
		neighbors: list
			coordinates for surrounding squares
		"""
		self.mark = mark
		self.neighbors = neighbors
		self.empties = len(neighbors)

class grid:
	"""The grid for the tic tac toe environment."""

	def near(self, X, positions):
		"""
		Find all squares in line with X.
		Parameters:
			X : tuple
				position of mark
			positions : list of tuples
				all possible positions
		"""
		neighbors = []
		for pos in positions:
			if alignCheck(X, pos) or diagonalCheck(X, pos):
				neighbors.append(pos)
			else:
				pass
		return neighbors

	def __init__(self, dim=2):
		"""
		Parameters:
			dim : int 
				The number of dimensions of the tic tac toe game. For example
				dim = 3 gives you a cube for the tic tac toe grid.
		"""
		if dim < 2:
			raise ValueError("Invalid dimension given." + \
				"It must be an integer greater than one.")
		iter = itertools.product([-1,0,1], repeat=dim)
		all = [x for x in iter]
		self.positions = {x : square(self.near(x, all), '') for x in all}
		self.marked = []
		self.dim = dim

	def viewPos(self, loc):
		if self.positions[loc].mark == '':
			pos = str(loc)
			pos = pos.replace('(1', '( 1').replace(',1)', ', 1)')
			pos = pos.replace('(0', '( 0').replace(',0)', ', 0)')
			pos = pos.replace(', -1)', ',-1)')
			return pos
		else:
			return '   ' + self.positions[loc].mark + '   '

	def showGrid(self, dim1=0, dim2=1):
		"""
		Produces a view of the grid with all the marks.
		Parameters (ignore if normal 2D tic tac toe:
			dim1 : int
				first dimension of slice view
			dim2 : int
				second dimension of slice view
		"""
		if dim1 < dim2:
			d1 = dim1
			d2 = dim2
		else:
			d1 = dim2
			d2 = dim1
		div1 = "\n       |       |       \n"
		div2 = "-----------------------"
		if self.dim > 2:
			iter = itertools.product([-1,0,1], repeat=(self.dim - 2))
			for x_other in iter:
				print 'Level:'
				print list(x_other).insert(d1, 'Dim 1').insert(d2, 'Dim 2')
				view = ""
				for y in [1, 'div', 0, 'div', -1]:
					if y == 'div':
						view += div2
					else:
						x1 = list(x_other).insert(d1, -1).insert(d2, y)
						x2 = list(x_other).insert(d1, 0).insert(d2, y)
						x3 = list(x_other).insert(d1, 1).insert(d2, y)
						m1 = self.viewPos((-1, y))
						m2 = self.viewPos((0, y))
						m3 = self.viewPos((1, y))
						view += div1
						view += "{0}|{1}|{2}".format(m1, m2, m3)
						view += div1
				print view
		else:
			view = ""
			for y in [1, 'div', 0, 'div', -1]:
				if y == 'div':
					view += div2
				else:
					m1 = self.viewPos((-1, y))
					m2 = self.viewPos((0, y))
					m3 = self.viewPos((1, y))
					view += div1
					view += "{0}|{1}|{2}".format(m1, m2, m3)
					view += div1
			print view

	def checkStatus(self):
		"""
		Check if someone has won the game.
		Parameters:
			loc : tuple
				location of last mark
		"""
		if len(self.marked) == 3**self.dim:
			return 0
		loc = self.marked[-1]
		sq1 = self.positions[loc]
		sq3 = None
		loc3 = None
		for loc2 in sq1.neighbors:
			sq2 = self.positions[loc2]
			loc3 = findDiff(loc, loc2)
			sq3 = self.positions[loc3]
			# print loc, loc2, loc3
			if sq3 is not None and sq3.mark == sq1.mark:
				aligned1 = alignCheck(loc, loc2) and \
						   alignCheck(loc2, loc3) and \
						   alignCheck(loc3, loc)
				aligned2 = diagonalCheck(loc, loc2) and \
						   diagonalCheck(loc2, loc3) and \
						   diagonalCheck(loc3, loc)
				aligned = aligned1 or aligned2
				matched = sq1.mark == sq2.mark == sq3.mark
				if matched and aligned:
					if sq1.mark == 'O':
						return -1
					elif sq1.mark == 'X':
						return 1
		return None

	def makeMark(self, loc, mark):
		"""
		Mark a single square in the grid.
		Parameters:
			loc : tuple
				where the mark will be located
			mark : string
				the string for the mark ('X' or 'O')
		"""
		self.marked.append(loc)
		self.positions[loc].mark = mark
		for pos in self.positions:
			if pos in self.positions[loc].neighbors:
				self.positions[pos].empties -= 1
		# print self.checkStatus()

	def findPotential(self):
		"""Which empty square in the grid has the most empty neighborhood?"""
		# for ties, the first one that matches the conditions is returned
		bestPos = None
		currEmpties = 0
		for pos in self.positions:
			sq = self.positions[pos] 
			if sq.empties >= currEmpties and sq.mark == '':
				currEmpties = sq.empties
				bestPos = pos
		return bestPos

	def findMatch(self, mark):
		"""Where is there 2/3 in a row marked?"""
		# mark = self.positions[loc].mark
		for pos0, pos1 in itertools.combinations(self.marked, 2):
			mark0 = self.positions[pos0].mark
			mark1 = self.positions[pos1].mark
			if mark0 == mark1 == mark:
				sq = self.positions[pos1]
				trivial = pos1 == pos0
				matched = sq.mark == mark
				candidate = findDiff(pos0, pos1)
				exists = candidate != None
				if not trivial and matched and exists:
					empty = self.positions[candidate].mark == ''
					if empty:
						return candidate
		return None

	def parseInput(self, input):
		"""
		Parses input into a usable tuple.

		Parameters:
			input : str
				input mark location string to be parsed into a tuple
		Return:
			parsed : tuple
				the tuple of parsed player's input
		"""
		if isinstance(input, str):
			parsed = input.replace('\n','').replace(' ','')
			parsed = parsed.strip(' ()')
			parsed = parsed.split(',')
			parsed = [int(a) for a in parsed]
		elif isinstance(input, tuple):
			parsed = input
		else:
			raise ValueError("Input needs to be either string or tuple.")
		return tuple(parsed)

	def playerMove(self, input):
		"""
		Parameters:
			input_func : function
				function the produces a tuple of player's input for next move
		"""
		playerInput = self.parseInput(input)
		sq = self.positions[playerInput]
		if sq.mark != '':
			print 'Invalid location.'
		self.makeMark(playerInput, 'X')

	def computerMove(self):
		computer_win_move = self.findMatch('O')
		player_win_move = self.findMatch('X')
		if computer_win_move:
			self.makeMark(computer_win_move, 'O')
		elif player_win_move:
			self.makeMark(player_win_move, 'O')
		else:
			print self.findPotential()
			self.makeMark(self.findPotential(), 'O')

	def checkValid(self, input):
		for x in input:
			if isinstance(x, int) and abs(x) <= 1:
				return True
			else:
				return False

	def getInput(self):
		self.showGrid()
		print "Where do you want your \'X\'?"
		message = "Please enter the coordinates of the location:\n"
		test_input = None
		while True:
			self.showGrid()
			test_input = self.parseInput(raw_input(message))
			valid = self.checkValid(test_input)
			if valid and self.positions[test_input].mark == '':
				break
			else:
				print 'Invalid location, please choose another.'
		return test_input

	def step(self, move='player'):
		if move == 'player':
			self.playerMove(self.getInput())
		elif move == 'computer':
			self.computerMove()
		else:
			error = "'move' parameter must be either 'player' or 'computer'."
			raise ValueError(error)