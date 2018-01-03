import sys, pygame
import random
import time
from operator import attrgetter

FPS        	= 10

#cores
AZUL 	 	= (0,0,139)
VERMELHO 	= (255,0,0)
CINZA 	 	= (105,105,105)
VERDE 	 	= (0,100,0)
PRETO 	 	= (0,0,0)
BRANCO 	 	= (255,255,255)

LARANJA  	= (255,165,0)
ROSA 	 	= (255,20,147)
AZUL_CLARO 	= (0,191,255)

NUM_LINHAS  = 64
NUM_COLUNAS = 32

# Tipos de movimento
ESCAPE    	= 1
ALEATORIO 	= 0
ATAQUE    	= 2

DIR   		= 1
ESQ   		= 2
CIMA  		= 3
BAIXO 		= 4

#deslocamento tela para colocar o score
DESLOCAMENTO = 40

matrizLogica = [ [ None for j in range(NUM_COLUNAS) ] for i in range(NUM_LINHAS) ]


class Presa():
	
	def __init__(self, vida):

		self.vida  = vida
		self.lider = True

class Pacman(Presa):

	def __init__(self):
		Presa.__init__(self, 3)
		self.pontuacao = 0

class Fantasma():

	idd = 0
	def __init__(self, vida, percepcao, idd):

		self.vida 		= vida
		self.percepcao	= percepcao
		self.idd 		= idd

class Rastro():

	def __init__(self, presa):
		self.duracao = 10
		self.presa   = presa 

class Parede():
	pass
	
class Pilula():
	pass

class PilulaEspecial():
	pass

