from PIL import Image
import numpy as np
import cv2

pixeles = 0

for i in range(1,2):
	im = Image.open("D:/Downloads/Beca/Cosas_que_voy_haciendo/frame"+str(i)+".bmp")
	pix = im.load()
	im2 = Image.open("D:/Downloads/Beca/Cosas_que_voy_haciendo/frame"+str(i+1)+".bmp")
	print (im.format, im.size, im.mode)
	(ancho, largo) = im.size

	ancho_bloq = ancho/32

	sobrante = (largo%ancho_bloq)/int(largo/ancho_bloq)
	num_filas = int(largo/ancho_bloq)

	#División de la imagen en todos sus bloques
	for i in range(0, num_filas-1):
		pixeles += sobrante
		if pixeles >= 1:
			alto_bloque_actual = 12
		else:
			alto_bloque_actual = 11
		for j in range(0, 31):
			trozo = im.crop((int(j*ancho_bloq),int(i*alto_bloque_actual),int((j+1)*ancho_bloq),int((i+1)*alto_bloque_actual)))


	#trozo.show()
	p = np.array(trozo)
	#for row in range(int(ancho_bloq)):
	#	print(p[row])


	trozo1 = im.crop ((341,50,352,61))
	p1 = np.array(trozo1)

	def conv(img1, img2):
		rows=img1.shape[0]-img2.shape[0]+1
		cols=img1.shape[1]-img2.shape[1]+1
		output=np.zeros((rows,cols), 'uint8')

		img2_reversed=np.rot90(np.rot90(img2))

		for i in range(0, output.shape[0]):
		   for j in range(0, output.shape[1]):
		        #desplazando el kernel
		        img1_patch=img1[i:i+len(img2),j:j+len(img2)]   
		        output[i][j]=(img2_reversed*img1_patch).sum()
		print (output)

	conv(p, p1)	        
