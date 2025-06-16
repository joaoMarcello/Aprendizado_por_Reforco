'''
	===========   ATIVIDADE DE INTRODUCAO A ROBOTICA :: IA EM ROBOTICA MOVEL   =================
		Simulacao de um agente chgando ao objetivo sem colidir com um obstaculo. Este script
	eh responsavel por testar o resultado do treinamento, exibindo algumas metricas ao final
	da execucao. 

	Joao Marcello, 2022
'''

import numpy as np
from utils import *
import time
import os
import pickle
import argparse

parser = argparse.ArgumentParser(description='Testa o aprendizado do agente.')
parser.add_argument('--show', type=str, default='true',help="Use 'true' para exibir a execucao do programa.")
args = parser.parse_args()

#=============================================================================================+
#                                      CONSTANTES                                             |
#=============================================================================================+

# Quantidade de episodios
MAX_EPISODES = 50000

# Se deve mostrar a execucao do programa
SHOW_EXECUTION = True if args.show == 'true' or args.show == 'True' or args.show == 't' else False

# Constante usada para a politica epsilon-greedy
epsilon = 0.

# Numero maximo de passos em cada episodio
max_steps = 2000

#=============================================================================================+
#                                         FUNCOES                                             |
#=============================================================================================+

# Carrega a matriz Q
def load_Q():
	file = open('q', 'rb')
	data = pickle.load(file)
	file.close()
	return data

'''	Escolhe a proxima acao do agente atraves da politica epsilon-greedy.
	- Recebe:
		- Q: a matriz que mapeia estado e acao atual para um valor
		- state: o estado atual do ambiente
	- Retorna:
		- A acao que deve ser executada pelo agente (um valor inteiro)
'''
def next_action(Q, state):
	def aux(arr, actual=0):
		arr = arr[state[actual]]

		if actual + 1 >= len(state):
			return arr
		else:
			return aux(arr, actual=actual+1)			

	action = 0

	if random.randint(0,1000) < 1000 * epsilon:
		action = random.randint(0,8)
	else:
		action = np.argmax(aux(Q))
	return action
#=============================================================================================+


#=============================================================================================+
#                                         MAIN                                                |
#=============================================================================================+
if __name__ == '__main__':

	env = Enviroment(show=SHOW_EXECUTION)

	state = env.reset()

	try:
		Q = load_Q()
	except:
		print(">>> Matriz Q nao encontrada.\n>>> Programa finalizado.\n>>> Pressione 'Enter' para continuar.")
		input()
		MAX_EPISODES = -1

	print(">>> Executando os testes (", MAX_EPISODES," episodios)...", sep='')

	# Vezes que o agente conseguiu chegar no objetivo
	win = 0
	# Das vezes que chegou ao objetivo, quantas precisou desviar do melhor caminho
	not_perfect = 0

	while env.episode < MAX_EPISODES:

		action1 = next_action(Q, state)
		
		state, reward, done = env.step(action1)	
		
		env.info = ">>> GOAL:  " + str(win) + "/" + str(env.episode)

		if done or env.stepCount >= max_steps:
			if env.reach_objective():
				win += 1
				if env.stepCount + 1 > env.distance(env.robot.initialPos, env.goal): not_perfect += 1

				if SHOW_EXECUTION:
					print("\n                CONCLUIDO EM ", env.stepCount+1, " PASSOS !")
					time.sleep(1.)
			
				state = env.reset()
				env.episode += 1
				env.stepCount = 0
			else:
				if SHOW_EXECUTION:
					print("\n                  COLISAO !")
					time.sleep(1.)
				state = env.reset()
				env.stepCount = 0
				env.episode += 1
		else:
			env.stepCount += 1

	if MAX_EPISODES > 0:
		erro = (MAX_EPISODES-win) + not_perfect

		# Porcentagem de vezes que chegou ao objetivo
		percent_win = 100./MAX_EPISODES * win

		# Pocentagem de vezes que colidiu
		percent_collide = 100./MAX_EPISODES * (MAX_EPISODES-win)

		# Porcentagem das vezes que chegou ao objetivo, quantas precisou desviar do melhor caminho
		percent_not_perfect = 100./win * not_perfect

		print("\n>>> Quantidade de episodios: ", MAX_EPISODES)
		print(">>> Total de chegada sem colisao:  ", win, " (", "{:0.2f}".format(percent_win), " %)",sep='')
		print(">>> Total de colisoes:  ", MAX_EPISODES-win, " (",  "{:0.2f}".format(percent_collide), " %)", sep= '')
		print(">>> Imperfeitos: ", not_perfect, " (",  "{:0.2f}".format(percent_not_perfect), " %)", sep= '')

		
