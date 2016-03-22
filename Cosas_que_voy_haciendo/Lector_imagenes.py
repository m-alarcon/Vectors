from PIL import Image, ImageDraw
import numpy as np
import cv2

def conv(img1, img2):
	rows=img1.shape[0]-img2.shape[0]+1
	cols=img1.shape[1]-img2.shape[1]+1
	output=np.zeros((rows,cols), 'uint64')

	img2_reversed=img2#np.rot90(np.rot90(img2))

	for i in range(0, output.shape[0]):
	   for j in range(0, output.shape[1]):
	        #desplazando el kernel
	        img1_patch=img1[i:i+len(img2),j:j+len(img2)]   
	        output[i][j]=abs((img2_reversed-img1_patch)).sum()
	return output


pixeles = 0

for p in range(1, 20):
	#im = Image.open("C:/Users/malarcon/Desktop/Alcatel/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD1.bmp")#+str(p)+".bmp")
	im = Image.open("C:/Users/malarcon/Desktop/Alcatel/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD"+str(p)+".bmp")
	#im = Image.open("D:/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD"+str(p)+".bmp")
	#im = Image.open("C:/Users/malarcon/Desktop/Alcatel/Fondo2.jpg")
	#im2 = Image.open("C:/Users/malarcon/Desktop/Alcatel/Cosas_que_voy_haciendo/Fotogramas para usar/SD_sillon/frameSD"+str(p+1)+".bmp")
	im2 = Image.open("C:/Users/malarcon/Desktop/Alcatel/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD"+str(p+1)+".bmp")
	#im2 = Image.open("D:/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD"+str(p)+".bmp")#estoy utilizando el mismo fotograma en los dos
	#im2 = im
	dibujo = ImageDraw.Draw(im2)
	im3 = im.convert('L')
	#im3.show()
	im4 = im2.convert('L')
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

	#Recorrer todos los cuadros de comparación de la imagen completa
	for x in range(0, fronteras_columnas.shape[0] - 1):
		for y in range(0, fronteras_filas.shape[0] - 1):
			#Recorrer el cuadro grande e ir sacando todos los bloques cuadrados
			imagen_comp = im4.crop((fronteras_columnas[x]+offset,fronteras_filas[y]+offset,fronteras_columnas[x]+ancho_bloq+offset,fronteras_filas[y]+ancho_bloq+offset))
			a_imagen_comp = np.array(imagen_comp)
			conv_vector = np.zeros((fronteras_columnas[x+1]-fronteras_columnas[x],ancho_bloq), 'uint16')
			for i in range(0, conv_vector.shape[0]):
				for j in range(0, conv_vector.shape[1]):
					imagen = im3.crop((fronteras_columnas[x]+j,fronteras_filas[y]+i,fronteras_columnas[x]+ancho_bloq+j,fronteras_filas[y]+ancho_bloq+i))
					a_imagen = np.array(imagen)
					conv_vector[i][j] = conv(a_imagen_comp, a_imagen)
					#print(conv(a_imagen_comp, a_imagen))

			#if(np.where(conv_vector == conv_vector.min())[0].shape[0] > 1):	
			#	indicesx = int(ancho_bloq/2)
			#	indicesy = int(ancho_bloq/2)
			#else:
			indicesx = np.where(conv_vector == conv_vector.min())[0][0]
			indicesy = np.where(conv_vector == conv_vector.min())[1][0]
			#print(conv_vector)
			#print(indicesx, indicesy)

			dibujo.line((fronteras_columnas[x+1], fronteras_filas[y+1]) + (fronteras_columnas[x+1]-offset+indicesx, fronteras_filas[y+1]-offset+indicesy), fill="red")

	#im2.show()
	im2.save("frame"+str(p)+"Vectores.bmp")