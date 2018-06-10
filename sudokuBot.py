# Define a function which counts the number of non zero entries in a list
def countNonZero(list):
	result = 0;
	
	for	item in list:
		if (item):
			result += 1
	
	return result;
	
def getCell(x, y):
	userInput = input(f'Enter the value at ({x},{y}): ')
	if (userInput):
		return int(userInput)
	else:
		return 0

# Define our own index of method, which returns -1 if the element is not
# present in the list
def indexOf(list, element):
	for x in enumerate(list):
		if x[1] == element:
			return x[0]
	else:
		return -1

def hasMissingEntries(list):
	return countNonZero(list) < len(list)
	
# Returns whether or not the specified list is valid for an order of puzzle
def isValid(list, order):
	# Make a copy of the list
	list = list[:]

	# Determine whether the list is valid by removing the first instance of
	# 1..n from the list and counting any remaining non-zero cells
	for i in range(1, order * order + 1):
		if indexOf(list, i) > -1:
			list.remove(i)
	return not countNonZero(list)
	
class Sudoku:
	rows = []
	
	def __init__(self, rows):
		# Make a deep copy of the new rows
		self.rows = []
		for row in rows:
			self.rows += [row[:]]
	
	def clone(sudoku):
		return Sudoku.fromRows(sudoku.getRows())
	
	def fromUserInput(order):
		rows = []
		for x in range(order * order):
			row = []
			for y in range(order * order):
				row += [getCell(x,y)]
			rows += [row]
		return Sudoku.fromRows(rows)
	
	def fromRows(rows):
		return Sudoku(rows)
	
	def fromColumns(columns):
		rows = []
		for x in range(len(columns)):
			row = []
			for y in columns:
				row += [y[x]]
			rows += [row]
		
		return Sudoku.fromRows(rows)
	
	def fromSquares(squares):
		order = round(len(squares) ** (1/2))
		rows = []
		for x in range(order):
			for y in range(order):
				row = []
				for i in range(order):
					for j in range(order):
						row += [(squares[i + x * order])[j + y * order]]
				rows += [row]
		return Sudoku.fromRows(rows)
	
	def fromWeb():
		# Download a new problem from http://davidbau.com/
		import requests
		
		print('Downloading new puzzle from http://davidbau.com/...');
		r = requests.get('http://davidbau.com/generated/sudoku.txt')
		lines = list(r.iter_lines())
		print('Puzzle downloaded')
		
		rows = []
		for x in range(0,9):
			row = []
			for y in range(1,10):
				cell = str(lines[1 + 2 * x])[y * 4]
				if cell == " ":
					cell = "0"
				row += [int(cell)]
			rows += [row]
		return Sudoku.fromRows(rows)
	
	def getLength(self):
		return len(self.rows)
		
	# We define the 'order' of a puzzle to be the square root of its row length
	# The order is zero for puzzles whose row length is not a square number
	def getOrder(self):
		order = self.getLength() ** (1/2)
		if (order % 1 == 0):
			return round(order)
		else:
			return 0
	
	def getRows(self):
		return self.rows[:]

	def getColumns(self):
		columns = []
		for x in range(len(self.rows)):
			column = []
			for row in self.rows:
				column += [row[x]]
			columns += [column]
		return columns

	def getSquare(self,x,y):
		order = self.getOrder()	
		if order == 0:
			return []
		else:
			square = []
			for i in range(order):
				for j in range(order):
					square += [(self.rows[i + x * order])[j + y * order]]
			return square
		
	def getSquares(self):
		order = self.getOrder()		
		if order == 0:
			return []
		else:
			squares = []
			for x in range(order):
				for y in range(order):
					squares += [self.getSquare(x, y)]
			return squares
		
	def isSolved(self):
		for row in self.getRows():
			if hasMissingEntries(row):
				return False
		else:
			return True

	def isValid(self):
		order = self.getOrder()
		for row in self.getRows():
			if not isValid(row, order):
				return False
		for column in self.getColumns():
			if not isValid(column, order):
				return False
		for square in self.getSquares():
			if not isValid(square, order):
				return False
		return True
						
	def render(self):
		lineBreak = '|'
		lineBreak += ('-' * 2 * (self.getLength() - 1))
		lineBreak += '-|'
		
		print(lineBreak)
		
		for	row in self.getRows():
			thisLine = '|'
			for cell in row:
				if cell == 0:
					thisLine += " "
				else:
					thisLine += str(cell)
				thisLine += '|'
			print(thisLine)
			print(lineBreak)

