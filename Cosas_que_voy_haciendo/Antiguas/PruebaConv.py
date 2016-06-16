from PIL import Image, ImageDraw
import numpy as np
import cv2
import time

def convprueba1(img1, img2):
	suma = 0
	g = 0
	conv = 0
	print(img1)
	print((img1*img2).sum())


	suma1 = 0
	g1 = 0
	conv1 = 0
	for y in range(0, img1.shape[1]):
		for x in range(0, img1.shape[0]):
			g1 = int(img1[x, y]) * int(img2[x, y])
			suma1 += g1
	print ("Valor de la convolucion: " + str(suma1))



	for dy in range(-img2.shape[1], img2.shape[1]):
		for dx in range(-img2.shape[0], img2.shape[0]):
			for y in range(0, img1.shape[1]):
				for x in range(0, img1.shape[0]):
					if (x-dx < 0):
						g = 0
					elif (y-dy < 0):
						g = 0
					elif (x-dx > img1.shape[0]-1):
						g = 0
					elif (y-dy > img1.shape[1]-1):
						g = 0
					else:
						g = int(img1[x, y]) * int(img2[x - dx, y - dy])
					suma += g
			if(suma > conv):
				conv = suma
				suma = 0
				print ("Valor de la convolucion: " + str(conv))
			else:
				suma = 0
	return conv

def convprueba2(img1, img2):
	suma1 = 0
	g1 = 0
	conv1 = 0
	for y in range(0, img1.shape[1]):
		for x in range(0, img1.shape[0]):
			g1 = int(img1[x, y]) * int(img2[x, y])
			suma1 += g1
	return suma1

def convprueba3(img1, img2):
	(ancho, largo) = img1.size
	ancho_bloq = int(ancho/32)
	pixeles = 0

	sobrante = (largo%ancho_bloq)/int(largo/ancho_bloq)
	num_filas = int(largo/ancho_bloq)
	fronteras_filas = np.zeros(num_filas+1, 'uint32')
	fronteras_columnas = np.zeros(33, 'uint32')

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
	fronteras_comp_filas = np.zeros(num_filas, 'uint32')
	for i in range(0, num_filas):
		pixeles += sobrante
		if i == 0:
			fronteras_comp_filas[i] = offset
		else:
			if pixeles >= 1:
				fronteras_comp_filas[i] = fronteras_comp_filas[i-1]+ancho_bloq+1
				pixeles -= 1
			else:
				fronteras_comp_filas[i] = fronteras_comp_filas[i-1]+ancho_bloq

	fronteras_comp_columnas = np.zeros(32, 'uint32')
	for i in range(0, 32):
		if i == 0:
			fronteras_comp_columnas[i] = offset
		else:
			fronteras_comp_columnas[i] = fronteras_comp_columnas[i-1]+ancho_bloq


	im1 = img1.crop((fronteras_comp_columnas[3],fronteras_comp_filas[3],fronteras_comp_columnas[4],fronteras_comp_filas[4]))
	im2 = img2.crop((fronteras_columnas[3],fronteras_filas[3],fronteras_columnas[5],fronteras_filas[5]))
	im1.show()
	im2.show()
	im1 = np.array(im1)
	im2 = np.array(im2)
	suma = 0
	conv = 0

	for dy in range(-ancho_bloq, 0):
		for dx in range(-ancho_bloq, 0):
			for y in range(0, im1.shape[1]):
				for x in range(0, im1.shape[0]):
					g = int(im1[x, y]) * int(im2[x - dx, y - dy])
					suma += g
			print ("Valor de la convolucion: " + str(suma))
			if(suma > conv):
				conv = suma
				suma = 0
			else:
				suma = 0
			print ("Valor maximo de la convolucion: " + str(conv))
			#time.sleep(1)

	suma1 = 0
	for y in range(0, im1.shape[1]):
		for x in range(0, im1.shape[0]):
			g1 = int(im1[x, y]) * int(im1[x, y])
			suma1 += g1
	print ("Valor de la convolucion con el bloque: " + str(suma1))

	return conv




im = Image.open("C:/Users/malarcon/Desktop/Alcatel/Cosas_que_voy_haciendo/Fotogramas para usar/SD_sillon/frameSD1.bmp")
im2 = im.convert('L')
#a_imagen = np.array(im2)
print (convprueba3(im2,im2))