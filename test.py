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

num_rows = 20
num_cols = 20

M = np.zeros((num_rows,num_cols,5), dtype=np.uint8)

class View:
	def __init__(self):
		pygame.init()
		#self.window = pygame.display.set_mode((640, 480), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)
		self.window = pygame.display.set_mode((scrw, scrh), pygame.DOUBLEBUF)
		pygame.display.set_caption('Maze')
		self.background = pygame.Surface(self.window.get_size())
		self.background.fill((0, 255, 0))
	
		#print(pygame.display.Info())

		self.window.blit(self.background, (0, 0))
		pygame.display.flip()
	
	def run(self):
		self.background.fill((255, 255, 255))

		#pygame.gfxdraw.line(self.background, 0, 0, scrw, scrh, (0, 0, 0))

		xsiz = scrw / num_cols
		ysiz = scrw / num_rows
		
		for y in range(0, num_rows):
			for x in range(0, num_cols):
				xpos = x * xsiz
				ypos = y * ysiz
				
				pygame.gfxdraw.line(self.background, xpos, ypos, xpos+xsiz, ypos+ysiz, (255, 0, 0))
				pygame.gfxdraw.line(self.background, xpos+xsiz, ypos, xpos, ypos+ysiz, (255, 0, 0))
			
				# L	
				if M[x, y, 0] == 0:
					pygame.gfxdraw.line(self.background, xpos, ypos, xpos+xsiz, ypos, (0, 0, 0))
			
				# U
				if M[x, y, 1] == 0:	
					pygame.gfxdraw.line(self.background, xpos, ypos, xpos, ypos+ysiz, (0, 0, 0))
			
				# R
				if M[x, y, 2] == 0:	
					pygame.gfxdraw.line(self.background, xpos, ypos+ysiz, xpos+xsiz, ypos+ysiz, (0, 0, 0))
			
				# D
				if M[x, y, 3] == 0:	
					pygame.gfxdraw.line(self.background, xpos+xsiz, ypos, xpos+xsiz, ypos+ysiz, (0, 0, 0))

				pygame.gfxdraw.circle(self.background, xpos, ypos, 10, (0, 255, 0))	

		self.window.blit(self.background, (0, 0))
		pygame.display.flip()

def clear_maze():
	for x in range(0, num_cols):
		for y in range(0, num_rows):
			for n in range(0, 4):
				M[x, y, n] = 0

def gen_maze():
	# Set starting row and column
	r = 0
	c = 0
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

def main():
	gen_maze()
	view = View()
	for n in range(0, 10):
		view.run()
		time.sleep(1)

if __name__ == "__main__":
	main()
	
