'''
	===========   ATIVIDADE DE INTRODUCAO A ROBOTICA :: IA EM ROBOTICA MOVEL   =================
		Simulacao de um agente chegando ao objetivo sem colidir com um obstaculo. Este script
	contem as classes Enviroment, Robot e Obstacle. 

	Joao Marcello, 2022
'''

import numpy as np
import random
import os
import time
import platform

SO = platform.system()

#=============================================================================================+
#                                      CONSTANTES                                             |
#=============================================================================================+

NAME = {'vazio' : 0, 'agente' : 1, 'obstaculo' : 2, 'goal' : 3}

ACTION = { 'stop' :  0,
			'move_up' : 1,
			'move_left_up' : 2,
			'move_left' : 3,
			'move_left_down' : 4,
			'move_down' : 5,
			'move_right_down' : 6,
			'move_right' : 7,
			'move_right_up' : 8 
		}
ACTION2 = { 0 : 'stop',
			1 : 'move_up',
			2 : 'move_left_up',
			3 : 'move_left',
			4 : 'move_left_down',
			5 : 'move_down',
			6 : 'move_right_down',
			7 : 'move_right',
			8 : 'move_right_up'
		}

def get_symbol(c):
	def switch(arg=0):
		s = {
			-1 : '-',
			0: ' ',  # espaco vazio
			1: 'A',  # agente
			2: 'O',  # obstaculo
			3: 'X',  # objetivo
		}
		return s[arg]
	return switch(c)

#=========================================================================================================


#=============================================================================================+
#                                      CLASSES                                                |
#=============================================================================================+

class Point:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y= y

	def equals(self, p): return self.x == p.x and self.y == p.y

	def equals_x(self, p): return self.x == p.x

	def equals_y(self, p): return self.y == p.y

#=========================================================================================================


class Robot:
	def __init__(self, enviroment, x=1, y=3):
		self.pos = Point(x, y)
		self.initialPos = Point(x, y)
		self.action = ACTION2[ACTION['stop']]
		enviroment.change(self.pos.x, self.pos.y, NAME['agente'])

	# Coloca o agente na posicao inicial
	def reset(self, env):
		self.setPosition(self.initialPos.x, self.initialPos.y, env)
	
	def setPosition(self, x, y, env):
		env.change(self.pos.x, self.pos.y, NAME['vazio'])
		self.pos = Point(x, y)
		env.change(self.pos.x, self.pos.y, NAME['agente'])

	def move_right(self, env):
		if self.pos.x < env.n - 1: 
			self.setPosition(self.pos.x + 1, self.pos.y, env)

	def move_left(self, env):
		if self.pos.x > 0: 
			self.setPosition(self.pos.x - 1, self.pos.y, env)

	def move_up(self, env):
		if self.pos.y > 0: 
			self.setPosition(self.pos.x, self.pos.y - 1, env)

	def move_down(self, env):
		if self.pos.y < env.m - 1: 
			self.setPosition(self.pos.x, self.pos.y + 1, env)

	def move_left_up(self, env):
		if self.pos.x > 0 and self.pos.y > 0: 
			self.setPosition(self.pos.x - 1, self.pos.y - 1, env)

	def move_left_down(self, env):
		if self.pos.x > 0 and self.pos.y < env.m - 1: 
			self.setPosition(self.pos.x - 1, self.pos.y + 1, env)

	def move_right_up(self, env):
		if self.pos.x < env.n - 1 and self.pos.y > 0: 
			self.setPosition(self.pos.x + 1, self.pos.y - 1, env)

	def move_right_down(self, env):
		if self.pos.x < env.n - 1 and self.pos.y < env.m - 1: 
			self.setPosition(self.pos.x + 1, self.pos.y + 1, env)

	def stop(self):
		return True

	def move(self, action, env):
		self.action = ACTION2[action]

		if action == ACTION['stop']: return self.stop()
		if action == ACTION['move_up']: return self.move_up(env)
		if action == ACTION['move_left_up']: return self.move_left_up(env)
		if action == ACTION['move_left']: return self.move_left(env)
		if action == ACTION['move_left_down']: return self.move_left_down(env)
		if action == ACTION['move_down']: return self.move_down(env)
		if action == ACTION['move_right_down']: return self.move_right_down(env)
		if action == ACTION['move_right']: return self.move_right(env)
		if action == ACTION['move_right_up']: return self.move_right_up(env)

#=========================================================================================================


