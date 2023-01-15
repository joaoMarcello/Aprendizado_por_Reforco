'''
	===========   ATIVIDADE DE INTRODUCAO A ROBOTICA :: IA EM ROBOTICA MOVEL   =================
		Simulacao de um agente chegando ao objetivo sem colidir com um obstaculo. Este script
	eh responsavel por realizar o treinamento atraves do aprendizado por reforco (SARSA). 

	Joao Marcello, 2022
'''
import time
import os
import random
import numpy as np
from utils import *
import pickle

#=============================================================================================+
#                                      CONSTANTES                                             |
#=============================================================================================+

# Se deve mostrar a execucao do programa
SHOW_EXECUTION = False

# Quantidade de episodios que devem ocorrer para salvar a matriz Q 
SAVE_EACH = 25000

# Atraso na visualizacao (somente usada caso SHOW_EXECUTION seja True)
DELAY = 0.#pow(2, -5)

# Numero de episodios 
total_episodes = 100000

# Numero maximo de passos em cada episodio
max_steps = 20000

# Constante para a politica epsilon-greedy
epsilon = 0.2

# Constante alpha do algoritmo SARSA
alpha = 0.05

# Constante gamma do algoritmo SARSA
gamma = 0.8

#=============================================================================================+
#                                         FUNCOES                                             |
#=============================================================================================+

def createQ(env, n_actions=9):
	def max_distance(p):
		v = np.array([ env.distance(Point(0,0), p), env.distance(Point(0,env.m-1), p),
			env.distance(Point(env.n-1,0), p), env.distance(Point(env.n-1, env.m-1), p)   ])
		return v[np.argmax(v)] + 1

	Q = np.zeros( (
		 # posicao do agente
		env.m * env.n,

		# distancia entre o agente e o objetivo                 
		max_distance(env.goal),

		# distancia do agente ate o obstaculo
		max_distance(Point(env.obstacle.pos.x, env.m-1)),   

		# posicao y do obstaculo
		env.m,

		# quantidade de acoes
		n_actions
	), dtype=np.float32)

	return Q

'''	Escolhe a proxima acao do agente atraves da politica epsilon-greedy.
	- Recebe:
		- Q: a matriz que mapeia estado e acao atual para um valor
		- state: o estado atual do ambiente
	- Retorna:
		- A acao que deve ser executada pelo agente (um valor inteiro)
'''
def choose_action(Q, states):
	def aux(arr, actual=0):
		arr = arr[states[actual]]

		if actual + 1 >= len(states):
			return arr
		else:
			return aux(arr, actual=actual+1)			

	action = 0

	if random.randint(0, 1000) < 1000 * epsilon:
		action = random.randint(0,8)
	else:
		action = np.argmax(aux(Q))
		if ACTION['stop'] and get_value(Q, states, action) == 0.:
			action = random.randint(0,8)
	return action

# Retorna o vetor de acoes da matriz Q, dado um estado
def aux2(arr, states, actual=0):
		arr = arr[states[actual]]

		if actual + 1 >=  len(states):
			return arr
		else:
			return aux2(arr, states=states, actual=actual+1)

# Retorna o valor de Q dado um estado e uma acao.
def get_value(Q, states, action):
	return aux2(Q, states)[action]

# Altera o valor de Q dado um estado, uma acao e o valor
def set_value(Q, states, action, value):
	aux2(Q, states)[action] = value

# Equacao de atualizacao da matriz Q (de acordo com o algoritmo SARSA)
def update(Q, state, state2, reward, action, action2):
	predict = get_value(Q, state, action)
	target = reward + gamma *  get_value(Q, state2, action2)
	set_value(Q, state, action, get_value(Q, state, action) + alpha * (target - predict) )

# Salva a matriz Q em disco em um arquivo de nome 'q'.
def save_Q(Q):
	file = open('q', 'wb')
	pickle.dump(Q, file)
	file.close()

# Carrega a matriz Q do disco
def load_Q():
	file = open('q', 'rb')
	data = pickle.load(file)
	file.close()
	return data
#=============================================================================================+


#=============================================================================================+
#                                         MAIN                                                |
#=============================================================================================+

if __name__ == '__main__':

	env = Enviroment(show=SHOW_EXECUTION)

	Q = createQ(env)

	try:
		Q = load_Q()
		print("\n>>> Matriz Q carregada com sucesso! O treinamento sera retomado.\n>>> Pressione 'Enter' para continuar.")
		input()
	except:
		print("\n>>> Matriz Q nao localizada. O treinamento acontecera do inicio.")
		print(">>> Pressione 'Enter' para continuar.")
		input()

	print(">>> Treinando com ", total_episodes," episodios. Aguarde...", sep='')

	t = np.zeros(shape=(total_episodes), dtype=int) #[]

	# Comecando o aprendizado atraves do algoritmo SARSA
	for episode in range(total_episodes):
		env.episode = episode
		env.stepCount = 0

		state1 = env.reset()
		action1 = choose_action(Q, state1)

		if not SHOW_EXECUTION:
			if env.episode % 1000 == 0:
				print(">>> episode:  ", env.episode, " / ", total_episodes, sep='')#'''

		while env.stepCount < max_steps:
			# Visualizando o treinamento
			env.show()
			
			# Pegando o proximo estado
			state2, reward, done = env.step(action1)

			# Escolhendo a proxima acao
			action2 = choose_action(Q, state2)
			
			# Atualizando o valor Q
			update(Q, state1, state2, reward, action1, action2)

			state1 = state2
			action1 = action2

			if SHOW_EXECUTION:
				time.sleep(DELAY)
			
			# Atualizando o passo atual
			env.stepCount += 1
			
			# Se houve colisao ou o agente chegou ao objetivo 
			if done:
				break
				

		t[episode] = env.stepCount

		if (env.episode % SAVE_EACH == 0 and env.episode != total_episodes-1 and env.episode != 0) or env.episode == total_episodes-1:
			print(">>> Salvando matriz Q...")
			save_Q(Q)  
			print(">>> Salvo no arquivo 'q'.\n")#'''

	'''max_value = t[np.argmax(t)]
	print("Max step: ", max_value)

	ss = 10 #int(total_episodes*0.01)
	y = t[:3000:ss]
	x = [i * ss for i in range(len(y))]

	plt.plot(x, y)
	plt.ylabel('Quantidade de passos')
	plt.xlabel('Episodio')
	plt.show()#'''

	print(">>> Programa finalizado. A matriz foi salva no arquivo 'q'.")

