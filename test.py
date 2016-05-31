#!/usr/bin/env python
#

import pygame
import pygame.gfxdraw
from pygame.locals import *
import time
import random
import numpy as np
import sys

scrw = 800
scrh = 600

num_rows = 200
num_cols = 200

thick = 0
run = True
max = 0

show_visits = False

def init():
		pygame.init()
		window = pygame.display.set_mode((scrw, scrh), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)
		#window = pygame.display.set_mode((scrw, scrh), pygame.DOUBLEBUF)
		pygame.display.set_caption('Maze')
		maze_srf = pygame.Surface(window.get_size())
		maze_srf.fill((0, 255, 0))

		path_srf = pygame.Surface(window.get_size())
		path_srf.set_colorkey((0, 0, 255))
		path_srf.fill((0, 0, 255))

		window.blit(maze_srf, (0, 0))
		pygame.display.flip()

		return window, maze_srf, path_srf
	
def render_maze(window, maze_srf, maze):
	maze_srf.fill((255, 255, 255))

	xsiz = scrw / num_cols
	ysiz = scrh / num_rows
		
	for y in range(0, num_rows):
		for x in range(0, num_cols):
			xpos = x * xsiz
			ypos = y * ysiz
				
			# U	
			if maze[x, y, 0] == 0:
				pygame.gfxdraw.line(maze_srf, xpos+thick, ypos+thick, \
					xpos+xsiz-thick, ypos+thick, (0, 0, 0))
			
			# L
			if maze[x, y, 1] == 0:	
				pygame.gfxdraw.line(maze_srf, xpos+thick, ypos+thick, \
					xpos+thick, ypos+ysiz-thick, (0, 0, 0))
			
			# D
			if maze[x, y, 2] == 0:	
				pygame.gfxdraw.line(maze_srf, xpos+thick, ypos+ysiz-thick, \
					xpos+xsiz-thick, ypos+ysiz-thick, (0, 0, 0))
				
			# R
			if maze[x, y, 3] == 0:	
				pygame.gfxdraw.line(maze_srf, xpos+xsiz-thick, ypos+thick, \
					xpos+xsiz-thick, ypos+ysiz-thick, (0, 0, 0))

			if show_visits:
				if maze[x, y, 4] == 1:
					pygame.gfxdraw.circle(maze_srf, xpos + (xsiz/2), ypos + (ysiz/2), 1, (0, 255, 0))	

	window.blit(maze_srf, (0, 0))
	pygame.display.flip()

def render_path(window, path_srf, solution):
	xsiz = scrw / num_cols
	ysiz = scrh / num_rows
	
	last = (xsiz/2, ysiz/2)
	
	for node in solution:
		xpos = ((node[0] + 1) * xsiz) - (xsiz/2)
		ypos = ((node[1] + 1) * ysiz) - (ysiz/2)
		pygame.gfxdraw.line(path_srf, last[0], last[1], xpos, ypos, (255, 0, 0))
	
		window.blit(path_srf, (last[0], last[1]), (last[0], last[1],  xpos, ypos))
		pygame.display.update()
		
		last = (xpos, ypos)

def gen_maze():
	M = np.zeros((num_rows,num_cols,5), dtype=np.uint8)
	# Set starting row and column
	r = 0
	c = 0
	history = None 
	history = [(r,c)] # The history is the 

	# Trace a path though the cells of the maze and open walls along the path.
	# We do this with a while loop, repeating the loop until there is no history, 
	# which would mean we backtracked to the initial start.
	while history:
		M[r,c,4] = 1 # designate this location as visited
		# check if the adjacent cells are valid for moving to
		check = []
		if c > 0 and M[r,c-1,4] == 0:
			check.append('L')  
		if r > 0 and M[r-1,c,4] == 0:
			check.append('U')
		if c < num_cols-1 and M[r,c+1,4] == 0:
			check.append('R')
		if r < num_rows-1 and M[r+1,c,4] == 0:
			check.append('D')    
    
		if len(check): # If there is a valid cell to move to.
			# Mark the walls between cells as open if we move
			history.append([r,c])
			move_direction = random.choice(check)
			if move_direction == 'L':
				M[r,c,0] = 1
				c = c-1
				M[r,c,2] = 1
			if move_direction == 'U':
				M[r,c,1] = 1
				r = r-1
				M[r,c,3] = 1
			if move_direction == 'R':
				M[r,c,2] = 1
				c = c+1
				M[r,c,0] = 1
			if move_direction == 'D':
				M[r,c,3] = 1
				r = r+1
				M[r,c,1] = 1
		else: # If there are no valid cells to move to.
			#retrace one step back in history if no move is possible
			r,c = history.pop()
    
         
	# Open the walls at the start and finish
	#M[0,0,0] = 1
	#M[num_rows-1,num_cols-1,2] = 1

	# reset the visited flag
	for y in range(0, num_rows):
		for x in range(0, num_cols):
			M[x, y, 4] = 0;

	return M

def solve(maze, solution):
	global run	
	global max	
		
	if len(solution) == 0:
		solution.append((0,0))
	else:
		found = False
		node = solution[len(solution)-1]

		if (maze[node[0], node[1], 0] == 1) and (node[1] > 0) and not found:
			# up - 0
			if maze[node[0], node[1]-1, 4] == 0:
				solution.append((node[0], node[1]-1))
				maze[node[0], node[1]-1, 4] = 1;
				found = True

		if (maze[node[0], node[1], 1] == 1) and (node[0] > 0) and not found:
			# left - 1
			if maze[node[0]-1, node[1], 4] == 0:
				solution.append((node[0]-1, node[1]))
				maze[node[0]-1, node[1], 4] = 1;
				found = True

		if (maze[node[0], node[1], 2] == 1) and (node[1] * (scrh/num_rows) < scrh) and not found:
			# down - 2
			if maze[node[0], node[1]+1, 4] == 0:
				solution.append((node[0], node[1]+1))
				maze[node[0], node[1]+1, 4] = 1
				found = True

		if (maze[node[0], node[1], 3] == 1) and (node[0] * (scrw/num_cols) < scrw) and not found:
			# right - 3
			if maze[node[0]+1, node[1], 4] == 0:
				solution.append((node[0]+1, node[1]))
				maze[node[0]+1, node[1], 4] = 1
				found = True

		if not found:
			solution.pop()

	if len(solution) > max:
		max = len(solution)

	current = solution[len(solution)-1]
	if current[0] == num_cols-1 and current[1] == num_rows-1:
		print("done")
		print(str(len(solution)) + " moves.")
		print("max: " + str(max))
		run = 0

	return maze, solution

def read_keyb():
	global run
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				run = False

def main():
	solution = []
	window, maze_srf, path_srf = init()
	maze = gen_maze()

	pygame.mouse.set_visible(False)

	render_maze(window, maze_srf, maze)
	
	while run:
		read_keyb()
		maze, solution = solve(maze, solution)

	render_path(window, path_srf, solution)
	time.sleep(5)

	pygame.mouse.set_visible(True)

import cProfile as profile

if __name__ == "__main__":
	profile.run('main()')
	#main()
	
