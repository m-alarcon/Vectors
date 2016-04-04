from PIL import Image, ImageDraw
import numpy as np
import cv2
import math
import json

def conv(g_l, g_r):
	
	res = abs((g_l-g_r)).sum()

	return res


pixeles = 0

for p in range(444, 446):
	#im = Image.open("C:/Users/malarcon/Desktop/Alcatel/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD1.bmp")#+str(p)+".bmp")
	im = Image.open("C:/Users/malarcon/Desktop/Alcatel/Cosas_que_voy_haciendo/Fotogramas para usar/Mario/mario"+str(p)+".bmp")
	print("Imagen anterior: Mario " + str(p))
	#im = Image.open("D:/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD"+str(p)+".bmp")
	#im = Image.open("C:/Users/malarcon/Desktop/Alcatel/Fondo2.jpg")
	#im2 = Image.open("C:/Users/malarcon/Desktop/Alcatel/Cosas_que_voy_haciendo/Fotogramas para usar/SD_sillon/frameSD"+str(p+1)+".bmp")
	im2 = Image.open("C:/Users/malarcon/Desktop/Alcatel/Cosas_que_voy_haciendo/Fotogramas para usar/Mario/mario"+str(p+1)+".bmp")
	print("Imagen siguiente: Mario " + str(p+1))
	#im2 = Image.open("D:/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD"+str(p)+".bmp")#estoy utilizando el mismo fotograma en los dos
	#im2 = im
	dibujo = ImageDraw.Draw(im2)
	im3 = im.convert('L')
	a_im3 = np.array(im3)
	#im3.show()
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
	#Recorrer todos los cuadros de comparación de la imagen completa
	for y in range(0, fronteras_filas.shape[0] - 2):
		for x in range(0, fronteras_columnas.shape[0] - 2):
			#Recorrer el cuadro grande e ir sacando todos los bloques cuadrados
			imagen_comp = im4.crop((fronteras_columnas[x]+offset,fronteras_filas[y]+offset,fronteras_columnas[x]+ancho_bloq+offset,fronteras_filas[y]+ancho_bloq+offset))

			a_imagen_comp = np.array(imagen_comp)
			corr_vector = np.zeros((ancho_bloq,ancho_bloq), 'int')
			for i in range(0, corr_vector.shape[0]):
				for j in range(0, corr_vector.shape[1]):
					imagen = im3.crop((fronteras_columnas[x]+j,fronteras_filas[y]+i,fronteras_columnas[x]+ancho_bloq+j,fronteras_filas[y]+ancho_bloq+i))
					a_imagen = np.array(imagen)
					corr_vector[i,j] = conv(a_imagen_comp, a_imagen)
					#print(conv(a_imagen_comp, a_imagen))
					#dibujo.rectangle((fronteras_columnas[x]+offset, fronteras_filas[y]+offset) + (fronteras_columnas[x]+ancho_bloq+offset, fronteras_filas[y]+ancho_bloq+offset), outline="blue")
					#dibujo.rectangle((fronteras_columnas[x]+j, fronteras_filas[y]+i) + (fronteras_columnas[x]+ancho_bloq+j, fronteras_filas[y]+ancho_bloq+i), outline="blue")
					#im2.show()
					#input("Presiona Enter para continuar...")
			#print(corr_vector)
			#input("Presiona Enter para continuar...")
			if(np.where(corr_vector == corr_vector.min())[0].shape[0] > 1):	#Hay que elegir uno de los que salen, elijo el del centro
				indicesx = int(ancho_bloq/2)
				indicesy = int(ancho_bloq/2)
			else:
				indicesx = np.where(corr_vector == corr_vector.min())[1]
				indicesy = np.where(corr_vector == corr_vector.min())[0]
			restaTotal += corr_vector[indicesx, indicesy]
			print(restaTotal)
			#print(indicesx, indicesy)
			dibujo.rectangle([(fronteras_columnas[x]+offset, fronteras_filas[y]+offset), (fronteras_columnas[x]+ancho_bloq+offset, fronteras_filas[y]+ancho_bloq+offset)], outline="green")
			dibujo.rectangle([(fronteras_columnas[x]+indicesx, fronteras_filas[y]+indicesy), (fronteras_columnas[x]+ancho_bloq+indicesx, fronteras_filas[y]+ancho_bloq+indicesy)], outline="red")
			dibujo.line([(fronteras_columnas[x+1], fronteras_filas[y+1]), (fronteras_columnas[x+1]-offset+indicesx, fronteras_filas[y+1]-offset+indicesy)], fill="blue")
	print ("Diferencia entre las imagenes con los vectores: "+str(restaTotal))
	print ("Diferencia entre las imagenes sin los vectores: "+str(abs((a_im4-a_im3)).sum()))
	im2.show()
	input("Presiona Enter para continuar...")

	#im2.show()
	im2.save("./PruebaResta/frame"+str(p+1)+"Vectores.bmp")