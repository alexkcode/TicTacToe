import main, ttt
import unittest
from cli import test
import itertools, collections

class GridTest(unittest.TestCase):

	def setUp(self):
		self.test_grid = ttt.grid()

	def test_positions(self):
		# check that we're getting the right set of positions
		pos = [idx for idx in self.test_grid.positions]
		good_pos = [x for x in itertools.product([-1,0,1], repeat=2)]
		self.assertEqual(sorted(pos), sorted(good_pos))

	def test_neighbors(self):
		neighbor = (0, 0)
		target = (1, 1)
		non_neighbor = (0, -1)
		square = self.test_grid.positions[target]
		self.assertTrue(neighbor in square.neighbors)
		self.assertTrue(non_neighbor not in square.neighbors)

	# def test_distCheck(self):
	# 	A, B = (0, 0), (1, 1)
	# 	self.assertTrue(ttt.distCheck(A, B))
	# 	A, B = (-1, -1), (1, 1)
	# 	self.assertFalse(ttt.distCheck(A, B))

	def test_alignCheck(self):
		A, B = (0, 0), (1, 1)
		self.assertFalse(ttt.alignCheck(A, B))
		self.assertFalse(ttt.alignCheck(B, A))
		A, B = (-1, -1), (-1, 0)
		self.assertTrue(ttt.alignCheck(A, B))
		self.assertTrue(ttt.alignCheck(B, A))
		A, B = (1, 1, 0), (-1, -1, 0)
		self.assertTrue(ttt.alignCheck(A, B, level='plane'))

	def test_tripleAlignCheck(self):
		A, B, C = (-1, 0), (0, 0), (1, 0)
		allAligned = ttt.alignCheck(A, B) and \
					 ttt.alignCheck(B, C) and \
					 ttt.alignCheck(C, A)
		self.assertTrue(allAligned)
		A, B, C = (-1, -1), (0, 0), (1, 1)
		allAligned = ttt.alignCheck(A, B) and \
					 ttt.alignCheck(B, C) and \
					 ttt.alignCheck(C, A)
		self.assertFalse(allAligned)

	def test_diagonalCheck(self):
		A, B = (0, 0), (1, 1)
		self.assertTrue(ttt.diagonalCheck(A, B))
		self.assertTrue(ttt.diagonalCheck(B, A))
		A = (-1, -1)
		self.assertTrue(ttt.diagonalCheck(A, B))
		A, B = (1, -1), (-1, 1)
		self.assertTrue(ttt.diagonalCheck(A, B))
		A, B = (0, 1), (-1, 1)
		self.assertFalse(ttt.diagonalCheck(A, B))
		A, B = (-1, 1), (-1, -1)
		self.assertFalse(ttt.diagonalCheck(A, B))
		A, B = (0, 0, 0), (1, 1, 1)
		self.assertTrue(ttt.diagonalCheck(A, B))
		A, B = (-1, -1, -1), (1, 1, 1)
		self.assertTrue(ttt.diagonalCheck(A, B))
		A, B = (-1, 1, 1), (1, -1, 0)
		self.assertFalse(ttt.diagonalCheck(A, B))
		A, B = (-1, 0, 1), (1, 0, -1)
		self.assertTrue(ttt.diagonalCheck(A, B))

	def test_tripleDiagonalCheck(self):
		loc1, loc2, loc3 = (1, 1), (0, 0), (-1, -1)
		aligned = ttt.diagonalCheck(loc1, loc2) and \
				  ttt.diagonalCheck(loc2, loc3) and \
				  ttt.diagonalCheck(loc3, loc1)
		self.assertTrue(aligned)

	def test_findDiff(self):
		A, B = (-1, 1), (-1, 0)
		self.assertEqual(ttt.findDiff(A, B), (-1, -1))
		A, B = (0, 0, 0, 1), (0, 0, 0, -1)
		self.assertEqual(ttt.findDiff(A, B), (0, 0, 0, 0))
		A, B = (0, -1, -1, -1), (0, 1, 1, 1)
		self.assertEqual(ttt.findDiff(A, B), (0, 0, 0, 0))
		A, B = (0, 0, 0), (1, 1, 1)
		self.assertEqual(ttt.findDiff(A, B), (-1, -1, -1))
		A, B = (1, 1), (0, 0)
		self.assertEqual(ttt.findDiff(A, B), (-1, -1))

	def test_findLastMark(self):
		self.assertEqual(self.test_grid.findLastMark('X'), None)
		self.test_grid.makeMark((-1, 1), 'X')
		self.test_grid.makeMark((0, 0), 'O')
		self.test_grid.makeMark((1, -1), 'X')
		X_pos = self.test_grid.findLastMark('X')
		O_pos = self.test_grid.findLastMark('O')
		self.assertEqual(X_pos, (1, -1))
		self.assertEqual(O_pos, (0, 0))

	def test_makeMark(self):
		self.test_grid.makeMark((1, 1), 'O')
		self.assertEqual(self.test_grid.positions[(1, 1)].mark, 'O')
		self.assertEqual(self.test_grid.marked[0], (1, 1))
		self.test_grid.makeMark((-1, -1), 'X')

	def test_findPotential(self):
		self.assertEqual(self.test_grid.findPotential(), (0, 0))
		self.test_grid.makeMark((1, -1), 'X')
		self.test_grid.makeMark((0, 0), 'O')
		self.test_grid.makeMark((-1, 1), 'X')
		potentialPos = self.test_grid.findPotential()
		self.assertTrue(potentialPos in [(1, 0), (-1, 0), (0, -1), (0, 1)])

		newTest = ttt.grid()
		newTest.makeMark((0, 0), 'X')
		newTest.makeMark((1, 1), 'O')
		newTest.makeMark((-1, -1), 'X')
		potentialPos = newTest.findPotential()
		self.assertTrue(potentialPos in [(-1, 1), (1, -1)])

	def test_checkStatus(self):
		newTest = ttt.grid()
		newTest.makeMark((1, 1), 'O')
		newTest.makeMark((0, 0), 'O')
		newTest.makeMark((-1, -1), 'O')
		self.assertEqual(newTest.checkStatus(), -1)

		newTest = ttt.grid()
		newTest.makeMark((1, 1), 'O')
		newTest.makeMark((0, 0), 'X')
		newTest.makeMark((-1, -1), 'O')
		newTest.makeMark((-1, 0), 'X')
		newTest.makeMark((1, 0), 'O')
		newTest.makeMark((1, -1), 'X')
		newTest.makeMark((-1, 1), 'O')
		newTest.makeMark((0, 1), 'X')
		newTest.makeMark((0, -1), 'O')
		self.assertEqual(newTest.checkStatus(), 0)

	def test_findMatch(self):
		self.test_grid.makeMark((1, 1), 'O')
		self.test_grid.makeMark((0, 0), 'O')
		self.assertEqual(self.test_grid.findMatch('O'), (-1,-1))
		self.assertEqual(self.test_grid.findMatch('X'), None)

	def test_parseInput(self):
		test = self.test_grid.parseInput('( 1,-1)')
		self.assertEqual(test, (1,-1))
		test = self.test_grid.parseInput('-1,-1')
		self.assertEqual(test, (-1,-1))
		test = self.test_grid.parseInput('   (\n-1,1 )\n')
		self.assertEqual(test, (-1,1))		

	def test_playerMove(self):
		testInput = '   \n( -1, 1)'
		self.test_grid.playerMove(testInput)
		last = self.test_grid.marked[-1]
		self.assertEqual(last, (-1, 1))
		self.assertEqual(self.test_grid.positions[last].mark, 'X')

	def test_computerMove(self):
		self.test_grid.makeMark((1, -1), 'X')
		self.test_grid.makeMark((0, 0), 'O')
		self.test_grid.makeMark((-1, 1), 'X')
		self.test_grid.computerMove()
		lastCompMove = self.test_grid.marked[-1]
		self.assertTrue(lastCompMove in [(1, 0), (-1, 0), (0, -1), (0, 1)])

		newTest = ttt.grid()
		newTest.makeMark((0, 0), 'X')
		newTest.makeMark((1, 1), 'O')
		newTest.makeMark((-1, 0), 'X')
		newTest.computerMove()
		lastCompMove = newTest.marked[-1]
		self.assertEqual(lastCompMove, (1, 0))

	def test_checkValid(self):
		# test = self.test_grid.checkValid(self.test_grid.parseInput('asb(,asd)'))
		# self.assertFalse(test)
		test = self.test_grid.checkValid(self.test_grid.parseInput('(9,9)'))
		self.assertFalse(test)
		test = self.test_grid.checkValid(self.test_grid.parseInput('(0,0)'))
		self.assertTrue(test)

class GameTest(test.FunctionalTest):
	pass

if __name__ == '__main__':
    unittest.main()