class Tela(object):

	def __init__(self):

		#pega tamanho da tela automaticamente
		#self.displayInfo = pygame.display.Info()
		#self.tela = pygame.display.set_mode((self.displayInfo.current_w,self.displayInfo.current_h))

		self.larguraTela = 320  #768
		self.alturaTela = 640 + DESLOCAMENTO	#640 ADD + 40 px para colocar o score na tela

		self.tela = pygame.display.set_mode((self.larguraTela,self.alturaTela))

		#calcula largura e altura ideal da rect do peixe e do tubarao conforme dimensao da tela 
		self.larguraRect = self.larguraTela//NUM_COLUNAS
		self.alturaRect = self.alturaTela//NUM_LINHAS

		print("Largura rect: ",self.larguraRect)
		print("Altura rect: ",self.alturaRect)

		pygame.display.set_caption('PACMAN')


	def blitarJogo(self):
		for i in range(NUM_LINHAS):
			for j in range(NUM_COLUNAS):

				if type(matrizLogica[i][j]) == None or matrizLogica[i][j] is None:
					pygame.draw.rect(self.tela,PRETO,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

				elif type(matrizLogica[i][j]) == Pacman or matrizLogica[i][j] is Pacman:
					pygame.draw.rect(self.tela,BRANCO,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

				elif type(matrizLogica[i][j]) == Fantasma or matrizLogica[i][j] is Fantasma:
					if matrizLogica[i][j].idd == 20:
						pygame.draw.rect(self.tela,LARANJA,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))
					elif matrizLogica[i][j].idd == 21:
						pygame.draw.rect(self.tela,ROSA,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))
					elif matrizLogica[i][j].idd == 22:
						pygame.draw.rect(self.tela,AZUL_CLARO,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

				elif type(matrizLogica[i][j]) == Pilula or matrizLogica[i][j] is Pilula:
					pygame.draw.rect(self.tela,CINZA,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

				elif type(matrizLogica[i][j]) == Parede or matrizLogica[i][j] is Parede:
					pygame.draw.rect(self.tela,AZUL,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

				elif type(matrizLogica[i][j]) == PilulaEspecial or matrizLogica[i][j] is PilulaEspecial:
					pygame.draw.rect(self.tela,VERDE,(j*self.larguraRect,i*self.alturaRect,self.larguraRect,self.alturaRect))

	def exibirScoreVida(self,score,vida):

		texto0 	= "Score:"
		texto1	= str(score)

		texto2 	= "Vida:"
		texto3	= str(vida)
		
		fonte 	= pygame.font.Font("fonte.ttf",17)

		texto0 	= fonte.render(texto0, True, VERMELHO)
		texto1	= fonte.render(texto1, True, VERMELHO)
		texto2 	= fonte.render(texto2, True, VERMELHO)
		texto3	= fonte.render(texto3, True, VERMELHO)
	
		self.tela.blit(texto0, (10,650))
		self.tela.blit(texto1, (80,650))
		self.tela.blit(texto2, (120,650))
		self.tela.blit(texto3, (180,650))

		pass				

class Game(object):

	def __init__(self):
		self.score = 0
		self.vida = 3
		pass

	def atualizarScore(self):
		self.score += 1
		pass

	def atualizarVida(self):
		self.vida -= 1
		
		if self.vida == 0:
			return True
		else:
			return False

	def andar(self, eixo, sit, i, j):

		if eixo == 'x': 
			if sit == '+':
				if j+1 < NUM_LINHAS - 1 and (matrizLogica[i][j+1] == None or type(matrizLogica[i][j+1]) is Pilula):

					aux					 = matrizLogica[i][j+1]
					matrizLogica[i][j+1] = matrizLogica[i][j]
					matrizLogica[i][j]	 = aux

			elif sit == '-':
				if j-1 > 0 and (matrizLogica[i][j-1] == None or type(matrizLogica[i][j-1]) is Pilula):

					aux					 = matrizLogica[i][j-1]
					matrizLogica[i][j-1] = matrizLogica[i][j]
					matrizLogica[i][j] 	 = aux

		if eixo == 'y':
			if sit == '+':
				if i+1 < NUM_LINHAS - 1 and (matrizLogica[i+1][j] == None or type(matrizLogica[i+1][j]) is Pilula):
			
					aux					 = matrizLogica[i+1][j]
					matrizLogica[i+1][j] = matrizLogica[i][j]
					matrizLogica[i][j]   = aux

			elif sit == '-':

				if i-1 > 0 and (matrizLogica[i-1][j] == None or type(matrizLogica[i-1][j]) is Pilula):

					aux					 = matrizLogica[i-1][j]
					matrizLogica[i-1][j] = matrizLogica[i][j]
					matrizLogica[i][j] 	 = aux

		


	def seguir(self):


		l = i 
		c = j

		agente 	= type(matrizLogica[l][c])
		perc 	= matrizLogica[l][c].percepcao

		itCol = 0
		itLin = 0

		#itera colunas para a direita
		while c < NUM_COLUNAS -1 and itCol < perc:

			if c != j:

				if type(matrizLogica[l][c]) is Rastro and agente is Pacman:
					
					if matrizLogica[i][j+1] is None:
						matrizLogica[i][j+1] = matrizLogica[i][j]
						matrizLogica[i][j] 	 = None

						#print("wl 1.1")
						return True
					else:
						return False

				elif type(matrizLogica[l][c]) is Rastro and agente is Fantasma:
					
					if matrizLogica[i][j+1] is None:
						matrizLogica[i][j+1] = matrizLogica[i][j]
						matrizLogica[i][j] 	 = None
						#print("wl 1.2")
						return True
					else:
						return False
				else:
					c+=1
					itCol+=1
			else:
				c+=1
					

		itCol = 0
		c = j

		#itera colunas para a esquerda
		while c > 0 and itCol < perc:
			if c != j:
				if type(matrizLogica[l][c]) is Rastro and agente is Pacman:
					
					if matrizLogica[i][j-1] is None:
						matrizLogica[i][j-1] = matrizLogica[i][j]
						matrizLogica[i][j] 	 = None
						return True
					else:
						return False
				elif type(matrizLogica[l][c]) is Rastro and agente is Fantasma:
					
					if matrizLogica[i][j-1] is None:
						matrizLogica[i][j-1] = matrizLogica[i][j]
						matrizLogica[i][j] 	 = None
						#print("wl 2.2")
						return True

					else:
						return False
				else:
					c-=1
					itCol+=1
			else:
				c-=1


		#itera linha para baixo
		while l < NUM_LINHAS -1 and itLin < perc:

			if l != i:
				if type(matrizLogica[l][c]) is Rastro and agente is Pacman:
					
					if matrizLogica[i+1][j] is None:
						matrizLogica[i+1][j] = matrizLogica[i][j]
						matrizLogica[i][j]   = None
						#print("wl 3.1")
						return True
					else:
						return False
				elif type(matrizLogica[l][c]) is Rastro and agente is Fantasma:
					if matrizLogica[i+1][j] is None:
						matrizLogica[i+1][j] = matrizLogica[i][j]
						matrizLogica[i][j] 	 = None
						#print("wl 3.2")
						return True
					else:
						return False
				else:
					l+=1
					itLin+=1
			else:
				l+=1

		itLin = 0
		l = i

		#itera linha para cima
		while l > 0 and itLin < perc:
			if l != i:
				if type(matrizLogica[l][c]) is Rastro and agente is Pacman:
					
					if matrizLogica[i-1][j] is None:
						matrizLogica[i-1][j] = matrizLogica[i][j]
						matrizLogica[i][j] 	 = None
						#print("wl 4.1")
						return True
					else:
						return False
				
				elif type(matrizLogica[l][c]) is Rastro and agente is Fantasma:
					if matrizLogica[i-1][j] is None:
						matrizLogica[i-1][j] = matrizLogica[i][j]
						matrizLogica[i][j] 	 = None
						#print("wl 4.2")
						return True
					else:
						return False
				else:
					l-=1
					itLin+=1
			else:
				l-=1

		return False

	def alcance(self,i,j):

		l = i 
		c = j

		if type(matrizLogica[l][c]) is Fantasma:

			agente 	= type(matrizLogica[l][c])
			perc 	= matrizLogica[l][c].percepcao

		else:

			agente 	= type(matrizLogica[l][c])
			perc 	= matrizLogica[l][c].percepcao

		itCol = 0
		itLin = 0

		#itera colunas para a direita
		while c < NUM_COLUNAS -1 and itCol < perc:

			if c != j:
				if type(matrizLogica[l][c]) == Pacman and agente is Fantasma:
					return ATAQUE,DIR
				else:
					c+=1
					itCol+=1
			else:
				c+=1
					

		itCol = 0
		c = j

		#itera colunas para a esquerda
		while c > 0 and itCol < perc:
			if c != j:
				if type(matrizLogica[l][c]) == Pacman and agente is Fantasma:
					return ATAQUE,ESQ
				else:
					c-=1
					itCol+=1
			else:
				c-=1


		#itera linha para baixo
		while l < NUM_LINHAS -1 and itLin < perc:

			if l != i:
				if type(matrizLogica[l][c]) == Pacman and agente is Fantasma:
					return ATAQUE,BAIXO
				else:
					l+=1
					itLin+=1
			else:
				l+=1

		itLin = 0
		l = i

		#itera linha para cima
		while l > 0 and itLin < perc:
			if l != i:
				if type(matrizLogica[l][c]) == Pacman and agente is Fantasma:
					return ATAQUE,CIMA
				else:
					l-=1
					itLin+=1
			else:
				l-=1

		return ALEATORIO

	def moverAgentes(self):
		sair = False
		vida = False
		for i in range(NUM_LINHAS):

			if sair:
				break

			for j in range(NUM_COLUNAS):
				if type(matrizLogica[i][j]) is Fantasma:    # Vê se é um fantasma e se ele vai atacar
					if self.alcance(i,j) == (ATAQUE, CIMA): # Também verifica as extremidades da matriz
						if i > 0:
							print(type(matrizLogica[i-1][j]))

							if type(matrizLogica[i-1][j]) == Pacman:
								vida 			   = self.atualizarVida()
								matrizLogica[1][1] = matrizLogica[i-1][j]
								matrizLogica[i-1][j] = matrizLogica[i][j]
								matrizLogica[i][j] = None
								return vida



							elif type(matrizLogica[i-1][j]) is not Parede:

								matrizLogica[i-1][j] = matrizLogica[i][j]
								matrizLogica[i][j]	 = None
								return vida

						elif i == 0:

							if type(matrizLogica[NUM_LINHAS-1][j]) is Pacman:
								vida 			   = self.atualizarVida()
								matrizLogica[1][1] = matrizLogica[NUM_LINHAS-1][j]
								matrizLogica[NUM_LINHAS-1][j] = matrizLogica[i][j]
								matrizLogica[i][j] = None
								return vida

							elif type(matrizLogica[NUM_LINHAS-1][j]) is not Parede:

								matrizLogica[NUM_LINHAS-1][j] = matrizLogica[i][j]
								matrizLogica[i][j]	 		  = None
								return vida

					elif self.alcance(i,j) == (ATAQUE, BAIXO):
						if i < NUM_LINHAS-1:

							if type(matrizLogica[i+1][j]) is Pacman:
								vida 			   = self.atualizarVida()
								matrizLogica[1][1] = matrizLogica[i+1][j]
								matrizLogica[i+1][j] = matrizLogica[i][j]
								matrizLogica[i][j] = None

								return vida

							elif type(matrizLogica[i+1][j]) is not Parede:
								print("Dif parede")

								matrizLogica[i+1][j] = matrizLogica[i][j]
								matrizLogica[i][j]	 = None

						elif i == NUM_LINHAS - 1:

							if type(matrizLogica[0][j]) is Pacman:
								vida 			   = self.atualizarVida()
								matrizLogica[1][1] = matrizLogica[0][j]
								matrizLogica[0][j] = matrizLogica[i][j]
								matrizLogica[i][j] = None

								return vida

							elif type(matrizLogica[0][j]) is not Parede:

								matrizLogica[0][j] 				 = matrizLogica[NUM_LINHAS-1][j]
								matrizLogica[NUM_LINHAS-1][j]	 = None

					elif self.alcance(i, j) == (ATAQUE, ESQ):
						if j > 0:
							if type(matrizLogica[i][j-1]) is Pacman:
								vida 			   = self.atualizarVida()
								matrizLogica[1][1] = matrizLogica[i][j-1]
								matrizLogica[i][j-1] = matrizLogica[i][j] #aqui
								matrizLogica[i][j] = None

								return vida

							elif type(matrizLogica[i][j-1]) is not Parede:

								matrizLogica[i][j-1] = matrizLogica[i][j]
								matrizLogica[i][j]	 = None

						elif j == 0:

							if type(matrizLogica[i][NUM_COLUNAS-1]) is Pacman:
								vida 			   = self.atualizarVida()
								matrizLogica[1][1] = matrizLogica[i][NUM_COLUNAS-1]
								matrizLogica[i][NUM_COLUNAS-1] = matrizLogica[i][j]
								matrizLogica[i][j] = None

								return vida

							elif type(matrizLogica[i][NUM_COLUNAS-1]) is not Parede :

								matrizLogica[i][NUM_COLUNAS-1] = matrizLogica[i][j]
								matrizLogica[i][j]	 		   = None

					elif self.alcance(i, j) == (ATAQUE, DIR):
						if j < NUM_COLUNAS-1:

							if type(matrizLogica[i][j+1]) is Pacman:
								vida 			   	 = self.atualizarVida()
								matrizLogica[1][1] 	 = matrizLogica[i][j+1]
								matrizLogica[i][j+1] = matrizLogica[i][j]
								matrizLogica[i][j] 	 = None

								return vida

							elif type(matrizLogica[i][j+1]) is not Parede:

								matrizLogica[i][j+1] = matrizLogica[i][j]
								matrizLogica[i][j]	 = None

						elif  j == NUM_COLUNAS-1:

							if type(matrizLogica[i][0]) is Pacman:
								vida 			   = self.atualizarVida()
								matrizLogica[1][1] = matrizLogica[i][0]
								matrizLogica[i][0] = matrizLogica[i][j]
								matrizLogica[i][j] = None

								return vida

							elif type(matrizLogica[i][0]) is not Parede :
								matrizLogica[i][0]   			 = matrizLogica[i][NUM_COLUNAS-1]
								matrizLogica[NUM_LINHAS-1][j]	 = None

					# Não tá atacando ninguém. Apenas seguindo o baile.
					else:
						eixo = random.choice('xy')
						sit  = random.choice('+-')
						self.andar(eixo, sit, i, j)
						#sair = True
						#break

		return vida
						
												


				
	def moverPacman(self,direcao):

		sair = False
		vida = False

		for i in range(NUM_LINHAS):
			for j in range(NUM_COLUNAS):

				if (type(matrizLogica[i][j]) == Pacman or matrizLogica[i][j] is Pacman) and direcao == [True,"RIGHT"]:

					if j+1 < NUM_COLUNAS:

						#caminho livre anda
						if type(matrizLogica[i][j+1]) == None or matrizLogica[i][j+1] is None:
							matrizLogica[i][j+1] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							sair 					= True
							break

						#caminho tem pilula, come pilula
						elif type(matrizLogica[i][j+1]) == Pilula or matrizLogica[i][j+1] is Pilula:
							matrizLogica[i][j+1] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							self.atualizarScore()
							print(self.score)
							sair 					= True
							break

						
						#caminho tem fantasma, perde vida
						elif type(matrizLogica[i][j+1]) == Fantasma or matrizLogica[i][j+1] is Fantasma:
							aux = matrizLogica[i][j]
							matrizLogica[i][j] 		 = matrizLogica[i][j+1]
							matrizLogica[i][j+1]	 = None 
							vida = self.atualizarVida()
							matrizLogica[1][1] 		 = aux
							sair = True
							break

						#caminho tem pilula especial
						elif type(matrizLogica[i][j+1]) == PilulaEspecial or matrizLogica[i][j+1] is PilulaEspecial:
							matrizLogica[i][j+1] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							
							#definir acao para pirula especial
							sair = True
							break


				elif (type(matrizLogica[i][j]) == Pacman or matrizLogica[i][j] is Pacman) and direcao == [True,"LEFT"]:
						

					if j > 0:

						#caminho livre anda
						if type(matrizLogica[i][j-1]) == None or matrizLogica[i][j-1] is None:
							matrizLogica[i][j-1] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							sair = True
							break

						#caminho tem pilula, come pilula
						elif type(matrizLogica[i][j-1]) == Pilula or matrizLogica[i][j-1] is Pilula:
							matrizLogica[i][j-1] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							self.atualizarScore()
							print(self.score)
							sair = True
							break

						#caminho tem fantasma, perde vida
						elif type(matrizLogica[i][j-1]) == Fantasma or matrizLogica[i][j-1] is Fantasma:
							#matrizLogica[i][j-1] 	= Fantasma(1, 10, matrizLogica[i][j-1].idd)
							aux = matrizLogica[i][j]
							matrizLogica[i][j] 		= matrizLogica[i][j-1]
							matrizLogica[i][j-1] 	= None
							vida 					= self.atualizarVida()
							matrizLogica[1][1] 		= aux
							sair = True
							break

						#caminho tem pilula especial
						elif type(matrizLogica[i][j-1]) == PilulaEspecial or matrizLogica[i][j-1] is PilulaEspecial:
							matrizLogica[i][j-1] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							
							#definir acao para pilula especial
							sair = True
							break					

				elif (type(matrizLogica[i][j]) == Pacman or matrizLogica[i][j] is Pacman) and direcao == [True,"UP"]:
						

					if i > 0:

						#caminho livre anda
						if type(matrizLogica[i-1][j]) == None or matrizLogica[i-1][j] is None:
							matrizLogica[i-1][j] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							sair 					= True
							break

						#caminho tem pilula, come pilula
						elif type(matrizLogica[i-1][j]) == Pilula or matrizLogica[i-1][j] is Pilula:
							matrizLogica[i-1][j] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							self.atualizarScore()
							sair 					= True
							break

						#caminho tem fantasma, perde vida
						elif type(matrizLogica[i-1][j]) == Fantasma or matrizLogica[i-1][j] is Fantasma:
							#matrizLogica[i-1][j] 	= Fantasma(1, 10, matrizLogica[i-1][j].idd)
							aux 					= matrizLogica[i][j]
							matrizLogica[i][j] 		= matrizLogica[i-1][j]
							vida 					= self.atualizarVida()
							matrizLogica[1][1] 		= aux
							sair 					= True
							break

						#caminho tem pilula especial
						elif type(matrizLogica[i-1][j]) == PilulaEspecial or matrizLogica[i-1][j] is PilulaEspecial:
							matrizLogica[i-1][j] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							
							#definir acao para pilula especial
							sair 					= True
							break					

				elif (type(matrizLogica[i][j]) == Pacman or matrizLogica[i][j] is Pacman) and direcao == [True,"DOWN"]:
						

					if i + 1 < NUM_LINHAS:

						#caminho livre anda
						if type(matrizLogica[i+1][j]) == None or matrizLogica[i+1][j] is None:
							matrizLogica[i+1][j] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							sair 					= True
							break

						#caminho tem pilula, come pilula
						elif type(matrizLogica[i+1][j]) == Pilula or matrizLogica[i+1][j] is Pilula:
							matrizLogica[i+1][j] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							self.atualizarScore()
							sair 					= True
							break

						#caminho tem fantasma, perde vida
						elif type(matrizLogica[i+1][j]) == Fantasma or matrizLogica[i+1][j] is Fantasma:
							#matrizLogica[i+1][j] 	= Fantasma(1, 10, matrizLogica[i+1][j].idd)
							aux 					= matrizLogica[i][j]
							matrizLogica[i][j]		= matrizLogica[i+1][j]
							matrizLogica[i+1][j] 	= None
							vida 					= self.atualizarVida()
							matrizLogica[1][1] 		= aux
							sair 					= True
							break

						#caminho tem pilula especial
						elif type(matrizLogica[i+1][j]) == PilulaEspecial or matrizLogica[i+1][j] is PilulaEspecial:
							matrizLogica[i+1][j] 	= matrizLogica[i][j]
							matrizLogica[i][j] 		= None
							
							#definir acao para pilula especial
							sair 					= True
							break

				

			if sair :
				break

		return vida
	
	def inicializaMatriz(self):

		#matriz logica
		arquivo = open('mapa.txt','r')
		conteudoArquivo = arquivo.read()
		linhas = conteudoArquivo.split('\n')
	

		for i,linha in enumerate(linhas):
			
			splitEspaco = linha.split(' ')

			for j,coluna in enumerate(splitEspaco):
				if coluna == '0':
					matrizLogica[i][j] = None

				elif coluna == '1':
					matrizLogica[i][j] = Pacman()

				elif coluna == '20' or coluna =='21' or coluna == '22':
					matrizLogica[i][j] = Fantasma(1,10,int(coluna))

				elif coluna == '3':
					matrizLogica[i][j] = Pilula()

				elif coluna == '5':
					matrizLogica[i][j] = PilulaEspecial()

				elif coluna == '4':
					matrizLogica[i][j] = Parede()
	

def main():

	#inicializaMatriz()

	#inicilizando pygame
	pygame.init()
	clock = pygame.time.Clock()  

	g1 = Game()

	#inicializando matriz logica
	g1.inicializaMatriz()

	#criando tela
	t1 = Tela()
	t1.blitarJogo()

	direcao = [None,None]

	last_time = time.time()
	
	loop = 1
	while(loop):
		#g1.moverAgentes()
		for evento in pygame.event.get():

			if evento.type == pygame.QUIT:
				loop = 0
			if evento.type == pygame.KEYDOWN:

				if evento.key == pygame.K_UP:
					direcao = [True,"UP"]
				elif evento.key == pygame.K_DOWN:
					direcao = [True,"DOWN"]  
				elif evento.key == pygame.K_RIGHT:
					direcao = [True,"RIGHT"] 
				elif evento.key == pygame.K_LEFT:
					direcao = [True,"LEFT"]
			

		new_time = time.time()

		sleep_time = ((1000.0 / FPS) - (new_time - last_time)) / 1000.0

		if sleep_time > 0:
			time.sleep(sleep_time)
		last_time = new_time	

		t1.tela.fill(PRETO) # isso limpa rastro do score
		t1.blitarJogo()
		t1.exibirScoreVida(g1.score,g1.vida)
	
		if direcao != [None,None]:
			if(not(g1.moverPacman(direcao)) and not(g1.moverAgentes())):		
				direcao = [None,None]
			else:
				print("FIM DE JOGO!")
				break

		pygame.display.update()
	pygame.quit()
	quit()
	

if __name__ == '__main__':
	main()