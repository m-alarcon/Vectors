from PIL import Image, ImageDraw
import numpy as np
import cv2
import math
import json

def conv(g_l, g_r):
	
	res = np.sum(np.absolute((g_l-g_r)))

	return res


pixeles = 0
nombre_imagen = "Bola"

for p in range(1, 29):
	im = Image.open("C:/Users/malarcon/Images/"+nombre_imagen+"/frame"+str(p)+".bmp")
	print("Imagen anterior: "+nombre_imagen+" " + str(p))
	im2 = Image.open("C:/Users/malarcon/Images/"+nombre_imagen+"/frame"+str(p+1)+".bmp")
	print("Imagen siguiente: "+nombre_imagen+" " + str(p+1))
	dibujo = ImageDraw.Draw(im2)
	im3 = im.convert('L')
	a_im3 = np.array(im3)
	im4 = im2.convert('L')
	a_im4 = np.array(im4)
	print (im.format, im.size, im.mode)
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

	restaTotal = 0
	m_vectores_x = np.zeros((fronteras_filas.shape[0] - 2,fronteras_columnas.shape[0] - 2), 'int8')
	m_vectores_y = np.zeros((fronteras_filas.shape[0] - 2,fronteras_columnas.shape[0] - 2), 'int8')
	#Recorrer todos los cuadros de comparación de la imagen completa
	for y in range(0, fronteras_filas.shape[0] - 2):
		for x in range(0, fronteras_columnas.shape[0] - 2):
			#Recorrer el cuadro grande e ir sacando todos los bloques cuadrados
			imagen_comp = im3.crop((fronteras_columnas[x]+offset,fronteras_filas[y]+offset,fronteras_columnas[x]+ancho_bloq+offset,fronteras_filas[y]+ancho_bloq+offset))

			a_imagen_comp = np.array(imagen_comp,'int32')
			corr_vector = np.zeros((ancho_bloq,ancho_bloq), 'float')
			for i in range(0, corr_vector.shape[0]):
				for j in range(0, corr_vector.shape[1]):
					imagen = im4.crop((fronteras_columnas[x]+j,fronteras_filas[y]+i,fronteras_columnas[x]+ancho_bloq+j,fronteras_filas[y]+ancho_bloq+i))
					a_imagen = np.array(imagen,'int32')
					corr_vector[i,j] = conv(a_imagen_comp, a_imagen)
			if(np.where(corr_vector == corr_vector.min())[1].shape[0] > 1):	#Hay que elegir uno de los que salen, elijo el del centro
				#print (np.where(corr_vector == corr_vector.min())[1].shape[0])
				if(np.where(corr_vector == corr_vector.min())[1].shape[0] == ancho_bloq):	#Hay que elegir uno de los que salen, elijo el del centro
					if(np.where(corr_vector == corr_vector.min())[0].shape[0] == ancho_bloq):
						#print("Hay menos de ancho_bloq*ancho_bloq")
						indicesx = np.where(corr_vector == corr_vector.min())[1][int(np.where(corr_vector == corr_vector.min())[1].shape[0]/2)]
						indicesy = np.where(corr_vector == corr_vector.min())[0][int(np.where(corr_vector == corr_vector.min())[0].shape[0]/2)]
					else:
						indicesx = np.where(corr_vector == corr_vector.min())[1][int(np.where(corr_vector == corr_vector.min())[1].shape[0]/2)]
						indicesy = int(ancho_bloq/2)
				elif(np.where(corr_vector == corr_vector.min())[1].shape[0] != ancho_bloq):
					if(np.where(corr_vector == corr_vector.min())[0].shape[0] == ancho_bloq):
						#print("Hay menos de ancho_bloq*ancho_bloq")
						indicesx = int(ancho_bloq/2)
						indicesy = np.where(corr_vector == corr_vector.min())[0][int(np.where(corr_vector == corr_vector.min())[0].shape[0]/2)]
					else:#(np.where(corr_vector == corr_vector.min())[0].shape[0] == ancho_bloq):	#Hay que elegir uno de los que salen, elijo el del centro
						#print("Todos los cuadros son iguales")
						indicesx = int(ancho_bloq/2)
						indicesy = int(ancho_bloq/2)
			else:
				indicesx = np.where(corr_vector == corr_vector.min())[1]
				indicesy = np.where(corr_vector == corr_vector.min())[0]
			restaTotal += corr_vector[indicesy, indicesx]

			dibujo.rectangle([(fronteras_columnas[x]+offset, fronteras_filas[y]+offset), (fronteras_columnas[x]+ancho_bloq+offset, fronteras_filas[y]+ancho_bloq+offset)], outline="green")
			dibujo.rectangle([(fronteras_columnas[x]+indicesx, fronteras_filas[y]+indicesy), (fronteras_columnas[x]+ancho_bloq+indicesx, fronteras_filas[y]+ancho_bloq+indicesy)], outline="red")
			dibujo.line([(fronteras_columnas[x+1], fronteras_filas[y+1]), (fronteras_columnas[x+1]-offset+indicesx, fronteras_filas[y+1]-offset+indicesy)], fill="blue")
			m_vectores_x[y][x] = abs(-offset+indicesx)
			m_vectores_y[y][x] = abs(-offset+indicesy)

	print ("Diferencia entre las imagenes con los vectores: "+str(restaTotal))
	print ("Diferencia entre las imagenes sin los vectores: "+str(np.absolute((a_im4-a_im3)).sum()))
	#input("Presiona Enter para continuar...")

	np.savetxt("vectorx"+nombre_imagen+str(p+1)+".txt", m_vectores_x, fmt='%i', delimiter=' ')
	np.savetxt("vectory"+nombre_imagen+str(p+1)+".txt", m_vectores_y, fmt='%i', delimiter=' ')	
	im2.save("./PruebaResta/"+nombre_imagen+str(p+1)+"Vectores.bmp")