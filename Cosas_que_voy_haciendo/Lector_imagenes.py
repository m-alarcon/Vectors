from PIL import Image
import numpy as np
import cv2

im = Image.open("D:/Downloads/Beca/Cosas_que_voy_haciendo/frame1.bmp")
pix = im.load()
#im.show()
print (im.format, im.size, im.mode)
(ancho, largo) = im.size
print (ancho)
print (largo)


ancho_bloq = ancho/32
print (ancho_bloq)

trozo = im.crop((0,0,int(ancho_bloq),int(ancho_bloq)))
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
