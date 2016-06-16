from PIL import Image, ImageDraw
import numpy as np
import cv2
import math
import json

for p in range(1, 30):
	with open("C:/Users/malarcon/Images/MetricasCuadrado/metricasframe"+str(p)+".txt") as archivo_json:
		metricas = json.load(archivo_json)

	filas = int(len(metricas)/33)
	m_metricas = np.zeros((33,filas,2), 'float')

	#Poner las metricas en una matriz
	for i in range(0, int(filas)):
		for j in range(0, 33):
			m_metricas[j][i][0] = metricas[33*i+j]["prx"]
			m_metricas[j][i][1] = metricas[33*i+j]["pry"]

	m_prx = np.zeros((filas-2,31), 'float')
	m_pry = np.zeros((filas-2,31), 'float')
	for i in range(1, m_metricas.shape[1]-1):
		for j in range(1, m_metricas.shape[0]-1):
			m_prx[i-1][j-1] = m_metricas[j][i][0]
			m_pry[i-1][j-1] = m_metricas[j][i][1]

	np.savetxt("prxframe"+str(p)+".txt", m_prx, fmt='%.4f', delimiter=' ')
	np.savetxt("pryframe"+str(p)+".txt", m_pry, fmt='%.4f', delimiter=' ')