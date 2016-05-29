#!/usr/bin/env python

import pygame
import pygame.gfxdraw
from pygame.locals import *
import time
import random
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm

scrw = 800
scrh = 600

num_rows = 40
num_cols = 40

thick = 0

window = None
background = None

def init():
		pygame.init()
		#window = pygame.display.set_mode((640, 480), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)
		window = pygame.display.set_mode((scrw, scrh), pygame.DOUBLEBUF)
		pygame.display.set_caption('Maze')
		background = pygame.Surface(window.get_size())
		background.fill((0, 255, 0))
	
		#print(pygame.display.Info())

		window.blit(background, (0, 0))
		pygame.display.flip()

		return window, background
	
def run(window, background, M):
	background.fill((255, 255, 255))

	#pygame.gfxdraw.line(self.background, 0, 0, scrw, scrh, (0, 0, 0))

	xsiz = scrw / num_cols
	ysiz = scrw / num_rows
		
	for y in range(0, num_rows):
		for x in range(0, num_cols):
			xpos = x * xsiz
			ypos = y * ysiz
				
			#pygame.gfxdraw.line(self.background, xpos, ypos, xpos+xsiz, ypos+ysiz, (255, 0, 0))
			#pygame.gfxdraw.line(self.background, xpos+xsiz, ypos, xpos, ypos+ysiz, (255, 0, 0))
			
			# U	
			if M[x, y, 0] == 0:
				pygame.gfxdraw.line(background, xpos+thick, ypos+thick, xpos+xsiz-thick, ypos+thick, (0, 0, 0))
			
			# L
			if M[x, y, 1] == 0:	
				pygame.gfxdraw.line(background, xpos+thick, ypos+thick, xpos+thick, ypos+ysiz-thick, (0, 0, 0))
			
			# D
			if M[x, y, 2] == 0:	
				pygame.gfxdraw.line(background, xpos+thick, ypos+ysiz-thick, xpos+xsiz-thick, ypos+ysiz-thick, (0, 0, 0))
				
			# R
			if M[x, y, 3] == 0:	
				pygame.gfxdraw.line(background, xpos+xsiz-thick, ypos+thick, xpos+xsiz-thick, ypos+ysiz-thick, (0, 0, 0))


			#pygame.gfxdraw.circle(self.background, xpos, ypos, 10, (0, 255, 0))	

	window.blit(background, (0, 0))
	pygame.display.flip()

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
	M[0,0,0] = 1
	M[num_rows-1,num_cols-1,2] = 1

	return M

def main():
	window, background = init()
	for n in range(0, 50):
		maze = gen_maze()
		run(window, background, maze)
		time.sleep(1)

if __name__ == "__main__":
	main()
	
