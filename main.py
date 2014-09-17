import ttt, collections

"""
AI Algorithm has 3 cases:
	1. Computer has 2/3 in a row.
	2. Player has 2/3 in a row.
	3. None of the above.
"""

if __name__ == '__main__':
	TicTacToe = ttt.grid()
	print "Do you want to go first?"
	start = raw_input("[N/y]: ")
	print "The computer's mark will be \'O\'."
	status = None
	if start == 'y':
		last_move = 'computer'
	else:
		last_move = 'player'
	while status is None:
		if last_move == 'player':
			last_move = 'computer'
		else:
			last_move = 'player'
		TicTacToe.step(move=last_move)
		status = TicTacToe.checkStatus()
		if status == -1:
			TicTacToe.showGrid()
			print 'You lose.'
			break
		elif status == 1:
			TicTacToe.showGrid()
			print 'You win!'
			break
		elif status == 0:
			TicTacToe.showGrid()
			print 'It\'s a draw :(.'
			break