# A branch point is a point in the puzzle solving logic where more than one
# move is possible. Moves are exhausted sequentially using brute force, and
# the current branch and puzzle state are stored in a BranchPoint for future
# use if we end up with an invalid puzzle
class BranchPoint:
	sudoku = None
	branchNumber = 0
	maxBranches = 0

	def __init__(self, sudoku, maxBranches):
		# Make a copy of the incoming puzzle
		self.sudoku = Sudoku.clone(sudoku)
		self.maxBranches = maxBranches
		
	def resume(self):
		# Increment the branch number, and return a copy of the
		# stored puzzle
		self.branchNumber += 1
		return Sudoku.clone(self.sudoku)
	
	def exhausted(self):
		return self.branchNumber >= self.maxBranches
			
# 3x3 example
#sudoku = [[1,0,3], [3,0,0], [0,3,0]]

# 4x4 example(s)
#sudoku = [[1,0,3,4],[3,1,0,2],[0,4,1,3],[4,0,0,0]]
#sudoku = [[0,0,0,3],[3,2,4,0],[0,4,3,2],[2,0,0,0]]
#sudoku = Sudoku.fromRows([[0,0,0,3],[3,2,4,0],[0,4,3,2],[2,0,0,0]])
#sudoku = Sudoku.fromRows([[0,0,0,3],[3,0,4,0],[0,4,0,2],[2,0,0,0]])

#order = int(input('Select an order of puzzle:\n'))
#sudoku = Sudoku.fromUserInput(order)

import time

print('SudokuBot 1.0.0 - by Alex Howgego\n')
sudoku = Sudoku.fromWeb()

print('Puzzle start:\n')
sudoku.render()
print('\n')
print('Press any key to solve\n')
input(' ')

showWorking = False
start, totalSteps = time.time(), 0

# Store branch points
branchPoints = []

while not sudoku.isSolved():
	if showWorking:
		# Print the current state of the problem
		sudoku.render()
		input(' ')
	
	branchPoint = None
	
	# Perform a validity check
	if not sudoku.isValid():
		# Get the last branch point and restore the puzzle
		if showWorking:
			print('Puzzle invalid, resuming from branch point...\n')
		branchPoint = branchPoints.pop()
		sudoku = branchPoint.resume()
		
		# Check that this branch point has not also been exhausted
		while branchPoint.exhausted():
			if showWorking:
				print('Branch point exhausted, winding up the stack...\n')
			branchPoint = branchPoints.pop()
			sudoku = branchPoint.resume()
			
		if showWorking:
			sudoku.render()
			input(' ')

	# Increment the step counter
	totalSteps += 1

	# Load the rows and columns from the puzzle
	rows = sudoku.getRows()
	columns = sudoku.getColumns()
	squares = sudoku.getSquares()

	# Determine which row/column to attempt to solve
	nextToSolve = [0] * sudoku.getLength()
	
	# Keep track of what type of candidate we are
	isRow, isColumn = True, True

	# Determine which row to solve by counting the number of
	# non-zero entries. If the number of non-zero entries is
	# greater than the current candidate, replace items
	for row in rows:
		if countNonZero(row) > countNonZero(nextToSolve):
			if hasMissingEntries(row):
				isRow = True
				isColumn = False
				nextToSolve = row
			
	for column in columns:
		if countNonZero(column) > countNonZero(nextToSolve):
			if hasMissingEntries(column):
				isRow = False
				isColumn = True
				nextToSolve = column
				
	for square in squares:
		if countNonZero(square) > countNonZero(nextToSolve):
			if hasMissingEntries(square):
				isRow = False
				isColumn = False
				nextToSolve = square
	
	# Initialise the list of values 1 -> sudoku length (incl.)
	values = list(range(1,sudoku.getLength() + 1))

	# Remove all the values which are currently present
	for x in nextToSolve:
		if x != 0:
			values.remove(x)

	# The remaining values are all the possible moves
	if len(values) > 1:
		# More than one move is possible, so create or resume a branch
		# point
		if branchPoint is None:
			branchPoint = BranchPoint(sudoku, len(values))
		
		# Get the branch number
		branchNumber = branchPoint.branchNumber
		
		if showWorking:
			print(f'Branch number: {branchNumber + 1}\n')
			
		# Push the branch point onto the stack, then use the branch
		# number to determine which value to try
		branchPoints.append(branchPoint)
		value = values[branchNumber]
	else:
		# Use the single value
		value = values[0]
		
	# Insert this value into the item to solve
	for x in enumerate(nextToSolve):
		if x[1] == 0:
			nextToSolve[x[0]] = value
			break

	# Refresh the puzzle (need to determine whether we changed the rows
	# or the columns
	if (isRow):
		sudoku = Sudoku.fromRows(rows)
	elif (isColumn):
		sudoku = Sudoku.fromColumns(columns)
	else:
		sudoku = Sudoku.fromSquares(squares)

# Get the end time
end = time.time()
		
# Render the sudoku
sudoku.render()

print('\n')
print(f'Solved problem in {totalSteps} step(s)')

if not showWorking:
	print(f'Time to solve was {end - start}s')