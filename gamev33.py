import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
n_cols = 10
n_lines = n_cols * 2
block_size = play_width/n_cols


top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

S = [['.....',
      '..00.',
      '.00..',
      '.....',
      '.....'],
     ['.....',
      '.0...',
      '.00..',
      '..0..',
      '.....']]

Z = [['.....',
      '.00..',
      '..00.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..',],
     ['.....',
      '...0.',
      '..0..',
      '.0...',
      '0....'],
     ['.....',
      '.....',
      '0000.',
      '.....',
      '.....'],
      ['.....',
      '0....',
      '.0...',
      '..0..',
      '...0.']]

O = [['.....',
      '.00..',
      '.00..',
      '.....',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

def create_grid():
	grid = [[(0,0,0) for x in range (n_cols)] for x in range(n_lines)]
	return grid

class Piece:
	def __init__(self, shape, rot_index, upper_line_ind, lefter_col_ind):
		self.shape = shape
		self.rot_index = rot_index
		self.upper_line_ind = upper_line_ind
		self.lefter_col_ind = lefter_col_ind
		self.inserted = False

	def drawable(piece, grid):
		s = piece.shape[piece.rot_index]
		for i in range(5):
			for j in range(5):
				if s[i][j] == '0':
					di = piece.upper_line_ind + i
					dj = piece.lefter_col_ind + j
					if di<0 or di>=n_lines or dj<0 or dj>=n_cols :
						return False
					elif grid[int(di)][int(dj)] != (0,0,0):
						return False
		return True

	def insert(piece, grid):
		if piece.drawable(grid):
			s = piece.shape[piece.rot_index]
			c = shape_colors[shapes.index(piece.shape)]
			for i in range(5):
				for j in range(5):
					if s[i][j] == '0':
						grid[int(piece.upper_line_ind + i)][int(piece.lefter_col_ind + j)] = c
			piece.inserted=True

	def remove(piece, grid):
		if piece.inserted : 
			s = piece.shape[piece.rot_index]
			for i in range(5):
				for j in range(5):
					if s[i][j] == '0':
						grid[int(piece.upper_line_ind + i)][int(piece.lefter_col_ind + j)] = (0,0,0)

	def move_left(piece, grid):
		piece.remove(grid)
		piece.lefter_col_ind -= 1
		if not piece.drawable(grid):
			piece.lefter_col_ind +=1
		piece.insert(grid)

	def move_right(piece, grid):
		piece.remove(grid)
		piece.lefter_col_ind += 1
		if not piece.drawable(grid):
			piece.lefter_col_ind -=1
		piece.insert(grid)

	def rotate(piece, grid):
		piece.remove(grid)
		piece.rot_index += 1
		piece.rot_index = piece.rot_index % len(piece.shape)
		if not piece.drawable(grid):
			piece.rot_index = piece.rot_index - 1 + len(piece.shape)
			piece.rot_index = piece.rot_index % len(piece.shape)
		piece.insert(grid)

	def move_down(piece, grid):
		res = True
		if not piece.inserted:
		 return False
		piece.remove(grid)
		piece.upper_line_ind += 1
		if not piece.drawable(grid):
			piece.upper_line_ind -=1
			res = False
		piece.insert(grid)

		return res

def get_random_piece():

	return Piece(random.choice(shapes),0, 0, n_cols/2 - 2)

def check_line(line):
	for j in range(len(line)):
		if line[j]==(0,0,0):
			return False
	return True

def check(grid):
	res = []
	for i in range(len(grid)-1, -1, -1):
		if check_line(grid[i]):
			res.append(i)
	return res

def erase_line(grid, index):
	for i in range(index, 0, -1):
		for j in range(len(grid[i])):
			grid[i][j] = grid[i-1][j]
		for j in range(len(grid[0])):
				grid[0][j] = (0,0,0)

def erase_lines(grid,line_indexes):
	line_indexes = [ line_indexes[k] + k for k in range(len(line_indexes))]
	for k in line_indexes:
		
		for i in range(k, 0, -1):
			for j in range(len(grid[i])):
				grid[i][j] = grid[i-1][j]
		for j in range(len(grid[0])):
				grid[0][j] = (0,0,0)

def erasing_lines(grid, line_indexes, stockage, flevel):
	for i in line_indexes:
		for j in range(len(grid[i])):
			grid[i][j] = tuple( int(k * (1 - flevel)) for k in stockage[i][j])


def draw_grid(surface, grid):
	
	for i in range(len(grid)):
		for j in range (len(grid[i])):
			pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, \
				block_size, block_size), 0)
			pygame.draw.line(surface, (5*i %255,5*i%255,5*i%255), (top_left_x, top_left_y + i*block_size),(top_left_x + play_width, top_left_y + i*block_size) )
			pygame.draw.line(surface, (2*j %255,2*j%255,2*j%255), (top_left_x + j * block_size, top_left_y),(top_left_x + j * block_size, top_left_y + play_height) )

	pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)

def draw_window(surface, grid):
	surface.fill((0,0,0))

	pygame.font.init()
	font = pygame.font.SysFont('comicsans', 60)
	label =  font.render('TETRIS', 1, (255,255,255))

	surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 10 ))

	draw_grid(surface, grid)

	pygame.display.update()	

def main(win):

	grid = create_grid()

	change_piece = False
	run = True
	current_piece = get_random_piece()
	current_piece.insert(grid)

	#next_piece = get_shape()
	clock = pygame.time.Clock()
	fall_time = 0
	fall_speed = 300
	
	erasing_time = 0
	erasing_indexes = []
	erasing_level = 0
	erasing = False
	stockage = []
	

	while run:
		if not erasing : 
			fall_time += clock.get_rawtime()
			clock.tick()	
			if fall_time > fall_speed:
				fall_time = 0
				if not current_piece.move_down(grid):
					if len(check(grid)) > 0:
						erasing = True
						erasing_time = 0
						erasing_indexes = check(grid)
						stockage = [[ grid[a][b] for b in range(len(grid[a]))] for a in range(len(grid))]
						erasing_level = 0
					else :
						current_piece = get_random_piece()
						current_piece.insert(grid)


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					
				if event.type ==  pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						current_piece.move_left(grid)

					if event.key == pygame.K_RIGHT:
						current_piece.move_right(grid)

					if event.key == pygame.K_UP:
						current_piece.rotate(grid)

					if event.key == pygame.K_DOWN:
						if not current_piece.move_down(grid):
							if len(check(grid)) > 0:
								erasing = True
								erasing_time = 0
								erasing_indexes = check(grid)
								stockage = [[ grid[a][b] for b in range(len(grid[a]))] for a in range(len(grid))]
								erasing_level = 0
							else :
								current_piece = get_random_piece()
								current_piece.insert(grid)
						
		
		else : 
			erasing_time += clock.get_rawtime()
			clock.tick()
			if erasing_time > 500:	
				erasing_level=0
				erasing = False
				erasing_time=0
				erase_lines(grid, erasing_indexes)	
				current_piece = get_random_piece()
				current_piece.insert(grid)
			elif erasing_time > (erasing_level) *100 :
				erasing_level += 1
				erasing_lines(grid, erasing_indexes, stockage, erasing_level/10.0)
			
				

		draw_window(win,grid)

def main_menu(win):

	main(win)

win = pygame.display.set_mode((s_width,s_height))
pygame.display.set_caption('TETRIS')
main_menu(win)