class Obstacle:
	def __init__(self, env, x=7, y=1):
		self.pos = Point(x, y)
		self.initialPos = Point(x, y)
		self.speed = random.randint(1,3)
		self.env = env
		self.env.change(self.pos.x, self.pos.y, NAME['obstaculo'])

	def reset(self):
		self.env.change(self.pos.x, self.pos.y, NAME['vazio'])
		self.pos = Point(self.initialPos.x, self.initialPos.y)
		self.env.change(self.pos.x, self.pos.y, NAME['obstaculo'])

	def move2(self):
		self.env.change(self.pos.x, self.pos.y, NAME['vazio'])

		for i in range(self.speed):
			self.pos.y = (self.pos.y + 1) % self.env.m
			if self.env.collide():
				break

		self.env.change(self.pos.x, self.pos.y, NAME['obstaculo'])
		self.speed = random.randint(1,3)

	def move3(self):
		from time import sleep

		for i in range(self.speed):
			self.env.change(self.pos.x, self.pos.y, NAME['vazio'])
			self.pos.y = (self.pos.y + 1) % self.env.m

			if self.env.collide():
				break

			self.env.change(self.pos.x, self.pos.y, NAME['obstaculo'])
			
			if self.env.showExecution:
				self.env.show()
				sleep(0.2)
		self.speed = random.randint(1,3)


#=========================================================================================================


class Enviroment:
	def __init__(self, linhas=9, colunas=14, show=True):
		self.m = linhas
		self.n = colunas
		self.mat = np.zeros((self.m,self.n))
		self.goal = Point(11, 3)
		self.mat[self.goal.y][self.goal.x] = NAME['goal']
		self.episode = 0
		self.stepCount = 0
		self.showExecution = show
		self.info = ""
		self.obstacle = Obstacle(self)
		self.robot = Robot(self)


	def reset(self):
		self.obstacle.reset()
		self.robot.reset(self)
		self.mat[self.goal.y][self.goal.x] = NAME['goal']
		return self.get_state()

	def reach_objective(self):
		return self.robot.pos.equals(self.goal)

	def collide(self):
		return self.robot.pos.equals(self.obstacle.pos)

	def step(self, action):
		r = self.robot.move(action, self)

		if self.showExecution and not self.collide():
			self.show()
			time.sleep(0.2)

		if not self.collide():
			self.obstacle.move3()

		st = self.get_state()
		rw = self.get_reward(st)
		done = self.done()

		return st, rw, done

	def change(self, x, y, value):
		self.mat[y][x] = value

	def get_value(self, x, y):
		return self.mat[y][x]

	# Exibe o mapa na tela do console
	def show(self):
		if not self.showExecution: return None

		os.system('cls' if SO =='Windows' else 'clear')

		print(">>> PASSO: ", self.stepCount+1, "  EPISODIO: ", self.episode+1, "  (" + self.robot.action + ")",sep="")
		if not self.info == "": print(self.info)

		[print(' ' if (i) % 4 == 0 else '_', end='') for i in range(self.n * 4 + 1)]
		print()

		for i in range(self.m):  # linha
			pl = "| "
			for j in range(self.n):
				pl += get_symbol(self.mat[i][j]) + " | "
			
			[print('|' if (i) % 4 == 0 else ' ', end='') for i in range(self.n * 4 + 2)]
			print()
			print(pl)
			if i == self.m-1 or True:
				[print('|' if (i) % 4 == 0 else '_', end='') for i in range(len(pl)-1)]
				print()#'''

	# Calcula a distancia entre dois pontos
	def distance(self, p1, p2):
		p1 = Point(p1.x, p1.y)

		if p1.x == p2.x or p1.y == p2.y: return abs(p1.x - p2.x) + abs(p1.y - p2.y)
		
		if p1.x < p2.x:
			p1.x += 1
		else:
			p1.x -= 1

		if p1.y < p2.y:
			p1.y += 1
		else:
			p1.y -= 1 #'''

		return 1 + self.distance(p1, p2)

	# Retorna a posicao relativa de um ponto
	def getPosition(self, p):
		return (p.y * self.n) + p.x

	# Se ja eh o fim do episodio atual (quando ha colisao ou o agente chega ao objetivo)
	def done(self):
		return self.reach_objective() or self.collide()

	def getVerticalDist(self):
		return (self.obstacle.pos.y - self.robot.pos.y) + (self.m-1)

	# Retorna o estado atual do ambiente
	def get_state(self):
		return np.array([
			# Posicao do agente
			self.getPosition(self.robot.pos), 

			# Distancia entre o agente e o objetivo                 
			self.distance(self.robot.pos, self.goal),

			# Distancia do agente ate o obstaculo                       
			self.distance(self.robot.pos, self.obstacle.pos),

			# Posicao do obstaculo 
			self.obstacle.pos.y               
		])

	# Retorna a recompensa
	def get_reward(self, states):
		if self.reach_objective(): return 1. 
		if self.collide(): return -1.
		return -(10. ** -10)#'''

#=========================================================================================================

