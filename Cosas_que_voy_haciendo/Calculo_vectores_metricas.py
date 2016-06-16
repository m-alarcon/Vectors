from PIL import Image, ImageDraw
import numpy as np
import cv2
import math
import json
import time

pixeles = 0
n_fotogramas = 30
with open("C:/Users/malarcon/Images/MetricasCuadrado/metricasframe1.txt") as archivo_json:
	metricas = json.load(archivo_json)

filas = int(len(metricas)/33)
m_prx_ant = np.zeros((31,filas-2,n_fotogramas-1), 'float')
m_prx_resta = np.zeros((31,filas-2,n_fotogramas-1), 'float')
ancho_bloq = 45 #Igual que el alto (en general)
#m_pry_ant = np.zeros((31,filas-2,n_fotogramas-1), 'float')
#m_pry_resta = np.zeros((31,filas-2,n_fotogramas-1), 'float')

#Creo las matrices que me van a decir si el bloque que estamos evaluando se ha desplazado en el fotograma anterior y la dirección hacia la 
#que se ha movido (0 = sin movimiento, 1 = derecha, 2 = izquierda)
m_mov_x = np.zeros((m_prx_ant.shape[0],m_prx_ant.shape[1]), 'uint8')
m_num_rep_x = np.zeros((m_prx_ant.shape[0],m_prx_ant.shape[1]), 'int8')
m_num_vec_x = np.zeros((m_prx_ant.shape[0],m_prx_ant.shape[1]), 'int8')

