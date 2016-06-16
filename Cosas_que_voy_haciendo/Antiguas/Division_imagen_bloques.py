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
	        output[i][j]=abs((img2_reversed-img1_patch).sum())
	return output



pixeles = 0

#for i in range(1,2):
im = Image.open("D:/Downloads/Beca/Cosas_que_voy_haciendo/framecol1HD.bmp")#+str(i)+"HD.bmp")
dibujo = ImageDraw.Draw(im)
im2 = Image.open("D:/Downloads/Beca/Cosas_que_voy_haciendo/framecol2HD.bmp")#+str(i+1)+"HD.bmp")
im3 = im.convert('L')
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


#for x in range(0,fronteras_comp_columnas.shape[0]-1):
#	for y in range(0, fronteras_comp_filas.shape[0]-1):
		#Recorrer el cuadro grande e ir sacando todos los bloques cuadrados
conv_vector = np.zeros((ancho_bloq,ancho_bloq), 'uint64') #Esto vale para bloques cuadrados, hay que cambiarlo para bloques con un px mas de alto
imagen_comp = im3.crop((fronteras_comp_columnas[1],fronteras_comp_filas[1],fronteras_comp_columnas[2],fronteras_comp_filas[2]))
a_imagen_comp = np.array(imagen_comp)
for i in range(0, conv_vector.shape[0]):
	for j in range(0, conv_vector.shape[1]):
		imagen = im3.crop((fronteras_columnas[1]+j,fronteras_filas[1]+i,fronteras_columnas[1]+ancho_bloq+j,fronteras_filas[1]+ancho_bloq+i))
		a_imagen = np.array(imagen)
		conv_vector[i][j] = conv(a_imagen_comp, a_imagen)

indices = np.where(conv_vector == conv_vector.max())
print(conv_vector)
print(indices)

dibujo.line((fronteras_columnas[1+1], fronteras_filas[1+1]) + (fronteras_comp_columnas[1]+indices[0], fronteras_comp_filas[1]+indices[1]), fill="red")

imagen1 = im3.crop((fronteras_columnas[1],fronteras_filas[1],fronteras_columnas[1]+ancho_bloq,fronteras_filas[1]+ancho_bloq))
imagen1.show()
imagen2= im3.crop((fronteras_columnas[2],fronteras_filas[1],fronteras_columnas[2]+ancho_bloq,fronteras_filas[1]+ancho_bloq))
imagen2.show()
imagen3 = im3.crop((fronteras_columnas[1],fronteras_filas[2],fronteras_columnas[1]+ancho_bloq,fronteras_filas[2]+ancho_bloq))
imagen3.show()
imagen4 = im3.crop((fronteras_columnas[2],fronteras_filas[2],fronteras_columnas[2]+ancho_bloq,fronteras_filas[2]+ancho_bloq))
imagen4.show()

im.show()
#im.save("frame1Vectores.bmp")