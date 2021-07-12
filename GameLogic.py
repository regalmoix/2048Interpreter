import random
import sys

subopt = 1

tileNames = [[[], [], [], []] for i in range(4)]

def update_tilename(from_x, from_y, to_x, to_y):
	tileNames[to_x][to_y] += tileNames[from_x][from_y] 


def init_board():
	
	EMPTY = 0
	mat = []
	for i in range(4):
		mat.append([EMPTY] * 4)

	add_random_tile(mat)
	return mat


def add_random_tile(mat):

	EMPTY = 0

	emptyList = []

	for i in range (0, 4):
		for j in range(0, 4):
			if mat[i][j] == EMPTY:
				emptyList.append((i,j))
	
	coordinates = random.choice(emptyList)

	x, y = coordinates

	random_val = random.choice([2,4])

	mat[x][y] = random_val


# Input Matrix assumed to have no Gaps between tiles assuming left
def left(mat, op):
	global tileNames

	EMPTY = 0
	updated = False

	tmp = []
	# names = []
	names = [[[], [], [], []] for i in range(4)]

	for i in range(4):
		tmp.append([EMPTY] * 4)
		# names.append([[]] * 4)

		
	for i in range(4):
		pos = 0

		for j in range(4):
			if(mat[i][j] != EMPTY):

				tmp[i][pos] = mat[i][j]
				names[i][pos] = tileNames[i][j]
				
				if(j != pos):
					updated = True
				pos += 1

	mat = tmp
	tileNames = names



	for i in range(4):
		for j in range(3):

			if op == "ADD" and mat[i][j] != EMPTY and mat[i][j+1] != EMPTY and mat[i][j] == mat[i][j + 1]:
				tileNames[i][j] += tileNames[i][j+1]
				tileNames[i][j+1] = []

				mat[i][j] = mat[i][j] + mat[i][j+1]
				mat[i][j + 1] = EMPTY							# So that this not involved in merge again with i, j+2

				updated = True

			elif(mat[i][j] == mat[i][j + 1] and mat[i][j] != EMPTY):
				tileNames[i][j] += tileNames[i][j+1]
				tileNames[i][j+1] = []
				

				if op == "SUBTRACT":

					if subopt == "1":
						mat[i][j] = 0
						mat[i][j + 1] = EMPTY							# So that this not involved in merge again with i, j+2

						updated = True
					
					else :
						mat[i][j] = -1
						mat[i][j + 1] = EMPTY							# So that this not involved in merge again with i, j+2

						updated = True

				elif op == "MULTIPLY":
					mat[i][j] = mat[i][j] ** 2
					mat[i][j + 1] = EMPTY							# So that this not involved in merge again with i, j+2

					updated = True

				elif op == "DIVIDE":
					if mat[i][j] != 0:
						mat[i][j] = 1
						mat[i][j + 1] = EMPTY							# So that this not involved in merge again with i, j+2

						updated = True
				

	tmp = []
	# names = []
	names = [[[], [], [], []] for i in range(4)]

	for i in range(4):
		tmp.append([EMPTY] * 4)
		# names.append([[]] * 4)
		
	for i in range(4):
		pos = 0

		for j in range(4):
			if(mat[i][j] != EMPTY):

				tmp[i][pos] = mat[i][j]
				names[i][pos] = tileNames[i][j]
				
				if(j != pos):
					updated = True
				pos += 1


	mat = tmp
	tileNames = names

	for i in range(4):
		for j in range(4):
			if (mat[i][j] == -1):
				mat[i][j] = EMPTY
				tileNames[i][j].clear()



	return mat, updated


def flip_matrix(mat):
	tmp =[]
	for i in range(4):
		tmp.append([])
		for j in range(4):
			tmp[i].append(mat[i][3 - j])
	return tmp


def transpose(mat):
	tmp = []
	for i in range(4):
		tmp.append([])
		for j in range(4):
			tmp[i].append(mat[j][i])
	return tmp


def right(grid, op):
	global tileNames

	tmp = flip_matrix(grid)
	tileNames = flip_matrix(tileNames)

	tmp, updated = left(tmp, op)

	tmp = flip_matrix(tmp)
	tileNames = flip_matrix(tileNames)

	return tmp, updated


def up(grid, op):
	global tileNames

	tmp = transpose(grid)
	tileNames = transpose(tileNames)

	tmp, updated = left(tmp, op)

	tmp = transpose(tmp)
	tileNames = transpose(tileNames)

	return tmp, updated


def down(grid, op):
	global tileNames

	tmp = transpose(grid)
	tileNames = transpose(tileNames)

	tmp, updated = right(tmp, op)

	tmp = transpose(tmp)
	tileNames = transpose(tileNames)

	return tmp, updated


def print_board(board):
	EMPTY = 0

	print('---------------------')

	for row in board:
		print ('|', end="")
		for val in row:
			if val != EMPTY:
				# val == '__'
				print ('{:4}'.format(val), end="|")

			else:
				x = ''
				print ('{:4}'.format(x), end="|")

		print()
		print('---------------------')
	
	for x in range(1, 5):
		for y in range(1, 5):
			if len(tileNames[x - 1][y-1]) != 0:
				print(f"{x},{y} => {tileNames[x - 1][y - 1]}")

	print()
	for i in range(4):
		for j in range(4):
			print(board[i][j], end=" ", file=sys.stderr)
	
	
	for i in range(4):
		for j in range(4):
			if len(tileNames[i][j]) != 0:
				print(f"{1+i},{1+j}", end="", file=sys.stderr)
				print(*tileNames[i][j], sep=",", file=sys.stderr, end=" ")
				
    
	print(file = sys.stderr)
	print()