for p in range(1, n_fotogramas):
	with open("C:/Users/malarcon/Images/MetricasCuadrado/metricasframe"+str(p)+".txt") as archivo_json:
		metricas = json.load(archivo_json)

	filas = int(len(metricas)/33)
	m_metricas = np.zeros((33,filas,2), 'float')

	#Poner las metricas en una matriz
	for y in range(0, int(filas)):
		for x in range(0, 33):
			m_metricas[x][y][0] = metricas[33*y+x]["prx"]
			m_metricas[x][y][1] = metricas[33*y+x]["pry"]

	m_prx = np.zeros((31,filas-2), 'float')
	m_pry = np.zeros((31,filas-2), 'float')

	for y in range(1, m_metricas.shape[1]-1):
		for x in range(1, m_metricas.shape[0]-1):
			m_prx[x-1][y-1] = m_metricas[x][y][0]
			#m_pry[i-1][j-1] = m_metricas[j][i][1]
			m_prx_ant[x-1][y-1][p-1] = m_prx[x-1][y-1]
			#m_pry_ant[i-1][j-1][p-1] = m_pry[i-1][j-1]
			if p == 1:
				m_prx_resta[x-1][y-1][p-1] = 0
				#m_pry_resta[i-1][j-1][p-1] = 0
			else:
				m_prx_resta[x-1][y-1][p-1] = m_prx[x-1][y-1] - m_prx_ant[x-1][y-1][p-2]
				#m_pry_resta[i-1][j-1][p-1] = m_pry[i-1][j-1] - m_pry_ant[i-1][j-1][p-2]
	
	#Creo las matrices donde se van a guardar los vectores con el mismo tamaño que las matrices de métricas
	m_vectores_x = np.zeros((m_prx.shape[0],m_prx.shape[1]), 'int8')
	#m_vectores_y = np.zeros((m_pry.shape[0],m_pry.shape[1]), 'int8')

	if p == 1:
		#Recorro la imagen poniendo todos los vectores a cero
		for y in range(0, m_prx.shape[1]):
			for x in range(0, m_prx.shape[0]):
				m_vectores_x[x][y] = 0
				m_num_rep_x[x][y] = 1
	else:
		for y in range(0, m_prx.shape[1]):
			for x in range(0, m_prx.shape[0]):
				if m_mov_x[x][y] == 0:
					#Si algo ha perdido importancia en un bloque
					if m_prx_resta[x][y][p-1] < -0.1:
						#Comprobar si se ha movido a izquierda o derecha
						if abs(m_prx_resta[x+1][y][p-1]) > 0.01:
							m_vectores_x[x][y] = int(ancho_bloq/(2*m_num_rep_x[x][y])) #Necesito el ancho del bloque para tener una mayor precisión. Aquí se lo pongo a mano.
							m_vectores_x[x+1][y] = int(ancho_bloq/(2*m_num_rep_x[x][y]))
							m_mov_x[x][y] = 1
						elif abs(m_prx_resta[x-1][y][p-1]) > 0.01:
							m_vectores_x[x][y] = int(ancho_bloq/(2*m_num_rep_x[x][y])) #Necesito el ancho del bloque para tener una mayor precisión. Aquí se lo pongo a mano.
							m_vectores_x[x-1][y] = int(ancho_bloq/(2*m_num_rep_x[x][y]))
							m_mov_x[x][y] = 2
					else:
						m_mov_x[x][y] = 0
						if m_num_rep_x[x][y] < ancho_bloq/10:
							m_num_rep_x[x][y] += 1
						else:
							m_num_rep_x[x][y] = m_num_rep_x[x][y]
				if m_mov_x[x][y] == 1:
					m_vectores_x[x][y] = 0
					m_vectores_x[x+1][y] = int(ancho_bloq/(2*m_num_rep_x[x][y]))
					m_num_rep_x[x][y] = m_num_rep_x[x][y]
				if m_mov_x[x][y] == 2:
					m_vectores_x[x][y] = 0
					m_vectores_x[x-1][y] = int(-ancho_bloq/(2*m_num_rep_x[x][y]))
					m_num_rep_x[x][y] = m_num_rep_x[x][y]


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
	#A partir de aqui pinto la imagen con los vectores para comprobar que se calculan bien.
	nombre_imagen = "Cuadrado"
	im = Image.open("C:/Users/malarcon/Images/"+nombre_imagen+"/frame"+str(p)+".bmp")
	dibujo = ImageDraw.Draw(im)
	print("Imagen calculada: "+nombre_imagen+ " " + str(p))
	(ancho, largo) = im.size
	ancho_bloq = int(ancho/32)

	sobrante = (largo%ancho_bloq)/int(largo/ancho_bloq)
	num_filas = int(largo/ancho_bloq)
	fronteras_filas = np.zeros(num_filas+1, 'uint32')
	fronteras_columnas = np.zeros(33, 'uint32')

	#Creación vector con las fronteras de las filas
	for i in range(1, num_filas+1):
		pixeles += sobrante
		if pixeles >= 1:
			alto_bloque_actual = ancho_bloq + 1
			pixeles -= 1
		else:
			alto_bloque_actual = ancho_bloq
			
		fronteras_filas[i] = fronteras_filas[i-1] + alto_bloque_actual

	#Creación vector con las fronteras laterales de las columnas
	for i in range(1, 33):
		fronteras_columnas[i] = fronteras_columnas[i-1] + ancho_bloq

	#Creación de los vectores con las fronteras de los bloques de las aristas
	offset = int(ancho_bloq/2)
	fronteras_comp_filas = np.zeros(num_filas-1, 'uint32')
	for i in range(0, num_filas-1):
		pixeles += sobrante
		if i == 0:
			fronteras_comp_filas[i] = offset
		else:
			if pixeles >= 1:
				fronteras_comp_filas[i] = fronteras_comp_filas[i-1]+ancho_bloq+1
				pixeles -= 1
			else:
				fronteras_comp_filas[i] = fronteras_comp_filas[i-1]+ancho_bloq

	fronteras_comp_columnas = np.zeros(31, 'uint32')
	for i in range(0, 31):
		if i == 0:
			fronteras_comp_columnas[i] = offset
		else:
			fronteras_comp_columnas[i] = fronteras_comp_columnas[i-1]+ancho_bloq

	for y in range(0, fronteras_filas.shape[0] - 2):
		for x in range(0, fronteras_columnas.shape[0] - 2):
			#dibujo.rectangle([(fronteras_columnas[x]+offset, fronteras_filas[y]+offset), (fronteras_columnas[x]+ancho_bloq+offset, fronteras_filas[y]+ancho_bloq+offset)], outline="green")
			#dibujo.rectangle([(fronteras_columnas[x]+m_vectores_x[x][y], fronteras_filas[y]+0), (fronteras_columnas[x]+ancho_bloq+m_vectores_x[x][y], fronteras_filas[y]+ancho_bloq+0)], outline="red")
			dibujo.line([(fronteras_columnas[x+1], fronteras_filas[y+1]), (fronteras_columnas[x+1]+m_vectores_x[x][y], fronteras_filas[y+1]+0)], fill="blue")
	im.save("./PruebaMetricas/"+nombre_imagen+str(p)+"Vectores.bmp")
